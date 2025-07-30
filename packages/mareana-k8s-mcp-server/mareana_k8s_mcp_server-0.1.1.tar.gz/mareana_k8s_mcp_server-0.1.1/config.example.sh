#!/bin/bash

# Configuration for Kubernetes MCP Server
# Based on the network logs from https://dashboard-dev.mareana.com/

# Kubernetes API Server URL
# The dashboard API calls go to the same host, so the API server is likely at the same domain
export K8S_API_SERVER="https://dashboard-dev.mareana.com/api/v1"

# Service Account Token (extracted from network logs)
# This is the actual JWT token used by the dashboard for authentication
export K8S_TOKEN="eyJhbGciOiJSUzI1NiIsImtpZCI6Ii1fT3MyMnphTkh2N1pJWFc0QVFxZndPNE1rYW8tRVBnRE9rNFd1ckNWOEkifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkZXZlbG9wZXItdXNlci10b2tlbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJkZXZlbG9wZXItdXNlciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImQ0OGUzMTRiLWZhMzEtNGQxZS1hM2Q5LTEwOGEwMzQ1ZjFhMyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlcm5ldGVzLWRhc2hib2FyZDpkZXZlbG9wZXItdXNlciJ9"

# SSL verification - keep enabled for production
export K8S_VERIFY_SSL="true"

echo "Kubernetes MCP Server environment configured"
echo "API Server: $K8S_API_SERVER"
echo "Using service account: system:serviceaccount:kubernetes-dashboard:developer-user"
echo "Token configured from dashboard network logs" 