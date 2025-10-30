#!/bin/bash
set -e

echo "==> Thawing workloads in sentimentanalysis-cluster (EKS)..."

# Step 1: Scale node group back up for workloads
echo "Scaling nodegroup up to min=3, desired=5, max=6..."
aws eks update-nodegroup-config \
  --cluster-name sentimentanalysis-cluster \
  --nodegroup-name sentiment-nodes-v9 \
  --scaling-config minSize=3,maxSize=6,desiredSize=5 \
  --region us-east-1

# Wait for nodes to register
echo "Waiting for nodes to become Ready..."
sleep 45
kubectl get nodes -o wide

# Step 2: Scale up deployments to operational levels
echo "Scaling deployments back up..."
kubectl scale deployment/api-gateway --replicas=10
kubectl scale deployment/car-value-service --replicas=10
kubectl scale deployment/review-service --replicas=10

# Step 3: Verify rollout
echo "Waiting for pods to come online..."
sleep 30
kubectl get pods -o wide

echo "==> Thaw complete. All app workloads scaled up and nodes restored."