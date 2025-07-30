import logging
from .context import trace_id_ctx


class TraceIdFilter(logging.Filter):
    """Filter that injects trace_id from context into log records"""
    
    def filter(self, record):
        record.trace_id = trace_id_ctx.get() or "-"
        return True