from pathlib import Path

import aiofiles
from blake3 import blake3

from cafs_cache_cdn_client.cafs.types import AsyncReader

__all__ = (
    'calc_hash',
    'calc_hash_file',
)

DEFAULT_BUFFER_SIZE = 4 * 1024 * 1024


async def calc_hash(
    reader: 'AsyncReader', buffer_size: int = DEFAULT_BUFFER_SIZE
) -> str:
    hasher = blake3()  # pylint: disable=not-callable

    while True:
        buffer = await reader.read(buffer_size)
        if not buffer:
            break
        hasher.update(buffer)

    return hasher.hexdigest()


async def calc_hash_file(
    file_path: Path, buffer_size: int = DEFAULT_BUFFER_SIZE
) -> str:
    async with aiofiles.open(file_path, 'rb') as f:
        return await calc_hash(f, buffer_size)
