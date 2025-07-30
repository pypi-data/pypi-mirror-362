import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from cafs_cache_cdn_client.cafs.blob.hash_ import calc_hash_file

__all__ = (
    'LocalFile',
    'walk',
    'compare_file_lists',
    'set_file_stat',
)


if sys.platform == 'win32':

    def is_same_mtime(
        t1: int,
        t2: int,
    ) -> bool:
        return t1 // 100 == t2 // 100
else:

    def is_same_mtime(
        t1: int,
        t2: int,
    ) -> bool:
        return t1 == t2


@dataclass
class LocalFile:
    path: Path
    mtime: int
    mode: int
    blob: str | None = None


def walk(directory: Path) -> list[LocalFile]:
    results = []
    for root, _, files in os.walk(str(directory)):
        root_ = Path(root)
        for file in files:
            file_ = root_ / file
            file_stat = file_.stat()
            results.append(
                LocalFile(
                    path=file_.relative_to(directory),
                    mtime=file_stat.st_mtime_ns,
                    mode=file_stat.st_mode & 0o777,
                )
            )
    return results


async def compare_file_lists(
    src_files: list[LocalFile],
    dst_files: list[LocalFile],
    directory: Path,
) -> tuple[list[LocalFile], list[LocalFile], list[LocalFile]]:
    src_files_dict = {file.path: file for file in src_files}
    dst_files_dict = {file.path: file for file in dst_files}
    to_remove = src_files_dict.keys() - dst_files_dict.keys()
    to_add = dst_files_dict.keys() - src_files_dict.keys()
    to_update = set()
    for same_file in src_files_dict.keys() & dst_files_dict.keys():
        if not dst_files_dict[same_file].blob:
            to_remove.add(same_file)
            to_add.add(same_file)
            continue
        if not src_files_dict[same_file].blob:
            src_files_dict[same_file].blob = await calc_hash_file(directory / same_file)
        if src_files_dict[same_file].blob != dst_files_dict[same_file].blob:
            to_remove.add(same_file)
            to_add.add(same_file)
            continue
        if (
            not is_same_mtime(
                src_files_dict[same_file].mtime, dst_files_dict[same_file].mtime
            )
            or src_files_dict[same_file].mode != dst_files_dict[same_file].mode
        ):
            to_update.add(same_file)

    return (
        [src_files_dict[file] for file in to_remove],
        [dst_files_dict[file] for file in to_add],
        [src_files_dict[file] for file in to_update],
    )


def set_file_stat(file: LocalFile, directory: Path) -> None:
    file_ = directory / file.path
    file_.chmod(file.mode)
    os.utime(file_, ns=(time.time_ns(), file.mtime))
