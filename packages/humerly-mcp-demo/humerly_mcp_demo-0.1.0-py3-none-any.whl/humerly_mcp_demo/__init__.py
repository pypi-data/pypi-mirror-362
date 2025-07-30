
from mcp.server.fastmcp import FastMCP #FastMCP 是一个框架类，用于快速构建 MCP 服务器

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool() # 注册了一个名为 add 的工具
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource,只是请求数据,不会产生副作用,提供一种通过特定 URI 格式访问数据的方式
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."

def main() -> None:
    mcp.run(transport='stdio') 
