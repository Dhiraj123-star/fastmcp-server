# Remote MCP Python Server

This project implements a **Model Context Protocol (MCP)** server using the **FastMCP** framework. It is designed as a high-performance, remote-capable capability layer for LLMs, optimized for containerized orchestration via Docker and Kubernetes.

## 🚀 Features

* **Remote Transport:** Uses **Streamable HTTP (SSE)** via FastMCP v2.0+ for networked LLM interactions.
* **Stateless & Scalable:** Configured with `stateless_http=True` and `json_response=True` for Horizontal Pod Autoscaling (HPA).
* **Self-Healing:** Includes **Liveness and Readiness probes** to ensure Kubernetes automatically restarts unhealthy pods.
* **Secure Communication:** HTTPS enabled via **Self-Signed SSL Certificates** and NGINX Ingress TLS termination.
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

### 2. Kubernetes (Minikube with SSL/TLS)

Best for simulating production scaling and encrypted domain-based routing.

**Step 1: Generate Self-Signed Certificates**

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout mcp-selfsigned.key \
  -out mcp-selfsigned.crt \
  -subj "/CN=mcp.local/O=MCP-Dev"

```

**Step 2: Create Kubernetes Secret & Enable Ingress**

```bash
minikube addons enable ingress
kubectl create secret tls mcp-tls-secret --key mcp-selfsigned.key --cert mcp-selfsigned.crt

```

**Step 3: Build & Deploy**

```bash
eval $(minikube docker-env)
docker build -t fastmcp-remote-python:v1 .
kubectl apply -f mcp-k8s.yaml

```

**Step 4: Map Local Domain**
Add your Minikube IP to `/etc/hosts`:

```text
<MINIKUBE_IP>  mcp.local

```

*Secure Endpoint: `https://mcp.local/mcp*`

---

## 📡 Usage & Verification

### Automated Testing (Python Client)

The `test_client.py` handles SSL verification bypass for self-signed certificates.

**Test Local Docker (HTTP):**

```bash
python3 test_client.py

```

**Test K8s Ingress (HTTPS):**

```bash
python3 test_client.py ingress

```

### Manual API Verification (curl)

Use the `-k` flag to allow self-signed certificates:

Verify the health endpoint:

```bash
curl -k https://mcp.local/health

```

Verify a tool call:

```bash
curl -k -X POST https://mcp.local/mcp \
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
* `test_client.py`: Python script with `urllib.parse` and SSL bypass for validation.
* `mcp-k8s.yaml`: K8s manifests including **Deployment** (Probes + Resources), **Service**, and **Ingress (TLS)**.
* `mcp-selfsigned.crt/key`: SSL certificates (Keep these secure and out of version control).

---