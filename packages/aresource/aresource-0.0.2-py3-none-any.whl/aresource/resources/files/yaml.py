import contextlib
import io
from collections.abc import AsyncIterator
from typing import Any

from yaml import SafeLoader, load_all

from aresource.manager import ResourceManager
from aresource.resources.files.base import BasePathResource

T = list[Any]


class YamlResource(BasePathResource[T]):
    """
    Resource that provides a JSON file in a package.
    """

    @contextlib.asynccontextmanager
    async def acquire(self, manager: "ResourceManager") -> AsyncIterator[T]:
        stream = io.StringIO(self.read().decode("utf-8"))
        yield list(load_all(stream, Loader=SafeLoader))
