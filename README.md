# 🚀 Branch Loan API — Production-Ready, Containerized & Monitored


This repository contains the complete **DevOps transformation** of the Branch Loan API, turning a simple local Flask app into a **production-grade, containerized service** with automated CI/CD, multi-environment support, observability, and security scanning.

---

## ✅ What’s Been Accomplished

| Feature | Status |
|----------|--------|
| **Containerization** | ✅ Runs via Docker Compose with PostgreSQL, Nginx (HTTPS), and self-signed certificate |
| **Multi-Environment Setup** | ✅ Dev, Staging, Prod via `.env` files (`.env.dev`, `.env.staging`, `.env.prod`) |
| **CI/CD Pipeline** | ✅ GitHub Actions automates Test → Build → Scan → Push to Docker Hub |
| **Observability & Monitoring** | ✅ Health Check + JSON Logging + Prometheus Metrics + Grafana Dashboard |
| **Security** | ✅ Vulnerability scanning (Trivy) — fails pipeline on critical CVEs (e.g., fixed Gunicorn 21.2.0) |

---

## 📦 Quick Start: Run Locally

Follow these steps to run locally 👇

### 🧩 Step 1: Clone and Fork

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/dummy-branch-app.git
cd dummy-branch-app
```

### 🔐 Step 2: Set Up Local Domain & SSL
Add this to your /etc/hosts (Linux/macOS) or C:\Windows\System32\drivers\etc\hosts (Windows):

```127.0.0.1 branchloans.com```

Generated a self-signed SSL certificate:
```
mkdir -p nginx/certs
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout nginx/certs/branchloans.key \
  -out nginx/certs/branchloans.crt \
  -subj "/CN=branchloans.com"
```

### 🐳 Step 3: Build & Start Services
```
docker compose --env-file .env.dev up -d --build
docker compose exec api alembic upgrade head
docker compose exec api python scripts/seed.py
```

### 🔎 Step 4: Verify Everything Works

#### ✅ Health Check (with real DB connectivity) 
  
  https://branchloans.com/health

  Response
  ```
{"status": "healthy", "database": "connected"}
```

#### ✅ Prometheus Dashboard

Visit: http://localhost:9090/targets

→ You should see branch-loan-api as UP ✅

<img width="1916" height="335" alt="branch-prometheus" src="https://github.com/user-attachments/assets/b1acedd1-eb98-4544-8ba9-a8f5858f952c" />

#### ✅ Grafana Dashboard

Visit: http://localhost:3000

→ Import or view pre-configured dashboard.

<img width="796" height="284" alt="branch-grafana2" src="https://github.com/user-attachments/assets/dafafee7-4f5c-494c-a63a-16e73f1c10e6" />


#### ✅ Prometheus Query Example

```In http://localhost:9090/graph``` : ```http_requests_total```

→ Displays request counts by endpoint and status.

<img width="1916" height="415" alt="branch-prometheus-graph" src="https://github.com/user-attachments/assets/50900c63-547d-4080-958e-67590b3a322f" />

## ⚙️ Multi-Environment Configuration

Switch environments easily:

| Environment     | Command                                                |
| --------------- | ------------------------------------------------------ |
| **Development** | `docker compose --env-file .env.dev up -d --build`     |
| **Staging**     | `docker compose --env-file .env.staging up -d --build` |
| **Production**  | `docker compose --env-file .env.prod up -d --build`    |


## 🛡️ CI/CD Pipeline — GitHub Actions

Automatically runs on push and PR events:

- Push to main → Builds, scans, and pushes image to Docker Hub.
- Pull Request → Runs tests & security scan, but does not push images.

⚙️ Pipeline Stages

- Test → Validates imports and app startup
- Build → Builds Docker image (tagged with Git SHA)

🔍 Security Scan → Trivy fails on critical CVEs

- Push → Publishes to Docker Hub (on main)
- Secrets (DOCKERHUB_USERNAME, DOCKERHUB_TOKEN) are securely stored in GitHub.


## 📊 Observability & Monitoring
### 🩺 /health Endpoint

Now checks real DB connectivity: 
```
{
  "status": "healthy",
  "database": "connected"
}
```

### 📈 Prometheus Metrics

http_requests_total: Count of all HTTP requests (by method, endpoint, status)

http_request_duration_seconds: Request latency histogram

System-level metrics (CPU, memory, file descriptors)

Endpoint: https://branchloans.com/metrics


## 🏗️ Architecture Diagram

![branch-workflow-gif](https://github.com/user-attachments/assets/8d78ad79-feed-49cc-ba63-8cae5a0c963c)


## Verify All Services
```
docker compose ps
docker compose logs api
curl -k https://branchloans.com/health
curl -k https://branchloans.com/metrics
```

Visit:

- Prometheus → http://localhost:9090
- Grafana → http://localhost:3000


## 🧑‍💻 Author

Soumyadeep Mallick

DevOps Engineer | Cloud & Automation Enthusiast

📧 soumyadeep.prof@gmail.com

🌐 https://github.com/Soumya-2003
