import asyncio
from pathlib import Path

from asyncinit import asyncinit

from dockwershell import Docker, DockerImage
from loguru import logger as log

async def debug():
    inst = await DockerImage(Path(__file__).parent / "Dockerfile.foobar")

asyncio.run(debug())

@asyncinit
class Dummy1:
    async def __init__(self):
        self.docker = await Docker()

@asyncinit
class Dummy2:
    async def __init__(self):
        self.docker = await Docker()

async def debug2():
    docker1 = await Dummy1()
    docker2 = await Dummy2()

asyncio.run(debug2())