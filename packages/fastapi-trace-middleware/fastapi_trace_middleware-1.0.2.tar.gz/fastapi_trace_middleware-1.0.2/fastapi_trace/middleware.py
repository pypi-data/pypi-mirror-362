from fastapi import Request
from nanoid import generate
from typing import Callable, Optional, Awaitable
from .context import trace_id_ctx


class TraceMiddleware:
    def __init__(
        self, 
        trace_header: str = "X-Trace-ID",
        trace_id_generator: callable = lambda: generate(size=8),
        include_response_header: bool = True,
        respect_existing_context: bool = False,
        pre_process_hook: Optional[Callable[[Request], Awaitable[None]]] = None,
        post_process_hook: Optional[Callable[[Request], Awaitable[None]]] = None
    ):
        self.trace_header = trace_header
        self.trace_id_generator = trace_id_generator
        self.include_response_header = include_response_header
        self.respect_existing_context = respect_existing_context
        self.pre_process_hook = pre_process_hook
        self.post_process_hook = post_process_hook

    async def __call__(self, request: Request, call_next):
        """Middleware to set trace ID context for each request"""
        
        # Check if trace_id already exists in context
        existing_trace_id = None
        if self.respect_existing_context:
            existing_trace_id = trace_id_ctx.get()
        
        # Get trace_id from header or generate new one (only if not already set)
        if existing_trace_id:
            trace_id = existing_trace_id
        else:
            trace_id = request.headers.get(self.trace_header)
            if not trace_id:
                trace_id = self.trace_id_generator()
            
            # Set trace_id in context
            trace_id_ctx.set(trace_id)

        # Execute pre-process hook for custom context setup
        if self.pre_process_hook:
            await self.pre_process_hook(request)

        # Process request
        response = await call_next(request)
        
        # Execute post-process hook for custom response handling
        if self.post_process_hook:
            await self.post_process_hook(request)
        
        # Add trace_id to response header if enabled
        if self.include_response_header:
            response.headers[self.trace_header] = trace_id
            
        return response


# Factory function for easy setup
def create_trace_middleware(
    trace_header: str = "X-Trace-ID",
    trace_id_generator: callable = lambda: generate(size=8),
    include_response_header: bool = True,
    respect_existing_context: bool = False,
    pre_process_hook: Optional[Callable[[Request], Awaitable[None]]] = None,
    post_process_hook: Optional[Callable[[Request], Awaitable[None]]] = None
) -> TraceMiddleware:
    """Factory function to create trace middleware"""
    return TraceMiddleware(
        trace_header=trace_header,
        trace_id_generator=trace_id_generator,
        include_response_header=include_response_header,
        respect_existing_context=respect_existing_context,
        pre_process_hook=pre_process_hook,
        post_process_hook=post_process_hook
    )


# Utility functions for integration with existing middleware
async def setup_trace_context(
    request: Request,
    trace_header: str = "X-Trace-ID",
    trace_id_generator: callable = lambda: generate(size=8)
) -> str:
    """Utility function to set up trace context - can be used in existing middleware"""
    trace_id = request.headers.get(trace_header)
    if not trace_id:
        trace_id = trace_id_generator()
    
    trace_id_ctx.set(trace_id)
    return trace_id


def add_trace_header_to_response(response, trace_id: str, trace_header: str = "X-Trace-ID"):
    """Utility function to add trace header to response"""
    response.headers[trace_header] = trace_id
    return response