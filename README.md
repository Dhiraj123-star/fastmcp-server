
# Remote MCP Python Server

This project implements a **Model Context Protocol (MCP)** server using the **FastMCP** framework. It is designed as a high-performance, remote-capable capability layer for LLMs, optimized for containerized orchestration via Docker and Kubernetes.

## 🚀 Features

* **Remote Transport:** Uses **Streamable HTTP (SSE)** via FastMCP v2.0+ for networked LLM interactions.
* **Stateless & Scalable:** Configured with `stateless_http=True` and `json_response=True` for Horizontal Pod Autoscaling (HPA).
* **Orchestration Ready:** Includes manifests for **Minikube** and **Kubernetes** deployment.
* **Production Hardened:** Follows enterprise patterns for resource isolation and tool discovery.

## 🛠️ Tools & Resources

### Tools

* **`greet`**: Returns a structured greeting string.

### Resources

* **`resource://system/status`**: Metadata regarding server version and environment.

---

## 📦 Deployment Options

### 1. Local (Docker Compose)

Best for rapid development.

```bash
docker-compose up --build -d

```

*Endpoint: `http://localhost:8081/mcp*`

### 2. Kubernetes (Minikube)

Best for simulating production scaling and resilience.

```bash
# Set shell to minikube docker
eval $(minikube docker-env)

# Build & Deploy
docker build -t fastmcp-remote-python:v1 .
kubectl apply -f mcp-k8s.yaml

# Get Access URL
minikube service python-mcp-service --url

```

---

## 📡 Usage & Verification

### Manual API Verification (curl)

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

### Automated Testing (Python)

Use the included test client for a quick health check:

```bash
python3 test_client.py

```

---

## 🏗️ Project Structure

* `remote_server.py`: FastMCP entry point with stateless HTTP enabled.
* `test_client.py`: Python script for JSON-RPC tool verification.
* `mcp-k8s.yaml`: Kubernetes Deployment (3 replicas) and Service manifests.
* `Dockerfile` & `docker-compose.yml`: Containerization and local orchestration.

---
