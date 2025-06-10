from langgraph.prebuilt import InjectedState
from typing import Annotated
from typing import Any, Callable, List


async def append_general_history(
    epoch: str,
    description: str,
    state: Annotated[dict, InjectedState],
) -> str:
    """
    Append a general history to the state.
    Arguments:
        epoch: The epoch of the history.
        description: The description of the history.
    """
    state["history"].append({
        "epoch": epoch,
        "description": description,
    })

    return "success"

TOOLS: List[Callable[..., Any]] = [append_general_history]
