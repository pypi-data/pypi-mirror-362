from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message


class HostFaultAgent:
    async def invoke(self, faultCode:str) -> str:
            print(f"getHostFaultCause, faultCode={faultCode}")
            faultCause = ""
            if (faultCode == 'F02'):
                faultCause = "主机硬盘故障，是由于硬盘的磁道损坏导致，需要更换磁盘"
            else:
                faultCause = f"未知故障，故障代码{faultCode}"
            return  faultCause


class HostFaultAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent = HostFaultAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        query = context.get_user_input()
        print(f"recv query: {query}")
        result = await self.agent.invoke(query)
        await event_queue.enqueue_event(new_agent_text_message(result))


    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')

