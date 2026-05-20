# Inventory API — Platform Engineering Portfolio Project

A production-style inventory management API built to demonstrate end-to-end platform engineering skills including containerization, Kubernetes orchestration, CI/CD automation, and AI-assisted cluster operations.

---

## What It Does

The Inventory API simulates a real-world retail inventory system — the kind that powers stock lookups on sites like Nordstrom.com. A user submits a request through a web interface, the request travels through an ingress controller to a Kubernetes service, hits the deployed API, and returns inventory data in a clean, consumable format. The long-term goal is to connect this to an AWS-hosted database replacing the current in-memory store, completing a full cloud-native request pipeline.

---

## Architecture
User Request
    ↓
Traefik Ingress (K3s)
    ↓
Kubernetes Service
    ↓
Flask API (Deployment — 2 replicas)
    ↓
In-memory inventory store → (planned: AWS RDS)
    ↓
JSON Response

**AI Cluster Assistant** — A natural language interface powered by Ollama (Mistral model) that allows engineers to query cluster health without needing to know kubectl commands. Ask "Are any of my pods unhealthy?" and get a plain-English answer with live cluster data.

**Monitoring** — Prometheus scrapes application metrics exposed via prometheus-flask-exporter. Grafana provides a visualization layer for cluster and application health.

**CI/CD** — Every push to main triggers a GitHub Actions pipeline on a self-hosted runner that builds the Docker image, pushes it to GitHub Container Registry (GHCR), and deploys to the K3s cluster automatically.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | Python, Flask |
| Containerization | Docker (multi-stage build) |
| Orchestration | Kubernetes (K3s) |
| Ingress | Traefik |
| CI/CD | GitHub Actions, self-hosted runner |
| Container Registry | GitHub Container Registry (GHCR) |
| Monitoring | Prometheus, Grafana (Helm) |
| AI Assistant | Ollama, Mistral |
| Infrastructure | Dell PowerEdge T630, Ubuntu |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/inventory` | Return all inventory items |
| GET | `/inventory/<id>` | Return a single item by ID |
| POST | `/cluster/ask` | Query cluster health in plain English |

### Example — Inventory
```bash
curl http://localhost/inventory
```

```json
[
  {"id": 1, "sku": "NK-001", "brand": "Nike", "category": "athletic", "quantity": 42},
  {"id": 2, "sku": "AD-002", "brand": "Adidas", "category": "athletic", "quantity": 18}
]
```

### Example — AI Cluster Assistant
```bash
curl -X POST http://localhost/cluster/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Are any of my pods unhealthy?"}'
```

```json
{
  "answer": "All pods are currently healthy with status Running.",
  "cluster_data": [...],
  "question": "Are any of my pods unhealthy?"
}
```

---

## CI/CD Pipeline

Git push to main
    ↓
GitHub Actions (self-hosted runner)
    ↓
Docker multi-stage build
    ↓
Push image to GHCR
    ↓
kubectl rollout to K3s cluster

The pipeline uses a multi-stage Dockerfile that separates the build environment from the runtime image, resulting in a smaller and more secure final container. The runtime stage runs as a non-root user with a built-in Docker healthcheck.

---

## What I Learned

- How Kubernetes ingress, services, and deployments work together as a request pipeline
- Multi-stage Docker builds and why runtime images should be lean and run as non-root
- How Prometheus scrapes metrics and how to expose them from a Flask application
- How to wire a self-hosted GitHub Actions runner to automate build and deploy on every push
- How to integrate a local LLM (Ollama/Mistral) as a practical operations tool
- Debugging real production issues — Ollama binding to localhost vs 0.0.0.0, snap conflicts with systemd, GHCR authentication in Kubernetes

---

## Planned Improvements

- Connect to AWS RDS for persistent inventory storage
- Terraform configuration for AWS infrastructure provisioning
- Frontend UI for inventory browsing
- Grafana dashboards with meaningful application metrics
- Horizontal pod autoscaling based on request load
