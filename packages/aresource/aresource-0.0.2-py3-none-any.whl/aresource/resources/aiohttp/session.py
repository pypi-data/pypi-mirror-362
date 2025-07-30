import contextlib
from collections.abc import AsyncIterator, Callable
from typing import Any

from aiohttp import ClientSession

from aresource.manager import BaseResource, ResourceManager


class ClientSessionResource(BaseResource[ClientSession]):
    """
    Resource that provides an aiohttp ClientSession.
    """

    def __init__(
        self, callback: Callable[[ResourceManager], dict[str, Any]] | None = None
    ) -> None:
        super().__init__()
        self.callback = callback

    @contextlib.asynccontextmanager
    async def acquire(self, manager: "ResourceManager") -> AsyncIterator[ClientSession]:
        kwargs = self.callback(manager) if self.callback else {}
        session = ClientSession(**kwargs)
        try:
            yield session
        finally:
            await session.close()  # Ensure the session is closed after use
