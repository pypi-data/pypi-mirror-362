import asyncio
from typing import Any
from uuid import uuid4

import click
import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
    SendStreamingMessageRequest,
)
from mcp.server.fastmcp import FastMCP
from pydantic import Field

base_url = 'http://localhost:37070'
mcp = FastMCP(name="Host_Fault_Cause")
host_fault_agent_card : AgentCard = None


async def init_a2a_client() -> A2AClient:
    PUBLIC_AGENT_CARD_PATH = '/.well-known/agent.json'

    async with httpx.AsyncClient() as httpx_client:
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=base_url,
        )

        final_agent_card_to_use: AgentCard | None = None
        try:
            print(f'Attempting to fetch public agent card from: {base_url}{PUBLIC_AGENT_CARD_PATH}')
            _public_card = await resolver.get_agent_card()  # Fetches from default public path
            print('Successfully fetched public agent card:')
            print(_public_card.model_dump_json(indent=2, exclude_none=True))
            final_agent_card_to_use = _public_card
            print('\nUsing PUBLIC agent card for client initialization (default).')
        except Exception as e:
            print(f'Critical error fetching public agent card: {e}')
            raise RuntimeError(
                'Failed to fetch the public agent card. Cannot continue.'
            ) from e

        return final_agent_card_to_use

async def send_a2a_msg(content: str, isStreaming:bool) -> str:
    async with httpx.AsyncClient() as httpx_client:
        a2a_client = A2AClient(httpx_client=httpx_client, agent_card=host_fault_agent_card)
        print('A2AClient initialized.')

        result:str = ''
        send_message_payload: dict[str, Any] = {
            'message': {
                'role': 'user',
                'parts': [
                    {
                        'kind': 'text',
                        'text': content
                    }
                ],
                'messageId': uuid4().hex,
            },
        }
        request = SendMessageRequest(
            id=str(uuid4()), params=MessageSendParams(**send_message_payload)
        )

        if(isStreaming):
            streaming_request = SendStreamingMessageRequest(
                id=str(uuid4()), params=MessageSendParams(**send_message_payload)
            )

            stream_response = a2a_client.send_message_streaming(streaming_request)

            async for chunk in stream_response:
                result += chunk.model_dump(mode='json', exclude_none=True)
            print(f'send_message_streaming result: {result}')
        else:
            _response = await a2a_client.send_message(request)
            response = _response.model_dump(mode='json', exclude_none=True)
            result = response['result']['parts'][0]['text']
            print(f'send_message result: {result}')

    return result

# @mcp.tool()
# def getHostFaultCause(
#     faultCode: str = Field(description="Host Fault Code"),
# ) -> str:
#     """主机故障解决方案"""
#     print(f"getHostFaultCause, faultCode={faultCode}")
#     faultCause = ""
#     if (faultCode == 'F02'):
#         faultCause = "主机硬盘故障，是由于硬盘的磁道损坏导致，需要更换磁盘"
#     else:
#         faultCause = f"未知故障，故障代码{faultCode}"
#     return  faultCause

@mcp.tool()
def getHostFaultCause(
    faultCode: str = Field(description="Host Fault Code"),
) -> str:
    """主机故障解决方案"""
    print(f"getHostFaultCause, faultCode={faultCode}")
    result = asyncio.run(send_a2a_msg(faultCode, False))
    print(f"getHostFaultCause result={result}")
    return result

@click.command()
@click.option("--host", default="0.0.0.0", help="Host to listen on for SSE")
@click.option("--port", default=27070, help="Port to listen on for SSE")
def main(host: str, port: int):
    global host_fault_agent_card
    host_fault_agent_card = asyncio.run(init_a2a_client())
    #getHostFaultCause('F02')  # For test

    mcp.settings.host = host
    mcp.settings.port = port
    print(f"MCP Server {mcp.name} starting on {host}:{port} !")
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
