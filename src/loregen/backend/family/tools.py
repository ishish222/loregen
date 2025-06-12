from langgraph.prebuilt import InjectedState
from typing import Annotated
from typing import Any, Callable, List
from loregen.backend.family.state import State


async def append_family_history(
    generation: str,
    description: str,
    state: Annotated[State, InjectedState],
) -> str:
    """
    Append a family history to the state.
    Arguments:
        generation: The generation of the history.
        description: The description of the history.
    """
    state.history.append({
        "generation": generation,
        "description": description,
    })

    return "success"

TOOLS: List[Callable[..., Any]] = [append_family_history]
