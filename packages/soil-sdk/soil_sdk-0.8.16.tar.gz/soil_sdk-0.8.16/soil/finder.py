"""Module generates"""

import asyncio
import os.path
from hashlib import sha256
from itertools import islice
from pathlib import Path
from typing import Generator

from soil.aio import api
from soil.types import GetModuleHash

FOLDER_BLACKLIST = [".vscode", ".venv", "test", ".git"]


BLOCK_SIZE = 1048576
MODULES_CHUNK = 25


def _hex_digest(data: bytes):
    file_hash = sha256()
    cursor = 0
    while cursor < len(data):
        file_hash.update(data[cursor : cursor + BLOCK_SIZE])
        cursor += BLOCK_SIZE
    return file_hash.hexdigest()


def _get_included_files() -> Generator[Path, None, None]:
    folders = [
        path
        for path in Path(".").glob("*")
        if path.is_dir() and path.name not in FOLDER_BLACKLIST
    ]
    for folder in folders:
        for selected_file in folder.rglob("*.py"):
            yield selected_file


def _filter_files(
    included_files: Generator[Path, None, None], file_hashes: list[GetModuleHash]
) -> Generator[tuple[str, str, bool], None, None]:
    file_hashes_dict = {module["name"]: module["hash"] for module in file_hashes}
    for file in included_files:
        code = file.read_text()
        code_hash = _hex_digest(bytes(code, encoding="utf-8"))
        module_name = str(file)[:-3].replace("/", ".")  # all are python files
        if file.stem == "__init__":
            module_name = module_name[: -len(".__init__")]
        if file_hashes_dict.get(module_name) != code_hash:
            yield (module_name, code, file.stem == "__init__")


async def _upload_selected_modules(
    modules: Generator[tuple[str, str, bool], None, None],
) -> None:
    mods = list(islice(modules, MODULES_CHUNK))
    tasks = []
    while len(mods) > 0:
        umods = []
        for module in mods:
            name, code, is_package = module
            umods.append({"name": name, "code": code, "is_package": is_package})
        tasks.append(api.upload_modules(modules=umods))
        mods = list(islice(modules, MODULES_CHUNK))
    await asyncio.gather(*tasks)


async def _upload_modules() -> None:
    modules = await api.get_modules()
    files_to_check = _get_included_files()
    modules_to_upload = _filter_files(files_to_check, modules)
    await _upload_selected_modules(modules_to_upload)
    await api.clean_client()


def upload_modules() -> None:
    """Upload modules to soil when not in a test environment."""
    if os.environ.get("PY_ENV", "development") in ("test", "docker"):
        return
    loop = None
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        asyncio.run(_upload_modules())
    if loop is not None:
        loop.create_task(_upload_modules())  # noqa: RUF006
