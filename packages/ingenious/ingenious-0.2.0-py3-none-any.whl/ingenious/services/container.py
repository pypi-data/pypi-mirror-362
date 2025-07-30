"""Dependency injection container for Ingenious services."""

from dependency_injector import containers, providers
from dotenv import load_dotenv

from ingenious.config.config import get_config as _get_config

# Legacy profile import removed - now using new config system
from ingenious.core.structured_logging import get_logger
from ingenious.db.chat_history_repository import (
    ChatHistoryRepository,
    DatabaseClientType,
)
from ingenious.errors import ConfigurationError
from ingenious.external_services.openai_service import OpenAIService
from ingenious.files.files_repository import FileStorage
from ingenious.services.chat_service import ChatService
from ingenious.services.message_feedback_service import MessageFeedbackService


def _get_database_type(config) -> DatabaseClientType:
    """Get database type from config with proper error handling."""
    db_type_val = config.chat_history.database_type.lower()
    try:
        return DatabaseClientType(db_type_val)
    except ValueError as e:
        raise ConfigurationError(
            f"Unknown database type: {db_type_val}",
            context={
                "database_type": db_type_val,
                "available_types": [t.value for t in DatabaseClientType],
            },
            cause=e,
            recovery_suggestion="Check the database_type configuration in config.yml",
        ) from e


def _create_chat_service(
    config,
    chat_history_repository: ChatHistoryRepository,
    conversation_flow: str = "",
) -> ChatService:
    """Factory function to create ChatService with proper dependencies."""
    cs_type = config.chat_service.type
    return ChatService(
        chat_service_type=cs_type,
        chat_history_repository=chat_history_repository,
        conversation_flow=conversation_flow,
        config=config,
    )


def _create_security_service(config):
    """Factory function for security service configuration."""
    return {
        "config": config,
        "authentication_enabled": config.web_configuration.authentication.enable,
        "username": config.web_configuration.authentication.username,
        "password": config.web_configuration.authentication.password,
    }


class Container(containers.DeclarativeContainer):
    """Dependency injection container for Ingenious application."""

    # Ensure environment variables are loaded
    wiring_config = containers.WiringConfiguration(
        modules=[
            "ingenious.api.routes.chat",
            "ingenious.api.routes.message_feedback",
            "ingenious.api.routes.auth",
            "ingenious.api.routes.prompts",
            "ingenious.api.routes.diagnostic",
            "ingenious.services.dependencies",
            "ingenious.services.auth_dependencies",
            "ingenious.services.chat_dependencies",
            "ingenious.services.file_dependencies",
            "ingenious.main",
        ]
    )

    # Core configuration
    config = providers.Singleton(lambda: _get_config())

    # Legacy profile system removed - all configuration now handled by the new config system

    logger = providers.Singleton(get_logger, __name__)

    # External services
    openai_service = providers.Factory(
        OpenAIService,
        azure_endpoint=providers.Callable(
            lambda cfg: str(cfg.models[0].base_url), config
        ),
        api_key=providers.Callable(lambda cfg: str(cfg.models[0].api_key), config),
        api_version=providers.Callable(
            lambda cfg: str(cfg.models[0].api_version), config
        ),
        open_ai_model=providers.Callable(lambda cfg: str(cfg.models[0].model), config),
    )

    # Database repository
    chat_history_repository = providers.Factory(
        ChatHistoryRepository,
        db_type=providers.Callable(lambda cfg: _get_database_type(cfg), config),
        config=config,
    )

    # File storage services
    file_storage_data = providers.Factory(
        FileStorage,
        config=config,
        Category="data",
    )

    file_storage_revisions = providers.Factory(
        FileStorage,
        config=config,
        Category="revisions",
    )

    # Business services - using Factory for per-request chat services
    chat_service_factory = providers.Factory(
        _create_chat_service,
        config=config,
        chat_history_repository=chat_history_repository,
    )

    message_feedback_service = providers.Factory(
        MessageFeedbackService,
        chat_history_repository=chat_history_repository,
    )

    # Authentication and security
    security_service = providers.Factory(
        _create_security_service,
        config=config,
    )


def _get_database_type(config) -> DatabaseClientType:
    """Get database type from config with proper error handling."""
    db_type_val = config.chat_history.database_type.lower()
    try:
        return DatabaseClientType(db_type_val)
    except ValueError as e:
        raise ConfigurationError(
            f"Unknown database type: {db_type_val}",
            context={
                "database_type": db_type_val,
                "available_types": [t.value for t in DatabaseClientType],
            },
            cause=e,
            recovery_suggestion="Check the database_type configuration in config.yml",
        ) from e


def _create_chat_service(
    config,
    chat_history_repository: ChatHistoryRepository,
    conversation_flow: str = "",
) -> ChatService:
    """Factory function to create ChatService with proper dependencies."""
    cs_type = config.chat_service.type
    return ChatService(
        chat_service_type=cs_type,
        chat_history_repository=chat_history_repository,
        conversation_flow=conversation_flow,
        config=config,
    )


# Global container instance
_container: Container | None = None


def get_container() -> Container:
    """Get the global container instance, creating it if needed."""
    global _container
    if _container is None:
        _container = Container()
    return _container


def init_container() -> Container:
    """Initialize the container and return it."""
    global _container

    # Load environment variables
    load_dotenv()

    # Create container if it doesn't exist
    if _container is None:
        _container = Container()

    # Wire the container
    _container.wire(
        modules=[
            "ingenious.api.routes.chat",
            "ingenious.api.routes.message_feedback",
            "ingenious.api.routes.auth",
            "ingenious.api.routes.prompts",
            "ingenious.api.routes.diagnostic",
            "ingenious.services.dependencies",
            "ingenious.services.auth_dependencies",
            "ingenious.services.chat_dependencies",
            "ingenious.services.file_dependencies",
            "ingenious.main",
        ]
    )

    return _container


def configure_for_testing():
    """Configure container for testing environment."""
    # Override with test configurations
    from unittest.mock import Mock

    # Mock external services for testing
    container = get_container()
    mock_openai_service = Mock()
    container.openai_service.override(mock_openai_service)

    # Use in-memory SQLite for testing
    test_config = container.config()
    test_config.chat_history.database_type = "sqlite"
    container.config.override(test_config)

    return container


def configure_for_development():
    """Configure container for development environment."""
    # Development-specific configurations
    return get_container()


def configure_for_production():
    """Configure container for production environment."""
    # Production-specific configurations
    return get_container()


def override_for_testing(**overrides):
    """Override container providers for testing."""
    container = get_container()
    for provider_name, override_value in overrides.items():
        if hasattr(container, provider_name):
            provider = getattr(container, provider_name)
            provider.override(override_value)


def reset_overrides():
    """Reset all container overrides."""
    container = get_container()
    container.reset_override()
