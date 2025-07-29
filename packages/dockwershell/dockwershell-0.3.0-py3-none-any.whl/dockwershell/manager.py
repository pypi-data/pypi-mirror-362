import asyncio
from functools import cached_property
from pathlib import Path

from async_property import async_cached_property
import re
from typing import Union


class DockerManager:
    images = {}
    from .image import AsyncDockerImage

    def __repr__(self):
        return "[Docker]"

    def __getattr__(self, name: str) -> AsyncDockerImage:
        try:
            return self.images[name]
        except KeyError:
            raise AttributeError(f"{self}: Image yet to be initialized!")

    def __getitem__(self, key: str) -> AsyncDockerImage:
        return self.images[key]

    @cached_property
    def docker(self):
        from .core import AsyncDocker
        return asyncio.run(AsyncDocker.get())

    @async_cached_property
    async def adock(self):
        from .core import AsyncDocker
        return await AsyncDocker.get()

    async def new(self, dockerfile: Path, alias: str = None, build_args: str = None, rebuild: bool = False,
                  run_args: str = None):
        from .image import AsyncDockerImage
        inst: AsyncDockerImage = await AsyncDockerImage.get(
            dockerfile=dockerfile,
            build_args=build_args,
            rebuild=rebuild,
            run_args=run_args
        )
        name = inst.image
        if alias: name = alias
        setattr(self, inst.image, name)
        self.images[inst.image] = inst
        return inst


Docker = DockerManager()
adock = Docker.adock


# compile once for speed
_DRIVE_RE = re.compile(r'^(?P<drive>[A-Za-z]):[\\/](?P<rest>.*)$')

def path_to_wsl(p: Union[Path, str], verbose: bool = False) -> str:
    """
    Convert a Windows path into WSL style.

    - C:\\Foo\\Bar → /mnt/c/Foo/Bar
    - C:/Foo/Bar  → /mnt/c/Foo/Bar
    - \\host\share\Dir → //host/share/Dir
    - relative\\path → relative/path

    Args:
        p: Windows path (Path or str).
        verbose: If true, emit a debug log of the conversion.

    Returns:
        A POSIX‐style path suitable for WSL.
    """
    s = str(p)
    m = _DRIVE_RE.match(s)
    if m:
        # drive‐letter path
        drive = m.group("drive").lower()
        rest = m.group("rest").replace("\\", "/")
        # strip any leading slash so we don’t get //mnt/c///
        rest = rest.lstrip("/")
        wsl = f"/mnt/{drive}/{rest}"
    elif s.startswith(("\\\\", "//")):
        # UNC share: \\host\share\dir → //host/share/dir
        unc = s.strip("\\/").replace("\\", "/")
        wsl = f"//{unc}"
    else:
        # no drive letter: just normalize slashes
        wsl = s.replace("\\", "/")

    if verbose:
        log.debug(f"path_to_wsl: {s!r} → {wsl!r}")
    return wsl