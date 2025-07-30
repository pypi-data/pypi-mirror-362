#!/bin/bash

echo "🔍 Checking Langfuse Features Status"
echo "=================================="

# Set error handling
set -e

# Get pod name
LANGFUSE_POD=$(kubectl get pods -n ai-observability -l app=langfuse -o jsonpath='{.items[0].metadata.name}')

if [ -z "$LANGFUSE_POD" ]; then
    echo "❌ No Langfuse pod found"
    exit 1
fi

echo "📍 Checking pod: $LANGFUSE_POD"

# Check if pod is running
POD_STATUS=$(kubectl get pod $LANGFUSE_POD -n ai-observability -o jsonpath='{.status.phase}')
echo "📊 Pod status: $POD_STATUS"

if [ "$POD_STATUS" != "Running" ]; then
    echo "❌ Pod is not running. Current status: $POD_STATUS"
    echo "📋 Pod logs:"
    kubectl logs -n ai-observability $LANGFUSE_POD --tail=20
    exit 1
fi

echo "✅ Pod is running"

# Check environment variables
echo ""
echo "🔧 Checking environment variables..."
kubectl exec -n ai-observability $LANGFUSE_POD -- printenv | grep -E "(LANGFUSE_ENABLE_|EXPERIMENTAL)" || echo "⚠️  No feature flags found"

# Check if service is accessible
echo ""
echo "🌐 Checking service accessibility..."
kubectl exec -n ai-observability $LANGFUSE_POD -- curl -s http://localhost:3000/api/public/health || echo "❌ Health check failed"

# Check recent logs for any errors
echo ""
echo "📋 Recent logs (last 20 lines):"
kubectl logs -n ai-observability $LANGFUSE_POD --tail=20

echo ""
echo "🎯 Quick troubleshooting steps:"
echo "1. Port forward: kubectl port-forward -n ai-observability svc/langfuse 3000:3000"
echo "2. Access dashboard: http://localhost:3000"
echo "3. Hard refresh browser: Ctrl+F5 (or Cmd+Shift+R on Mac)"
echo "4. Try incognito/private browsing mode"
echo "5. Check browser console for JavaScript errors"
echo ""
echo "📚 If features are still missing, they may not be available in the current version."
echo "Consider checking the Langfuse documentation or GitHub releases for feature availability." 