# FastAPI Trace Middleware

A simple and effective middleware for FastAPI applications that automatically adds trace IDs to requests and integrates with Python logging.

## Features

- 🔍 Automatic trace ID generation for each request
- 📝 Seamless integration with Python logging
- 🎛️ Configurable trace ID headers and generators
- 🔄 Context-aware trace ID access throughout your application
- 📦 Easy setup with sensible defaults

## Installation

```bash
pip install fastapi-trace-middleware
```

## Quick Start

```python
from fastapi import FastAPI
from fastapi_trace import create_trace_middleware, setup_simple_trace_logging
import logging.config

# Setup logging with trace support
logging.config.dictConfig(setup_simple_trace_logging())

app = FastAPI()

# Add trace middleware
trace_middleware = create_trace_middleware()
app.middleware("http")(trace_middleware)

@app.get("/")
async def root():
    from fastapi_trace import get_trace_id
    logging.info("Processing request")  # Will include trace_id automatically
    return {"message": "Hello World", "trace_id": get_trace_id()}
```

## Documentation

### Basic Usage

The middleware automatically:
1. Extracts trace ID from request headers (default: `X-Trace-ID`)
2. Generates a new trace ID if none exists
3. Sets the trace ID in context for the entire request lifecycle
4. Adds trace ID to response headers
5. Makes trace ID available in logs

### Configuration

```python
from fastapi_trace import create_trace_middleware

# Custom configuration
trace_middleware = create_trace_middleware(
    trace_header="X-Custom-Trace-ID",  # Custom header name
    include_response_header=True,       # Include in response
    trace_id_generator=lambda: "custom-" + generate(size=10)  # Custom generator
)
```

### Accessing Trace ID

```python
from fastapi_trace import get_trace_id

async def my_function():
    trace_id = get_trace_id()
    print(f"Current trace ID: {trace_id}")
```

### Integration with Existing Middleware

If you already have context middleware (e.g., for user authentication), you can integrate trace functionality without conflicts:

```python
from fastapi_trace import create_trace_middleware

async def custom_context_hook(request):
    # Your existing context setup logic (e.g., Azure user ID)
    if auth_header := request.headers.get("Authorization"):
        # Extract and set user context
        pass

# Create middleware with hooks
trace_middleware = create_trace_middleware(
    pre_process_hook=custom_context_hook,
)
app.middleware("http")(trace_middleware())
```


### Custom Logging Setup

```python
from fastapi_trace import setup_trace_logging

# Custom formatters and handlers
config = setup_trace_logging(
    formatters={
        "custom": {
            "format": "%(asctime)s [%(trace_id)s] %(levelname)s: %(message)s"
        }
    }
)

import logging.config
logging.config.dictConfig(config)
```

## Requirements

- Python 3.8+
- FastAPI 0.68.0+
- nanoid 2.0.0+

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.