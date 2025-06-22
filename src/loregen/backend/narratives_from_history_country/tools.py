from langgraph.prebuilt import InjectedState
from typing import Annotated
from typing import Any, Callable, List
from loregen.backend.narratives_from_history_country.state import State


async def append_grand_narrative(
    name: str,
    description: str,
    state: Annotated[State, InjectedState],
) -> str:
    """
    Append a grand narrative to the state.

    Grand narratives are the contemporary interpretations of what happened during the country's history
    in order to try and make sense of it. They can be religious, social, political, economic, cultural,
    philosophical, etc.

    Please remember, narratives are contemporary, so they need to interpret the history from perspective
    of the final epoch.

    Examples of grand narratives related to the country (from the real world):
    - “Middle Kingdom”: For millennia China has envisioned itself as the civilized core around which lesser states revolve, blessed with a cosmic Mandate of Heaven. Modern PRC leaders recast the idea as “national rejuvenation,” urging unity behind centralized rule and global resurgence, while dissidents, Uyghurs, and Hong Kong democrats invoke the same mandate logic to argue Beijing has forfeited moral legitimacy.
    - “Guardians of the Revolution”: Post-1979 Iran positions itself as the vanguard of Islamic anti-imperial resistance, tasked with exporting a model of justice rooted in Shiʿa theology. Loyalists rally behind slogans of independence and martyrdom, while reformists, women’s-rights activists, and secular Persians rebel, framing the same revolutionary myth as a shield for authoritarianism and economic mismanagement.
    - “La Grande Nation”: France's self-image fuses Enlightenment universalism with republican virtue—Liberté, Égalité, Fraternité—claiming its revolutions and culture set humanity’s moral compass. Patriots celebrate laïcité, haute couture, and human-rights diplomacy; minority communities, post-colonial scholars, and yellow-vest protesters argue the grandeur conceals racism, empire, and social stratification.

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
