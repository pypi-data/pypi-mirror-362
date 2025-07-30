from pathlib import Path

from .package import CompressionT

__all__ = ('choose_compression',)

MAGIC_HEADER_SIZE = 4
MINIMAL_COMPRESSION_SIZE = 1024


# Magic header prefixes for various compression formats
MAGIC_HEADER_PREFIXES = [
    bytes([0x1F, 0x8B]),  # gzip
    bytes([0x42, 0x5A, 0x68]),  # bzip2
    bytes([0x50, 0x4B, 0x03]),  # zip
    bytes([0x28, 0xB5, 0x2F, 0xFD]),  # zstd
    bytes([0x78, 0x01]),  # default compression level
]


def is_file_already_compressed(file_path: Path) -> bool:
    with open(file_path, 'rb') as file:
        magic_header_buff = file.read(MAGIC_HEADER_SIZE)

    return any(magic_header_buff.startswith(prefix) for prefix in MAGIC_HEADER_PREFIXES)


def choose_compression(
    file_path: Path, preferred_compression: CompressionT = CompressionT.NONE
) -> CompressionT:
    if preferred_compression == CompressionT.NONE:
        return preferred_compression

    if file_path.stat().st_size < MINIMAL_COMPRESSION_SIZE:
        return CompressionT.NONE

    if is_file_already_compressed(file_path):
        return CompressionT.NONE

    return preferred_compression
