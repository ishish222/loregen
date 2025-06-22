import os
import gradio as gr
import pandas as pd
from loregen.backend.common import model_default_name
from langgraph_sdk import get_client
from dotenv import load_dotenv, find_dotenv
from loregen.frontend.common import get_secret

_ = load_dotenv(find_dotenv())

ENDPOINT_HISTORY = os.environ['ENDPOINT_HISTORY']
LANGCHAIN_API_KEY = os.environ['LANGCHAIN_API_KEY']
ENVIRONMENT = os.environ['ENVIRONMENT']


if ENVIRONMENT == "local":
    langchain_api_key = os.environ['LANGCHAIN_API_KEY']
else:
    langchain_secret_arn = os.environ['LANGCHAIN_API_KEY']
    langchain_api_key = get_secret(langchain_secret_arn)


async def generate_history_world(
    final_conditions: str,
    number_of_epochs: int = 5,
    model_id: str = model_default_name
):
    # check if we have everything we need
    if len(final_conditions) == 0:
        raise gr.Error("Please provide a final conditions for generating the world's history")

    client = get_client(url=ENDPOINT_HISTORY, api_key=langchain_api_key)

    assistant_id = "history_world"
    new_thread = await client.threads.create()
    print(new_thread)

    input = {
        "final_conditions": final_conditions,
        "number_of_epochs": number_of_epochs
    }

    config = {
        "configurable": {
            "model": model_id
        }
    }

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        assistant_id,
        input=input,
        config=config,
        stream_mode="values"
    ):
        if "history_world" in event:
            history_world = pd.DataFrame(event["history_world"])
            yield history_world


async def generate_history_country(
    final_conditions: str,
    history_world: pd.DataFrame,
    model_id: str = model_default_name
):
    # check if we have everything we need
    if len(final_conditions) == 0:
        raise gr.Error("Please provide a final conditions for generating the country's history")
    if len(history_world) == 0:
        raise gr.Error("Please provide a history for the world")

    client = get_client(url=ENDPOINT_HISTORY, api_key=langchain_api_key)

    assistant_id = "history_country"
    new_thread = await client.threads.create()
    print(new_thread)

    # Convert DataFrame to dictionary
    history_world_dict = history_world.to_dict(orient='records')

    input = {
        "final_conditions": final_conditions,
        "history_world": history_world_dict
    }

    config = {
        "configurable": {
            "model": model_id
        }
    }

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        assistant_id,
        input=input,
        config=config,
        stream_mode="values"
    ):
        if "history_country" in event:
            history_country = pd.DataFrame(event["history_country"])
            yield history_country


async def generate_history_city(
    final_conditions: str,
    history_world: pd.DataFrame,
    history_country: pd.DataFrame,
    model_id: str = model_default_name
):
    # check if we have everything we need
    if len(final_conditions) == 0:
        raise gr.Error("Please provide a final conditions for generating the city's history")
    if len(history_world) == 0:
        raise gr.Error("Please provide a history for the world")
    if len(history_country) == 0:
        raise gr.Error("Please provide a history for the country")

    client = get_client(url=ENDPOINT_HISTORY, api_key=langchain_api_key)

    assistant_id = "history_city"
    new_thread = await client.threads.create()
    print(new_thread)

    # Convert DataFrames to dictionaries
    history_world_dict = history_world.to_dict(orient='records')
    history_country_dict = history_country.to_dict(orient='records')

    input = {
        "final_conditions": final_conditions,
        "history_world": history_world_dict,
        "history_country": history_country_dict
    }

    config = {
        "configurable": {
            "model": model_id
        }
    }

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        assistant_id,
        input=input,
        config=config,
        stream_mode="values"
    ):
        if "history_city" in event:
            history_city = pd.DataFrame(event["history_city"])
            yield history_city


async def generate_history_family(
    final_conditions: str,
    history_city: pd.DataFrame,
    history_country: pd.DataFrame,
    number_of_generations: int = 10,
    model_id: str = model_default_name
):
    # check if we have everything we need
    if len(final_conditions) == 0:
        raise gr.Error("Please provide a final conditions for generating the family's history")
    if len(history_city) == 0:
        raise gr.Error("Please provide a history for the city")
    if len(history_country) == 0:
        raise gr.Error("Please provide a history for the country")

    client = get_client(url=ENDPOINT_HISTORY, api_key=langchain_api_key)

    assistant_id = "history_family"
    new_thread = await client.threads.create()
    print(new_thread)

    # Convert DataFrames to dictionaries
    history_city_dict = history_city.to_dict(orient='records')
    history_country_dict = history_country.to_dict(orient='records')

    input = {
        "final_conditions": final_conditions,
        "history_city": history_city_dict,
        "history_country": history_country_dict,
        "number_of_generations": number_of_generations
    }

    config = {
        "configurable": {
            "model": model_id
        }
    }

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        assistant_id,
        input=input,
        config=config,
        stream_mode="values"
    ):
        if "history_family" in event:
            history_family = pd.DataFrame(event["history_family"])
            yield history_family


async def generate_history_character(
    final_conditions: str,
    history_family: pd.DataFrame,
    history_city: pd.DataFrame,
    number_of_chapters: int = 10,
    model_id: str = model_default_name
):
    # check if we have everything we need
    if len(final_conditions) == 0:
        raise gr.Error("Please provide a final conditions for generating the character's history")
    if len(history_family) == 0:
        raise gr.Error("Please provide a history for the family")
    if len(history_city) == 0:
        raise gr.Error("Please provide a history for the city")

    client = get_client(url=ENDPOINT_HISTORY, api_key=langchain_api_key)

    assistant_id = "history_character"
    new_thread = await client.threads.create()
    print(new_thread)

    # Convert DataFrames to dictionaries
    history_family_dict = history_family.to_dict(orient='records')
    history_city_dict = history_city.to_dict(orient='records')

    input = {
        "final_conditions": final_conditions,
        "history_family": history_family_dict,
        "history_city": history_city_dict,
        "number_of_chapters": number_of_chapters
    }

    config = {
        "configurable": {
            "model": model_id
        }
    }

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        assistant_id,
        input=input,
        config=config,
        stream_mode="values"
    ):
        if "history_character" in event:
            yield pd.DataFrame(event["history_character"])
