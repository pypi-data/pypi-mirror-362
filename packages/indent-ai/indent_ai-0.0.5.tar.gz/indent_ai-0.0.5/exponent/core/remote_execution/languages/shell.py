import asyncio
import os
import platform
import shutil
from collections.abc import Callable
from dataclasses import dataclass

STDOUT_FD = 1
STDERR_FD = 2
MAX_TIMEOUT = 300


"""
Deprecated, use shell_streaming.py
"""


@dataclass
class ShellExecutionResult:
    output: str
    cancelled_for_timeout: bool
    exit_code: int | None
    halted: bool = False


def get_rc_file_source_command(shell_path: str) -> str:
    """
    Returns a command to source the user's shell rc file
    Login profiles are already sourced via the -l flag
    """
    # On Windows, shell behavior is different
    if platform.system() == "Windows":
        return ""  # Windows shells don't typically use rc files in the same way

    shell_name = os.path.basename(shell_path)
    home_dir = os.path.expanduser("~")

    if shell_name == "zsh":
        zshrc = os.path.join(home_dir, ".zshrc")
        if os.path.exists(zshrc):
            return f"source {zshrc} 2>/dev/null || true; "
    elif shell_name == "bash":
        bashrc = os.path.join(home_dir, ".bashrc")
        if os.path.exists(bashrc):
            return f"source {bashrc} 2>/dev/null || true; "

    return ""  # No rc file found or unsupported shell


def is_native_windows() -> bool:
    return os.name == "nt" and "WSL_DISTRO_NAME" not in os.environ


async def execute_shell(
    code: str,
    working_directory: str,
    timeout: int,
    should_halt: Callable[[], bool] | None = None,
) -> ShellExecutionResult:
    timeout = min(timeout, MAX_TIMEOUT)

    shell_path = os.environ.get("SHELL") or shutil.which("bash") or shutil.which("sh")

    if not shell_path:
        process = await asyncio.create_subprocess_shell(
            code,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=working_directory,
        )
    else:
        # Add rc file sourcing to the command
        rc_source_cmd = get_rc_file_source_command(shell_path)
        full_command = f"{rc_source_cmd}{code}"

        process = await asyncio.create_subprocess_exec(
            shell_path,
            "-l",
            "-c",
            full_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=working_directory,
        )

    exit_code = None
    output: list[tuple[int, str]] = []
    halted = False
    assert process.stdout
    assert process.stderr

    stdout_capture_task = asyncio.create_task(
        capture(process.stdout, STDOUT_FD, output)
    )
    stderr_capture_task = asyncio.create_task(
        capture(process.stderr, STDERR_FD, output)
    )

    async def capture_until_exit() -> int:
        nonlocal halted
        while True:
            if should_halt and should_halt():
                process.kill()
                halted = True
                break

            if process.returncode is not None:
                break

            await asyncio.sleep(0.1)

        return await process.wait()

    try:
        exit_code = await asyncio.wait_for(capture_until_exit(), timeout)
    except TimeoutError:
        process.kill()
    except Exception:
        raise
    finally:
        # Wait for capture tasks to complete naturally after streams are closed
        await asyncio.gather(
            stdout_capture_task, stderr_capture_task, return_exceptions=True
        )

    formatted_output = "".join([chunk for (_, chunk) in output]).strip() + "\n\n"

    return ShellExecutionResult(
        output=formatted_output,
        cancelled_for_timeout=exit_code is None and not halted,
        exit_code=exit_code,
        halted=halted,
    )


async def capture(
    stream: asyncio.StreamReader, fd: int, output: list[tuple[int, str]]
) -> None:
    while True:
        data = await stream.read(4096)
        if not data:
            break

        chunk = data.decode(errors="replace")
        output.append((fd, chunk))
