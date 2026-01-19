
# Remote MCP Python Server

This project implements a **Model Context Protocol (MCP)** server using the **FastMCP** framework. It is designed to be a high-performance, remote-capable capability layer that allows Large Language Models (LLMs) to interact with enterprise-grade Python tools and resources via a secure, standardized interface.

## 🚀 Features

* **Remote Transport:** Uses **Streamable HTTP (SSE)** to allow connections over a network, making it suitable for cloud and Kubernetes deployments.
* **Stateless Execution:** Configured with `stateless_http=True` to support Horizontal Pod Autoscaling (HPA) and load balancing.
* **FastMCP Architecture:** Optimized for low latency and high-frequency agent actions.
* **Dockerized:** Fully containerized using a `python-slim` base image for portability and reproducible deployments.
* **Enterprise Ready:** Built-in support for standardized tool discovery and resource sharing.

## 🛠️ Tools & Resources

### Tools

* **`greet`**: A core demonstration tool that takes a `name` string and returns a structured greeting.

### Resources

* **`resource://system/status`**: A read-only resource providing metadata about the server's version, status, and environment.

---

## 📦 Getting Started

### Prerequisites

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Installation & Deployment

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd fastmcp-server

```


2. **Build and Start with Docker Compose:**
```bash
docker-compose up --build -d

```


3. **Verify the Server:**
The server will be available at `http://localhost:8081/mcp`.

---

## 📡 Usage & Integration

### Connecting via MCP Clients

To use this server with an MCP-compatible host (like Claude Desktop or Cursor), add the following to your configuration:

```json
{
  "mcpServers": {
    "remote-python-server": {
      "url": "http://localhost:8081/mcp",
      "transport": "http"
    }
  }
}

```

### Manual API Verification

Since the server uses `stateless_http` and `json_response` mode, you can verify it directly via `curl`.

**Command:**

```bash
curl -X POST http://localhost:8081/mcp \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -d '{
       "jsonrpc": "2.0",
       "id": "1",
       "method": "tools/call",
       "params": {
         "name": "greet",
         "arguments": {"name": "Dhiraj"}
       }
     }'

```

---

## 🏗️ Project Structure

* `remote_server.py`: The main entry point using FastMCP.
* `Dockerfile`: Multi-stage build for the Python environment.
* `docker-compose.yml`: Local orchestration and port mapping.
* `requirements.txt`: Project dependencies (FastMCP).

---

