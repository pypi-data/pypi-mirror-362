# Python MCP Cat Facts

A FastAPI server that implements the Model Context Protocol (MCP) using Server-Sent Events (SSE) transport to provide cat facts.

## Features

- Get a single random cat fact
- Subscribe to a stream of cat facts delivered every 10 seconds
- SSE (Server-Sent Events) for real-time communication
- FastAPI framework with automatic OpenAPI documentation

## Requirements

- Python 3.12+
- Dependencies:
  - fastapi
  - mcp[cli]
  - uvicorn
  - cmake

## Installation

### Clone the repository

```bash
git clone <repository-url>
cd python-mcp
```

### Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### Install dependencies

```bash
pip install -e .
```

## Starting the Server in SSE Mode

Start the server using the uv run command:

```bash
uv run start
```

Once the server is running, it will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## VS Code Integration

To use this MCP server with VS Code, you need to add the following configuration to your `mcp.json` file:

```json
{
    "servers": {
        "mcp-sse": {
            "type": "sse",
            "url": "http://0.0.0.0:8000/sse"
        }
    }
}
```

This configuration tells VS Code how to connect to your MCP server using SSE transport.

## Using the Cat Facts API

### Get a single cat fact:

Connect to the SSE endpoint and request a single cat fact. The response will always start with "Hi!".


## API Endpoints

- `GET /`: Homepage
- `GET /about`: Information about the application
- `GET /status`: Current server status
- `GET /sse`: SSE endpoint for MCP communication
- `GET /docs`: API documentation (Swagger UI)
- `GET /redoc`: Alternative API documentation (ReDoc)

## License

[MIT](LICENSE)