import asyncio

from async_property import AwaitLoader, async_cached_property
from loguru import logger as log
from pywershell import pywersl
from pywershell.pywershell import CMDResult
from pywershell.pywersl import Distro

class AsyncDocker(AwaitLoader):
    instance = None

    def __init__(self):
        self.base_cmd: str = "docker "
        log.success(f"{self}: Successfully initialized!")

    def __repr__(self):
        return "[Docker]"

    @classmethod
    async def get(cls):
        if cls.instance is None:
            inst = cls()
            cls.instance = inst
        return cls.instance

    INSTALL_DOCKER = [
        "apt-get update",
        "apt-get install -y curl",
        "curl -fsSL https://get.docker.com -o get-docker.sh",
        "sudo sh get-docker.sh",
        "sudo usermod -aG docker mileslib"
    ]

    BOOT_DOCKER = [
        "grep -q WSL2 /proc/version",
        "sudo service docker start",
        "docker info"
    ]

    @async_cached_property
    async def debian(self):
        pyw = await pywersl
        deb: Distro = await pyw.distro
        return deb

    @async_cached_property
    async def version(self):
        deb: Distro = await self.debian
        ver_cmd = self.base_cmd + "--version"
        try:
            output = await deb.run(ver_cmd)
            version = output.str
            if "Docker version" in version:
                log.info(f"{self}: {version}")
                return version
            else:
                raise Exception

        except Exception as e:
            log.warning(f"Docker not ready: {e}. Installing Docker...")
            await deb.run(self.INSTALL_DOCKER)
            await deb.run(self.BOOT_DOCKER)

            output = await deb.run(ver_cmd)
            version = output.str
            if "Docker version" in version:
                log.success(f"{self}: {version}")
                return version
            raise Exception

    async def run(self, cmd: str | list[str], **kwargs) -> CMDResult | None:
        deb: Distro = await self.debian

        prefix = kwargs.pop("prefix", None)
        if prefix:
            prefix = f"{self.base_cmd} {prefix}"
        else:
            prefix = self.base_cmd

        if isinstance(cmd, str): cmd = [cmd]
        cmds = cmd

        out = await deb.run(cmds, prefix=prefix, **kwargs)
        return out

    @async_cached_property
    async def images(self):
        log.debug(f"{self}: Retrieving images...")
        cmd = "images --format {{.Repository}}"
        out = await self.run(cmd)
        out_str = out.str
        imgs = [line.strip() for line in out_str.splitlines() if line.strip()]
        if imgs:
            log.debug(f"{self} Available Images:\n" + "\n".join(f"  - {img}" for img in imgs))
        else:
            log.warning(f"{self} No images found.")
        return imgs

    async def uninstall(self, purge: bool = False):
        log.warning(f"{self}: Uninstalling Docker from WSL...")
        cmds = [
            "sudo service docker stop",
            "sudo apt-get remove -y docker docker-engine docker.io containerd runc docker-ce docker-ce-cli",
        ]
        if purge:
            cmds += [
                "sudo apt-get purge -y docker-ce docker-ce-cli containerd.io",
                "sudo rm -rf /var/lib/docker",
                "sudo rm -rf /var/lib/containerd",
                "sudo rm -rf /etc/docker",
                "sudo rm -rf ~/.docker",
            ]
        out = await self.debian(cmds)
        return out


async def debug():
    cls = await AsyncDocker.get()
    await cls.version


if __name__ == "__main__":
    asyncio.run(debug())
