import asyncio
from collections.abc import (
    AsyncIterator,
    Callable,
    Collection,
    Coroutine,
    MutableMapping,
)
from contextlib import asynccontextmanager
from enum import Enum
from logging import Logger, LoggerAdapter, getLogger
from pathlib import Path
from typing import Any, Self, TypeVar

import aiofiles
import aiofiles.os as aio_os

from .blob.hash_ import calc_hash_file
from .blob.package import CompressionT, Packer, Unpacker
from .blob.utils import choose_compression
from .exceptions import (
    BlobNotFoundError,
    CAFSClientError,
    EmptyConnectionPoolError,
    UnexpectedResponseError,
)
from .types import AsyncReader, AsyncWriter

__all__ = ('CAFSClient',)


DEFAULT_CONNECT_TIMEOUT = 5.0

module_logger = getLogger(__name__)


class CommandT(bytes, Enum):
    VERSION = b'VERS'
    CHECK = b'CHCK'
    STREAM = b'STRM'
    SIZE = b'SIZE'
    PULL = b'PULL'

    def __str__(self) -> str:
        return self.value.decode('utf-8')


class ResponseT(bytes, Enum):
    VERSION_OK_RESPONSE = b'NONE'
    CHECK_FOUND_RESPONSE = b'HAVE'
    CHECK_NOT_FOUND_RESPONSE = b'NONE'
    STREAM_OK_RESPONSE = b'HAVE'
    SIZE_NOT_FOUND_RESPONSE = b'NONE'
    SIZE_OK_RESPONSE = b'SIZE'
    PULL_FOUND_RESPONSE = b'TAKE'
    PULL_NOT_FOUND_RESPONSE = b'NONE'


RESPONSE_LENGTH = 4
HELLO_HEADER_LENGTH = 20

CLIENT_VERSION = b'001'
HASH_TYPE = b'blake3'
CAFS_DEFAULT_PORT = 2403
STREAM_MAX_CHUNK_SIZE = 65534


class ConnectionLoggerAdapter(LoggerAdapter):
    def process(
        self, msg: Any, kwargs: MutableMapping[str, Any]
    ) -> tuple[str, MutableMapping[str, Any]]:
        return (
            f'[{self.extra["host"]}:{self.extra["port"]}:{self.extra["connection_id"]}] {msg}',  # type: ignore[index]
            kwargs,
        )


class CAFSConnection:
    host: str
    port: int
    timeout: float
    server_root: bytes
    logger: ConnectionLoggerAdapter
    verbose_debug: bool

    _reader: asyncio.StreamReader | None = None
    _writer: asyncio.StreamWriter | None = None

    def __init__(
        self,
        server_root: str,
        host: str,
        port: int = CAFS_DEFAULT_PORT,
        timeout: float = DEFAULT_CONNECT_TIMEOUT,
        logger: Logger | LoggerAdapter | None = None,
        verbose_debug: bool = False,
    ) -> None:
        self.server_root = server_root.encode('utf-8')
        self.host = host
        self.port = port
        self.timeout = timeout
        self.is_connected = False
        self.logger = ConnectionLoggerAdapter(
            logger or module_logger,
            {'host': host, 'port': port, 'connection_id': id(self)},
        )
        self.verbose_debug = verbose_debug

    async def connect(self) -> None:
        if self.is_connected:
            return

        try:
            self.logger.debug('Connecting')
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port), timeout=self.timeout
            )
            await self._auth()
            self.is_connected = True
            self.logger.debug('Connected')
        except asyncio.TimeoutError:
            self.logger.error('Connection timed out')
            raise CAFSClientError('Connection timed out')
        except (ConnectionRefusedError, OSError) as err:
            self.logger.error('Failed to connect: %s', str(err))
            raise err

    async def disconnect(self) -> None:
        if self._writer and not self._writer.is_closing():
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except Exception as e:  # pylint: disable=broad-exception-caught
                self.logger.error('Failed to close connection: %s', e)

        self.is_connected = False
        self._reader = None
        self._writer = None
        self.logger.debug('Disconnected')

    async def _send(self, data: bytes) -> None:
        if not self._writer:
            raise CAFSClientError('Connection is not established')
        self._writer.write(data)
        await self._writer.drain()

    async def _receive(self, n: int = -1) -> bytes:
        if not self._reader:
            raise CAFSClientError('Connection is not established')
        try:
            return await asyncio.wait_for(
                self._reader.readexactly(n), timeout=self.timeout
            )
        except (asyncio.IncompleteReadError, asyncio.TimeoutError) as err:
            self.logger.error('Failed to receive data: %s', err)
            raise

    async def _auth(self) -> None:
        self.logger.debug('Authenticating')
        await self._receive(HELLO_HEADER_LENGTH)
        self.logger.debug('Got hello header')

        self.logger.debug('Sending version')
        await self._send(CommandT.VERSION + CLIENT_VERSION)

        response = await self._receive(RESPONSE_LENGTH)

        if response != ResponseT.VERSION_OK_RESPONSE:
            self.logger.error('Authentication failed, received: %s', response)
            raise UnexpectedResponseError(response)

        buff = bytearray(1 + len(self.server_root))
        buff[0] = len(self.server_root)
        buff[1:] = self.server_root
        await self._send(buff)
        self.logger.debug('Authenticated')

    async def check(self, blob_hash: str) -> bool:
        if not self.is_connected:
            await self.connect()

        self.logger.debug('Checking for blob: %s', blob_hash)
        blob_hash_bytes = bytes.fromhex(blob_hash)
        await self._send(CommandT.CHECK + HASH_TYPE + blob_hash_bytes)
        self.logger.debug('Sent %s command', CommandT.CHECK)

        response = await self._receive(RESPONSE_LENGTH)
        self.logger.debug('Got response: %s', response)
        if response == ResponseT.CHECK_FOUND_RESPONSE:
            return True
        if response == ResponseT.CHECK_NOT_FOUND_RESPONSE:
            return False

        self.logger.error('Received unexpected response: %s', response)
        raise UnexpectedResponseError(response)

    async def size(self, blob_hash: str) -> int:
        if not self.is_connected:
            await self.connect()

        self.logger.debug('Getting size for blob: %s', blob_hash)
        blob_hash_bytes = bytes.fromhex(blob_hash)
        await self._send(CommandT.SIZE + HASH_TYPE + blob_hash_bytes)
        self.logger.debug('Sent %s command', CommandT.SIZE)

        response = await self._receive(RESPONSE_LENGTH + 8)
        self.logger.debug('Got response: %s', response)
        if response[:RESPONSE_LENGTH] == ResponseT.SIZE_NOT_FOUND_RESPONSE:
            self.logger.error('Blob not found: %s', blob_hash)
            raise BlobNotFoundError(blob_hash)
        if response[:RESPONSE_LENGTH] != ResponseT.SIZE_OK_RESPONSE:
            self.logger.error('Received unexpected response: %s', response)
            raise UnexpectedResponseError(response)
        return int.from_bytes(response[RESPONSE_LENGTH:], 'little')

    async def stream(self, blob_hash: str, reader: 'AsyncReader') -> None:
        if not self.is_connected:
            await self.connect()

        self.logger.debug('Streaming blob: %s', blob_hash)
        blob_hash_bytes = bytes.fromhex(blob_hash)
        await self._send(CommandT.STREAM + HASH_TYPE + blob_hash_bytes)

        chunk = await reader.read(STREAM_MAX_CHUNK_SIZE)
        while chunk:
            size_header = len(chunk).to_bytes(2, 'little')
            if self.verbose_debug:
                self.logger.debug(
                    'Streaming chunk of size: %d (%s)', len(chunk), size_header.hex()
                )
            await self._send(size_header)
            await self._send(chunk)
            chunk = await reader.read(STREAM_MAX_CHUNK_SIZE)

        self.logger.debug('Ending stream')
        await self._send(b'\x00\x00')

        response = await self._receive(RESPONSE_LENGTH)
        self.logger.debug('Got response: %s', response)
        if response != ResponseT.STREAM_OK_RESPONSE:
            self.logger.error('Received unexpected response: %s', response)
            raise UnexpectedResponseError(response)

    async def pull(self, blob_hash: str, writer: AsyncWriter) -> None:
        if not self.is_connected:
            await self.connect()

        self.logger.debug('Pulling blob: %s', blob_hash)
        blob_hash_bytes = bytes.fromhex(blob_hash)
        await self._send(CommandT.PULL + HASH_TYPE + blob_hash_bytes + b'\x00' * 12)

        response = await self._receive(RESPONSE_LENGTH)
        if response == ResponseT.PULL_NOT_FOUND_RESPONSE:
            self.logger.error('Blob not found: %s', blob_hash)
            raise BlobNotFoundError(blob_hash)

        if response != ResponseT.PULL_FOUND_RESPONSE:
            self.logger.error('Received unexpected response: %s', response)
            raise UnexpectedResponseError(response)

        response = await self._receive(len(HASH_TYPE) + len(blob_hash_bytes) + 12)

        blob_size = int.from_bytes(
            response[len(HASH_TYPE) + len(blob_hash_bytes) : -4], 'little'
        )
        self.logger.debug('Blob size: %d', blob_size)
        received = 0

        while received < blob_size:
            chunk_size = min(STREAM_MAX_CHUNK_SIZE, blob_size - received)
            if self.verbose_debug:
                self.logger.debug('Pulling chunk of size: %d', chunk_size)
            chunk = await self._receive(chunk_size)
            received += chunk_size
            if self.verbose_debug:
                self.logger.debug('Received %d bytes', len(chunk))
            await writer.write(chunk)

        await writer.flush()

        self.logger.debug('Pulled %d for blob %s', received, blob_hash)


class ConnectionPool:
    connect_timeout: float
    server_root: str
    servers: set[tuple[str, int]]
    connection_per_server: int
    logger: Logger | LoggerAdapter
    verbose_debug: bool

    _lock: asyncio.Lock
    _connections: set[CAFSConnection]
    _connection_queue: asyncio.Queue[CAFSConnection]
    _close_event: asyncio.Event

    def __init__(
        self,
        server_root: str,
        servers: Collection[tuple[str, int]],
        connection_per_server: int = 1,
        connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
        logger: Logger | LoggerAdapter | None = None,
        verbose_debug: bool = False,
    ) -> None:
        self.server_root = server_root
        self.connect_timeout = connect_timeout
        self.servers = set(servers)
        self.connection_per_server = connection_per_server

        self._connections = set()
        self._connection_queue = asyncio.Queue()
        self._lock = asyncio.Lock()
        self._close_event = asyncio.Event()
        self.logger = logger or module_logger
        self.verbose_debug = verbose_debug

    async def get_connection_count(self) -> int:
        async with self._lock:
            return len(self._connections)

    async def initialize(self) -> None:
        self.logger.debug(
            'Initializing connection pool with %d servers (%d connections each)',
            len(self.servers),
            self.connection_per_server,
        )
        for server in self.servers:
            host, port = server
            for _ in range(self.connection_per_server):
                conn = CAFSConnection(
                    self.server_root,
                    host,
                    port,
                    timeout=self.connect_timeout,
                    logger=self.logger,
                    verbose_debug=self.verbose_debug,
                )
                self._connections.add(conn)
                await self._connection_queue.put(conn)
        self.logger.debug('Connection pool initialized')

    async def _get_connection(self) -> CAFSConnection:
        if self._close_event.is_set():
            raise EmptyConnectionPoolError()
        get_task = asyncio.create_task(self._connection_queue.get())
        close_task = asyncio.create_task(self._close_event.wait())
        self.logger.debug('Waiting for connection')
        _, pending = await asyncio.wait(
            [get_task, close_task], return_when=asyncio.FIRST_COMPLETED
        )

        for task in pending:
            task.cancel()

        if get_task in pending:
            raise EmptyConnectionPoolError()

        conn = get_task.result()
        self.logger.debug('Got connection %s', id(conn))
        return conn

    async def _release_connection(self, conn: CAFSConnection) -> None:
        self.logger.debug('Releasing connection %s', id(conn))
        await self._connection_queue.put(conn)

    async def _delete_connection(self, conn: CAFSConnection) -> None:
        self.logger.debug('Deleting connection %s', id(conn))
        await conn.disconnect()
        async with self._lock:
            self._connections.remove(conn)
            if not self._connections:
                self.logger.debug('Connection pool is empty, closing')
                self._close_event.set()

    async def close(self) -> None:
        self.logger.debug('Closing connection pool')
        async with self._lock:
            self._close_event.set()
            for conn in self._connections:
                if conn.is_connected:
                    await conn.disconnect()
            self._connections.clear()

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[CAFSConnection]:
        conn = await self._get_connection()
        try:
            yield conn
        except Exception:
            await self._delete_connection(conn)
            raise
        await self._release_connection(conn)

    async def __aenter__(self) -> Self:
        await self.initialize()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()


T = TypeVar('T')


async def _until_pool_empty_wrapper(
    func: Callable[[], Coroutine[Any, Any, T]], retry: bool = True
) -> T:
    if not retry:
        return await func()

    while True:
        try:
            return await func()
        except EmptyConnectionPoolError:
            raise
        except Exception:  # pylint: disable=broad-exception-caught  # nosec: try_except_pass
            pass


class CAFSClient:
    logger: Logger | LoggerAdapter
    verbose_debug: bool

    _connection_pool: ConnectionPool

    def __init__(
        self,
        server_root: str,
        servers: Collection[str],
        connection_per_server: int = 1,
        connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
        logger: Logger | LoggerAdapter | None = None,
        verbose_debug: bool = False,
    ) -> None:
        self.verbose_debug = verbose_debug
        servers_ = {self.parse_server_uri(server) for server in servers}
        self.logger = logger or module_logger
        self._connection_pool = ConnectionPool(
            server_root,
            servers_,
            connection_per_server,
            connect_timeout,
            logger=self.logger,
            verbose_debug=self.verbose_debug,
        )

    async def pull(self, blob_hash: str, path: Path, retry: bool = True) -> None:
        self.logger.info('Pulling %s to %s', blob_hash, path)
        await aio_os.makedirs(path.parent, exist_ok=True)

        async def _pull() -> None:
            async with aiofiles.open(path, 'wb') as file:
                async with self._connection_pool.connection() as conn:
                    unpacker = Unpacker(
                        file, logger=conn.logger, verbose_debug=self.verbose_debug
                    )
                    await conn.pull(blob_hash, unpacker)

        await _until_pool_empty_wrapper(_pull, retry=retry)

    async def pull_batch(
        self,
        blobs: list[tuple[str, Path]],
        retry: bool = True,
        max_concurrent: int | None = None,
    ) -> None:
        if not blobs:
            return

        max_concurrent = min(
            max_concurrent or await self._connection_pool.get_connection_count(),
            len(blobs),
        )

        files_queue: asyncio.Queue[tuple[str, Path]] = asyncio.Queue()
        for blob_hash, blob_path in blobs:
            files_queue.put_nowait((blob_hash, blob_path))

        async def worker(stop_event_: asyncio.Event) -> None:
            while not stop_event_.is_set():
                try:
                    f_hash, f_path = files_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
                try:
                    await self.pull(f_hash, f_path, retry=retry)
                except EmptyConnectionPoolError:
                    stop_event_.set()
                    raise
                finally:
                    files_queue.task_done()

        stop_event = asyncio.Event()
        self.logger.debug('Initializing %d workers', max_concurrent)
        workers = [
            asyncio.create_task(worker(stop_event)) for _ in range(max_concurrent)
        ]
        errors = await asyncio.gather(*workers, return_exceptions=True)

        for err in errors:
            if isinstance(err, Exception):
                raise err

    async def check(self, blob_hash: str, retry: bool = True) -> bool:
        async def _check() -> bool:
            async with self._connection_pool.connection() as conn:
                return await conn.check(blob_hash)

        return await _until_pool_empty_wrapper(_check, retry=retry)

    async def size(self, blob_hash: str, retry: bool = True) -> int:
        async def _size() -> int:
            async with self._connection_pool.connection() as conn:
                return await conn.size(blob_hash)

        return await _until_pool_empty_wrapper(_size, retry=retry)

    async def stream(
        self,
        path: Path,
        compression: CompressionT = CompressionT.NONE,
        retry: bool = True,
    ) -> str:
        blob_hash: str = await calc_hash_file(path)
        compression = choose_compression(path, preferred_compression=compression)
        self.logger.info(
            'Streaming %s to %s with %s compression', path, blob_hash, compression
        )

        async def _stream() -> str:
            async with aiofiles.open(path, 'rb') as file:
                async with self._connection_pool.connection() as conn:
                    packer = Packer(
                        file,
                        compression=compression,
                        logger=conn.logger,
                        verbose_debug=self.verbose_debug,
                    )
                    await conn.stream(blob_hash, packer)
            return blob_hash

        return await _until_pool_empty_wrapper(_stream, retry=retry)

    async def stream_batch(
        self,
        paths: list[Path],
        compression: CompressionT = CompressionT.NONE,
        retry: bool = True,
        max_concurrent: int | None = None,
    ) -> list[str]:
        if not paths:
            return []

        max_concurrent = min(
            max_concurrent or await self._connection_pool.get_connection_count(),
            len(paths),
        )

        files_queue: asyncio.Queue[tuple[int, Path]] = asyncio.Queue()
        for idx, path in enumerate(paths):
            files_queue.put_nowait((idx, path))
        results: list[str | None] = [None] * len(paths)

        async def worker(stop_event_: asyncio.Event) -> None:
            while not stop_event_.is_set():
                try:
                    f_idx, f_path = files_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
                try:
                    blob_hash = await self.stream(
                        f_path, compression=compression, retry=retry
                    )
                    results[f_idx] = blob_hash
                except EmptyConnectionPoolError:
                    stop_event_.set()
                    raise
                finally:
                    files_queue.task_done()

        stop_event = asyncio.Event()
        self.logger.debug('Initializing %d workers', max_concurrent)
        workers = [
            asyncio.create_task(worker(stop_event)) for _ in range(max_concurrent)
        ]
        errors = await asyncio.gather(*workers, return_exceptions=True)

        for err in errors:
            if isinstance(err, Exception):
                raise err
        if any(res is None for res in results):
            raise CAFSClientError(
                'Unexpected error during streaming, some blobs are None'
            )

        return results

    async def __aenter__(self) -> Self:
        await self._connection_pool.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self._connection_pool.__aexit__(exc_type, exc_val, exc_tb)

    @staticmethod
    def parse_server_uri(uri: str) -> tuple[str, int]:
        if ':' in uri:
            host, port = uri.rsplit(':', maxsplit=1)
            return host, int(port)
        return uri, CAFS_DEFAULT_PORT
