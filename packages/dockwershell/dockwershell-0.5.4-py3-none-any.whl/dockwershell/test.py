import asyncio
from pathlib import Path

from dockwershell import Docker, DockerImage
from loguru import logger as log

async def debug():
    inst = await DockerImage(Path(__file__).parent / "Dockerfile.foobar")

asyncio.run(debug())