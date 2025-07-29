<!-- README.md -->
# DockwerShell

Asynchronous Docker management for Debian-based WSL2 using the [pywershell] engine under the hood.

```python
import asyncio
from dockwershell.core import AsyncDocker

async def main():
    # get singleton instance
    docker = await AsyncDocker.get()

    # print version (auto-installs if needed)
    version = await docker.version
    print("Docker version:", version)

    # list images
    images = await docker.images
    print("Available images:", images)

    # run an ad‐hoc command
    await docker.run("ps -a")
```

```python
from pathlib import Path
from dockwershell.manager import DockerManager

async def build_and_run():
    mgr = DockerManager()
    img = await mgr.new(
        dockerfile=Path("Dockerfile.app"),
        build_args="ENV=prod",
        rebuild=False,
        run_args="-d -p 8000:8000"
    )
    result = await img.run()
    print(result.str)

asyncio.run(build_and_run())
```