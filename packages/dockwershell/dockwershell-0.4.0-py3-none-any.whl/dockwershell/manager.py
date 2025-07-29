import asyncio
from functools import cached_property
from pathlib import Path, PureWindowsPath

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