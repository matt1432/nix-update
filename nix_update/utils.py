import os
import shlex
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import IO, Any

HAS_TTY = sys.stdout.isatty()
ROOT = Path(os.path.dirname(os.path.realpath(__file__)))

def color_text(code: int, file: IO[Any] = sys.stdout) -> Callable[[str], None]:
    def wrapper(text: str, quiet: bool = False) -> None:
        if quiet:
            return
        if HAS_TTY:
            print(f"\x1b[{code}m{text}\x1b[0m", file=file)
        else:
            print(text, file=file)

    return wrapper


info = color_text(32)


def run(
    command: list[str],
    cwd: Path | str | None = None,
    stdout: None | int | IO[Any] = subprocess.PIPE,
    stderr: None | int | IO[Any] = None,
    check: bool = True,
    extra_env: dict[str, str] | None = None,
    quiet: bool = False,
) -> "subprocess.CompletedProcess[str]":
    if extra_env is None:
        extra_env = {}
    info("$ " + shlex.join(command), quiet)
    env = os.environ.copy()
    env.update(extra_env)
    return subprocess.run(
        command, cwd=cwd, check=check, text=True, stdout=stdout, stderr=stderr, env=env
    )
