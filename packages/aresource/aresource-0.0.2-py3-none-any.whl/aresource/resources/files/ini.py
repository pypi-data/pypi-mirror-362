import configparser
import contextlib
from collections.abc import AsyncIterator
from configparser import ConfigParser

from aresource.manager import ResourceManager
from aresource.resources.files.base import BasePathResource


class IniResource(BasePathResource[ConfigParser]):
    """
    Resource that provides a JSON file in a package.
    """

    @contextlib.asynccontextmanager
    async def acquire(self, manager: "ResourceManager") -> AsyncIterator[ConfigParser]:
        config = configparser.ConfigParser()
        config.read_string(self.read().decode("utf-8"))
        yield config
