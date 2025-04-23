import gradio as gr
import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

ENVIRONMENT = os.environ['ENVIRONMENT']
APP_HOST = os.environ['APP_HOST']
APP_PORT = os.environ['APP_PORT']
COGNITO_DOMAIN = os.environ['COGNITO_DOMAIN']
CLIENT_ID = os.environ['COGNITO_DOMAIN_CLIENT_ID']
REDIRECT_URI_LOGIN = os.environ['COGNITO_DOMAIN_REDIRECT_URI_LOGIN']
REDIRECT_URI_LOGOUT = os.environ['COGNITO_DOMAIN_REDIRECT_URI_LOGOUT']
CODE_VERSION = os.environ['CODE_VERSION']


def generate_global_history(conditions):
    history_rows = []

    for i in range(10):
        history_rows.append({
            "epoch": i,
            "name": "test",
            "description": "test"
        })

    history_df = pd.DataFrame(history_rows)

    return history_df


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

    gh_button.click(fn=generate_global_history, inputs=[gh_conditions], outputs=[gh_output])