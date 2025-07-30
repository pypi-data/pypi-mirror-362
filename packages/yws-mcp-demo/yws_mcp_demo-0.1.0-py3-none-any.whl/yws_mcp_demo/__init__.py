# server.py
from mcp.server.fastmcp import FastMCP
import socket
import os   

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    token = os.getenv("token")
    if not token:
        raise ValueError(">>>>>>请设置环境变量token！！")
    print(f"获取到的Token为: {token}")
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

def main() -> None:
    print("mcp server started...")
    mcp.run(transport="stdio")
