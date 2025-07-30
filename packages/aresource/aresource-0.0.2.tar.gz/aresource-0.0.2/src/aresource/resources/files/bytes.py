import contextlib
from collections.abc import AsyncIterator

from aresource.manager import ResourceManager
from aresource.resources.files.base import BasePathResource


class BytesResource(BasePathResource[bytes]):
    """
    Resource that provides a binary file in a package.
    """

    @contextlib.asynccontextmanager
    async def acquire(self, manager: "ResourceManager") -> AsyncIterator[bytes]:
        yield self.read()
