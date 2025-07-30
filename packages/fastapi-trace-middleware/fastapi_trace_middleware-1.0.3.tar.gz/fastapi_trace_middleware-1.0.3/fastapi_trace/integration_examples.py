"""
Integration examples for fastapi-trace-middleware

This file contains examples showing how to integrate the trace middleware 
with existing middleware without conflicts.
"""

from fastapi import Request
from jwt import decode
from .middleware import create_trace_middleware
from .context import trace_id_ctx


# Example: Using hooks to extend trace middleware with Azure user context
async def azure_user_context_hook(request: Request) -> None:
    """Hook function to set Azure user ID context"""
    if auth_header := request.headers.get("Authorization"):
        try:
            token = auth_header.split(" ")[1]
            payload = decode(token, options={"verify_signature": False})
            # Assuming you have a way to set azure user context
            # azure_user_ctx.set(payload["preferred_username"])
        except (IndexError, KeyError):
            pass


def create_extended_trace_middleware():
    """Create trace middleware with Azure user context support"""
    return create_trace_middleware(
        pre_process_hook=azure_user_context_hook,
    )
