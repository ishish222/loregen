from langgraph.prebuilt import InjectedState
from typing import Annotated
from typing import Any, Callable, List
from loregen.backend.world.state import State


async def append_general_history(
    epoch: str,
    description: str,
    state: Annotated[State, InjectedState],
) -> str:
    """
    Append a general history to the state.
    Arguments:
        epoch: The epoch of the history.
        description: The description of the history.
    """
    state.history.append({
        "epoch": epoch,
        "description": description,
    })

    return "success"


async def append_grand_narrative(
    name: str,
    description: str,
    state: Annotated[State, InjectedState],
) -> str:
    """
    Append a grand narrative to the state. Grand narratives are the contemporary interpretations of what happened during the world's history to try to make sense of it. They can be religious, social, political, economic, cultural, filosophical, etc.
    Please remember, narratives are contemporary, so they need to interpret the history from perspective of the final epoch.
    Arguments:
        name: The name of the grand narrative.
        description: The description of the grand narrative.
    """
    state.grand_narratives.append({
        "name": name,
        "description": description,
    })

    return "success"


TOOLS: List[Callable[..., Any]] = [append_general_history]
TOOLS_NARRATIVES: List[Callable[..., Any]] = [append_grand_narrative]
