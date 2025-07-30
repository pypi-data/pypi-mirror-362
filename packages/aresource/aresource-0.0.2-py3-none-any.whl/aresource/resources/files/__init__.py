from .base import BasePathResource
from .bytes import BytesResource
from .ini import IniResource
from .json import JsonResource
from .path import PathResource

__all__ = [
    "BasePathResource",
    "BytesResource",
    "HoconResource",
    "IniResource",
    "JsonResource",
    "PathResource",
]

try:
    from .hocon import HoconResource

    __all__.append("HoconResource")
except ImportError:
    pass


try:
    from .yaml import YamlResource  # noqa: F401

    __all__.append("YamlResource")
except ImportError:
    pass
