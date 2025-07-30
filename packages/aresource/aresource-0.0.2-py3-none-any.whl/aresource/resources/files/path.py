import contextlib
from collections.abc import AsyncIterator
from importlib.resources import as_file
from pathlib import Path

from aresource.manager import ResourceManager
from aresource.resources.files.base import BasePathResource


class PathResource(BasePathResource[Path]):
    """
    Resource that provides a path to a file in a package.
    """

    @contextlib.asynccontextmanager
    async def acquire(self, manager: "ResourceManager") -> AsyncIterator[Path]:
        with as_file(self.resource) as resource_path:
            yield resource_path
