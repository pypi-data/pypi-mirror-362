import contextlib
import json
from collections.abc import AsyncIterator
from typing import Any

from aresource.manager import ResourceManager
from aresource.resources.files.base import BasePathResource

T = dict[str, Any] | list[Any]


class JsonResource(BasePathResource[T]):
    """
    Resource that provides a JSON file in a package.
    """

    @contextlib.asynccontextmanager
    async def acquire(self, manager: "ResourceManager") -> AsyncIterator[T]:
        data = self.read()
        yield json.loads(data)
