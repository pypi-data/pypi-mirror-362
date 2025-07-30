from typing import TypedDict

__all__ = (
    'SettingsResponse',
    'RefInfoResponse',
    'RefInfoBody',
    'FileMetadata',
)


class FileMetadata(TypedDict):
    blob: str
    path: str
    mtime: int
    mode: int


class SettingsResponse(TypedDict):
    blob_urls: list[str]


class RefInfoResponse(TypedDict):
    revision: int
    archive: bool
    ttl: int
    updated: int
    files: list[FileMetadata]


class RefInfoBody(TypedDict):
    archive: bool
    ttl: int
    comment: str | None
    files: list[FileMetadata]
