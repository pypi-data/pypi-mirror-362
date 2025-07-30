# Langfuse Production Deployment Guide

This guide outlines the steps required to deploy Langfuse in a production environment using Helm charts.

## Prerequisites

- Kubernetes cluster 1.24+
- Helm 3.8+
- External PostgreSQL database (e.g., AWS RDS)
- SSL certificates (or cert-manager setup)
- Storage classes for persistent volumes
- SigNoz for monitoring and observability

## Pre-deployment Checklist

1. Database Setup
   - [ ] Create RDS instance
   - [ ] Configure security groups
   - [ ] Create database and user
   - [ ] Note down connection details

2. Storage
   - [ ] Configure storage classes
   - [ ] Ensure sufficient quota
   - [ ] Set up backup solutions

3. Networking
   - [ ] Configure domain DNS
   - [ ] Set up ingress controller
   - [ ] Configure SSL certificates
   - [ ] Set up network policies

4. Security
   - [ ] Create necessary secrets
   - [ ] Configure RBAC
   - [ ] Set up pod security policies
   - [ ] Configure network policies

5. Monitoring
   - [ ] Deploy SigNoz
   - [ ] Configure sampling rate
   - [ ] Set up retention policies
   - [ ] Configure alerts

## Configuration Steps

1. Create the production namespace:
   ```bash
   kubectl create namespace langfuse-prod
   ```

2. Create required secrets:
   ```bash
   # PostgreSQL secrets
   kubectl create secret generic langfuse-secrets \
     --namespace ai-observability \
     --from-literal=database-password='your-db-password' \
     --from-literal=nextauth-secret='your-nextauth-secret' \
     --from-literal=salt='your-salt' \
     --from-literal=encryption-key='your-encryption-key'

   # ClickHouse secrets
   kubectl create secret generic clickhouse-secrets \
     --namespace langfuse-prod \
     --from-literal=clickhouse-password='your-clickhouse-password'

   # Redis secrets
   kubectl create secret generic redis-secrets \
     --namespace langfuse-prod \
     --from-literal=redis-password='your-redis-password'

   # MinIO secrets
   kubectl create secret generic minio-secrets \
     --namespace langfuse-prod \
     --from-literal=root-password='your-minio-password'
   ```

3. Configure values-production.yaml:
   - Update domain names
   - Set appropriate resource limits
   - Configure storage classes
   - Set SigNoz options

4. Install cert-manager (if not already installed):
   ```bash
   helm repo add jetstack https://charts.jetstack.io
   helm repo update
   helm install cert-manager jetstack/cert-manager \
     --namespace cert-manager \
     --create-namespace \
     --version v1.13.0 \
     --set installCRDs=true
   ```

5. Create ClusterIssuer for SSL:
   ```yaml
   apiVersion: cert-manager.io/v1
   kind: ClusterIssuer
   metadata:
     name: letsencrypt-prod
   spec:
     acme:
       server: https://acme-v02.api.letsencrypt.org/directory
       email: your-email@example.com
       privateKeySecretRef:
         name: letsencrypt-prod
       solvers:
       - http01:
           ingress:
             class: nginx
   ```

## Deployment

1. Add required Helm repositories:
   ```bash
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm repo update
   ```

2. Deploy Langfuse:
   ```bash
   helm upgrade --install langfuse ./helm \
     --namespace langfuse-prod \
     --values values-production.yaml \
     --timeout 10m
   ```

## Post-deployment Verification

1. Check all pods are running:
   ```bash
   kubectl get pods -n langfuse-prod
   ```

2. Verify services:
   ```bash
   kubectl get svc -n langfuse-prod
   ```

3. Check ingress and SSL:
   ```bash
   kubectl get ingress -n langfuse-prod
   ```

4. Test database connectivity:
   ```bash
   kubectl exec -it deployment/langfuse -n langfuse-prod -- \
     curl http://localhost:3000/api/public/health
   ```

5. Monitor logs and traces in SigNoz:
   ```bash
   # Access SigNoz UI at your configured endpoint
   # Default: https://signoz.yourdomain.com
   ```

## Monitoring with SigNoz

1. Access SigNoz:
   - URL: https://signoz.yourdomain.com
   - Monitor application metrics, traces, and logs
   - Set up custom dashboards for Langfuse components

2. Key Metrics to Monitor:
   - Application latency
   - Error rates
   - Resource utilization
   - Database performance
   - Queue lengths
   - API response times

3. Configure Alerts:
   - Set up alert rules for critical metrics
   - Configure notification channels
   - Define escalation policies

## Backup and Recovery

1. Database Backups:
   - RDS automated backups
   - ClickHouse backups at 2 AM daily
   - Retention: 7 daily, 4 weekly, 3 monthly

2. Recovery Procedures:
   - See disaster recovery documentation
   - Test recovery procedures regularly

## Scaling

The deployment includes HorizontalPodAutoscaler configurations:
- Langfuse: 3-10 replicas
- Workers: 2-8 replicas
- Based on CPU (70%) and Memory (80%) utilization

## Security Notes

1. All passwords should be changed from defaults
2. Network policies restrict pod communication
3. Pod security context enforces non-root execution
4. Regular security audits recommended

## Troubleshooting

Common issues and solutions:

1. Pod startup failures:
   - Check resource limits
   - Verify secrets exist
   - Check storage class availability

2. Database connection issues:
   - Verify RDS security groups
   - Check connection strings
   - Validate credentials

3. Performance issues:
   - Monitor resource usage in SigNoz
   - Check connection pools
   - Verify autoscaling behavior

## Support

For production support:
1. Check SigNoz for logs and traces
2. Review error patterns
3. Contact Langfuse support with:
   - Deployment details
   - Error logs
   - Recent changes

## Maintenance

Regular maintenance tasks:
1. Update Helm charts
2. Rotate credentials
3. Review and adjust resource limits
4. Check SigNoz retention policies
5. Verify backup integrity 