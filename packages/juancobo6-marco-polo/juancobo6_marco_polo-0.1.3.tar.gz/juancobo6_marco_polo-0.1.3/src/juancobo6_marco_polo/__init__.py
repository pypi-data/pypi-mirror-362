"""Marco Polo game init."""

from .marco_polo import marco_polo

try:
    from importlib.metadata import version

    __version__ = version("juancobo6-marco-polo")
except Exception:
    __version__ = "unknown"

__all__ = ["marco_polo", "__version__"]
