import zlib
from enum import Enum
from logging import Logger, LoggerAdapter, getLogger
from typing import Protocol

try:
    import zstandard as zstd
except ImportError:
    zstd = None  # type: ignore[assignment]

from cafs_cache_cdn_client.cafs.types import AsyncReader, AsyncWriter

__all__ = (
    'CompressionT',
    'Packer',
    'Unpacker',
)


module_logger = getLogger(__name__)


class CompressionT(bytes, Enum):
    ZSTD = b'ZSTD'
    ZLIB = b'ZLIB'
    NONE = b'NONE'

    def __str__(self) -> str:
        return self.decode('utf-8')


FULL_HEADER_SIZE = 16
COMPRESSION_HEADER_SIZE = 4
DEFAULT_CHUNK_SIZE = 16 * 1024 * 1024


class Compressor(Protocol):
    def compress(self, data: bytes) -> bytes:
        pass

    def flush(self) -> bytes:
        pass


class Decompressor(Protocol):
    def decompress(self, data: bytes) -> bytes:
        pass

    def flush(self) -> bytes:
        pass


class Packer:
    logger: Logger | LoggerAdapter
    chunk_size: int
    verbose_debug: bool

    _reader: 'AsyncReader'
    _eof_reached: bool
    _buffer: bytearray
    _compressor: Compressor | None

    def __init__(
        self,
        reader: 'AsyncReader',
        compression: CompressionT = CompressionT.NONE,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        logger: Logger | LoggerAdapter | None = None,
        verbose_debug: bool = False,
    ) -> None:
        self._reader = reader
        self._eof_reached = False
        self.chunk_size = chunk_size
        self.verbose_debug = verbose_debug

        self._compressor = None
        if compression == CompressionT.ZLIB:
            self._compressor = zlib.compressobj()
        elif compression == CompressionT.ZSTD:
            if not zstd:
                raise RuntimeError(
                    'ZSTD compression is not available, please install zstandard'
                )
            self._compressor = zstd.ZstdCompressor().compressobj()

        self._buffer = bytearray(
            compression + b'\x00' * (FULL_HEADER_SIZE - COMPRESSION_HEADER_SIZE)
        )
        self.logger = logger or module_logger
        self.logger.debug('Initialized packer with compression: %s', compression)

    async def read(self, size: int = -1) -> bytes:
        if size == 0:
            return b''

        while (size > 0 and len(self._buffer) < size) and not self._eof_reached:
            await self._fill_buffer()

        if size < 0 or len(self._buffer) <= size:
            result = bytes(self._buffer)
            self._buffer.clear()
            return result

        result = bytes(self._buffer[:size])
        self._buffer = self._buffer[size:]
        return result

    async def _fill_buffer(self) -> None:
        chunk = await self._reader.read(self.chunk_size)
        if self.verbose_debug:
            self.logger.debug('Filling buffer with chunk of %d bytes', len(chunk))

        if not chunk:
            self._eof_reached = True
            self.logger.debug('EOF reached')
            if self._compressor:
                data = self._compressor.flush()
                if self.verbose_debug:
                    self.logger.debug('Flushing compressor: %d bytes', len(data))
                self._buffer.extend(data)
            return

        if not self._compressor:
            self._buffer.extend(chunk)
            return

        data = self._compressor.compress(chunk)
        if self.verbose_debug:
            self.logger.debug('Got %d bytes from compressor', len(data))
        self._buffer.extend(data)


class Unpacker:
    logger: Logger | LoggerAdapter
    chunk_size: int
    verbose_debug: bool

    _writer: 'AsyncWriter'
    _header: bytearray
    _buffer: bytearray
    _decompressor: Decompressor | None

    def __init__(
        self,
        writer: 'AsyncWriter',
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        logger: Logger | LoggerAdapter | None = None,
        verbose_debug: bool = False,
    ) -> None:
        self._writer = writer
        self._buffer = bytearray()
        self._decompressor = None
        self._header = bytearray()
        self.chunk_size = chunk_size
        self.logger = logger or module_logger
        self.verbose_debug = verbose_debug

    async def write(self, data: bytes, /) -> None:
        if not data:
            return
        await self._fill_buffer(data)
        if len(self._buffer) >= self.chunk_size:
            await self._writer.write(self._buffer)
            self._buffer.clear()

    async def flush(self) -> None:
        if self._decompressor:
            data = self._decompressor.flush()
            if self.verbose_debug:
                self.logger.debug('Flushing decompressor: %d bytes', len(data))
            self._buffer.extend(data)
        if self._buffer:
            await self._writer.write(self._buffer)
            self._buffer.clear()
            await self._writer.flush()

    async def _fill_buffer(self, data: bytes) -> None:
        if self.verbose_debug:
            self.logger.debug('Filling buffer with chunk of %d bytes', len(data))
        if len(self._header) < FULL_HEADER_SIZE:
            header_offset = FULL_HEADER_SIZE - len(self._header)
            self._header.extend(data[:header_offset])
            data = data[header_offset:]
            if len(self._header) < FULL_HEADER_SIZE:
                return

            compression_type = CompressionT(self._header[:COMPRESSION_HEADER_SIZE])
            self.logger.debug('Extracted compression type: %s', compression_type)

            if compression_type == CompressionT.NONE:
                self._decompressor = None
            elif compression_type == CompressionT.ZLIB:
                d = zlib.decompressobj()
                self._decompressor = d
            elif compression_type == CompressionT.ZSTD:
                if not zstd:
                    raise RuntimeError('zstandard is not available')
                self._decompressor = zstd.ZstdDecompressor().decompressobj()

        if not data:
            return

        if not self._decompressor:
            self._buffer.extend(data)
            return

        data = self._decompressor.decompress(data)
        if self.verbose_debug:
            self.logger.debug('Got %d bytes from decompressor', len(data))
        self._buffer.extend(data)
