from dataclasses import dataclass, field
from typing import Sequence
import pandas as pd
from typing_extensions import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from langgraph.managed import IsLastStep


@dataclass
class InputState:
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )
    history_city: pd.DataFrame = field(default_factory=pd.DataFrame)
    history_country: pd.DataFrame = field(default_factory=pd.DataFrame)
    final_conditions: str = field(default="")
    number_of_generations: int = field(default=10)
    history_family: list[dict] = field(default_factory=list)


@dataclass
class State(InputState):
    is_last_step: IsLastStep = field(default=False)
