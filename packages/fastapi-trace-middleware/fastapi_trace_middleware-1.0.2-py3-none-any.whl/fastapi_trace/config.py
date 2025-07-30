import logging
from typing import Dict, Any
from .logging_filters import TraceIdFilter


def setup_trace_logging(
    formatters: Dict[str, Dict[str, Any]] | None = None,
    handlers: Dict[str, Dict[str, Any]] | None = None,
    loggers: Dict[str, Dict[str, Any]] | None = None
) -> Dict[str, Any]:
    """
    Setup logging configuration with trace ID support
    
    Args:
        formatters: Custom formatters dict
        handlers: Custom handlers dict  
        loggers: Custom loggers dict
        
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
    
    # Default handlers with trace filter
    default_handlers = {
        "console": {
            "formatter": "uvicorn_detailed",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": ["trace_id_filter"],
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
    
    # Merge with custom configs
    final_formatters = {**default_formatters, **(formatters or {})}
    final_handlers = {**default_handlers, **(handlers or {})}
    final_loggers = {**default_loggers, **(loggers or {})}
    
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "trace_id_filter": {
                "()": "fastapi_trace.logging_filters.TraceIdFilter",
            },
        },
        "formatters": final_formatters,
        "handlers": final_handlers,
        "loggers": final_loggers,
    }


def setup_simple_trace_logging() -> Dict[str, Any]:
    """Quick setup for basic trace logging"""
    return setup_trace_logging()