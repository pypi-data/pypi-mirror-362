import logging
import logging.handlers
import os
import sys

import colorlog  # type: ignore

from .structured_logging import setup_structured_logging


def setup_logging(app_module_name: str | None) -> None:
    root_log_level = os.environ.get("ROOTLOGLEVEL", "WARNING")
    log_level = os.environ.get("LOGLEVEL", "WARNING")

    # Check if structured logging is enabled via environment variable
    use_structured_logging = (
        os.environ.get("STRUCTURED_LOGGING", "true").lower() == "true"
    )
    json_output = os.environ.get("JSON_LOGGING", "true").lower() == "true"

    if use_structured_logging:
        # Use new structured logging
        setup_structured_logging(
            log_level=log_level, json_output=json_output, include_stdlib=True
        )
    else:
        # Legacy logging setup
        _setup_legacy_logging(app_module_name, root_log_level, log_level)


def _setup_legacy_logging(
    app_module_name: str | None, root_log_level: str, log_level: str
) -> None:
    """Legacy logging setup for backward compatibility."""
    # Create a stream handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(asctime)s - %(log_color)s[%(levelname)s]%(reset)s - %(name)s - %(message)s"
        )
    )

    # Handlers
    handlers = [stream_handler]

    # Root logger
    if root_log_level:
        root_logger = logging.getLogger()
        root_logger.setLevel(root_log_level)
        root_logger.handlers = handlers  # type: ignore

    # App logger
    logger = logging.getLogger(app_module_name)
    logger.setLevel(log_level)
    logger.handlers = handlers  # type: ignore

    # Get uvicorn access logger
    access_logger = logging.getLogger("uvicorn.access")
    access_logger.setLevel(log_level)
    access_logger.handlers = handlers  # type: ignore

    # Get uvicorn error logger
    error_logger = logging.getLogger("uvicorn.error")
    error_logger.setLevel(log_level)
    error_logger.handlers = handlers  # type: ignore
