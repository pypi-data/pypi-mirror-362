"""FastAPI dependency injection using the DI container."""

import secrets
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer
from typing_extensions import Annotated

from ingenious.auth.jwt import get_username_from_token
from ingenious.core.structured_logging import get_logger
from ingenious.db.chat_history_repository import ChatHistoryRepository
from ingenious.files.files_repository import FileStorage
from ingenious.services.chat_service import ChatService
from ingenious.services.container import Container
from ingenious.services.message_feedback_service import MessageFeedbackService

logger = get_logger(__name__)
security = HTTPBasic()
bearer_security = HTTPBearer()


@inject
def get_config(config=Provide[Container.config]):
    """Get config from container."""
    return config


# Legacy profile system removed - all configuration now in the main config object


@inject
def get_openai_service(openai_service=Provide[Container.openai_service]):
    """Get OpenAI service from container."""
    return openai_service


@inject
def get_chat_history_repository(
    chat_history_repository=Provide[Container.chat_history_repository],
) -> ChatHistoryRepository:
    """Get chat history repository from container."""
    return chat_history_repository


@inject
def get_chat_service(
    conversation_flow: str = "",
    config=Provide[Container.config],
    chat_history_repository=Provide[Container.chat_history_repository],
) -> ChatService:
    """Get chat service from container with conversation flow."""
    cs_type = config.chat_service.type
    return ChatService(
        chat_service_type=cs_type,
        chat_history_repository=chat_history_repository,
        conversation_flow=conversation_flow,
        config=config,
    )


@inject
def get_message_feedback_service(
    feedback_service=Provide[Container.message_feedback_service],
) -> MessageFeedbackService:
    """Get message feedback service from container."""
    return feedback_service


@inject
def get_file_storage_data(
    file_storage=Provide[Container.file_storage_data],
) -> FileStorage:
    """Get file storage for data from container."""
    return file_storage


@inject
def get_file_storage_revisions(
    file_storage=Provide[Container.file_storage_revisions],
) -> FileStorage:
    """Get file storage for revisions from container."""
    return file_storage


@inject
def get_project_config(config=Provide[Container.config]):
    """Get project config from container."""
    return config


def get_security_service(
    token: Annotated[str, Depends(bearer_security)] = None,
    credentials: Annotated[HTTPBasicCredentials, Depends(security)] = None,
    config=Depends(get_config),
):
    """Security service with JWT and Basic Auth support."""
    if not config.web_configuration.authentication.enable:
        logger.warning(
            "Authentication is disabled. This is not recommended for production use."
        )
        return "anonymous"

    # Try JWT token first
    if token and token.credentials:
        try:
            username = get_username_from_token(token.credentials)
            return username
        except HTTPException:
            pass

    # Fall back to basic auth
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = config.web_configuration.authentication.username.encode(
        "utf-8"
    )
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = config.web_configuration.authentication.password.encode(
        "utf-8"
    )
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.username


def get_security_service_optional(
    credentials: Optional[HTTPBasicCredentials] = None,
    config=Depends(get_config),
):
    """Optional security service that doesn't require credentials when auth is disabled."""
    if not config.web_configuration.authentication.enable:
        logger.warning(
            "Authentication is disabled. This is not recommended for production use."
        )
        return None

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Basic"},
        )

    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = config.web_configuration.authentication.username.encode(
        "utf-8"
    )
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = config.web_configuration.authentication.password.encode(
        "utf-8"
    )
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def get_auth_user(request: Request, config=Depends(get_config)) -> str:
    """Get authenticated user - supports both JWT and Basic Auth."""
    if not config.web_configuration.authentication.enable:
        logger.warning(
            "Authentication is disabled. This is not recommended for production use."
        )
        return "anonymous"

    auth_header = request.headers.get("Authorization", "")

    # Try JWT Bearer token first
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
        try:
            username = get_username_from_token(token)
            return username
        except HTTPException:
            pass

    # Fall back to Basic Auth
    if auth_header.startswith("Basic "):
        import base64

        try:
            credentials_str = base64.b64decode(auth_header[6:]).decode("utf-8")
            username, password = credentials_str.split(":", 1)
        except (ValueError, UnicodeDecodeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication format",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Validate credentials
        current_username_bytes = username.encode("utf8")
        correct_username_bytes = (
            config.web_configuration.authentication.username.encode("utf-8")
        )
        is_correct_username = secrets.compare_digest(
            current_username_bytes, correct_username_bytes
        )

        current_password_bytes = password.encode("utf8")
        correct_password_bytes = (
            config.web_configuration.authentication.password.encode("utf-8")
        )
        is_correct_password = secrets.compare_digest(
            current_password_bytes, correct_password_bytes
        )

        if not (is_correct_username and is_correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return username

    # No valid authentication method provided
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_conditional_security(request: Request, config=Depends(get_config)) -> str:
    """Get authenticated user - wrapper around get_auth_user for compatibility."""
    return get_auth_user(request, config)


def sync_templates(config=Depends(get_config)):
    """Sync templates from file storage."""
    if config.file_storage.storage_type == "local":
        return
    else:
        import os

        fs = FileStorage(config)
        working_dir = os.getcwd()
        template_path = os.path.join(working_dir, "ingenious", "templates")
        template_files = fs.list_files(file_path=template_path)
        for file in template_files:
            file_name = os.path.basename(file)
            file_contents = fs.read_file(file_name=file_name, file_path=template_path)
            file_path = os.path.join(working_dir, "ingenious", "templates", file_name)
            with open(file_path, "w") as f:
                f.write(file_contents)
