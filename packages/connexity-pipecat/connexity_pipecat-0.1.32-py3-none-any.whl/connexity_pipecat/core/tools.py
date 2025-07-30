from typing import Any

from pipecat_tools import ToolManager

tool_manager = ToolManager()


def register_custom_tools(handlers_dir, config_file):
    tool_manager.register_tools_from_directory(
        handlers_dir=handlers_dir,
        config_file=config_file
    )
    return tool_manager


def get_tool_manager():
    """
    Return the current global ToolManager instance, reflecting all registrations.
    """
    return tool_manager


def get_required_constants(aget_id: str, function_names):
    """Return unresolved constants for the supplied functions.

    Args:
        aget_id:
        function_names: Iterable of function names to inspect.

    Returns:
        Dict[str, List[str]]: A mapping where each key is a function name
        and the value is a sorted list of constant names that are still
        unset (``None``).
    """
    return tool_manager.get_required_constants(aget_id, function_names)


def get_all_set_constants(agent_id: str):
    """Return every constant that already has a value.

    Returns:
        Dict[str, Dict[str, object]]: Mapping of function names to a
        sub‑mapping of constant names and their current values.
    """
    return tool_manager.get_all_set_constants(agent_id)


def set_constants(agent_id: str | None = "default", tools: dict[str, dict[str, Any]] = None) -> ToolManager:
    """
    Merge constants from an in-memory `tools` dict.

    This dict should look like:

        {
          "end_call": {},
          "book_appointment": {
            "webhook_url": "https://…/webhook/tool/book_appointment",
            "timeout_seconds": 30,
          },
        }

    Args:
        agent_id:
        tools: mapping of function_name → { constant_name: value, … }.

    Returns:
        The singleton ToolManager, updated in place.
    """
    agent_id = agent_id or "default"
    tool_manager.set_constants(agent_id, tools)
    return tool_manager


