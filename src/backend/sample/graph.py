from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode



sample_graph = StateGraph(State, input=InputState, config_schema=Configuration)