import asyncio
import click

from mcp.client.session import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import StdioServerParameters, stdio_client

@click.command()
@click.option("--host", default="localhost", help="Host to listen on for SSE")
@click.option("--port", default=27070, help="Port to listen on for SSE")
def main(host: str, port: int):
    url = f"http://{host}:{port}/sse"
    async def run_sse(url):
        async with sse_client(url, sse_read_timeout=5) as streams:
            async with ClientSession(*streams) as session:
                await session.initialize()

                # list available tools
                response = await session.list_tools()
                tools = response.tools
                print("\n list_tools:", [(tool.name, tool.description) for tool in tools])

                # call the runmcp tool
                result = await session.call_tool("getHostFaultCause", {"faultCode": "02"})
                print('\n call_tool getHostFaultCause result:', result)

    asyncio.run(run_sse(url))


if __name__ == "__main__":
    main()
