from dataclasses import dataclass, field
from typing import Sequence
import pandas as pd
from typing_extensions import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from langgraph.managed import IsLastStep


@dataclass
class InputState:
    final_conditions: str = field(default="")
    family_history: pd.DataFrame = field(default_factory=pd.DataFrame)
    city_history: pd.DataFrame = field(default_factory=pd.DataFrame)
    number_of_chapters: int = field(default=10)
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )
    history: list[dict] = field(default_factory=list)


@dataclass
class State(InputState):
    is_last_step: IsLastStep = field(default=False)
