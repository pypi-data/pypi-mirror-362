#!/usr/bin/env python3
"""
Main module for outscraper_mcp package
"""

import sys
import os

def main():
    """Main entry point - determine whether to run HTTP or stdio mode"""
    # Check if we're being called as server_http module
    if len(sys.argv) > 0 and 'server_http' in sys.argv[0]:
        from .server_http import main as http_main
        http_main()
    else:
        # Default to stdio mode for backward compatibility
        from .server import mcp
        mcp.run()

if __name__ == "__main__":
    main() 