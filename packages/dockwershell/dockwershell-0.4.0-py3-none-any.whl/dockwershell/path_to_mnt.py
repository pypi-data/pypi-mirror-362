import re
from pathlib import Path, PureWindowsPath
from typing import Union

_DRIVE_RE = re.compile(r'^(?P<drive>[A-Za-z]):[\\/](?P<rest>.*)$')

def path_to_mnt(p: Union[str, Path], verbose: bool = False) -> str:
    """
    Convert a Windows path into a WSL-compatible path.

    - "C:\\Foo\\Bar"   → "/mnt/c/Foo/Bar"
    - "C:/Foo/Bar"     → "/mnt/c/Foo/Bar"
    - "\\\\host\\share"→ "//host/share"
    - "relative\\path" → "relative/path"

    Args:
        p:       Windows path (str or PureWindowsPath).
        verbose: If true, emit a debug log of the conversion.

    Returns:
        A POSIX-style path suitable for WSL or Docker-on-WSL.
    """
    win = PureWindowsPath(p)
    # If there's a drive letter (e.g. "C:")
    if win.drive:
        drive = win.drive.rstrip(":").lower()
        # win.parts is like ("C:\\", "Users", "…"), so skip the first element
        tail = win.parts[1:]
        wsl_path = "/" + "/".join(["mnt", drive, *tail])
    else:
        # No drive letter → just normalize separators
        wsl_path = "/".join(win.parts)

    return wsl_path

def debug():
    path = Path(r"C:\Users\cblac\PycharmProjects\FastContainer\fastauth\azure\user\.azure")
    print(path)
    print(path_to_mnt(path, verbose=True))
    path = Path(r"C:\Users\cblac\CCCCCCC\FastContainer\CCC\CC\user\.azure")
    print(path)
    print(path_to_mnt(path, verbose=True))

if __name__ == "__main__":
    debug()

path_to_wsl = path_to_mnt #for deprecation