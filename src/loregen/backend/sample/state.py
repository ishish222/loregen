from dataclasses import dataclass, field
from typing import Sequence
from typing_extensions import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from langgraph.managed import IsLastStep


@dataclass
class InputState:
    conditions: str = field(default="")
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )
    history: list[dict] = field(default_factory=list)


@dataclass
class State(InputState):
    is_last_step: IsLastStep = field(default=False)
