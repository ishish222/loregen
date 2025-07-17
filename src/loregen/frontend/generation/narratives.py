import os
import gradio as gr
import pandas as pd
from loregen_common import model_default_name
from langgraph_sdk import get_client
from dotenv import load_dotenv, find_dotenv
from loregen.frontend.common import get_secret

_ = load_dotenv(find_dotenv())

ENDPOINT_NARRATIVES = os.environ['ENDPOINT_NARRATIVES']
LANGCHAIN_API_KEY = os.environ['LANGCHAIN_API_KEY']
ENVIRONMENT = os.environ['ENVIRONMENT']


if ENVIRONMENT == "local":
    langchain_api_key = os.environ['LANGCHAIN_API_KEY']
else:
    langchain_secret_arn = os.environ['LANGCHAIN_API_KEY']
    langchain_api_key = get_secret(langchain_secret_arn)


async def generate_narratives_from_history(
    history_world: pd.DataFrame,
    history_country: pd.DataFrame,
    history_city: pd.DataFrame,
    history_family: pd.DataFrame,
    number_of_narratives_from_world: int,
    number_of_narratives_from_country: int,
    number_of_narratives_from_city: int,
    number_of_narratives_from_family: int,
    model_id: str = model_default_name
):
    # check if we have everything we need
    if len(history_world) == 0:
        raise gr.Error("Please provide a history for the world")
    if len(history_country) == 0:
        raise gr.Error("Please provide a history for the country")
    if len(history_city) == 0:
        raise gr.Error("Please provide a history for the city")
    if len(history_family) == 0:
        raise gr.Error("Please provide a history for the family")

    client = get_client(url=ENDPOINT_NARRATIVES, api_key=langchain_api_key)

    narratives_from_history_world = []
    narratives_from_history_country = []
    narratives_from_history_city = []
    narratives_from_history_family = []
    grand_narratives = []

    # Convert DataFrames to dictionaries
    history_world_dict = history_world.to_dict(orient='records')
    history_country_dict = history_country.to_dict(orient='records')
    history_city_dict = history_city.to_dict(orient='records')
    history_family_dict = history_family.to_dict(orient='records')

    config = {
        "configurable": {
            "model": model_id
        }
    }

    new_thread = await client.threads.create()
    print(new_thread)

    # Generate narratives from world history

    input = {
        "history_world": history_world_dict,
        "history_country": history_country_dict,
        "history_city": history_city_dict,
        "history_family": history_family_dict,
        "number_of_narratives_from_world": number_of_narratives_from_world,
        "number_of_narratives_from_country": number_of_narratives_from_country,
        "number_of_narratives_from_city": number_of_narratives_from_city,
        "number_of_narratives_from_family": number_of_narratives_from_family,
    }

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        "narratives_from_history_world",
        input=input,
        config=config,
        stream_mode="values"
    ):
        if "world_grand_narratives" in event:
            if len(event["world_grand_narratives"]) > 0:
                # grand_narratives.extend(event["grand_narratives"])
                grand_narratives.extend(event["world_grand_narratives"])
                yield pd.DataFrame(grand_narratives)

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        "narratives_from_history_country",
        input=input,
        config=config,
        stream_mode="values"
    ):
        if "country_grand_narratives" in event:
            if len(event["country_grand_narratives"]) > 0:
                # grand_narratives.extend(event["grand_narratives"])
                grand_narratives.extend(event["country_grand_narratives"])
                yield pd.DataFrame(grand_narratives)

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        "narratives_from_history_city",
        input=input,
        config=config,
        stream_mode="values"
    ):
        if "city_grand_narratives" in event:
            if len(event["city_grand_narratives"]) > 0:
                # grand_narratives.extend(event["grand_narratives"])
                grand_narratives.extend(event["city_grand_narratives"])
                yield pd.DataFrame(grand_narratives)

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        "narratives_from_history_family",
        input=input,
        config=config,
        stream_mode="values"
    ):
        if "family_grand_narratives" in event:
            if len(event["family_grand_narratives"]) > 0:
                # grand_narratives.extend(event["grand_narratives"])
                grand_narratives.extend(event["family_grand_narratives"])
                yield pd.DataFrame(grand_narratives)
