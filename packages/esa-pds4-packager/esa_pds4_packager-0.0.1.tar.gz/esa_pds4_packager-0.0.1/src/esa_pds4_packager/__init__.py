import sys

from loguru import logger as log

import importlib.metadata as metadata

from .packager import PDS4Packager

from .java import is_java_available


if not is_java_available():
    print(
        "Java is not available. Please ensure Java is installed and accessible in your PATH."
    )

__all__ = ["PDS4Packager"]

__version__ = metadata.version("esa_pds4_packager")

log.disable("esa_pds4_packager")


def log_enable(
    level: str = "INFO", mod: str = "esa_pds4_packager", remove_handlers: bool = True
) -> None:
    """Enable logging for a given module at specific level, by default it operates on the whole module."""
    if remove_handlers:
        log.remove()
    log.enable(mod)
    log.add(sys.stderr, level=level)


def log_enable_debug() -> None:
    """Enable debug logging for a given module, by default it operates on the whole module."""
    log_enable(level="DEBUG")


def log_disable(mod: str = "esa_pds4_packager") -> None:
    """Totally disable logging from this module, by default it operates on the whole module."""
    log.disable(mod)
