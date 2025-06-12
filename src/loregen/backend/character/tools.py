from langgraph.prebuilt import InjectedState
from typing import Annotated
from typing import Any, Callable, List
from loregen.backend.character.state import State


async def append_character_history(
    chapter: str,
    description: str,
    state: Annotated[State, InjectedState],
) -> str:
    """
    Append a character history to the state.
    Arguments:
        chapter: The chapter of the history.
        description: The description of the history.
    """
    state.history.append({
        "chapter": chapter,
        "description": description,
    })

    return "success"

TOOLS: List[Callable[..., Any]] = [append_character_history]
