"""
Kubernetes MCP Server - provides tools for interacting with Kubernetes clusters
"""
import asyncio
import json
import logging
from typing import Any

from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
)

from .k8s_client import create_k8s_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("k8s-mcp-server")

# Create the MCP server
server = Server("k8s-mcp-server")

# Global client variable for lazy initialization
k8s_client = None

async def initialize_client():
    """Initialize the Kubernetes client lazily"""
    global k8s_client
    if k8s_client is None:
        try:
            k8s_client = create_k8s_client()
            logger.info("Kubernetes client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kubernetes client: {e}")
            raise

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available Kubernetes tools"""
    return [
        Tool(
            name="get_pod_logs",
            description="Get logs from a Kubernetes pod",
            inputSchema={
                "type": "object",
                "properties": {
                    "pod_name": {
                        "type": "string",
                        "description": "Name of the pod"
                    },
                    "namespace": {
                        "type": "string", 
                        "description": "Kubernetes namespace",
                        "default": "default"
                    },
                    "lines": {
                        "type": "integer",
                        "description": "Number of log lines to retrieve",
                        "default": 100
                    }
                },
                "required": ["pod_name"]
            }
        ),
        Tool(
            name="list_namespace_pods",
            description="List all pods in a Kubernetes namespace",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {
                        "type": "string",
                        "description": "Kubernetes namespace to list pods from",
                        "default": "default"
                    }
                },
                "required": ["namespace"]
            }
        ),
        Tool(
            name="list_namespaces",
            description="List all available Kubernetes namespaces",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_pod_environment",
            description="Get environment variables and secrets for a Kubernetes pod",
            inputSchema={
                "type": "object",
                "properties": {
                    "pod_name": {
                        "type": "string",
                        "description": "Name of the pod"
                    },
                    "namespace": {
                        "type": "string", 
                        "description": "Kubernetes namespace",
                        "default": "default"
                    }
                },
                "required": ["pod_name"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute a tool call"""
    if k8s_client is None:
        await initialize_client()
    
    try:
        if name == "get_pod_logs":
            pod_name = arguments.get("pod_name")
            namespace = arguments.get("namespace", "default")
            lines = arguments.get("lines", 100)
            
            if not pod_name:
                return [TextContent(type="text", text="Error: pod_name is required")]
            
            logs = k8s_client.get_pod_logs(pod_name, namespace, lines)
            if logs:
                result = {
                    "pod_name": pod_name,
                    "namespace": namespace,
                    "lines_requested": lines,
                    "logs": logs
                }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            else:
                return [TextContent(type="text", text=f"No logs found for pod '{pod_name}' in namespace '{namespace}'")]
        
        elif name == "list_namespace_pods":
            namespace = arguments.get("namespace", "default")
            
            pods = k8s_client.list_pods(namespace)
            result = {
                "namespace": namespace,
                "pods": pods,
                "total_count": len(pods)
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "list_namespaces":
            namespaces = k8s_client.list_namespaces()
            result = {
                "namespaces": namespaces,
                "total_count": len(namespaces)
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_pod_environment":
            pod_name = arguments.get("pod_name")
            namespace = arguments.get("namespace", "default")
            
            if not pod_name:
                return [TextContent(type="text", text="Error: pod_name is required")]
            
            env_data = k8s_client.get_pod_environment_variables(pod_name, namespace)
            return [TextContent(type="text", text=json.dumps(env_data, indent=2))]
        
        else:
            return [TextContent(type="text", text=f"Error: Unknown tool '{name}'")]
    
    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    """Run the MCP server"""
    # Don't initialize client on startup - do it lazily when needed
    logger.info("Starting Kubernetes MCP server (lazy initialization)")
    
    # Import here to avoid issues with uvloop on some systems
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

def main_entry():
    """Entry point for the MCP server."""
    asyncio.run(main())

if __name__ == "__main__":
    main_entry()
