from typing import Callable
from typing import Any
import asyncio
from .models import ChatCompletionRequest, ChatCompletionResponse


class LocalAgentExecutor:
    def __init__(
        self,
        agent_function: Callable[[Any], Any],
        input_adapter: Callable[[ChatCompletionRequest], Any],
        output_adapter: Callable[[Any], ChatCompletionResponse],
    ):
        self.agent_function = agent_function
        self.input_adapter = input_adapter
        self.output_adapter = output_adapter

    async def completions(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        # Adapt request into agent input
        agent_input = self.input_adapter(request)

        # If the agent function is async, await it
        if asyncio.iscoroutinefunction(self.agent_function):
            agent_output = await self.agent_function(agent_input)
        else:
            agent_output = self.agent_function(agent_input)

        # Convert agent output into expected response format
        return self.output_adapter(agent_output)
