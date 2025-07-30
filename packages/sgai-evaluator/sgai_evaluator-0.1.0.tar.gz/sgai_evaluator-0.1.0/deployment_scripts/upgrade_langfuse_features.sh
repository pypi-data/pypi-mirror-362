#!/bin/bash

echo "🔄 Upgrading Langfuse to Latest Version with Evaluation & Playground Features"
echo "============================================================================"

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

# Backup current deployment
echo "📦 Creating backup of current deployment..."
kubectl get deployment langfuse -n ai-observability -o yaml > langfuse-deployment-backup.yaml
echo "✅ Backup saved to langfuse-deployment-backup.yaml"

# Update configuration with new features
echo "🔧 Updating configuration with new features..."
kubectl apply -f kubernetes/langfuse-secrets.yaml

# Scale down current deployment
echo "⏸️  Scaling down current deployment..."
kubectl scale deployment langfuse -n ai-observability --replicas=0

# Wait for pods to terminate
echo "⏳ Waiting for pods to terminate..."
kubectl wait --for=delete pods -l app=langfuse -n ai-observability --timeout=60s

# Update deployment with latest image
echo "🚀 Deploying latest Langfuse with new features..."
kubectl apply -f kubernetes/langfuse-deployment.yaml

# Wait for deployment to be ready
echo "⏳ Waiting for new deployment to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/langfuse -n ai-observability

# Check deployment status
echo "📊 Checking deployment status..."
kubectl get pods -n ai-observability -l app=langfuse

# Get the pod name for logs
LANGFUSE_POD=$(kubectl get pods -n ai-observability -l app=langfuse -o jsonpath='{.items[0].metadata.name}')

echo "📋 Checking startup logs..."
kubectl logs -n ai-observability $LANGFUSE_POD --tail=50

echo ""
echo "🎉 Upgrade completed!"
echo "========================================="
echo "✅ Langfuse upgraded to latest version"
echo "✅ Experimental features enabled"
echo "✅ Evaluation features enabled"
echo "✅ Playground features enabled"
echo "✅ Database migrations enabled"
echo ""
echo "🔧 Next steps:"
echo "1. Access your Langfuse dashboard: http://localhost:3000"
echo "2. Log in with your admin credentials"
echo "3. Look for the 'Evaluation' and 'Playground' tabs in the left sidebar"
echo "4. If tabs are still missing, check the pod logs for any errors"
echo ""
echo "📋 To check logs:"
echo "kubectl logs -n ai-observability $LANGFUSE_POD"
echo ""
echo "🔄 To port-forward if needed:"
echo "kubectl port-forward -n ai-observability svc/langfuse 3000:3000"
echo ""
echo "⚠️  Note: If you still don't see the tabs, try:"
echo "- Hard refresh your browser (Ctrl+F5 or Cmd+Shift+R)"
echo "- Clear browser cache"
echo "- Try in incognito/private browsing mode" 