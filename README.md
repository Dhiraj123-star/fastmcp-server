# Remote MCP Python Server

This project implements a **Model Context Protocol (MCP)** server using the **FastMCP** framework. It is designed as a high-performance, remote-capable capability layer for LLMs, optimized for containerized orchestration via Docker and Kubernetes.

## 🚀 Features

* **Remote Transport:** Uses **Streamable HTTP (SSE)** via FastMCP v2.0+ for networked LLM interactions.
* **Stateless & Scalable:** Configured with `stateless_http=True` and `json_response=True` for Horizontal Pod Autoscaling (HPA).
* **Self-Healing:** Includes **Liveness and Readiness probes** to ensure Kubernetes automatically restarts unhealthy pods.
* **Secure Communication:** HTTPS enabled via **Self-Signed SSL Certificates** and NGINX Ingress TLS termination.
* **CI/CD Ready:** Integrated with **GitHub Actions** for automated builds and push to **Docker Hub**.
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

### 2. Kubernetes (Minikube with Docker Hub)

Best for simulating production scaling and encrypted domain-based routing using remote images.

**Step 1: Generate Self-Signed Certificates**

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout mcp-selfsigned.key \
  -out mcp-selfsigned.crt \
  -subj "/CN=mcp.local/O=MCP-Dev"

```

**Step 2: Create Secrets & Enable Ingress**

```bash
minikube addons enable ingress
kubectl create secret tls mcp-tls-secret --key mcp-selfsigned.key --cert mcp-selfsigned.crt

```

**Step 3: Deploy to Kubernetes**
The manifest is configured to pull the latest image from `dhiraj918106/fastmcp-remote-python`.

```bash
kubectl apply -f mcp-k8s.yaml

```

**Step 4: Map Local Domain**
Add your Minikube IP to `/etc/hosts`:

```text
<MINIKUBE_IP>  mcp.local

```

*Secure Endpoint: `https://mcp.local/mcp*`

---

## ⚙️ CI/CD Workflow

The project uses GitHub Actions (`.github/workflows/deploy.yml`) to automate the build process.

1. **Push to `main**`: Triggers the workflow.
2. **Build & Push**: Image is built and pushed to `dhiraj918106/fastmcp-remote-python:latest`.
3. **Manual Cluster Update**: To pull the fresh image into your local Minikube:
```bash
kubectl rollout restart deployment python-mcp

```



---

## 📡 Usage & Verification

### Automated Testing (Python Client)

The `test_client.py` handles SSL verification bypass for self-signed certificates and validates infrastructure health.

**Test Local Docker:**

```bash
python3 test_client.py

```

**Test K8s Ingress:**

```bash
python3 test_client.py ingress

```

### Manual API Verification (curl)

```bash
# Verify Health
curl -k https://mcp.local/health

# Verify Tool
curl -k -X POST https://mcp.local/mcp \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","id":"1","method":"tools/call","params":{"name":"greet","arguments":{"name":"Dhiraj"}}}'

```

---

## 🏗️ Project Structure

* `.github/workflows/`: CI/CD pipeline definitions.
* `remote_server.py`: FastMCP entry point with custom health routes.
* `test_client.py`: Python script for environment validation.
* `mcp-k8s.yaml`: Deployment (pulling from Docker Hub), Service, and TLS Ingress.
* `.gitignore`: Configured to exclude `.key`, `.crt`, and `__pycache__`.

---
