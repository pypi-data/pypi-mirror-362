#!/usr/bin/env python3
"""
Test the MCP server protocol directly
"""
import json
import subprocess
import sys
import os

def test_mcp_server():
    print("=== Testing MCP Server Protocol ===")
    
    # Test server initialization
    print("\n1. Testing server initialization...")
    
    # Create test messages
    init_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        }
    }
    
    # Test tools list
    tools_message = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    # Test calling a tool
    call_message = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "get_memory_context",
            "arguments": {}
        }
    }
    
    print("   Messages prepared for testing:")
    print(f"   - Initialize: {json.dumps(init_message, indent=2)}")
    print(f"   - List tools: {json.dumps(tools_message, indent=2)}")
    print(f"   - Call tool: {json.dumps(call_message, indent=2)}")
    
    print("\n2. To test manually, run:")
    print("   python mcp_server.py")
    print("   Then send these JSON messages via stdin")

if __name__ == "__main__":
    test_mcp_server()