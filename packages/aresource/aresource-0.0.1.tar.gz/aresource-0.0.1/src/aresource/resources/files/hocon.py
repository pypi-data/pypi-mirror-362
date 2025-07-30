import contextlib
from collections.abc import AsyncIterator

from pyhocon import ConfigFactory, ConfigTree

from aresource.manager import ResourceManager
from aresource.resources.files.base import BasePathResource


class HoconResource(BasePathResource[ConfigTree]):
    """
    Resource that provides a JSON file in a package.
    """

    @contextlib.asynccontextmanager
    async def acquire(self, manager: "ResourceManager") -> AsyncIterator[ConfigTree]:
        yield ConfigFactory.parse_string(self.read().decode("utf-8"))
