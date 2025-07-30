import click
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from .hostfault_agent_executor import (
    HostFaultAgentExecutor,  # type: ignore[import-untyped]
)


@click.command()
@click.option("--host", default="0.0.0.0", help="Host to listen on for SSE")
@click.option("--port", default=37070, help="Port to listen on for SSE")
def main(host: str, port: int):
    base_url = f"http://{host}:{port}/"

    skill = AgentSkill(
        id='getHostFaultCause',
        name='getHostFaultCause',
        description='Get Host Fault Cause by Code',
        tags=[],
        examples=[],
    )

    public_agent_card = AgentCard(
        name='HostFaultAgent',
        description='Handle Host Fault Cause',
        url=base_url,
        version='1.0.0',
        defaultInputModes=['text'],
        defaultOutputModes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],  # Only the basic skill for the public card
        supportsAuthenticatedExtendedCard=False,
    )

    request_handler = DefaultRequestHandler(
        agent_executor=HostFaultAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=public_agent_card,
        http_handler=request_handler
    )

    uvicorn.run(server.build(), host=host, port=port)

if __name__ == '__main__':
    main()
