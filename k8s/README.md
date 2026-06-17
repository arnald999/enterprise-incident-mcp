# Kubernetes Deployment

These manifests deploy the Enterprise Incident MCP Server and PostgreSQL with pgvector.

## Apply

```bash
kubectl apply -f k8s/
```

## Check Pods

```bash
kubectl get pods -n enterprise-incident
```

## Check Services

```bash
kubectl get svc -n enterprise-incident
```

## Logs

```bash
kubectl logs -n enterprise-incident deployment/enterprise-incident-mcp
```

## Delete

```bash
kubectl delete namespace enterprise-incident
```

## Note

This is a local/development Kubernetes setup. For production, use:

- Managed PostgreSQL
- External secrets
- Persistent volumes
- Resource limits
- Health probes
- CI/CD image publishing
