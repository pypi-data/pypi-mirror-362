import logging
from typing import Dict, Any, List
from .logging_filters import TraceIdFilter


def setup_trace_logging(
    formatters: Dict[str, Dict[str, Any]] | None = None,
    handlers: Dict[str, Dict[str, Any]] | None = None,
    loggers: Dict[str, Dict[str, Any]] | None = None,
    custom_filters: Dict[str, Dict[str, Any]] | None = None,
    default_handler_filters: List[str] | None = None,
) -> Dict[str, Any]:
    """
    Setup logging configuration with trace ID support and custom filters

    Args:
        formatters: Custom formatters dict
        handlers: Custom handlers dict
        loggers: Custom loggers dict
        custom_filters: Additional filters to include beyond trace_id_filter
                       Format: {"filter_name": {"()": "module.path.FilterClass", "param": "value"}}
        default_handler_filters: List of filter names to apply to default handlers
                               If None, defaults to ["trace_id_filter"]

    Returns:
        Complete logging configuration dict
    """

    # Default formatters with trace_id support
    default_formatters = {
        "console": {
            "format": "%(asctime)s | %(levelname)-6s | TraceID:%(trace_id)s | %(filename)s-%(funcName)s-%(lineno)04d | %(message)s"
        },
        "uvicorn_detailed": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": "%(levelprefix)s [TraceID:%(trace_id)s] [%(asctime)s] [%(filename)s-%(funcName)s-%(lineno)04d] %(message)s",
            "datefmt": "%d-%m-%Y %H:%M:%S",
            "use_colors": True,
        },
        "uvicorn_simple": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": "%(levelprefix)s [TraceID:%(trace_id)s] [%(asctime)s] %(message)s",
            "datefmt": "%d-%m-%Y %H:%M:%S",
            "use_colors": True,
        },
    }

    # Determine which filters to apply to default handlers
    if default_handler_filters is None:
        default_handler_filters = ["trace_id_filter"]

    # Default handlers with configurable filters
    default_handlers = {
        "console": {
            "formatter": "uvicorn_detailed",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": default_handler_filters.copy(),
        },
    }

    # Default loggers
    default_loggers = {
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    }

    # Build filters configuration
    filters_config = {
        "trace_id_filter": {
            "()": "fastapi_trace.logging_filters.TraceIdFilter",
        },
    }

    # Add any custom filters
    if custom_filters:
        filters_config.update(custom_filters)

    # Merge with custom configs
    final_formatters = {**default_formatters, **(formatters or {})}
    final_handlers = {**default_handlers, **(handlers or {})}
    final_loggers = {**default_loggers, **(loggers or {})}

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": filters_config,
        "formatters": final_formatters,
        "handlers": final_handlers,
        "loggers": final_loggers,
    }


def setup_simple_trace_logging() -> Dict[str, Any]:
    """Quick setup for basic trace logging"""
    return setup_trace_logging()
