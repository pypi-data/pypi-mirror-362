# Kubernetes MCP Server

An MCP server for fetching Kubernetes pod logs. This server provides AI assistants with the ability to list namespaces, pods, and access pod logs.

## Features

- List available namespaces
- List pods in a namespace
- Get pod logs (with optional container selection and line limiting)
- Stream pod logs in real-time

## Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Configure Kubernetes access:

   **Option A: Using Environment Variables (Recommended for specific cluster)**
   ```bash
   export K8S_API_SERVER="https://your-k8s-api-server"
   export K8S_TOKEN="your-service-account-token"
   ```

   **Option B: Using Local Kubeconfig**
   - The server will automatically try to use in-cluster configuration if running inside Kubernetes
   - Otherwise, it will fall back to using your local kubeconfig file

   **For the Mareana dashboard cluster:**
   ```bash
   # Use the provided configuration
   source config.example.sh
   
   # Or set manually:
   export K8S_API_SERVER="https://dashboard-dev.mareana.com/api/v1"
   export K8S_TOKEN="eyJhbGciOiJSUzI1NiIsImtpZCI6Ii1fT3MyMnphTkh2N1pJWFc0QVFxZndPNE1rYW8tRVBnRE9rNFd1ckNWOEkifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkZXZlbG9wZXItdXNlci10b2tlbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJkZXZlbG9wZXItdXNlciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImQ0OGUzMTRiLWZhMzEtNGQxZS1hM2Q5LTEwOGEwMzQ1ZjFhMyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlcm5ldGVzLWRhc2hib2FyZDpkZXZlbG9wZXItdXNlciJ9"
   export K8S_VERIFY_SSL="true"
   ```

   Make sure you have the necessary permissions to access pod logs with your service account.

## Running the Server

```bash
python -m k8s_mcp_server.server
```

## Available Resources

The server provides the following resources:

1. Namespaces:
   ```
   namespace/{namespace_name}
   ```

2. Pods:
   ```
   pod/{namespace_name}/{pod_name}
   ```

## Available Tools

1. Get Pod Logs:
   - Tool: `get_pod_logs`
   - Parameters:
     - `namespace`: Kubernetes namespace
     - `pod_name`: Name of the pod
     - `container`: (optional) Container name
     - `tail_lines`: (optional) Number of lines to return from the end

2. List Namespace Pods:
   - Tool: `list_namespace_pods`
   - Parameters:
     - `namespace`: Kubernetes namespace 