from __future__ import annotations

from dataclasses import dataclass, field, fields
from loregen.backend.narratives_from_history_city.prompts import SYSTEM_PROMPT
from typing import Annotated, Optional

from langchain_core.runnables import RunnableConfig, ensure_config


@dataclass(kw_only=True)
class Configuration:
    """Configuration for the sample agent"""

    system_prompt: str = field(
        default=SYSTEM_PROMPT,
        metadata={
            "description": "The system prompt to use for the agent's interactions. "
            "This should be a short description of the agent's role and capabilities."
        }
    )

    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="anthropic/claude-3-5-sonnet-20240620",
        metadata={
            "description": "The name of the language model to use for the agent's main interactions. "
            "Should be in the form: provider/model-name."
        },
    )

    @classmethod
    def from_runnable_config(
        cls,
        config: Optional[RunnableConfig] = None,
    ) -> Configuration:
        """Create a Configuration instance from a RunnableConfig object."""

        config = ensure_config(config)
        configurable = config.get("configurable") or {}
        _fields = {f.name for f in fields(cls) if f.init}
        return cls(**{k: v for k, v in configurable.items() if k in _fields})
