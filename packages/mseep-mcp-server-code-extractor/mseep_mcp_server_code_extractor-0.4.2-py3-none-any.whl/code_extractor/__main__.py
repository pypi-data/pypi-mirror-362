#!/usr/bin/env python3
"""
MCP Code Extractor - Main entry point

Entry point for running the MCP server as a module:
- python -m code_extractor
- uvx mcp-server-code-extractor
"""

from .server import main

if __name__ == "__main__":
    main()