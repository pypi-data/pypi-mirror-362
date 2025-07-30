from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.services.llm_service import FunctionCallParams


def with_agent_id(handler, agent_id):
    """Return a wrapper that adds agent_id function call."""

    async def _wrapper(params: FunctionCallParams):
        params.arguments = dict(params.arguments)
        params.arguments["agent_id"] = agent_id
        return await handler(params)

    return _wrapper