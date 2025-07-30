import asyncio
from typing import Any

from .core import _Docker

def _launch() -> _Docker:
    return asyncio.run(_Docker())

Docker = _launch()

from .path_to_mnt import path_to_mnt
path_to_wsl = path_to_mnt
from .image import DockerImage