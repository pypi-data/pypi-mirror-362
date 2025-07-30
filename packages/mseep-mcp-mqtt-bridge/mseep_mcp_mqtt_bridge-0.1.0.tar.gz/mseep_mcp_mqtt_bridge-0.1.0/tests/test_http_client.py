#!/usr/bin/env python3
"""
Simple client to test the MQTT MCP server running with HTTP transport.
Make sure to start the server first with:
    python mqtt_mcp_server.py --transport streamable-http
"""

import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def test_mqtt_server():
    """Test the MQTT MCP server running on HTTP."""
    server_url = "http://127.0.0.1:8000/mcp"
    
    print(f"Connecting to MQTT MCP server at {server_url}...")
    print("💡 Make sure the server is running with: python mqtt_mcp_server.py --transport streamable-http")
    
    try:
        # Connect to the HTTP server
        async with sse_client(url=server_url) as streams:
            async with ClientSession(*streams) as session:
                # Initialize the session
                await session.initialize()
                print("✅ Connected to MQTT MCP server!")
                
                # List available tools
                tools_response = await session.list_tools()
                print(f"\n📋 Available tools:")
                for tool in tools_response.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # Test MQTT publish
                print(f"\n📤 Testing MQTT publish...")
                result = await session.call_tool("mqtt_publish", {
                    "topic": "test/topic",
                    "message": "Hello from MCP HTTP client!",
                    "qos": 0,
                    "retain": False
                })
                print(f"Publish result: {result.content[0].text}")
                
                # Test MQTT subscribe (this will wait for messages)
                print(f"\n📥 Testing MQTT subscribe...")
                print("Note: This will wait for messages on 'test/topic' for 5 seconds...")
                result = await session.call_tool("mqtt_subscribe", {
                    "topic": "test/topic",
                    "num_messages": 1,
                    "timeout": 5
                })
                
                # Parse the returned JSON string
                import json
                messages = json.loads(result.content[0].text)
                if messages:
                    print(f"Received {len(messages)} message(s):")
                    for msg in messages:
                        print(f"  Topic: {msg['topic']}, Payload: {msg['payload']}")
                else:
                    print("No messages received within timeout period")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure the MQTT MCP server is running with HTTP transport!")
        print("Run: python mqtt_mcp_server.py --transport streamable-http")

if __name__ == "__main__":
    asyncio.run(test_mqtt_server()) 