from langgraph.prebuilt import InjectedState
from typing import Annotated
from typing import Any, Callable, List
from loregen.backend.narratives_from_history_world.state import State


async def append_grand_narrative(
    name: str,
    description: str,
    state: Annotated[State, InjectedState],
) -> str:
    """
    Append a grand narrative to the state.

    Grand narratives are the contemporary interpretations of what happened throughout the family's history
    in order to try and make sense of it. They can be religious, social, political, economic, cultural,
    philosophical, etc.

    Please remember, narratives are contemporary, so they need to interpret the history from perspective
    of the final epoch.

    Examples of grand narratives related to families (from the real world):

    - “The Crown Endures”: Britain’s royal family frames itself as an unbroken constitutional anchor that steadies the nation through war, decolonization, and cultural churn; televised weddings and coronations invite subjects to fold monarchy into personal identity and soft-power branding. Republicans, anti-colonial activists, and austerity critics push back, calling the pageantry a gilded veil over privilege and empire.
    - “Guardians of the Two Holy Mosques”: The Saʿudi dynasty weds Wahhābi zeal to petroleum wealth, claiming divine mandate to police Islamic purity while ushering modern megaprojects. Many Sunni Muslims accept the custodianship narrative and televised hajj crowds as proof of legitimacy; Shia minorities, feminist reformers, and pan-Islamist rivals cast it as absolutism fueled by oil and U.S. arms.
    - “Camelot Reborn”: From JFK’s New Frontier to the torch-lit funeral, the Kennedys project a myth of youthful meritocracy and noblesse oblige battling injustice. Admirers weave civil-rights speeches and moonshot swagger into the American dream, while critics cite dynastic entitlement, scandal, and Cold War brinkmanship to puncture the Camelot sheen.
    - “Dynasty of Freedom Struggle”: Beginning with Motilal and Jawaharlal Nehru and sanctified by Mahatma Gandhi’s martyrdom, this lineage presents itself as steward of secular democracy and social justice. Congress loyalists internalize the narrative through tricolor rallies and Indira’s “Garibi Hatao,” whereas Hindu nationalists, Dalit activists, and regional parties decry it as hereditary rule masking corruption and emergency-era repression.
    - “Bankers of Nations”: Across five branches spread from Frankfurt, the Rothschilds cultivated an aura of near-mythic financial alchemy, financing railways, wars, and art that reshaped the 19th-century West. Admirers cite philanthropy and innovation; antisemitic conspiracists weaponize the same legend, spinning it into shadow-government tropes that Jews themselves often battle.
    - “Sun of the Nation”: Kims Il-sung, Jong-il, and Jong-un forge a personality-cult tale of revolutionary blood that alone shields Koreans from foreign wolves. Indoctrinated citizens pledge filial devotion and reenact anti-Japanese guerrilla myths, while defectors and global observers brand the narrative a totalitarian fabrication propped up by famine and nuclear blackmail.
    - “The Last Tsars”: From Peter the Great’s westernizing grandeur to Nicholas II’s tragic downfall, Romanov lore paints a sacred autocracy guiding Mother Russia. Monarchists and nostalgia markets romanticize Fabergé eggs and Orthodox revival, whereas Soviet historiography and modern liberals spotlight serfdom, pogroms, and military debacles hidden beneath the imperial snow.

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
