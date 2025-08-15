# test_client.py
import asyncio
import json
import subprocess
import sys
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession

async def test_mcp_server():
    """Test our EC2 MCP server"""
    
    # Configure server parameters
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["ec2_mcp_server.py"]
    )
    
    try:
        # Connect to the server using proper stdio client
        async with stdio_client(server_params) as (read_stream, write_stream):
            # Create client session
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize the session
                await session.initialize()
                
                print("✅ MCP Server connection established!")
                
                # Test 1: List available resources
                print("\n🔍 Testing resource listing...")
                try:
                    resources_result = await session.list_resources()
                    resources = resources_result.resources
                    print(f"Found {len(resources)} resources:")
                    for resource in resources[:3]:  # Show first 3
                        print(f"  - {resource.name}")
                except Exception as e:
                    print(f"Resource listing failed: {e}")
            
                # Test 2: List available tools
                print("\n🛠️  Testing tool listing...")
                try:
                    tools_result = await session.list_tools()
                    tools = tools_result.tools
                    print(f"Found {len(tools)} tools:")
                    for tool in tools:
                        print(f"  - {tool.name}: {tool.description}")
                except Exception as e:
                    print(f"Tool listing failed: {e}")
            
                # Test 3: Read a resource (if any exist)
                if 'resources' in locals() and resources:
                    print(f"\n📖 Testing resource reading...")
                    try:
                        resource_content = await session.read_resource(resources[0].uri)
                        # Handle the response properly
                        if hasattr(resource_content, 'contents'):
                            content = resource_content.contents[0].text if resource_content.contents else "No content"
                        else:
                            content = str(resource_content)
                        print(f"Resource content preview: {content[:200]}...")
                    except Exception as e:
                        print(f"Resource reading failed: {e}")
            
                # Test 4: Tool execution test
                print(f"\n⚡ Testing tool execution...")
                if 'tools' in locals() and tools:
                    print("Tool execution test skipped (requires real instance ID)")
                    print("To test with real instance, uncomment and modify:")
                    print('# result = await session.call_tool("get_instance_status", {"instance_id": "i-your-instance-id"})')
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
