import json
import pandas as pd
from typing import Dict, Any


def save_state(
    world_conditions: str,
    world_epochs: int,
    world_df: pd.DataFrame,
    country_conditions: str,
    country_df: pd.DataFrame,
    city_conditions: str,
    city_df: pd.DataFrame,
    family_conditions: str,
    family_generations: int,
    family_df: pd.DataFrame,
    character_conditions: str,
    character_chapters: int,
    character_df: pd.DataFrame,
) -> str:
    """Save the current state of all components to a file."""

    state = {
        "world": {
            "conditions": world_conditions,
            "epochs": world_epochs,
            "data": world_df.to_dict(orient='records') if not world_df.empty else []
        },
        "country": {
            "conditions": country_conditions,
            "data": country_df.to_dict(orient='records') if not country_df.empty else []
        },
        "city": {
            "conditions": city_conditions,
            "data": city_df.to_dict(orient='records') if not city_df.empty else []
        },
        "family": {
            "conditions": family_conditions,
            "generations": family_generations,
            "data": family_df.to_dict(orient='records') if not family_df.empty else []
        },
        "character": {
            "conditions": character_conditions,
            "chapters": character_chapters,
            "data": character_df.to_dict(orient='records') if not character_df.empty else []
        }
    }

    return json.dumps(state)


def load_state(state_json: str) -> Dict[str, Any]:
    """Load state from a JSON string and return a dictionary of components."""

    state = json.loads(state_json)

    return {
        "world_conditions": state["world"]["conditions"],
        "world_epochs": state["world"]["epochs"],
        "world_df": pd.DataFrame(state["world"]["data"]) if state["world"]["data"] else pd.DataFrame(),
        "country_conditions": state["country"]["conditions"],
        "country_df": pd.DataFrame(state["country"]["data"]) if state["country"]["data"] else pd.DataFrame(),
        "city_conditions": state["city"]["conditions"],
        "city_df": pd.DataFrame(state["city"]["data"]) if state["city"]["data"] else pd.DataFrame(),
        "family_conditions": state["family"]["conditions"],
        "family_generations": state["family"]["generations"],
        "family_df": pd.DataFrame(state["family"]["data"]) if state["family"]["data"] else pd.DataFrame(),
        "character_conditions": state["character"]["conditions"],
        "character_chapters": state["character"]["chapters"],
        "character_df": pd.DataFrame(state["character"]["data"]) if state["character"]["data"] else pd.DataFrame()
    }


def save_state_to_file(state_json: str, filename: str) -> None:
    """Save state to a .save file."""
    with open(filename, 'w') as f:
        f.write(state_json)


def load_state_from_file(filename: str) -> str:
    """Load state from a .save file."""
    with open(filename, 'r') as f:
        return f.read()
