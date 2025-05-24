import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

mcp=MultiServerMCPClient({
    "github":{
        "command":"python",
        "args":["./github.py"],
        "transport":"stdio",
    }
})

async def main():
    tools = await mcp.get_tools()
    print(tools)

asyncio.run(main())