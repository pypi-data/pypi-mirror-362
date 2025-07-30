import contextvars

# Define a context variable for trace_id
trace_id_ctx = contextvars.ContextVar("trace_id", default=None)

def get_trace_id() -> str | None:
    """Get the current trace ID from context"""
    return trace_id_ctx.get()

def set_trace_id(trace_id: str) -> None:
    """Set the trace ID in context"""
    trace_id_ctx.set(trace_id)