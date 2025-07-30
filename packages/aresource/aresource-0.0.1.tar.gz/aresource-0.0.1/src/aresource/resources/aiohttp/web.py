import contextlib
from collections.abc import AsyncIterator, Callable
from typing import Any

from aiohttp import web

from aresource.manager import BaseResource, ResourceManager


class WebAppResource(BaseResource[web.Application]):
    """
    Resource that provides an aiohttp ClientSession.
    """

    def __init__(
        self,
        routes: Callable[[ResourceManager], web.RouteTableDef],
        callback: Callable[[ResourceManager], dict[str, Any]] | None = None,
    ) -> None:
        super().__init__()
        self.callback = callback
        self.routes = routes

    @contextlib.asynccontextmanager
    async def acquire(self, manager: "ResourceManager") -> AsyncIterator[web.Application]:
        kwargs = self.callback(manager) if self.callback else {}
        app = web.Application(**kwargs)

        routes = self.routes(manager)
        app.add_routes(routes)

        runner = web.AppRunner(app)

        await runner.setup()
        site = web.TCPSite(runner, "localhost", 8081)

        try:
            await site.start()
            yield app
        finally:
            await site.stop()
            await app.shutdown()
