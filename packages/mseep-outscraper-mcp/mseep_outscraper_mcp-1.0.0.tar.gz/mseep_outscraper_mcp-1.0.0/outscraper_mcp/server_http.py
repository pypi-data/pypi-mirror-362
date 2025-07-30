#!/usr/bin/env python3
"""
Outscraper MCP HTTP Server

HTTP server wrapper for Smithery deployment that exposes the MCP server
over HTTP at the /mcp endpoint.
"""

import os
import asyncio
import json
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("outscraper-mcp-http")

# Import the existing MCP server
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from outscraper_mcp.server import mcp

app = FastAPI(
    title="Outscraper MCP Server",
    description="HTTP wrapper for Outscraper MCP server",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint for container health monitoring"""
    api_key_set = bool(os.environ.get("OUTSCRAPER_API_KEY", "").strip())
    return {
        "status": "healthy",
        "service": "outscraper-mcp",
        "version": "1.0.0",
        "api_key_configured": api_key_set
    }

@app.get("/mcp")
async def mcp_get(request: Request):
    """Handle GET requests to /mcp endpoint for Smithery"""
    # Parse query parameters into config
    config = _parse_query_params(dict(request.query_params))
    
    # Set environment variables from config
    if config.get("apiKey"):
        os.environ["OUTSCRAPER_API_KEY"] = config["apiKey"]
    
    # Return server info and available tools
    return {
        "server": {
            "name": "outscraper-mcp",
            "version": "1.0.0"
        },
        "tools": [
            {
                "name": "google_maps_search",
                "description": "Search for businesses and places on Google Maps",
                "parameters": {
                    "query": {"type": "string", "required": True},
                    "limit": {"type": "integer", "default": 20},
                    "language": {"type": "string", "default": "en"},
                    "region": {"type": "string", "required": False}
                }
            },
            {
                "name": "google_maps_reviews", 
                "description": "Extract reviews from Google Maps places",
                "parameters": {
                    "query": {"type": "string", "required": True},
                    "reviews_limit": {"type": "integer", "default": 10},
                    "sort": {"type": "string", "default": "most_relevant"}
                }
            }
        ]
    }

@app.post("/mcp")
async def mcp_post(request: Request):
    """Handle POST requests to /mcp endpoint for tool execution"""
    try:
        # Parse query parameters into config
        config = _parse_query_params(dict(request.query_params))
        
        # Set environment variables from config
        if config.get("apiKey"):
            os.environ["OUTSCRAPER_API_KEY"] = config["apiKey"]
            logger.info("API key set from request parameters")
        
        # Get request body
        try:
            body = await request.json()
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in request body")
        
        # Extract tool call information
        tool_name = body.get("tool")
        arguments = body.get("arguments", {})
        
        if not tool_name:
            raise HTTPException(status_code=400, detail="Missing 'tool' in request body")
        
        # Log the tool execution
        logger.info(f"Executing tool: {tool_name} with arguments: {list(arguments.keys())}")
        
        # Execute the tool using the MCP server
        result = await _execute_tool(tool_name, arguments)
        
        return {"result": result}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in mcp_post: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/mcp")
async def mcp_delete():
    """Handle DELETE requests to /mcp endpoint for cleanup"""
    return {"message": "Server cleanup completed"}

def _parse_query_params(params: Dict[str, str]) -> Dict[str, Any]:
    """Parse dot-notation query parameters into nested config object"""
    config = {}
    
    for key, value in params.items():
        if "." in key:
            # Handle nested properties like "server.host"
            parts = key.split(".")
            current = config
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value
        else:
            config[key] = value
    
    return config

async def _execute_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Execute a tool using the MCP server
    
    Args:
        tool_name: Name of the tool to execute
        arguments: Arguments to pass to the tool
        
    Returns:
        Tool execution result as a string
        
    Raises:
        ValueError: If tool name is unknown
    """
    
    # Import the tool functions from server
    from outscraper_mcp.server import google_maps_search, google_maps_reviews
    
    try:
        if tool_name == "google_maps_search":
            return google_maps_search(**arguments)
        elif tool_name == "google_maps_reviews":
            return google_maps_reviews(**arguments)
        else:
            raise ValueError(f"Unknown tool: {tool_name}. Available tools: google_maps_search, google_maps_reviews")
    except TypeError as e:
        # Handle missing or invalid arguments
        raise ValueError(f"Invalid arguments for {tool_name}: {str(e)}")
    except Exception as e:
        # Log the error and re-raise
        logger.error(f"Error executing tool {tool_name}: {str(e)}", exc_info=True)
        raise

def main():
    """Main entry point for HTTP server"""
    port = int(os.environ.get("PORT", 8000))
    
    print(f"🚀 Starting Outscraper MCP HTTP Server on port {port}")
    print(f"🔗 Health check: http://0.0.0.0:{port}/health")
    print(f"🔗 MCP endpoint: http://0.0.0.0:{port}/mcp")
    
    try:
        uvicorn.run(
            app,  # Use the app object directly instead of string import
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        raise

if __name__ == "__main__":
    main() 