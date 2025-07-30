import contextlib
import copy
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Callable
from typing import Any, ClassVar, Self, TypeVar

T = TypeVar("T")


class BaseResource[T](ABC):
    name: str | None = None

    def __get__(self, instance: "ResourceManager", owner: "type[ResourceManager]") -> T:
        return instance.get_resource(self.name)  # type: ignore[no-any-return]

    def __set_name__(self, owner: "type[ResourceManager]", name: str) -> None:
        owner.register_resource(name, self)

    @abstractmethod
    @contextlib.asynccontextmanager
    async def acquire(self, manager: "ResourceManager") -> AsyncIterator[T]:
        """Acquire the resource asynchronously."""
        yield None  # type: ignore[misc]


class CallBackResource[T](BaseResource[T]):
    def __init__(
        self,
        callback: Callable[["ResourceManager"], AsyncIterator[T]],
    ) -> None:
        self.callback = contextlib.asynccontextmanager(callback)

    @contextlib.asynccontextmanager
    async def acquire(self, manager: "ResourceManager") -> AsyncIterator[T]:
        async with self.callback(manager) as value:
            yield value


def resource[T](fn: Callable[["ResourceManager"], AsyncIterator[T]]) -> CallBackResource[T]:
    return CallBackResource(fn)


class ResourceManager:
    _cls: Any = None
    _resources: ClassVar[dict[str, tuple[BaseResource[Any], Any]]] = {}

    def __init__(self) -> None:
        self._exitstack: contextlib.AsyncExitStack | None = None

    @classmethod
    def register_resource(cls, name: str, resource: BaseResource[Any]) -> None:
        """Register a resource with the manager."""
        if not isinstance(resource, BaseResource):
            raise TypeError(f"{resource.__name__} is not a subclass of BaseResource")
        if name in cls._resources:
            raise AttributeError(f"Resource {name} is already registered in {cls.__name__}")
        # Create a copy of the class resources to avoid modifying the superclass
        if cls._cls is not cls:
            cls._resources = copy.deepcopy(cls._resources)
            cls._cls = cls

        cls._resources[name] = (resource, ...)
        resource.name = name

    def get_resource(self, name: str | None) -> Any:
        """
        Get the value of a registered resource by name.
        """
        if name not in self._resources:
            raise AttributeError(f"Resource {name} is not registered in {self.__class__.__name__}")
        value = self._resources[name][1]
        if value is Ellipsis:
            raise AttributeError(
                f"Resource {name} is not initialized in {self.__class__.__name__}"
            )
        return value

    def set_resource(self, name: str, value: Any) -> None:
        """
        Set the value of a registered resource by name.
        Raises AttributeError if the resource is not registered.
        """
        if name not in self._resources:
            raise AttributeError(f"Resource {name} is not registered in {self.__class__.__name__}")

        resource = self._resources[name][0]
        self._resources[name] = (resource, value)

    async def setup(self) -> None:
        await self.__aenter__()

    async def __aenter__(self) -> Self:
        """Asynchronously enter the resource manager context, acquiring all resources.
        Each resource is acquired using its async context manager and set in the manager.
        Returns self.
        """
        if self._exitstack is not None:
            raise RuntimeError("ResourceManager is already set up")

        self._exitstack = contextlib.AsyncExitStack()
        try:
            for name, (resource, _) in self._resources.items():
                value = await self._exitstack.enter_async_context(resource.acquire(self))
                self.set_resource(name, value)
        except BaseException as exc:
            suppress = await self.__aexit__(type(exc), exc, exc.__traceback__)
            if not suppress:
                raise

        return self

    async def aclose(self) -> None:
        """Asynchronously close the resource manager, releasing all resources."""
        await self.__aexit__()

    async def __aexit__(self, *exc: Any) -> bool | None:
        """Asynchronously exit the resource manager context, releasing all resources.
        Delegates to the AsyncExitStack's __aexit__ method.
        Returns the result of the exit stack's __aexit__.
        """
        res: bool | None = False
        if self._exitstack is not None:
            res = await self._exitstack.__aexit__(*exc)
        self._exitstack = None
        return res
