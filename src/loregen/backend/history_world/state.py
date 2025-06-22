from dataclasses import dataclass, field
from typing import Sequence
from typing_extensions import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from langgraph.managed import IsLastStep


@dataclass
class InputState:
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )
    final_conditions: str = field(default="")
    number_of_epochs: int = field(default=10)
    history_world: list[dict] = field(default_factory=list)


@dataclass
class State(InputState):
    is_last_step: IsLastStep = field(default=False)
