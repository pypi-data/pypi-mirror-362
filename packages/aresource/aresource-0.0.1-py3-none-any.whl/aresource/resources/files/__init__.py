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
except ImportError:
    pass
else:
    __all__.append("HoconResource")
