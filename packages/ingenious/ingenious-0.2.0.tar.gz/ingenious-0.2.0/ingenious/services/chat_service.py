from abc import ABC, abstractmethod

from ingenious.core.error_handling import operation_context
from ingenious.core.structured_logging import get_logger
from ingenious.db.chat_history_repository import ChatHistoryRepository
from ingenious.errors import (
    ChatServiceError,
)
from ingenious.models.chat import ChatRequest, ChatResponse
from ingenious.models.config import Config
from ingenious.utils.imports import import_class_with_fallback

logger = get_logger(__name__)


class IChatService(ABC):
    service_class = None

    @abstractmethod
    async def get_chat_response(self, chat_request: ChatRequest) -> ChatResponse:
        pass


class ChatService(IChatService):
    def __init__(
        self,
        chat_service_type: str,
        chat_history_repository: ChatHistoryRepository,
        conversation_flow: str,
        config: Config,
        revision: str = "dfe19b62-07f1-4cb5-ae9a-561a253e4b04",
    ):
        class_name = f"{chat_service_type.lower()}_chat_service"
        self.config = config
        self.revision = revision

        with operation_context(
            "chat_service_initialization",
            "services.chat",
            error_class=ChatServiceError,
            service_type=chat_service_type,
            conversation_flow=conversation_flow,
        ) as ctx:
            try:
                module_name = (
                    f"services.chat_services.{chat_service_type.lower()}.service"
                )
                service_class = import_class_with_fallback(
                    module_name, class_name, expected_methods=["get_chat_response"]
                )

                ctx.add_metadata(
                    module_name=module_name, class_name=class_name, successful=True
                )

                logger.info(
                    "Chat service class loaded successfully",
                    service_type=chat_service_type,
                    module_name=module_name,
                    class_name=class_name,
                )

            except ImportError as e:
                raise ChatServiceError(
                    "Failed to import chat service module",
                    context={
                        "service_type": chat_service_type,
                        "module_name": module_name,
                        "attempted_modules": [
                            module_name,
                            f"ingenious.services.chat_services.{chat_service_type.lower()}.service",
                        ],
                    },
                    cause=e,
                    recoverable=False,
                    recovery_suggestion="Check if the chat service module exists and is properly installed",
                ) from e

            except AttributeError as e:
                raise ChatServiceError(
                    "Chat service class not found in module",
                    context={
                        "service_type": chat_service_type,
                        "module_name": module_name,
                        "expected_class": class_name,
                    },
                    cause=e,
                    recoverable=False,
                    recovery_suggestion="Ensure the class name matches the service type",
                ) from e

            except Exception as e:
                raise ChatServiceError(
                    "Unexpected error during chat service initialization",
                    context={
                        "service_type": chat_service_type,
                        "module_name": module_name,
                        "class_name": class_name,
                    },
                    cause=e,
                    recovery_suggestion="Check chat service configuration and dependencies",
                ) from e

        self.service_class = service_class(
            config=config,
            chat_history_repository=chat_history_repository,
            conversation_flow=conversation_flow,
        )

    async def get_chat_response(self, chat_request: ChatRequest) -> ChatResponse:
        if not chat_request.conversation_flow:
            raise ValueError(f"conversation_flow not set {chat_request}")
        return await self.service_class.get_chat_response(chat_request)  # type: ignore
