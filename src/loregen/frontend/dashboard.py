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


async def generate_global_history(
    conditions: str,
    number_of_epochs: int = 5
):
    if ENVIRONMENT == "local":
        langchain_api_key = os.environ['LANGCHAIN_API_KEY']
    else:
        langchain_secret_arn = os.environ['LANGCHAIN_API_KEY']
        langchain_api_key = get_secret(langchain_secret_arn)

    client = get_client(url=ENDPOINT_HISTORY, api_key=langchain_api_key)

    assistant_id = "agent"
    new_thread = await client.threads.create()
    print(new_thread)

    input = {
        "conditions": conditions,
        "number_of_epochs": number_of_epochs
        }

    history_rows = []

    async for namespace, event in client.runs.stream(
        new_thread["thread_id"],
        assistant_id,
        input=input,
        stream_mode="values"
    ):
        if "history" in event:
            # new_row = {
            #     "epoch": 0,
            #     "name": "test",
            #     "description": json.dumps(event["history"])
            # }
            # history_rows.append(new_row)
            yield pd.DataFrame(event["history"])

    # history_rows.append(new_row)
    # yield pd.DataFrame(history_rows)

with gr.Blocks() as dashboard:
    with gr.Row():
        with gr.Column():
            account_label = gr.Label("account", label="Account")
        with gr.Column():
            logout_btn = gr.Button("Logout", link="/logout")
    with gr.Row():
        with gr.Tabs() as main_tabs:
            with gr.TabItem("Global history"):
                gh_conditions = gr.Textbox(label="Global history")
                gh_number_of_epochs = gr.Number(label="Number of epochs", value=5)
                gh_button = gr.Button("Generate")
                gh_output = gr.DataFrame(label="Global history")
            with gr.TabItem("Country history"):
                gr.DataFrame(label="Country history")
            with gr.TabItem("City history"):
                gr.DataFrame(label="City history")
            with gr.TabItem("Family history"):
                gr.DataFrame(label="Family history")
            with gr.TabItem("Character history"):
                gr.DataFrame(label="Character history")

    gh_button.click(fn=generate_global_history, inputs=[gh_conditions, gh_number_of_epochs], outputs=[gh_output])
