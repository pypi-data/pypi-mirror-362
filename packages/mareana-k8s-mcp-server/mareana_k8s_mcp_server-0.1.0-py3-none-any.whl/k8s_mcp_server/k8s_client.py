"""
Kubernetes Dashboard Client for MCP Server
"""
import requests
import json
import os
from urllib3.exceptions import InsecureRequestWarning
import warnings
from typing import List, Dict, Any, Optional

# Suppress SSL warnings since we're using insecure-skip-tls-verify
warnings.filterwarnings('ignore', category=InsecureRequestWarning)

class K8sDashboardClient:
    """
    Kubernetes client that uses the dashboard API endpoints
    """
    
    def __init__(self, dashboard_url: str, token: str):
        self.dashboard_url = dashboard_url.rstrip('/')
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        self.session = requests.Session()
        self.session.verify = False  # Skip SSL verification
        
    def list_namespaces(self) -> List[str]:
        """List all namespaces using dashboard API"""
        try:
            url = f"{self.dashboard_url}/api/v1/namespace"
            response = self.session.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if 'namespaces' in data:
                return [ns['objectMeta']['name'] for ns in data['namespaces']]
            return []
                
        except Exception as e:
            raise Exception(f"Failed to list namespaces: {e}")
    
    def list_pods(self, namespace: str = "default") -> List[Dict[str, Any]]:
        """List pods in a namespace using dashboard API"""
        try:
            url = f"{self.dashboard_url}/api/v1/pod/{namespace}"
            response = self.session.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if 'pods' in data:
                pods = []
                for pod in data['pods']:
                    pod_info = {
                        'name': pod['objectMeta']['name'],
                        'namespace': pod['objectMeta']['namespace'],
                        'phase': pod.get('podPhase', 'Unknown'),
                        'creation_timestamp': pod['objectMeta'].get('creationTimestamp', ''),
                        'status': pod.get('podStatus', 'Unknown')
                    }
                    pods.append(pod_info)
                return pods
            return []
                
        except Exception as e:
            raise Exception(f"Failed to list pods in namespace {namespace}: {e}")

    def get_pod_logs(self, pod_name: str, namespace: str = "default", lines: int = 100) -> str:
        """Get pod logs using dashboard API"""
        try:
            url = f"{self.dashboard_url}/api/v1/log/{namespace}/{pod_name}"
            params = {'tailLines': lines}
            response = self.session.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if 'logs' in data:
                # Extract log content from the response structure
                log_lines = []
                for log_entry in data['logs']:
                    timestamp = log_entry.get('timestamp', '')
                    content = log_entry.get('content', '')
                    log_lines.append(f"{timestamp} {content}")
                
                return '\n'.join(log_lines)
            return ""
                
        except Exception as e:
            raise Exception(f"Failed to get logs for pod {pod_name} in namespace {namespace}: {e}")

    def get_pod_environment_variables(self, pod_name: str, namespace: str = "default") -> Dict[str, Any]:
        """Get environment variables and secrets for a pod using dashboard API"""
        try:
            url = f"{self.dashboard_url}/api/v1/pod/{namespace}/{pod_name}"
            response = self.session.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract environment variables from all containers
            pod_env_info = {
                'pod_name': pod_name,
                'namespace': namespace,
                'containers': []
            }
            
            # Process main containers
            if 'containers' in data:
                for container in data['containers']:
                    container_env = {
                        'container_name': container.get('name', 'unknown'),
                        'image': container.get('image', 'unknown'),
                        'environment_variables': []
                    }
                    
                    if 'env' in container:
                        for env_var in container['env']:
                            env_info = {
                                'name': env_var.get('name', ''),
                                'value': env_var.get('value', ''),
                                'source': 'direct'
                            }
                            
                            # Check if it's from a configMap or secret
                            if env_var.get('valueFrom'):
                                value_from = env_var['valueFrom']
                                if 'configMapKeyRef' in value_from:
                                    env_info['source'] = 'configMap'
                                    env_info['config_map'] = value_from['configMapKeyRef'].get('name', '')
                                    env_info['key'] = value_from['configMapKeyRef'].get('key', '')
                                elif 'secretKeyRef' in value_from:
                                    env_info['source'] = 'secret'
                                    env_info['secret'] = value_from['secretKeyRef'].get('name', '')
                                    env_info['key'] = value_from['secretKeyRef'].get('key', '')
                                    # Don't expose secret values in logs - mark as redacted
                                    env_info['value'] = '[REDACTED - Secret Value]'
                            
                            container_env['environment_variables'].append(env_info)
                    
                    pod_env_info['containers'].append(container_env)
            
            # Process init containers if present
            if 'initContainers' in data and data['initContainers']:
                for container in data['initContainers']:
                    container_env = {
                        'container_name': f"{container.get('name', 'unknown')} (init)",
                        'image': container.get('image', 'unknown'),
                        'environment_variables': []
                    }
                    
                    if 'env' in container:
                        for env_var in container['env']:
                            env_info = {
                                'name': env_var.get('name', ''),
                                'value': env_var.get('value', ''),
                                'source': 'direct'
                            }
                            
                            if env_var.get('valueFrom'):
                                value_from = env_var['valueFrom']
                                if 'configMapKeyRef' in value_from:
                                    env_info['source'] = 'configMap'
                                    env_info['config_map'] = value_from['configMapKeyRef'].get('name', '')
                                    env_info['key'] = value_from['configMapKeyRef'].get('key', '')
                                elif 'secretKeyRef' in value_from:
                                    env_info['source'] = 'secret'
                                    env_info['secret'] = value_from['secretKeyRef'].get('name', '')
                                    env_info['key'] = value_from['secretKeyRef'].get('key', '')
                                    env_info['value'] = '[REDACTED - Secret Value]'
                            
                            container_env['environment_variables'].append(env_info)
                    
                    pod_env_info['containers'].append(container_env)
            
            return pod_env_info
                
        except Exception as e:
            raise Exception(f"Failed to get environment variables for pod {pod_name} in namespace {namespace}: {e}")

def create_k8s_client() -> K8sDashboardClient:
    """Create and return a configured Kubernetes dashboard client from environment variables"""
    dashboard_url = os.getenv('K8S_DASHBOARD_URL')
    token = os.getenv('K8S_TOKEN')
    
    if not all([dashboard_url, token]):
        raise Exception(
            "Missing required environment variables: K8S_DASHBOARD_URL, K8S_TOKEN"
        )
    
    return K8sDashboardClient(dashboard_url, token)