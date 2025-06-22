from langgraph.prebuilt import InjectedState
from typing import Annotated
from typing import Any, Callable, List
from loregen.backend.narratives_from_history_city.state import State


async def append_grand_narrative(
    name: str,
    description: str,
    state: Annotated[State, InjectedState],
) -> str:
    """
    Append a grand narrative to the state.

    Grand narratives are the contemporary interpretations of what happened during the city's history
    in order to try and make sense of it. They can be religious, social, political, economic, cultural,
    philosophical, etc.

    Please remember, narratives are contemporary, so they need to interpret the history from perspective
    of the final epoch.

    Examples of grand narratives related to the city (from the real world):
    - “The Promised Land”: Jerusalem is imagined as the earthly anchor of a divine covenant: Jews see it as the city promised by God to Israel; Christians revere it as the stage for Christ’s passion and resurrection; Muslims honor it as the Prophet’s ascension point. Believers fold this promise into their sense of destiny and moral geography, organizing pilgrimages, prayers, and political claims around it, while secularists, Palestinians under occupation, and some post-Zionist Israelis push back, challenging the narrative's exclusivity and its use to justify territorial control.
    - “The Eternal City”: Rome embodies the story that legitimate power, law, and universal faith radiate from a single seat that has never truly fallen—from the Caesars through the papacy to modern Italy. Catholics, classicists, and tourists absorb this continuity myth in marble and ritual, affirming Rome as an unbroken center of Western civilization, whereas anti-clerical Italians and scholars of empire critique it as selective memory that smooths over collapse, corruption, and fascism.
    - “City on a Hill”: Washington, D.C. embodies the American myth that the republic is a moral beacon whose institutions safeguard liberty for all. Patriots and many immigrants weave this into personal identity, touring the Mall as secular pilgrimage; critics—from Black Lives Matter activists to foreign observers—highlight slavery, empire, and partisanship as evidence the shining ideal is aspirational or hypocritical.

    Arguments:
        name: The name of the grand narrative.
        description: The description of the grand narrative.
    """
    state.grand_narratives.append({
        "name": name,
        "description": description,
    })

    return "success"


TOOLS: List[Callable[..., Any]] = [append_grand_narrative]
