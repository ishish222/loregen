from langgraph.prebuilt import InjectedState
from typing import Annotated
from typing import Any, Callable, List


async def append_general_history(
    epoch: str,
    name: str,
    description: str,
    state: Annotated[dict, InjectedState],
) -> str:
    state["history"].append({
        "epoch": epoch,
        "name": name,
        "description": description,
    })

    return "success"

TOOLS: List[Callable[..., Any]] = [append_general_history]
