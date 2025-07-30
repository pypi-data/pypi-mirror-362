import asyncio
import functools
from collections.abc import Awaitable, Callable
from logging import Logger, LoggerAdapter, getLogger
from os.path import normpath
from pathlib import Path
from typing import Any, Self, TypeVar

import aiofiles.os as aio_os

from cafs_cache_cdn_client.cafs import CAFSClient, CompressionT
from cafs_cache_cdn_client.file_utils import (
    LocalFile,
    compare_file_lists,
    set_file_stat,
    walk,
)
from cafs_cache_cdn_client.repo import RepoClient

__all__ = ('CacheCdnClient',)


package_logger = getLogger(__name__.split('.')[0])


CAFS_SERVER_ROOT = '/cache'


T = TypeVar('T')


def needs_cafs_client(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    @functools.wraps(func)
    async def wrapper(self: 'CacheCdnClient', *args: Any, **kwargs: Any) -> T:
        await self._init_cafs_client()
        return await func(self, *args, **kwargs)

    return wrapper


class CacheCdnClient:
    verbose_debug: bool

    _cafs_client: CAFSClient | None = None
    _repo_client: RepoClient

    __connection_per_cafs_server: int
    __cafs_client_lock: asyncio.Lock

    def __init__(
        self,
        server: str,
        connection_per_cafs_server: int = 1,
        logger: Logger | LoggerAdapter | None = None,
        verbose_debug: bool = False,
    ) -> None:
        self.logger = logger or package_logger
        self._repo_client = RepoClient(server, logger=self.logger)
        self.__connection_per_cafs_server = connection_per_cafs_server
        self.verbose_debug = verbose_debug
        self.__cafs_client_lock = asyncio.Lock()

    async def _init_cafs_client(self) -> None:
        self.logger.debug(
            'Initializing CAFS client with %d connections per server',
            self.__connection_per_cafs_server,
        )
        async with self.__cafs_client_lock:
            if self._cafs_client:
                self.logger.debug('CAFS client already initialized')
                return
            self.logger.debug('Fetching blob URLs from the server')
            blob_urls = await self._repo_client.get_blob_urls()
            self.logger.debug('Blob URLs: %s', blob_urls)
            self._cafs_client = await CAFSClient(
                CAFS_SERVER_ROOT,
                blob_urls,
                connection_per_server=self.__connection_per_cafs_server,
                logger=self.logger,
                verbose_debug=self.verbose_debug,
            ).__aenter__()

    @needs_cafs_client
    async def push(
        self,
        repo: str,
        ref: str,
        directory: Path | str,
        ttl_hours: int = 0,
        comment: str | None = None,
        compression: CompressionT = CompressionT.NONE,
    ) -> None:
        self.logger.info(
            'Pushing %s to %s/%s with ttl=%d hours, compression=%s',
            directory,
            repo,
            ref,
            ttl_hours,
            compression,
        )
        if isinstance(directory, str):
            directory = Path(directory)
        if not directory.is_dir():
            raise ValueError(f'{directory} is not a directory')
        files = walk(directory)
        self.logger.debug('Uploading %d files to CAFS server')
        hashes = await self._cafs_client.stream_batch(
            [directory / file.path for file in files],
            compression=compression,
        )
        self.logger.debug('CAFS upload complete, uploading metadata to the server')
        await self._repo_client.post_ref_info(
            repo,
            ref,
            {
                'archive': False,
                'ttl': ttl_hours * 60 * 60 * 10**9,
                'comment': comment,
                'files': [
                    {
                        'blob': blob,
                        'path': file.path.as_posix(),
                        'mtime': file.mtime,
                        'mode': file.mode,
                    }
                    for blob, file in zip(hashes, files)
                ],
            },
        )
        self.logger.info('Pushed %d files to %s/%s successfully', len(files), repo, ref)

    async def check(self, repo: str, ref: str) -> bool:
        self.logger.info('Checking %s/%s', repo, ref)
        res = await self._repo_client.is_ref_exist(repo, ref)
        if res:
            self.logger.info('Ref %s/%s exists', repo, ref)
        else:
            self.logger.info('Ref %s/%s does not exist', repo, ref)
        return res

    async def delete(self, repo: str, ref: str) -> None:
        self.logger.info('Deleting %s/%s', repo, ref)
        await self._repo_client.delete_ref(repo, ref)
        self.logger.info('Deleted %s/%s successfully', repo, ref)

    async def attach(self, repo: str, ref: str, file_path: Path) -> None:
        self.logger.info('Attaching %s to %s/%s', file_path, repo, ref)
        await self._repo_client.attach_file(repo, ref, file_path)
        self.logger.info('Attached %s to %s/%s successfully', file_path, repo, ref)

    @needs_cafs_client
    async def pull(self, repo: str, ref: str, directory: Path | str) -> None:
        self.logger.info('Pulling %s/%s to %s', repo, ref, directory)
        if isinstance(directory, str):
            directory = Path(directory)
        await aio_os.makedirs(directory, exist_ok=True)
        self.logger.debug('Fetching info about %s/%s from the server', repo, ref)
        ref_info = await self._repo_client.get_ref_info(repo, ref)
        remote_files = [
            LocalFile(
                path=Path(normpath(file['path'])),
                mtime=file['mtime'],
                mode=file['mode'],
                blob=file['blob'],
            )
            for file in ref_info['files']
        ]
        self.logger.debug('%d files on the server', len(remote_files))
        local_files = walk(directory)
        self.logger.debug('%d files locally', len(local_files))
        to_remove, to_add, to_update = await compare_file_lists(
            local_files, remote_files, directory
        )
        self.logger.debug(
            'Files to remove: %d, files to add: %d, files to update: %d',
            len(to_remove),
            len(to_add),
            len(to_update),
        )
        for file in to_remove:
            await aio_os.unlink(directory / file.path)
        if to_add:
            self.logger.debug('Downloading %d files from CAFS server', len(to_add))
            await self._cafs_client.pull_batch(
                [(file.blob, directory / file.path) for file in to_add]
            )
            self.logger.debug('CAFS download complete')
        for file in to_add + to_update:
            set_file_stat(file, directory)
        self.logger.info(
            'Pulled %d files from %s/%s successfully, updated %d files, removed %d files',
            len(to_add),
            repo,
            ref,
            len(to_update),
            len(to_remove),
        )

    async def tag(self, repo: str, ref: str, tag: str) -> None:
        self.logger.info('Tagging %s/%s to %s', repo, ref, tag)
        await self._repo_client.tag_ref(repo, ref, tag)
        self.logger.info('Tagged %s/%s to %s successfully', repo, ref, tag)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        async with self.__cafs_client_lock:
            if not self._cafs_client:
                return
            await self._cafs_client.__aexit__(exc_type, exc_val, exc_tb)
            self._cafs_client = None
