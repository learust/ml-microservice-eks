#!/bin/bash
set -e

echo "==> Freezing workloads in sentimentanalysis-cluster (EKS)..."

# Step 1: Scale down all application deployments to 0 replicas
echo "Scaling down deployments to 0 replicas..."
kubectl scale deployment/api-gateway --replicas=0
kubectl scale deployment/car-value-service --replicas=0
kubectl scale deployment/review-service --replicas=0

# Step 2: Verify scaling
echo "Waiting for pods to terminate..."
sleep 15
kubectl get pods -o wide

# Step 3: Reduce nodegroup to minimum (optional for cost saving)
echo "Scaling nodegroup down to minSize=0..."
aws eks update-nodegroup-config \
  --cluster-name sentimentanalysis-cluster \
  --nodegroup-name sentiment-nodes-v9 \
  --scaling-config minSize=0,maxSize=6,desiredSize=0 \
  --region us-east-1

echo "==> Freeze complete. All app workloads stopped and nodegroup scaled to 0."