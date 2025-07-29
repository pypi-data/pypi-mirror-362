from pathlib import Path

from async_property import AwaitLoader, async_cached_property
from loguru import logger as log
from pywershell.pywershell import CMDResult

from .core import AsyncDocker
from .path_to_mnt import path_to_wsl


class AsyncDockerImage(AwaitLoader):
    instances = {}

    def __init__(self, dockerfile: Path, build_args=None, rebuild: bool = False, run_args: str = None):
        self.file = dockerfile
        self.args_raw = build_args
        self.rebuild = rebuild
        self.image = self.file.name.replace("Dockerfile.", "")
        self.run_args = run_args

    def __repr__(self):
        return f"[{self.image}.AsyncDockerImage]"

    @classmethod
    async def get(cls, dockerfile: Path, **kwargs):
        name = dockerfile.name.replace("Dockerfile.", "")
        pad = max(len(k) for k in kwargs)
        log.debug(f"[{name.title()}.AsyncDockerImage] Initializing with kwargs:\n" + "\n".join(
            f"  - {k.ljust(pad)} = {v}" for k, v in kwargs.items()))
        if not name in cls.instances:
            obj = cls(
                dockerfile=dockerfile,
                **kwargs
            )
            await obj
            cls.instances[name] = obj
            inst = cls.instances[name]
            log.success(f"{inst}: Image successfully initialized!")
        return cls.instances[name]

    # parse build args once, cached
    @async_cached_property
    async def build_args(self):
        if not self.args_raw:
            return []
        raw = self.args_raw if isinstance(self.args_raw, list) else [self.args_raw]
        out = []
        for s in raw:
            s = s.strip().lstrip("--build-arg").lstrip("--build_arg")
            if "=" not in s:
                raise ValueError("build arg must look like KEY=VAL")
            out.append(f"--build-arg {s}")
        return out

    @async_cached_property
    async def build(self):
        from .manager import adock
        docker: AsyncDocker = await adock

        images = await docker.images
        if self.image in images and not self.rebuild:
            log.debug(f"{self}: Skipping build: '{self.image}' already exists")
            return f"run {self.run_args} {self.image}"

        cmd = f"build -f {path_to_wsl(self.file)} -t {self.image} {path_to_wsl(self.file.parent)}"
        if self.build_args:
            cmd += " " + " ".join(await self.build_args)
        await docker.run(cmd)
        log.success(f"{self}: Successfully built {self.image}")
        return f"run {self.run_args} {self.image}"

    async def run(self, cmd: str = "", headless: bool = True, **kwargs) -> CMDResult | None:
        from .manager import adock
        docker: AsyncDocker = await adock

        args = " ".join(f"-{k} {v}" for k, v in kwargs.items())
        full = f"{await self.build} {args} {cmd}".strip()

        if not headless:
            kwargs["new_windows"] = {full: True}

        log.debug(f"{self}: Sending request:\n   - receiver={docker}\n   - kwargs={kwargs}\n   - cmd={full}")
        return await docker.run(cmd=full, **kwargs)
