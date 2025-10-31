# ML Microservices on Amazon EKS

A scalable microservices architecture deployed on Amazon EKS (Elastic Kubernetes Service) for car value estimation and review sentiment analysis.

## Architecture

This project consists of three microservices:

1. **API Gateway** - Orchestrates requests and aggregates responses
2. **Car Value Service** - ML-based car trade-in value estimation
3. **Review Service** - Sentiment analysis for car reviews

```
┌─────────────┐
│  API Gateway│ :8080
└──────┬──────┘
       │
       ├─────────► Car Value Service :5001
       │           (Linear Regression ML Model)
       │
       └─────────► Review Service :5002
                   (Sentiment Analysis)
```

## Services

### API Gateway:
- **Port:** 8080
- **Endpoints:**
  - `GET /health` - Health check
  - `POST /api/car-analysis` - Combined car value + sentiment analysis
  - `POST /api/car-value` - Car value estimation only
  - `POST /api/review-sentiment` - Sentiment analysis only

### Car Value Service:
- **Port:** 5001
- **Technology:** scikit-learn Linear Regression
- **Endpoint:** `POST /api/trade`
- **Input:** `{"year": 2018, "mileage": 45000}`

### Review Service:
- **Port:** 5002
- **Technology:** Keyword-based sentiment analysis
- **Endpoint:** `POST /api/review`
- **Input:** `{"review": "Great car!"}`

## Quick Start

### Local Development (Docker Compose)

```bash
# Build and run all services
docker-compose up --build

# Test the API
curl -X POST http://localhost:8080/api/car-analysis \
  -H "Content-Type: application/json" \
  -d '{"year":2018,"mileage":45000,"review":"Great car!"}'
```

### Kubernetes Deployment

```bash
# Deploy services
kubectl apply -f gateway/deployment.yaml
kubectl apply -f car-value-service/deployment.yaml
kubectl apply -f review-service/deployment.yaml

# Deploy Horizontal Pod Autoscalers
kubectl apply -f gateway/hpa.yaml
kubectl apply -f car-value-service/hpa.yaml
kubectl apply -f review-service/hpa.yaml

# Check deployment status
kubectl get pods
kubectl get svc
```

## Auto-Scaling Configuration

All services are configured with Horizontal Pod Autoscalers (HPA):

- **Min Replicas:** 10
- **Max Replicas:** 25
- **CPU Target:** 50-60% utilization

## Load Testing

Run load tests using the provided load generator:

```bash
# Deploy load generator
kubectl apply -f loadgen.yaml

# View results
kubectl logs -f loadgen
```

## Cluster Management Scripts

### Freeze Cluster (Cost Saving)
Scales down all workloads and nodes to zero:
```bash
./freeze.sh
```

### Thaw Cluster (Restore)
Scales cluster back to operational state:
```bash
./thaw.sh
```

## Project Structure

```
.
├── gateway/              # API Gateway service
│   ├── app.py
│   ├── Dockerfile
│   ├── deployment.yaml
│   ├── hpa.yaml
│   └── requirements.txt
├── car-value-service/    # Car valuation ML service
│   ├── app.py
│   ├── price.py
│   ├── Dockerfile
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── requirements.txt
│   └── data/
│       └── Car_Value_Dataset.csv
├── review-service/       # Sentiment analysis service
│   ├── app.py
│   ├── sentiment.py
│   ├── Dockerfile
│   ├── deployment.yaml
│   ├── hpa.yaml
│   └── requirements.txt
├── docker-compose.yml    # Local development
├── loadgen.yaml         # Kubernetes load testing
├── freeze.sh            # Scale down cluster
└── thaw.sh              # Scale up cluster
```

## Technologies

- **Backend:** Python, Flask
- **ML:** scikit-learn
- **Containerization:** Docker
- **Orchestration:** Kubernetes (EKS)
- **Scaling:** Horizontal Pod Autoscaler
- **Web Server:** Gunicorn