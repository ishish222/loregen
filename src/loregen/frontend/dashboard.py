import gradio as gr
import os
import pandas as pd
import boto3
import json
from dotenv import load_dotenv, find_dotenv
from langgraph_sdk import get_client
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
    number_of_epochs: int = 5
):

    client = get_client(url=ENDPOINT_HISTORY, api_key=langchain_api_key)

    assistant_id = "world"
    new_thread = await client.threads.create()
    print(new_thread)

    input = {
        "final_conditions": final_conditions,
        "number_of_epochs": number_of_epochs
        }

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        assistant_id,
        input=input,
        stream_mode="values"
    ):
        if "history" in event:
            yield pd.DataFrame(event["history"])


async def generate_country_history(
    final_conditions: str,
    world_history: pd.DataFrame
):
    client = get_client(url=ENDPOINT_HISTORY, api_key=langchain_api_key)

    assistant_id = "country"
    new_thread = await client.threads.create()
    print(new_thread)

    input = {
        "final_conditions": final_conditions,
        "world_history": world_history
    }

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        assistant_id,
        input=input,
        stream_mode="values"
    ):
        if "history" in event:
            yield pd.DataFrame(event["history"])


async def generate_city_history(
    final_conditions: str,
    world_history: pd.DataFrame,
    country_history: pd.DataFrame
):
    client = get_client(url=ENDPOINT_HISTORY, api_key=langchain_api_key)

    assistant_id = "city"
    new_thread = await client.threads.create()
    print(new_thread)

    input = {
        "final_conditions": final_conditions,
        "world_history": world_history,
        "country_history": country_history
    }

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        assistant_id,
        input=input,
        stream_mode="values"
    ):
        if "history" in event:
            yield pd.DataFrame(event["history"])


async def generate_family_history(
    final_conditions: str,
    city_history: pd.DataFrame,
    country_history: pd.DataFrame,
    number_of_generations: int = 10
):
    client = get_client(url=ENDPOINT_HISTORY, api_key=langchain_api_key)

    assistant_id = "family"
    new_thread = await client.threads.create()
    print(new_thread)

    input = {
        "final_conditions": final_conditions,
        "city_history": city_history,
        "country_history": country_history,
        "number_of_generations": number_of_generations
    }

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        assistant_id,
        input=input,
        stream_mode="values"
    ):
        if "history" in event:
            yield pd.DataFrame(event["history"])


async def generate_character_history(
    final_conditions: str,
    family_history: pd.DataFrame,
    city_history: pd.DataFrame,
    number_of_chapters: int = 10
):
    client = get_client(url=ENDPOINT_HISTORY, api_key=langchain_api_key)

    assistant_id = "character"  
    new_thread = await client.threads.create()
    print(new_thread)

    input = {
        "final_conditions": final_conditions,
        "family_history": family_history,
        "city_history": city_history,
        "number_of_chapters": number_of_chapters
    }

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        assistant_id,
        input=input,
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
        with gr.Tabs() as main_tabs:
            with gr.TabItem("Global history"):
                gh_conditions_world = gr.Textbox(label="Global history's final conditions")
                gh_number_of_epochs = gr.Number(label="Number of epochs", value=5)
                gh_button_world = gr.Button("Generate")
                gh_output_world = gr.DataFrame(label="Global history")
            with gr.TabItem("Country history"):
                gh_conditions_country = gr.Textbox(label="Country's final conditions")
                gh_button_country = gr.Button("Generate")
                gh_output_country = gr.DataFrame(label="Country's history")
            with gr.TabItem("City history"):
                gh_conditions_city = gr.Textbox(label="City's final conditions")
                gh_button_city = gr.Button("Generate")
                gh_output_city = gr.DataFrame(label="City's history")
            with gr.TabItem("Family history"):
                gh_conditions_family = gr.Textbox(label="Family's final conditions")
                gh_number_of_generations = gr.Number(label="Number of generations", value=10)
                gh_button_family = gr.Button("Generate")
                gh_output_family = gr.DataFrame(label="Family's history")
            with gr.TabItem("Character history"):
                gh_conditions_character = gr.Textbox(label="Character's final conditions")
                gh_number_of_chapters = gr.Number(label="Number of chapters", value=10)
                gh_button_character = gr.Button("Generate")
                gh_output_character = gr.DataFrame(label="Character's history")

    gh_button_world.click(fn=generate_global_history, inputs=[gh_conditions_world, gh_number_of_epochs], outputs=[gh_output_world])
    gh_button_country.click(fn=generate_country_history, inputs=[gh_conditions_country, gh_output_world], outputs=[gh_output_country])
    gh_button_city.click(fn=generate_city_history, inputs=[gh_conditions_city, gh_output_country, gh_output_world], outputs=[gh_output_city])
    gh_button_family.click(fn=generate_family_history, inputs=[gh_conditions_family, gh_output_city, gh_output_country, gh_number_of_generations], outputs=[gh_output_family])
    gh_button_character.click(fn=generate_character_history, inputs=[gh_conditions_character, gh_output_family, gh_output_city, gh_number_of_chapters], outputs=[gh_output_character])
