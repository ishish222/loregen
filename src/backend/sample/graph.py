from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langchain_core.runnables import RunnableConfig
from typing import Dict, List, Literal, cast
from langchain_core.messages import AIMessage, HumanMessage

from sample.state import InputState, State
from sample.configuration import Configuration
from sample.tools import TOOLS
from sample.utils import load_chat_model


async def system(
    state: State,
    config: RunnableConfig,
) -> Dict[str, List[AIMessage]]:

    configuration = Configuration.from_runnable_config(config)

    conditions = state['conditions']
    number_of_epochs = state['number_of_epochs']

    system_message = configuration.system_prompt.format(
        conditions=conditions,
        number_of_epochs=number_of_epochs
    )

    return {
        "messages": system_message
    }


async def reasoning(
    state: State,
    config: RunnableConfig,
) -> Dict[str, List[AIMessage]]:

    configuration = Configuration.from_runnable_config(config)

    model = load_chat_model(configuration.model).bind_tools(TOOLS)

    reasoning_message = "Please add another epoch to the world."

    state['messages'].append(HumanMessage(content=reasoning_message))
    messages = state['messages']

    response = cast(
        AIMessage,
        await model.ainvoke(
            messages, config
        ),
    )

    state['messages'].append(response)

    # Handle the case when it's the last step and the model still wants to use a tool
    if state.is_last_step and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="Sorry, I could not find an answer to your question in the specified number of steps.",
                )
            ]
        }

    return {
        'messages': [response],
    }

builder = StateGraph(State, input=InputState, config_schema=Configuration)

builder.add_node(system)
builder.add_node(reasoning)
builder.add_node("tools", ToolNode(TOOLS))

builder.add_edge("__start__", "system")
builder.add_edge("system", "reasoning")


def route_model_output(state: State) -> Literal["__end__", "tools"]:
    """Determine the next node based on the model's output.

    This function checks if the model's last message contains tool calls.

    Args:
        state (State): The current state of the conversation.

    Returns:
        str: The name of the next node to call ("__end__" or "tools").
    """
    last_message = state.messages[-1]
    if not isinstance(last_message, AIMessage):
        raise ValueError(
            f"Expected AIMessage in output edges, but got {type(last_message).__name__}"
        )
    # If there is no tool call, then we finish
    if not last_message.tool_calls:
        return "__end__"
    # Otherwise we execute the requested actions
    return "tools"


builder.add_conditional_edges(
    "reasoning",
    # After reasoning finishes running, the next node(s) are scheduled
    # based on the output from route_model_output
    route_model_output,
)

builder.add_edge("tools", "reasoning")

graph = builder.compile(
    interrupt_before=[],  # Add node names here to update state before they're called
    interrupt_after=[],  # Add node names here to update state after they're called
)
graph.name = "Generate World Agent"  # This customizes the name in LangSmith
