import contextlib
from abc import ABCMeta
from collections.abc import Iterator
from importlib.resources import as_file, files
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import TypeVar

from aresource.manager import BaseResource

T = TypeVar("T")


class BasePathResource[T](BaseResource[T], metaclass=ABCMeta):
    def __init__(self, package: str, path: str) -> None:
        super().__init__()
        self.package = package
        self.path = path

    @property
    def resource(self) -> Traversable:
        """
        Get the path to the resource in the package.
        """
        return files(self.package).joinpath(self.path)

    @contextlib.contextmanager
    def as_file(self) -> Iterator[Path]:
        """
        Context manager to yield the path to the resource as a file.
        """
        with as_file(self.resource) as resource_path:
            yield resource_path

    def read(self) -> bytes:
        return self.resource.read_bytes()
