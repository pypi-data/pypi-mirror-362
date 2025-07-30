from typing import Any, Protocol

__all__ = (
    'AsyncReader',
    'AsyncWriter',
)


class AsyncReader(Protocol):
    async def read(self, size: int = -1) -> bytes:
        pass


class AsyncWriter(Protocol):
    async def write(self, data: bytes, /) -> Any:
        pass

    async def flush(self) -> None:
        pass
