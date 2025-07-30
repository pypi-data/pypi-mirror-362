from __future__ import annotations

import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

import platformdirs
import typed_settings as ts
from attrs import field

if TYPE_CHECKING:
    from logging import Logger as StdLogger
    from typing import Literal

    from loguru._logger import Logger as LoguruLogger


def get_cache_dir() -> Path:
    """
    Get the directory for the PDS4 packager.
    """
    return Path(platformdirs.user_cache_dir("pds4-packager", "ESA"))


def get_tmp_dir() -> Path:
    return Path(tempfile.gettempdir())


@ts.settings
class Config:
    mission: str = ts.option(
        default="JUICE",
        help="Mission name",
        converter=str.lower,
    )
    version: str = ts.option(
        default="SNAPSHOT",
        help="Version number of the PDS4 stack to use",
        converter=str,
    )
    workspace_location: Path = ts.option(factory=get_cache_dir)
    temp_path: Path = ts.option(factory=get_tmp_dir)
    log_engine: str = ts.option(
        default="loguru",
        help="Logging engine to use, either loguru or logging",
        converter=str.lower,
    )

    _logger: Any = field(init=False, repr=False)

    @property
    def logger(self) -> LoguruLogger | StdLogger:
        """
        Get the logger type.
        """
        if not hasattr(self, "_logger"):
            self._logger = self._make_logger()

        return self._logger

    def _make_logger(self) -> LoguruLogger | StdLogger:
        if self.log_engine == "loguru":
            from loguru import logger as log

            return log
        if self.log_engine == "logging":
            import logging

            return logging.getLogger(__name__)
        raise ValueError(f"Unknown logger type: {self.logger}")


default_settings = ts.load(
    cls=Config,
    appname="esa_pds4_packager",
)
