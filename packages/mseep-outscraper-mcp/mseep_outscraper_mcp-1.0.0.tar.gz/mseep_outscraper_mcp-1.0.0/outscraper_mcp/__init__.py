"""
Outscraper MCP Server

This package provides tools for accessing Outscraper's Google Maps data extraction services.
It includes tools for searching Google Maps places and extracting reviews.
"""

from .server import mcp

__version__ = "1.0.0"
__all__ = ["mcp", "main"]

def main():
    """Main entry point for the MCP server"""
    mcp.run() 