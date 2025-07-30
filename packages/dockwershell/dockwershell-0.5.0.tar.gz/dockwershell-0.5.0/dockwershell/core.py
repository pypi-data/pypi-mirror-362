import asyncio
from functools import cached_property
from types import coroutine
from typing import Coroutine, Any

from async_property import AwaitLoader, async_cached_property
from asyncinit import asyncinit
from loguru import logger as log
from pywershell import pywersl, Debian, CMDResult
from singleton_decorator import singleton

@singleton
@asyncinit
class _Docker:
    async def __init__(self):
        self.debian = await Debian()
        self.debian = await self.debian
        _ = await self.version
        _ = await self.images

    def __repr__(self):
        return "[Docker]"

    PREFIX = "docker"

    VERSION = "--version"

    INSTALL_DOCKER = [
        "'apt-get update'",
        "'apt-get install -y curl'",
        "'curl -fsSL https://get.docker.com -o get-docker.sh'",
        "'sudo sh get-docker.sh'",
        "'sudo usermod -aG docker mileslib'"
    ]

    BOOT_DOCKER = [
        "'grep -q WSL2 /proc/version'",
        "'sudo service docker start'",
        "'docker info'"
    ]

    @async_cached_property
    async def version(self):
        ver_cmd = "--version"
        try:
            resp = await self.run(ver_cmd)
            version = resp.output
            if "Docker version" in version:
                log.info(f"{self}: {version}")
                return version
            else:
                raise Exception

        except Exception as e:
            log.warning(f"Docker not ready: {e}. Installing _Docker...")
            await self.debian.run(self.INSTALL_DOCKER)
            await self.debian.run(self.BOOT_DOCKER)

            resp = await self.debian.run(ver_cmd)
            version = resp.output
            if "_Docker version" in version:
                log.success(f"{self}: {version}")
                return version
            raise Exception

    async def run(self, cmd: str | list[str], **kwargs) -> CMDResult | None:
        if isinstance(cmd, str): cmd = [cmd]
        cmds = cmd

        for i, cmd in enumerate(cmds):
            log.debug(f"{self}: Executing command {i}...")
            cmds[i] = f"'{self.PREFIX} {cmd}'"

        return await self.debian.run(cmds)

    @async_cached_property
    async def images(self) -> list:
        log.debug(f"{self}: Retrieving images...")
        cmd = "images --format {{.Repository}}"
        resp = await self.run(cmd)
        out_str = resp.output
        imgs = [line.strip() for line in out_str.splitlines() if line.strip()]
        if imgs: log.info(f"{self} Available Images:\n" + "\n".join(f"  - {img}" for img in imgs))
        else: log.warning(f"{self} No images found.")
        return imgs

    async def uninstall(self, purge: bool = False):
        log.warning(f"{self}: Uninstalling _Docker from WSL...")
        cmds = [
            "'sudo service docker stop'",
            "'sudo apt-get remove -y docker docker-engine docker.io containerd runc docker-ce docker-ce-cli'",
        ]
        if purge:
            cmds += [
                "'sudo apt-get purge -y docker-ce docker-ce-cli containerd.io'",
                "'sudo rm -rf /var/lib/docker'",
                "'sudo rm -rf /var/lib/containerd'",
                "'sudo rm -rf /etc/docker'",
                "'sudo rm -rf ~/.docker'",
            ]
        out = await self.debian.run(cmds)

Docker: [Any, Any, _Docker] = _Docker()

if __name__ == "__main__":
    asyncio.run(Docker)
