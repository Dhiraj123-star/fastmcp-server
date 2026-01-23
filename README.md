# Remote MCP Python Server

This project implements a **Model Context Protocol (MCP)** server using the **FastMCP** framework. It is designed as a high-performance, remote-capable capability layer for LLMs, optimized for containerized orchestration via Docker and Kubernetes.

## 🚀 Features

* **Remote Transport:** Uses **Streamable HTTP (SSE)** via FastMCP v2.0+ for networked LLM interactions.
* **Stateless & Scalable:** Configured with `stateless_http=True` and `json_response=True` for Horizontal Pod Autoscaling (HPA).
* **Self-Healing:** Includes **Liveness and Readiness probes** to ensure Kubernetes automatically restarts unhealthy pods.
* **Custom Routing:** Implements a dedicated `/health` endpoint using `@mcp.custom_route` for infrastructure monitoring.
* **Ingress Integration:** Support for custom domain routing (`mcp.local`) via NGINX Ingress Controller.

## 🛠️ Tools & Resources

### Tools

* **`greet`**: A tool that returns a structured greeting string based on a provided name.

### Resources

* **`resource://status`**: A system resource providing a simple health status.

---

## 📦 Deployment Options

### 1. Local (Docker Compose)

Best for rapid development and testing.

```bash
docker-compose up --build -d

```

*Endpoint: `http://localhost:8081/mcp*`

### 2. Kubernetes (Minikube with Ingress)

Best for simulating production scaling and domain-based routing.

**Step 1: Enable Ingress and Build Image**

```bash
minikube addons enable ingress
eval $(minikube docker-env)
docker build -t fastmcp-remote-python:v1 .

```

**Step 2: Apply Manifests**

```bash
kubectl apply -f mcp-k8s.yaml

```

**Step 3: Map Local Domain**
Get your Minikube IP using `minikube ip`, then add it to `/etc/hosts`:

```text
<MINIKUBE_IP>  mcp.local

```

*Endpoint: `http://mcp.local/mcp*`

---

## 📡 Usage & Verification

### Automated Testing (Python Client)

The `test_client.py` uses robust URL parsing to verify both the infrastructure health and the MCP tool logic.

**Test Local Docker:**

```bash
python3 test_client.py

```

**Test K8s Ingress:**

```bash
python3 test_client.py ingress

```

### Manual API Verification (curl)

Verify the health endpoint directly:

```bash
curl http://mcp.local/health

```

Verify a tool call:

```bash
curl -X POST http://mcp.local/mcp \
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

* `remote_server.py`: FastMCP entry point with custom health routes and stateless settings.
* `test_client.py`: Python script for dual-mode (Local/Ingress) validation.
* `mcp-k8s.yaml`: K8s manifests including **Deployment** (3 replicas + Probes), **Service**, and **Ingress**.
* `Dockerfile` & `docker-compose.yml`: Containerization and local orchestration.

---
