from fastapi import Request
from nanoid import generate
from .context import trace_id_ctx


class TraceMiddleware:
    def __init__(
        self, 
        trace_header: str = "X-Trace-ID",
        trace_id_generator: callable = lambda: generate(size=8),
        include_response_header: bool = True
    ):
        self.trace_header = trace_header
        self.trace_id_generator = trace_id_generator
        self.include_response_header = include_response_header

    async def __call__(self, request: Request, call_next):
        """Middleware to set trace ID context for each request"""
        
        # Get trace_id from header or generate new one
        trace_id = request.headers.get(self.trace_header)
        if not trace_id:
            trace_id = self.trace_id_generator()
        
        # Set trace_id in context
        trace_id_ctx.set(trace_id)

        # Process request
        response = await call_next(request)
        
        # Add trace_id to response header if enabled
        if self.include_response_header:
            response.headers[self.trace_header] = trace_id
            
        return response


# Factory function for easy setup
def create_trace_middleware(
    trace_header: str = "X-Trace-ID",
    trace_id_generator: callable = lambda: generate(size=8),
    include_response_header: bool = True
) -> TraceMiddleware:
    """Factory function to create trace middleware"""
    return TraceMiddleware(
        trace_header=trace_header,
        trace_id_generator=trace_id_generator,
        include_response_header=include_response_header
    )