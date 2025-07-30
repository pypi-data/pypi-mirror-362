import asyncio
from pathlib import Path

from asyncinit import asyncinit
from async_property import AwaitLoader, async_cached_property
from loguru import logger as log
from pywershell import CMDResult

from dockwershell import Docker, path_to_wsl

# from .path_to_mnt import path_to_wsl

@asyncinit
class DockerImage(AwaitLoader):
    instances = {}

    async def __init__(self, dockerfile: Path, rebuild: bool = False, run_args: str = None, **kwargs):
        self.docker = await Docker
        self.file = dockerfile
        self.rebuild = rebuild
        self.run_args = run_args
        self.name = dockerfile.name.replace("Dockerfile.", "")
        self.image = self.name

        if kwargs:
            pad = max(len(k) for k in kwargs)
            log.debug(f"{self}: Initializing with kwargs:\n" + "\n".join(
                f"  - {k.ljust(pad)} = {v}" for k, v in kwargs.items()))

        _ = await self.build

    def __repr__(self):
        return f"[{self.image}.AsyncDockerImage]"

    # # parse build args once, cached
    # @async_cached_property
    # async def build_args(self):
    #     if not self.args_raw:
    #         return []
    #     raw = self.args_raw if isinstance(self.args_raw, list) else [self.args_raw]
    #     out = []
    #     for s in raw:
    #         s = s.strip().lstrip("--build-arg").lstrip("--build_arg")
    #         if "=" not in s:
    #             raise ValueError("build arg must look like KEY=VAL")
    #         out.append(f"--build-arg {s}")
    #     return out

    @async_cached_property
    async def build(self):
        images = await self.docker.images
        if self.image in images and not self.rebuild:
            log.debug(f"{self}: Skipping build: '{self.image}' already exists")
            return f"run {self.run_args} {self.image}"

        cmd = f"build -f {path_to_wsl(self.file)} -t {self.image} {path_to_wsl(self.file.parent)}"
        # if self.build_args:
        #     cmd += " " + " ".join(await self.build_args)
        await self.docker.run(cmd)
        log.success(f"{self}: Successfully built {self.image}")
        return f"run {self.run_args} {self.image}"

    async def run(self, cmd: str = "", headless: bool = True, **kwargs) -> CMDResult | None:
        args = " ".join(f"-{k} {v}" for k, v in kwargs.items())
        full = f"{await self.build} {args} {cmd}".strip()
        log.debug(f"{self}: Sending request:\n   - receiver={self.docker}\n   - kwargs={kwargs}\n   - cmd={full}")
        return await self.docker.run(cmd=full, **kwargs)

async def debug():
    await DockerImage(Path(r'C:\Users\cblac\PycharmProjects\Dockwershell\dockwershell\Dockerfile.foobar'))

if __name__ == "__main__":
    asyncio.run(debug())