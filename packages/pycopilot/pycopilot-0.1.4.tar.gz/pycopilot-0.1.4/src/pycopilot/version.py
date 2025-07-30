import subprocess
import shlex
from importlib import metadata
import os


DIR = os.path.dirname(os.path.realpath(__file__))

VERSION = metadata.version("pycopilot")


def cmd(cmd, kind="") -> str:
    """
    Get git subprocess output
    """
    output = "unknown"
    try:
        output = (
            subprocess.check_output(shlex.split(cmd), cwd=DIR, stderr=subprocess.STDOUT)
            .decode()
            .strip()
        )
    except Exception as _:
        ...
    return f"{kind}{output}"


def last_commit_id() -> str:
    return cmd("git describe --always --dirty")


def branch() -> str:
    return cmd("git rev-parse --abbrev-ref HEAD")


def get_git_version() -> str:
    v = f"-{last_commit_id()}-{branch()}"
    return v if v != "-unknown-unknown" else ""


__version__ = f"{VERSION}{get_git_version()}"
