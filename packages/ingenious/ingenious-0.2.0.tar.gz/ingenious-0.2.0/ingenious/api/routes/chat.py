from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from typing_extensions import Annotated

import ingenious.utils.namespace_utils as ns_utils
from ingenious.core.structured_logging import get_logger
from ingenious.errors.content_filter_error import ContentFilterError
from ingenious.errors.token_limit_exceeded_error import TokenLimitExceededError
from ingenious.models.chat import ChatRequest, ChatResponse
from ingenious.models.http_error import HTTPError
from ingenious.services.chat_service import ChatService
from ingenious.services.dependencies import get_chat_service, get_conditional_security

logger = get_logger(__name__)
router = APIRouter()

import os
import sys

parent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../../../..")
)
sys.path.append(parent_dir)


@router.post(
    "/chat",
    responses={
        400: {"model": HTTPError, "description": "Bad Request"},
        406: {"model": HTTPError, "description": "Not Acceptable"},
        413: {"model": HTTPError, "description": "Payload Too Large"},
    },
)
async def chat(
    chat_request: ChatRequest,
    chat_service: Annotated[ChatService, Depends(get_chat_service)],
    credentials: Annotated[HTTPBasicCredentials, Depends(get_conditional_security)],
) -> ChatResponse:
    try:
        ns_utils.print_namespace_modules(
            "ingenious.services.chat_services.multi_agent.conversation_flows"
        )
        if not chat_request.conversation_flow:
            raise ValueError(f"conversation_flow not set {chat_request}")
        return await chat_service.get_chat_response(chat_request)
    except ValueError as e:
        logger.error(
            "Chat request validation error",
            conversation_flow=chat_request.conversation_flow,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(status_code=400, detail=str(e))
    except ContentFilterError as cfe:
        logger.error(
            "Content filter error",
            conversation_flow=chat_request.conversation_flow,
            error=str(cfe),
            exc_info=True,
        )
        raise HTTPException(status_code=406, detail=ContentFilterError.DEFAULT_MESSAGE)
    except TokenLimitExceededError as tle:
        logger.error(
            "Token limit exceeded",
            conversation_flow=chat_request.conversation_flow,
            error=str(tle),
            exc_info=True,
        )
        raise HTTPException(
            status_code=413, detail=TokenLimitExceededError.DEFAULT_MESSAGE
        )
    except Exception as e:
        logger.error(
            "Chat request failed",
            conversation_flow=chat_request.conversation_flow if chat_request else None,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=str(e))
