from mcp.server.fastmcp import FastMCP

def main() -> None:
    mcp = FastMCP("MathTools")
    
    @mcp.tool(name="multiply")
    def multiply(a: int, b: int) -> int:
        """Multiply two integers and return the product"""
        return a * b
    
    # @mcp.resource("greeting://{name}")
    # def get_greeting(name: str) -> str:
    #     return f"Hello, {name}!"
    print("Registered tools:", mcp.list_tools())
    # 不需要 mcp.refresh_tools()
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()