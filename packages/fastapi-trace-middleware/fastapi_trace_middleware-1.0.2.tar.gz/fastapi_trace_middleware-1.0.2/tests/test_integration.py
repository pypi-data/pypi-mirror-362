import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from fastapi_trace import create_trace_middleware, setup_trace_context, add_trace_header_to_response, trace_id_ctx


class TestIntegrationFeatures:
    """Test integration features for compatibility with existing middleware"""

    def test_respect_existing_context(self):
        """Test that middleware respects existing trace context"""
        app = FastAPI()
        
        # Create middleware that respects existing context
        trace_middleware = create_trace_middleware(respect_existing_context=True)
        app.middleware("http")(trace_middleware)
        
        # Middleware that sets context before trace middleware
        @app.middleware("http")
        async def existing_middleware(request: Request, call_next):
            trace_id_ctx.set("existing-trace-123")
            response = await call_next(request)
            return response
        
        @app.get("/")
        async def root():
            return {"trace_id": trace_id_ctx.get()}
        
        client = TestClient(app)
        response = client.get("/")
        
        # Should use existing trace ID, not generate new one
        assert response.json()["trace_id"] == "existing-trace-123"
        assert response.headers["X-Trace-ID"] == "existing-trace-123"

    def test_hooks_functionality(self):
        """Test that pre and post process hooks work correctly"""
        app = FastAPI()
        
        hook_data = {"pre_called": False, "post_called": False}
        
        async def pre_hook(request: Request):
            hook_data["pre_called"] = True
            request.state.custom_data = "hook_set"
        
        async def post_hook(request: Request):
            hook_data["post_called"] = True
        
        trace_middleware = create_trace_middleware(
            pre_process_hook=pre_hook,
            post_process_hook=post_hook
        )
        app.middleware("http")(trace_middleware)
        
        @app.get("/")
        async def root(request: Request):
            return {"custom_data": getattr(request.state, "custom_data", None)}
        
        client = TestClient(app)
        response = client.get("/")
        
        assert hook_data["pre_called"] is True
        assert hook_data["post_called"] is True
        assert response.json()["custom_data"] == "hook_set"

    def test_utility_functions_integration(self):
        """Test utility functions work correctly in existing middleware"""
        app = FastAPI()
        
        @app.middleware("http")
        async def custom_context_middleware(request: Request, call_next):
            # Use utility function to set up trace context
            trace_id = await setup_trace_context(request, trace_header="X-Custom-Trace")
            
            # Process request
            response = await call_next(request)
            
            # Use utility function to add header
            add_trace_header_to_response(response, trace_id, "X-Custom-Trace")
            return response
        
        @app.get("/")
        async def root():
            return {"trace_id": trace_id_ctx.get()}
        
        client = TestClient(app)
        
        # Test without header (should generate)
        response = client.get("/")
        trace_id = response.json()["trace_id"]
        assert trace_id is not None
        assert response.headers["X-Custom-Trace"] == trace_id
        
        # Test with header (should use provided)
        response = client.get("/", headers={"X-Custom-Trace": "provided-trace-456"})
        assert response.json()["trace_id"] == "provided-trace-456"
        assert response.headers["X-Custom-Trace"] == "provided-trace-456"

    def test_no_override_when_context_exists(self):
        """Test that trace middleware doesn't override existing context"""
        app = FastAPI()
        
        # Setup existing middleware that sets trace context
        @app.middleware("http")
        async def existing_middleware(request: Request, call_next):
            trace_id_ctx.set("middleware-set-123")
            response = await call_next(request)
            return response
        
        # Add trace middleware with respect_existing_context=True
        trace_middleware = create_trace_middleware(respect_existing_context=True)
        app.middleware("http")(trace_middleware)
        
        @app.get("/")
        async def root():
            return {"trace_id": trace_id_ctx.get()}
        
        client = TestClient(app)
        response = client.get("/")
        
        # Should keep the existing context value
        assert response.json()["trace_id"] == "middleware-set-123"

    def test_override_when_context_exists_disabled(self):
        """Test that trace middleware overrides when respect_existing_context=False"""
        app = FastAPI()
        
        # Add trace middleware first (will execute last, so it overrides)
        trace_middleware = create_trace_middleware(respect_existing_context=False)
        app.middleware("http")(trace_middleware)
        
        # Setup existing middleware that sets trace context (executes first)
        @app.middleware("http") 
        async def existing_middleware(request: Request, call_next):
            trace_id_ctx.set("middleware-set-123")
            response = await call_next(request)
            return response
        
        @app.get("/")
        async def root():
            return {"trace_id": trace_id_ctx.get()}
        
        client = TestClient(app)
        response = client.get("/", headers={"X-Trace-ID": "header-trace-456"})
        
        # Should use the header value, overriding existing context
        assert response.json()["trace_id"] == "header-trace-456" 