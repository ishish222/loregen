from __future__ import annotations

import os
import gradio as gr
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from loregen.frontend.state_manager import (
    save_state,
    load_state,
    save_state_to_file,
    load_state_from_file
)
from loregen.frontend.generation.history import (
    generate_history_world,
    generate_history_country,
    generate_history_city,
    generate_history_family,
    generate_history_character
)
from loregen.frontend.generation.narratives import (
    generate_narratives_from_history
)
from loregen_common import model_default_name, models

_ = load_dotenv(find_dotenv())

APP_HOST = os.environ['APP_HOST']
APP_PORT = os.environ['APP_PORT']
COGNITO_DOMAIN = os.environ['COGNITO_DOMAIN']
CLIENT_ID = os.environ['COGNITO_DOMAIN_CLIENT_ID']
REDIRECT_URI_LOGIN = os.environ['COGNITO_DOMAIN_REDIRECT_URI_LOGIN']
REDIRECT_URI_LOGOUT = os.environ['COGNITO_DOMAIN_REDIRECT_URI_LOGOUT']
CODE_VERSION = os.environ['CODE_VERSION']


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
                gh_output_history_world = gr.DataFrame(label="Global history", wrap=True)
            with gr.TabItem("Country history"):
                gh_conditions_country = gr.Textbox(label="Country's final conditions")
                gh_button_country = gr.Button("Generate")
                gh_output_history_country = gr.DataFrame(label="Country's history", wrap=True)
            with gr.TabItem("City history"):
                gh_conditions_city = gr.Textbox(label="City's final conditions")
                gh_button_city = gr.Button("Generate")
                gh_output_history_city = gr.DataFrame(label="City's history", wrap=True)
            with gr.TabItem("Family history"):
                gh_conditions_family = gr.Textbox(label="Family's final conditions")
                gh_number_of_generations = gr.Number(label="Number of generations", value=5, maximum=10)
                gh_button_family = gr.Button("Generate")
                gh_output_history_family = gr.DataFrame(label="Family's history", wrap=True)
            with gr.TabItem("Grand narratives"):
                gh_number_of_narratives_from_world = gr.Number(label="Number of narratives from world", value=2, maximum=10)
                gh_number_of_narratives_from_country = gr.Number(label="Number of narratives from country", value=2, maximum=10)
                gh_number_of_narratives_from_city = gr.Number(label="Number of narratives from city", value=2, maximum=10)
                gh_number_of_narratives_from_family = gr.Number(label="Number of narratives from family", value=2, maximum=10)
                gh_button_grand_narratives = gr.Button("Generate")
                gh_output_grand_narratives = gr.DataFrame(label="Grand narratives", wrap=True)
            with gr.TabItem("Character history"):
                gh_conditions_character = gr.Textbox(label="Character's final conditions")
                gh_number_of_chapters = gr.Number(label="Number of chapters", value=5, maximum=10)
                gh_button_character = gr.Button("Generate")
                gh_output_history_character = gr.DataFrame(label="Character's history", wrap=True)
            with gr.TabItem("Character sheet"):
                gh_conditions_character_sheet = gr.Textbox(label="Character's final conditions")
                gh_button_character_sheet = gr.Button("Generate")
                with gr.Group():
                    gh_output_character_sheet_primary_sex = gr.Dropdown(["male", "female"], value="male", label="Character's primary sex", interactive=True)
                    gh_output_character_sheet_brain_sex = gr.Dropdown(["male", "female"], value="male", label="Character's brain sex", interactive=True)
                    gh_output_character_sheet_sexuality = gr.Dropdown(["heterosexual", "homosexual"], value="heterosexual", label="Character's sexuality", interactive=True)
                    gh_output_character_sheet_hexaco_traits = gr.DataFrame(label="Character's HEXACO traits", wrap=True)
                with gr.Group():
                    gh_output_character_sheet_family_systems_inheritance = gr.DataFrame(label="Character's family systems inheritance", wrap=True)
                    gh_output_character_sheet_grand_narratives = gr.DataFrame(label="Character's grand narratives", wrap=True)
                    gh_output_character_sheet_pursued_identities = gr.DataFrame(label="Character's pursued identities", wrap=True)
                    gh_output_character_sheet_avoided_identities = gr.DataFrame(label="Character's avoided identities", wrap=True)
                    gh_output_character_sheet_values = gr.DataFrame(label="Character's values", wrap=True)
                    gh_output_character_sheet_behavioral_repertoire = gr.DataFrame(label="Character's behavioral repertoire", wrap=True)
                    gh_output_character_sheet_language_and_vocabulary = gr.DataFrame(label="Character's language and vocabulary", wrap=True)

    with gr.Row():
        with gr.Column():
            save_btn = gr.Button("Save State")
            save_file = gr.File(label="Download Save File", file_types=[".save"])
        with gr.Column():
            load_file = gr.File(label="Upload Save File", file_types=[".save"])
            load_btn = gr.Button("Load State")

    # Event handlers
    gh_button_world.click(
        fn=generate_history_world,
        inputs=[
            gh_conditions_world,
            gh_number_of_epochs,
            model_choice
            ],
        outputs=[gh_output_history_world]
        )

    gh_button_country.click(
        fn=generate_history_country,
        inputs=[
            gh_conditions_country,
            gh_output_history_world,
            model_choice
            ],
        outputs=[gh_output_history_country]
        )

    gh_button_city.click(
        fn=generate_history_city,
        inputs=[
            gh_conditions_city,
            gh_output_history_country,
            gh_output_history_world,
            model_choice
            ],
        outputs=[gh_output_history_city]
        )

    gh_button_family.click(
        fn=generate_history_family,
        inputs=[
            gh_conditions_family,
            gh_output_history_city,
            gh_output_history_country,
            gh_number_of_generations,
            model_choice
            ],
        outputs=[gh_output_history_family]
        )

    gh_button_grand_narratives.click(
        fn=generate_narratives_from_history,
        inputs=[
            gh_output_history_world,
            gh_output_history_country,
            gh_output_history_city,
            gh_output_history_family,
            gh_number_of_narratives_from_world,
            gh_number_of_narratives_from_country,
            gh_number_of_narratives_from_city,
            gh_number_of_narratives_from_family,
            model_choice
            ],
        outputs=[gh_output_grand_narratives]
        )

    gh_button_character.click(
        fn=generate_history_character,
        inputs=[gh_conditions_character,
                gh_output_history_family,
                gh_output_history_city,
                gh_number_of_chapters,
                model_choice
                ],
        outputs=[gh_output_history_character]
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
            gh_output_history_world,
            gh_conditions_country,
            gh_output_history_country,
            gh_conditions_city,
            gh_output_history_city,
            gh_conditions_family,
            gh_number_of_generations,
            gh_output_history_family,
            gh_conditions_character,
            gh_number_of_chapters,
            gh_output_history_character
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
            gh_output_history_world,
            gh_conditions_country,
            gh_output_history_country,
            gh_conditions_city,
            gh_output_history_city,
            gh_conditions_family,
            gh_number_of_generations,
            gh_output_history_family,
            gh_conditions_character,
            gh_number_of_chapters,
            gh_output_history_character
        ]
    )
