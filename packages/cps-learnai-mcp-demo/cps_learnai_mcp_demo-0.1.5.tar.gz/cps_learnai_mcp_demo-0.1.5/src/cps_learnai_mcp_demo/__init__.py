from mcp.server.fastmcp import FastMCP

def main() -> None:
    # 在main函数内部创建MCP实例
    mcp = FastMCP("Demo")
    
    # 注册减法工具
    @mcp.tool()
    def multiply(a: int, b: int) -> int:
        """multiply two numbers"""
        return a * b
    
    # 注册问候资源
    @mcp.resource("greeting://{name}")
    def get_greeting(name: str) -> str:
        """Get a personalized greeting"""
        return f"Hello, {name}!"
    
    # 启动MCP服务器
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()