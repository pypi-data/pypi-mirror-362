"""
Chat service related dependency injection.

This module provides FastAPI dependency injection functions
for chat services and related repositories.
"""

from dependency_injector.wiring import Provide, inject

from ingenious.db.chat_history_repository import ChatHistoryRepository
from ingenious.services.chat_service import ChatService
from ingenious.services.container import Container
from ingenious.services.message_feedback_service import MessageFeedbackService


@inject
def get_chat_history_repository(
    chat_history_repository=Provide[Container.chat_history_repository],
) -> ChatHistoryRepository:
    """Get chat history repository from container."""
    return chat_history_repository  # type: ignore


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
    return feedback_service  # type: ignore
