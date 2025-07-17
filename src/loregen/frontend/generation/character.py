import os
import gradio as gr
import numpy as np
import pandas as pd
from loregen_common import model_default_name
from langgraph_sdk import get_client
from dotenv import load_dotenv, find_dotenv
from loregen.frontend.common import get_secret

_ = load_dotenv(find_dotenv())

ENDPOINT_CHARACTER = os.environ['ENDPOINT_CHARACTER']
LANGCHAIN_API_KEY = os.environ['LANGCHAIN_API_KEY']
ENVIRONMENT = os.environ['ENVIRONMENT']


if ENVIRONMENT == "local":
    langchain_api_key = os.environ['LANGCHAIN_API_KEY']
else:
    langchain_secret_arn = os.environ['LANGCHAIN_API_KEY']
    langchain_api_key = get_secret(langchain_secret_arn)


async def generate_character_sheet(
    final_conditions: str,
    number_of_epochs: int = 5,
    model_id: str = model_default_name
):
    # check if we have everything we need
    if len(final_conditions) == 0:
        raise gr.Error("Please provide a final conditions for generating the world's history")

    client = get_client(url=ENDPOINT_CHARACTER, api_key=langchain_api_key)

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


async def randomize_sex_sexuality() -> tuple[str, str, str]:

    # biological sex distribution: 49%, 49%, 2%
    biological_sex_distribution = [0.49, 0.49, 0.02]
    biological_sex = np.random.choice(
        ["male", "female", "intersex"],
        p=biological_sex_distribution
    )

    # biological sex / gender identity alignment: 97%, 3%
    gender_identity_alignment_distribution = [0.97, 0.03]
    gender_identity_aligned = np.random.choice(
        [True, False],
        p=gender_identity_alignment_distribution
    )

    if not gender_identity_aligned or biological_sex == "intersex":
        gender_identity = np.random.choice(
            ["male", "female", "non-binary"]
        )
    else:
        gender_identity = biological_sex

    # sexuality distribution: 90%, 3%, 5%, 1%, 1%
    sexuality_distribution = [0.90, 0.03, 0.05, 0.01, 0.01]
    sexuality = np.random.choice(
        ["heterosexual", "homosexual", "bisexual", "pansexual", "asexual"],
        p=sexuality_distribution
    )

    return biological_sex, gender_identity, sexuality


async def randomize_hexaco_traits() -> tuple[int, int, int, int, int, int]:
    # distribution of hexaco traints is assumed to be normal/Gaussian
    hexaco_traits = np.random.normal(5.5, 2, 6)      # mean 5½, σ ≈ 2
    hexaco_traits = np.rint(hexaco_traits).astype(int).clip(1, 10)
    return tuple(hexaco_traits)


async def generate_family_systems_inheritance(
    history_city: pd.DataFrame,
    history_family: pd.DataFrame,
    biological_sex: str,
    gender_identity: str,
    sexuality: str,
    hexaco_honesty_humility: int,
    hexaco_emotionality: int,
    hexaco_extraversion: int,
    hexaco_agreeableness: int,
    hexaco_conscientiousness: int,
    hexaco_openness_to_experience: int,
    model_id: str = model_default_name
):
    
    # First let's generate a random number of entries between 1 and 4
    number_of_inheritance_components = np.random.randint(1, 5)

    client = get_client(url=ENDPOINT_CHARACTER, api_key=langchain_api_key)

    assistant_id = "family_systems_inheritance"
    new_thread = await client.threads.create()
    print(new_thread)

    input = {
        "history_city": history_city.to_dict(orient='records'),
        "history_family": history_family.to_dict(orient='records'),
        "biological_sex": biological_sex,
        "gender_identity": gender_identity,
        "sexuality": sexuality,
        "hexaco_honesty_humility": hexaco_honesty_humility,
        "hexaco_emotionality": hexaco_emotionality,
        "hexaco_extraversion": hexaco_extraversion,
        "hexaco_agreeableness": hexaco_agreeableness,
        "hexaco_conscientiousness": hexaco_conscientiousness,
        "hexaco_openness_to_experience": hexaco_openness_to_experience,
        "number_of_inheritance_components": number_of_inheritance_components
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
        if "inheritance_components" in event:
            inheritance_components = pd.DataFrame(event["inheritance_components"])
            yield inheritance_components
