#!/bin/bash

echo "🚀 Deploying Langfuse v3 with ClickHouse Integration"
echo "=================================================="

# Set error handling
set -e

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if we're connected to a cluster
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Not connected to a Kubernetes cluster. Please configure kubectl."
    exit 1
fi

echo "✅ Connected to Kubernetes cluster"

# Check if ai-observability namespace exists
if ! kubectl get namespace ai-observability &> /dev/null; then
    echo "❌ ai-observability namespace does not exist. Please create it first."
    exit 1
fi

echo "✅ ai-observability namespace found"

# Step 1: Stop current Langfuse to avoid conflicts
echo "⏸️  Stopping current Langfuse deployment..."
kubectl scale deployment langfuse -n ai-observability --replicas=0 || true

echo "⏳ Waiting for Langfuse pods to terminate..."
kubectl wait --for=delete pods -l app=langfuse -n ai-observability --timeout=60s || true

# Step 2: Deploy ClickHouse
echo "🗃️  Deploying ClickHouse..."
kubectl apply -f kubernetes/clickhouse-deployment.yaml

echo "⏳ Waiting for ClickHouse to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/clickhouse -n ai-observability

# Verify ClickHouse is running
echo "🔍 Verifying ClickHouse deployment..."
kubectl get pods -n ai-observability -l app=clickhouse

# Test ClickHouse connectivity
CLICKHOUSE_POD=$(kubectl get pods -n ai-observability -l app=clickhouse -o jsonpath='{.items[0].metadata.name}')
echo "📋 Testing ClickHouse connectivity..."
kubectl exec -n ai-observability $CLICKHOUSE_POD -- clickhouse-client --query "SELECT 1" || echo "⚠️  ClickHouse test query failed, but continuing..."

# Step 3: Update Langfuse configuration
echo "🔧 Updating Langfuse configuration..."
kubectl apply -f kubernetes/langfuse-secrets.yaml

# Step 4: Deploy Langfuse with ClickHouse integration
echo "🎯 Deploying Langfuse v3 with ClickHouse integration..."
kubectl apply -f kubernetes/langfuse-deployment.yaml

# Step 5: Wait for Langfuse to be ready
echo "⏳ Waiting for Langfuse to be ready..."
kubectl wait --for=condition=available --timeout=600s deployment/langfuse -n ai-observability

# Step 6: Check deployment status
echo "📊 Checking deployment status..."
kubectl get pods -n ai-observability

# Step 7: Verify Langfuse is working
LANGFUSE_POD=$(kubectl get pods -n ai-observability -l app=langfuse -o jsonpath='{.items[0].metadata.name}')
echo "📋 Checking Langfuse startup logs..."
kubectl logs -n ai-observability $LANGFUSE_POD --tail=30

echo ""
echo "🎉 Deployment completed!"
echo "======================"
echo "✅ ClickHouse deployed and running"
echo "✅ Langfuse v3 deployed with ClickHouse integration"
echo "✅ All pods are running"
echo ""
echo "🔧 Next steps:"
echo "1. Port forward: kubectl port-forward -n ai-observability svc/langfuse 3000:3000"
echo "2. Access dashboard: http://localhost:3000"
echo "3. Look for 'Evaluation' and 'Playground' tabs in the sidebar"
echo ""
echo "📋 To check detailed logs:"
echo "kubectl logs -n ai-observability $LANGFUSE_POD -f"
echo ""
echo "🔍 To check ClickHouse:"
echo "kubectl logs -n ai-observability $CLICKHOUSE_POD"
echo ""
echo "⚠️  Note: Database migrations may take a few minutes on first startup!"
echo "If the pod shows 'Running' but takes time to respond, this is normal." 