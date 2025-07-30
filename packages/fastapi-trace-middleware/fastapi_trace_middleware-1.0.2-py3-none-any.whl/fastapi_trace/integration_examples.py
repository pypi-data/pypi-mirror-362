"""
Integration examples for fastapi-trace-middleware

This file contains examples showing how to integrate the trace middleware 
with existing middleware without conflicts.
"""

from fastapi import Request
from jwt import decode
from .middleware import create_trace_middleware, setup_trace_context, add_trace_header_to_response
from .context import trace_id_ctx


# Example 1: Using hooks to extend trace middleware with Azure user context
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
        respect_existing_context=True  # Don't override if already set
    )


# Example 2: Integration with existing context middleware using utility functions
async def enhanced_context_middleware(request: Request, call_next):
    """Enhanced version of existing context middleware using trace utilities"""
    
    # Set up trace context using utility function
    trace_id = await setup_trace_context(request)
    
    # Your existing Azure user ID logic
    if auth_header := request.headers.get("Authorization"):
        try:
            token = auth_header.split(" ")[1]
            payload = decode(token, options={"verify_signature": False})
            # extract_and_set_azure_user_id(payload["preferred_username"])
        except (IndexError, KeyError):
            pass

    # Process request
    response = await call_next(request)
    
    # Add trace header using utility function
    add_trace_header_to_response(response, trace_id)
    
    return response


# Example 3: Composable middleware approach
class ComposableTraceMiddleware:
    """Middleware that can be composed with other context middleware"""
    
    def __init__(self, existing_middleware_func=None):
        self.existing_middleware = existing_middleware_func
        self.trace_middleware = create_trace_middleware(respect_existing_context=True)
    
    async def __call__(self, request: Request, call_next):
        """Execute existing middleware first, then trace middleware"""
        
        if self.existing_middleware:
            # Wrap the call_next to intercept and add trace handling
            async def wrapped_call_next(req):
                return await self.trace_middleware(req, call_next)
            
            return await self.existing_middleware(request, wrapped_call_next)
        else:
            return await self.trace_middleware(request, call_next)


# Example 4: Factory for backward compatibility
def create_compatible_middleware(existing_context_middleware=None):
    """
    Factory function that creates middleware compatible with existing context middleware
    
    Args:
        existing_context_middleware: Your existing context middleware function
        
    Returns:
        A middleware that combines trace functionality with your existing middleware
    """
    if existing_context_middleware:
        return ComposableTraceMiddleware(existing_context_middleware)
    else:
        return create_trace_middleware()


# Example 5: Direct replacement for existing context middleware
async def unified_context_middleware(request: Request, call_next):
    """
    Direct replacement for your existing context_middleware that includes
    both trace and Azure user context functionality
    """
    
    # Set up trace context
    trace_id = await setup_trace_context(request, trace_header="X-Trace-ID")
    
    # Set Azure user ID context (your existing logic)
    if auth_header := request.headers.get("Authorization"):
        try:
            token = auth_header.split(" ")[1]
            payload = decode(token, options={"verify_signature": False})
            # extract_and_set_azure_user_id(payload["preferred_username"])
        except (IndexError, KeyError):
            pass

    # Process request
    response = await call_next(request)
    
    # Add trace ID header
    response.headers["X-Trace-ID"] = trace_id
    
    return response 