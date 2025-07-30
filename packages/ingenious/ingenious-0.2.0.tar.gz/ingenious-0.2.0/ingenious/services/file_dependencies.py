"""
File storage related dependency injection.

This module provides FastAPI dependency injection functions
for file storage services and template synchronization.
"""

import os
from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from ingenious.files.files_repository import FileStorage
from ingenious.services.container import Container


@inject
def get_config(config=Provide[Container.config]) -> Any:
    """Get config from container."""
    return config


@inject
def get_file_storage_data(
    file_storage=Provide[Container.file_storage_data],
) -> FileStorage:
    """Get file storage for data from container."""
    return file_storage  # type: ignore


@inject
def get_file_storage_revisions(
    file_storage=Provide[Container.file_storage_revisions],
) -> FileStorage:
    """Get file storage for revisions from container."""
    return file_storage  # type: ignore


def sync_templates(config=Depends(get_config)) -> None:
    """Sync templates from file storage."""
    if config.file_storage.storage_type == "local":
        return
    else:
        fs = FileStorage(config)
        working_dir = os.getcwd()
        template_path = os.path.join(working_dir, "ingenious", "templates")
        import asyncio

        async def sync_files():
            template_files = await fs.list_files(file_path=template_path)
            for file in template_files:
                file_name = os.path.basename(file)
                file_contents = await fs.read_file(
                    file_name=file_name, file_path=template_path
                )
                file_path = os.path.join(
                    working_dir, "ingenious", "templates", file_name
                )
                with open(file_path, "w") as f:
                    f.write(file_contents)

        asyncio.run(sync_files())
