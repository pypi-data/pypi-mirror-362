"""GDSFactory+ Logger."""

import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, TypeAlias

from loguru import logger

if TYPE_CHECKING:
    import loguru

__all__ = ["Logger", "fix_log_line_numbers", "logger", "setup_logger", "setup_logger"]

Logger: TypeAlias = "loguru.Logger"


def setup_logger() -> "loguru.Logger":
    """Logger setup."""
    from logging.handlers import RotatingFileHandler

    from .project import maybe_find_docode_project_dir

    project_dir = Path(maybe_find_docode_project_dir() or Path.cwd())
    ws_port_path = Path(project_dir) / "build" / "log" / "_server.log"
    ws_port_path.parent.mkdir(parents=True, exist_ok=True)
    ws_port_path.touch(exist_ok=True)
    logger.remove()
    _format = "{time:HH:mm:ss} | {level: <8} | {message}"
    os.makedirs(os.path.dirname(os.path.abspath(ws_port_path)), exist_ok=True)
    logger.add(sys.stdout, level="INFO", colorize=True, format=_format)
    logger.add(
        RotatingFileHandler(ws_port_path, maxBytes=20 * 1024 * 1024, backupCount=14),
        level="DEBUG",
        format=_format,
    )
    return logger


def fix_log_line_numbers(content: str) -> str:
    """Patches a different format for file + line nr combination into logs."""
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if '", line ' in line:
            first, rest = line.split('", line ')
            nbr, rest = rest.split(",")
            lines[i] = f'{first}:{nbr}",{rest}'
    return "\n".join(lines)
