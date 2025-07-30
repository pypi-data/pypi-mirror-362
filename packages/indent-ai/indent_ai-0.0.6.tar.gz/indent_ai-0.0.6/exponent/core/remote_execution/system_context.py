import getpass
import os
import platform

from anyio import Path as AsyncPath

from exponent.core.remote_execution.git import get_git_info
from exponent.core.remote_execution.languages import python_execution
from exponent.core.remote_execution.types import (
    SystemContextRequest,
    SystemContextResponse,
    SystemInfo,
)
from exponent.core.remote_execution.utils import safe_read_file

EXPONENT_TXT_FILENAMES = [
    "exponent.txt",
]


async def get_system_context(
    request: SystemContextRequest, working_directory: str
) -> SystemContextResponse:
    return SystemContextResponse(
        correlation_id=request.correlation_id,
        exponent_txt=await _read_exponent_txt(working_directory),
        system_info=await get_system_info(working_directory),
    )


async def get_system_info(working_directory: str) -> SystemInfo:
    return SystemInfo(
        name=getpass.getuser(),
        cwd=working_directory,
        os=platform.system(),
        shell=_get_user_shell(),
        git=await get_git_info(working_directory),
        python_env=python_execution.get_python_env_info(),
    )


async def _read_exponent_txt(working_directory: str) -> str | None:
    for filename in EXPONENT_TXT_FILENAMES:
        file_path = AsyncPath(os.path.join(working_directory, filename.lower()))
        exists = await file_path.exists()

        if exists:
            return await safe_read_file(file_path)

    return None


def _get_user_shell() -> str:
    return os.environ.get("SHELL", "bash")
