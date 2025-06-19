from __future__ import annotations

import os
import gradio as gr
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from loregen.backend.common import models, model_default_name
from loregen.frontend.state_manager import save_state, load_state, save_state_to_file, load_state_from_file
from langgraph_sdk import get_client
import boto3

_ = load_dotenv(find_dotenv())

ENVIRONMENT = os.environ['ENVIRONMENT']
APP_HOST = os.environ['APP_HOST']
APP_PORT = os.environ['APP_PORT']
COGNITO_DOMAIN = os.environ['COGNITO_DOMAIN']
CLIENT_ID = os.environ['COGNITO_DOMAIN_CLIENT_ID']
REDIRECT_URI_LOGIN = os.environ['COGNITO_DOMAIN_REDIRECT_URI_LOGIN']
REDIRECT_URI_LOGOUT = os.environ['COGNITO_DOMAIN_REDIRECT_URI_LOGOUT']
CODE_VERSION = os.environ['CODE_VERSION']
ENDPOINT_HISTORY = os.environ['ENDPOINT_HISTORY']


def get_secret(secret_arn):
    secrets_client = boto3.client('secretsmanager')
    response = secrets_client.get_secret_value(SecretId=secret_arn)
    return response['SecretString']


if ENVIRONMENT == "local":
    langchain_api_key = os.environ['LANGCHAIN_API_KEY']
else:
    langchain_secret_arn = os.environ['LANGCHAIN_API_KEY']
    langchain_api_key = get_secret(langchain_secret_arn)


async def generate_global_history(
    final_conditions: str,
    number_of_epochs: int = 5,
    grand_narratives: pd.DataFrame = None,
    model_id: str = model_default_name
):
    client = get_client(url=ENDPOINT_HISTORY, api_key=langchain_api_key)

    assistant_id = "world"
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

    if grand_narratives is None:
        grand_narratives = []
    else:
        grand_narratives = grand_narratives.to_dict(orient='records')

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        assistant_id,
        input=input,
        config=config,
        stream_mode="values"
    ):
        if "history" in event:
            history = pd.DataFrame(event["history"])
            if "grand_narratives" in event:
                grand_narratives = event["grand_narratives"]

            grand_narratives_df = pd.DataFrame(grand_narratives)
            yield history, grand_narratives_df


async def generate_country_history(
    final_conditions: str,
    world_history: pd.DataFrame,
    grand_narratives: pd.DataFrame = None,
    model_id: str = model_default_name
):
    client = get_client(url=ENDPOINT_HISTORY, api_key=langchain_api_key)

    assistant_id = "country"
    new_thread = await client.threads.create()
    print(new_thread)

    # Convert DataFrame to dictionary
    world_history_dict = world_history.to_dict(orient='records')

    input = {
        "final_conditions": final_conditions,
        "world_history": world_history_dict
    }

    config = {
        "configurable": {
            "model": model_id
        }
    }

    if grand_narratives is None:
        grand_narratives = []
    else:
        grand_narratives = grand_narratives.to_dict(orient='records')

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        assistant_id,
        input=input,
        config=config,
        stream_mode="values"
    ):
        if "history" in event:
            history = pd.DataFrame(event["history"])
            if "grand_narratives" in event:
                grand_narratives = event["grand_narratives"]

            grand_narratives_df = pd.DataFrame(grand_narratives)
            yield history, grand_narratives_df


async def generate_city_history(
    final_conditions: str,
    world_history: pd.DataFrame,
    country_history: pd.DataFrame,
    grand_narratives: pd.DataFrame = None,
    model_id: str = model_default_name
):
    client = get_client(url=ENDPOINT_HISTORY, api_key=langchain_api_key)

    assistant_id = "city"
    new_thread = await client.threads.create()
    print(new_thread)

    # Convert DataFrames to dictionaries
    world_history_dict = world_history.to_dict(orient='records')
    country_history_dict = country_history.to_dict(orient='records')

    input = {
        "final_conditions": final_conditions,
        "world_history": world_history_dict,
        "country_history": country_history_dict
    }

    config = {
        "configurable": {
            "model": model_id
        }
    }

    if grand_narratives is None:
        grand_narratives = []
    else:
        grand_narratives = grand_narratives.to_dict(orient='records')

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        assistant_id,
        input=input,
        config=config,
        stream_mode="values"
    ):
        if "history" in event:
            history = pd.DataFrame(event["history"])
            if "grand_narratives" in event:
                grand_narratives = event["grand_narratives"]

            grand_narratives_df = pd.DataFrame(grand_narratives)
            yield history, grand_narratives_df


async def generate_family_history(
    final_conditions: str,
    city_history: pd.DataFrame,
    country_history: pd.DataFrame,
    number_of_generations: int = 10,
    grand_narratives: pd.DataFrame = None,
    model_id: str = model_default_name
):
    client = get_client(url=ENDPOINT_HISTORY, api_key=langchain_api_key)

    assistant_id = "family"
    new_thread = await client.threads.create()
    print(new_thread)

    # Convert DataFrames to dictionaries
    city_history_dict = city_history.to_dict(orient='records')
    country_history_dict = country_history.to_dict(orient='records')

    input = {
        "final_conditions": final_conditions,
        "city_history": city_history_dict,
        "country_history": country_history_dict,
        "number_of_generations": number_of_generations
    }

    config = {
        "configurable": {
            "model": model_id
        }
    }

    if grand_narratives is None:
        grand_narratives = []
    else:
        grand_narratives = grand_narratives.to_dict(orient='records')

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        assistant_id,
        input=input,
        config=config,
        stream_mode="values"
    ):
        if "history" in event:
            history = pd.DataFrame(event["history"])
            if "grand_narratives" in event:
                grand_narratives = event["grand_narratives"]

            grand_narratives_df = pd.DataFrame(grand_narratives)
            yield history, grand_narratives_df


async def generate_character_history(
    final_conditions: str,
    family_history: pd.DataFrame,
    city_history: pd.DataFrame,
    number_of_chapters: int = 10,
    model_id: str = model_default_name
):
    client = get_client(url=ENDPOINT_HISTORY, api_key=langchain_api_key)

    assistant_id = "character"  
    new_thread = await client.threads.create()
    print(new_thread)

    # Convert DataFrames to dictionaries
    family_history_dict = family_history.to_dict(orient='records')
    city_history_dict = city_history.to_dict(orient='records')

    input = {
        "final_conditions": final_conditions,
        "family_history": family_history_dict,
        "city_history": city_history_dict,
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
        if "history" in event:
            yield pd.DataFrame(event["history"])


with gr.Blocks() as dashboard:
    with gr.Row():
        with gr.Column():
            account_label = gr.Label("account", label="Account")
        with gr.Column():
            logout_btn = gr.Button("Logout", link="/logout")
    with gr.Row():
        with gr.Accordion("Configuration", open=False):
            with gr.Row():
                model_choice = gr.Dropdown(
                    models.keys(),
                    value=model_default_name,
                    label='model',
                    interactive=True
                    )

    with gr.Row():
        with gr.Tabs() as main_tabs:
            with gr.TabItem("Global history"):
                gh_conditions_world = gr.Textbox(label="Global history's final conditions")
                gh_number_of_epochs = gr.Number(label="Number of epochs", value=5, maximum=10)
                gh_button_world = gr.Button("Generate")
                gh_output_world = gr.DataFrame(label="Global history", wrap=True)
            with gr.TabItem("Country history"):
                gh_conditions_country = gr.Textbox(label="Country's final conditions")
                gh_button_country = gr.Button("Generate")
                gh_output_country = gr.DataFrame(label="Country's history", wrap=True)
            with gr.TabItem("City history"):
                gh_conditions_city = gr.Textbox(label="City's final conditions")
                gh_button_city = gr.Button("Generate")
                gh_output_city = gr.DataFrame(label="City's history", wrap=True)
            with gr.TabItem("Family history"):
                gh_conditions_family = gr.Textbox(label="Family's final conditions")
                gh_number_of_generations = gr.Number(label="Number of generations", value=5, maximum=10)
                gh_button_family = gr.Button("Generate")
                gh_output_family = gr.DataFrame(label="Family's history", wrap=True)
            with gr.TabItem("Grand narratives"):
                gh_button_grand_narratives = gr.Button("Generate")
                gh_output_grand_narratives = gr.DataFrame(label="Grand narratives", wrap=True)
            with gr.TabItem("Character history"):
                gh_conditions_character = gr.Textbox(label="Character's final conditions")
                gh_number_of_chapters = gr.Number(label="Number of chapters", value=5, maximum=10)
                gh_button_character = gr.Button("Generate")
                gh_output_character = gr.DataFrame(label="Character's history", wrap=True)
    with gr.Row():
        with gr.Column():
            save_btn = gr.Button("Save State")
            save_file = gr.File(label="Download Save File", file_types=[".save"])
        with gr.Column():
            load_file = gr.File(label="Upload Save File", file_types=[".save"])
            load_btn = gr.Button("Load State")

    # Event handlers
    gh_button_world.click(
        fn=generate_global_history,
        inputs=[gh_conditions_world, gh_number_of_epochs, gh_output_grand_narratives, model_choice],
        outputs=[gh_output_world, gh_output_grand_narratives]
        )

    gh_button_country.click(
        fn=generate_country_history,
        inputs=[gh_conditions_country, gh_output_world, gh_output_grand_narratives, model_choice],
        outputs=[gh_output_country, gh_output_grand_narratives]
        )

    gh_button_city.click(
        fn=generate_city_history,
        inputs=[gh_conditions_city, gh_output_country, gh_output_world, gh_output_grand_narratives, model_choice],
        outputs=[gh_output_city, gh_output_grand_narratives]
        )

    gh_button_family.click(
        fn=generate_family_history,
        inputs=[gh_conditions_family, gh_output_city, gh_output_country, gh_number_of_generations, gh_output_grand_narratives, model_choice],
        outputs=[gh_output_family, gh_output_grand_narratives]
        )

    # for now, let's leave grand narratives as RO

    gh_button_character.click(
        fn=generate_character_history,
        inputs=[gh_conditions_character, gh_output_family, gh_output_city, gh_number_of_chapters, model_choice],
        outputs=[gh_output_character, gh_output_grand_narratives]
        )

    # Save/Load handlers
    def save_state_handler(
        world_conditions: str,
        world_epochs: int,
        world_df: pd.DataFrame,
        country_conditions: str,
        country_df: pd.DataFrame,
        city_conditions: str,
        city_df: pd.DataFrame,
        family_conditions: str,
        family_generations: int,
        family_df: pd.DataFrame,
        grand_narratives: pd.DataFrame,
        character_conditions: str,
        character_chapters: int,
        character_df: pd.DataFrame,
    ) -> str:
        state_json = save_state(
            world_conditions,
            world_epochs,
            world_df,
            country_conditions,
            country_df,
            city_conditions,
            city_df,
            family_conditions,
            family_generations,
            family_df,
            grand_narratives,
            character_conditions,
            character_chapters,
            character_df
        )
        # Save to a temporary file
        temp_file = "temp_state.save"
        save_state_to_file(state_json, temp_file)
        return temp_file

    save_btn.click(
        fn=save_state_handler,
        inputs=[
            gh_conditions_world,
            gh_number_of_epochs,
            gh_output_world,
            gh_conditions_country,
            gh_output_country,
            gh_conditions_city,
            gh_output_city,
            gh_conditions_family,
            gh_number_of_generations,
            gh_output_family,
            gh_output_grand_narratives,
            gh_conditions_character,
            gh_number_of_chapters,
            gh_output_character
        ],
        outputs=[save_file]
    )

    def load_state_handler(file_obj):
        if file_obj is None:
            return None
        state_json = load_state_from_file(file_obj.name)
        state = load_state(state_json)
        return [
            state["world_conditions"],
            state["world_epochs"],
            state["world_df"],
            state["country_conditions"],
            state["country_df"],
            state["city_conditions"],
            state["city_df"],
            state["family_conditions"],
            state["family_generations"],
            state["family_df"],
            state["grand_narratives"],
            state["character_conditions"],
            state["character_chapters"],
            state["character_df"]
        ]

    load_btn.click(
        fn=load_state_handler,
        inputs=[load_file],
        outputs=[
            gh_conditions_world,
            gh_number_of_epochs,
            gh_output_world,
            gh_conditions_country,
            gh_output_country,
            gh_conditions_city,
            gh_output_city,
            gh_conditions_family,
            gh_number_of_generations,
            gh_output_family,
            gh_output_grand_narratives,
            gh_conditions_character,
            gh_number_of_chapters,
            gh_output_character
        ]
    )
