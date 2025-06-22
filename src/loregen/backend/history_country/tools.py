from langgraph.prebuilt import InjectedState
from typing import Annotated
from typing import Any, Callable, List
from loregen.backend.history_country.state import State


async def append_country_history(
    epoch: str,
    description: str,
    state: Annotated[State, InjectedState],
) -> str:
    """
    Append a country history to the state.
    Arguments:
        epoch: The epoch of the country's history (string).
        description: The description of the country's history (string).
    """
    state.history.append({
        "epoch": epoch,
        "description": description,
    })

    return "success"

TOOLS: List[Callable[..., Any]] = [append_country_history]
