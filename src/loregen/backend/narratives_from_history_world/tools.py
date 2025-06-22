from langgraph.prebuilt import InjectedState
from typing import Annotated
from typing import Any, Callable, List
from loregen.backend.narratives_from_history_family.state import State


async def append_grand_narrative(
    name: str,
    description: str,
    state: Annotated[State, InjectedState],
) -> str:
    """
    Append a grand narrative to the state.

    Grand narratives are the contemporary interpretations of what happened during the world's history
    in order to try and make sense of it. They can be religious, social, political, economic, cultural,
    philosophical, etc.

    Please remember, narratives are contemporary, so they need to interpret the history from perspective
    of the final epoch.

    Examples of grand narratives (from the real world):

    - “Scientific Empiricism”: The conviction that knowledge must be grounded in sensory evidence and reproducible experiment sits at the core of modern science, legitimizing technologies, medicines, and entire university systems; devotees trust peer review and data to arbitrate truth, while critics—from certain theologians to post-modern theorists—challenge its claim to objectivity, pointing to cultural bias, funding pressures, or the limits of measuring consciousness and meaning.
    - “Humanism”: Humanism tells a story in which human dignity, reason, and moral agency replace divine command as the yardstick of value—fueling Renaissance art, Enlightenment politics, and contemporary human-rights charters; secular liberals celebrate it as emancipation from superstition, whereas religious traditionalists and some eco-philosophers resist, warning that centering humans can erode sacred order or non-human life.
    - “Capitalism”: Capitalism frames free markets, private property, and profit motive as natural engines of innovation and personal freedom; entrepreneurs, consumers, and many governments weave this narrative into their identity and policy, while anti-globalization activists, socialist thinkers, and some religious leaders rebuke it for deepening inequality, commodifying human relations, and endangering the planet.
    - “Socialism”: Socialism proclaims that collective ownership of the means of production and egalitarian distribution will liberate workers from exploitation and build solidarity; trade-unionists and left parties internalize this ideal as moral imperative, yet libertarians, historical revisionists, and survivors of authoritarian regimes contest it as a utopian script that can slide into state coercion and economic stagnation.
    - “Buddhism”: Rooted in the Four Noble Truths, Buddhism offers a path to end suffering through mindfulness, ethical conduct, and insight into impermanence; millions practice meditation and compassion, embedding the dharma in daily life, while skeptics question karma and rebirth, and nationalist monks or modern psychologists selectively reinterpret the tradition to fit ethnic politics or secular therapy.
    - “Islam”: Islamic narrative centers on submission to one God and continuity of prophetic guidance culminating in the Qur'an, binding believers into a global umma through ritual, law, and social justice ideals; faithful Muslims orient identity around sharia and the Five Pillars, whereas secularists, ex-Muslims, and reformists debate patriarchal readings, political Islam, or pluralist reinterpretations.
    - “Nihilism”: Nihilism insists that ultimate meaning, morality, or purpose does not exist, a stance that can dissolve hierarchies and spur radical freedom; some artists and philosophers embrace the void to craft new values, while religious communities, therapists, and civic moralists see it as a corrosive force leading to despair, violence, or apathetic consumerism.

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
