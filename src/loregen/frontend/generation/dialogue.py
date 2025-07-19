
import os
from gradio import ChatMessage
from langchain_core.messages import HumanMessage
from langgraph_sdk import get_client
from dotenv import load_dotenv, find_dotenv
from loregen_common import model_default_name
from loregen.frontend.common import get_secret
from typing import Sequence
from langchain_core.messages import AnyMessage

_ = load_dotenv(find_dotenv())

ENDPOINT_CHARACTER = os.environ['ENDPOINT_CHARACTER']
LANGCHAIN_API_KEY = os.environ['LANGCHAIN_API_KEY']
ENVIRONMENT = os.environ['ENVIRONMENT']

if ENVIRONMENT == "local":
    langchain_api_key = os.environ['LANGCHAIN_API_KEY']
else:
    langchain_secret_arn = os.environ['LANGCHAIN_API_KEY']
    langchain_api_key = get_secret(langchain_secret_arn)


def prepare_dialogue_agent(
):

    client = get_client(url=ENDPOINT_CHARACTER, api_key=langchain_api_key)
    return client


dialogue_agent = prepare_dialogue_agent()


async def generate_response(
    dialogue_history: list[ChatMessage],
    dialogue_input: str,
    model_id: str = model_default_name
):
    assistant_id = "dialogue"

    new_thread = await dialogue_agent.threads.create()

    user_message = ChatMessage(content=dialogue_input, role="user")
    all_dialogue = dialogue_history + [user_message]
    yield all_dialogue, ''

    input = {
        "dialogue": dialogue_history,
        "user_message": dialogue_input
    }

    config = {
        "configurable": {
            "model": model_id
        }
    }

    internal_dialogue = []
    external_dialogue = []

    response = ''
    async for namespace, event in dialogue_agent.runs.stream(
        new_thread["thread_id"],
        assistant_id,
        input=input,
        config=config,
        stream_mode="values"
    ):
        if "internal_dialogue" in event:
            internal_dialogue = event["internal_dialogue"]

        if "response" in event and len(event["response"]) > 0:
            response = event["response"][-1]

        all_dialogue = dialogue_history + [user_message] + [ChatMessage(content=response, role="assistant")]

        yield all_dialogue, ''
