from mcp.server.fastmcp import FastMCP
import math

mcp = FastMCP("calculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def sqrt(x: float) -> float:
    return math.sqrt(x)

if __name__ == "__main__":
    print("  calculator MCP server starting…", flush=True)
    mcp.run(transport="stdio")