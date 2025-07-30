# pytest tests/test_middleware.py -v
import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from fastapi_trace import create_trace_middleware, get_trace_id


@pytest.fixture
def app():
    app = FastAPI()
    
    trace_middleware = create_trace_middleware()
    app.middleware("http")(trace_middleware)
    
    @app.get("/test")
    async def test_endpoint():
        return {"trace_id": get_trace_id()}
    
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


def test_trace_id_generation(client):
    """Test that trace ID is generated when not provided"""
    response = client.get("/test")
    assert response.status_code == 200
    
    data = response.json()
    assert "trace_id" in data
    assert data["trace_id"] is not None
    assert len(data["trace_id"]) == 8  # Default nanoid size


def test_trace_id_from_header(client):
    """Test that trace ID is extracted from header"""
    test_trace_id = "test-trace-123"
    response = client.get("/test", headers={"X-Trace-ID": test_trace_id})
    
    assert response.status_code == 200
    data = response.json()
    assert data["trace_id"] == test_trace_id


def test_response_header_included(client):
    """Test that trace ID is included in response header"""
    response = client.get("/test")
    assert "X-Trace-ID" in response.headers
    
    trace_id_from_header = response.headers["X-Trace-ID"]
    trace_id_from_body = response.json()["trace_id"]
    assert trace_id_from_header == trace_id_from_body