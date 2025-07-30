# server.py
import httpx
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("mcp-star-demo")

# 不是老说 AI 不会计算吗？那我们直接给 Ai 安排上加法功能，让 AI 再也不会算错了 hh
# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# 获取当前本地 ip 地址
@mcp.tool()
async def fetch_current_ip() -> str:
    """fetch current ip"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://ipinfo.io/ip")
        return response.text
