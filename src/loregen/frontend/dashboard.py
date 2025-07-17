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
from loregen.frontend.generation.character import (
    randomize_sex_sexuality,
    randomize_hexaco_traits,
    generate_family_systems_inheritance
)
from loregen_common import model_default_name, models
import boto3
import tempfile

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
            with gr.TabItem("Character sheet"):
                gh_conditions_character_sheet = gr.Textbox(label="Character's final conditions")
                gh_button_character_sheet = gr.Button("Generate")
                with gr.Accordion("Sex / sexuality", open=True):
                    with gr.Row():
                        gh_randomize_sex_sexuality_btn = gr.Button("Randomize")
                    with gr.Row():
                        with gr.Column():
                            # biological sex distribution: 49%, 49%, 2%
                            gh_output_character_sheet_biological_sex = gr.Dropdown(["male", "female", "intersex"], value="male", label="Character's biological sex", interactive=True)
                        with gr.Column():
                            # biological sex / gender identity alignment: 97%, 3%
                            gh_output_character_sheet_gender_identity = gr.Dropdown(["male", "female", "non-binary"], value="male", label="Character's gender identity", interactive=True)
                        with gr.Column():
                            # sexuality distribution: 90%, 3%, 5%, 1%, 1%
                            gh_output_character_sheet_sexuality = gr.Dropdown(["heterosexual", "homosexual", "bisexual", "pansexual", "asexual"], value="heterosexual", label="Character's sexuality", interactive=True)
                with gr.Accordion("Hexaco traits", open=True):
                    # distribution of hexaco traints is assumed to be normal/Gaussian (mean 0, std 1)
                    with gr.Row():
                        gh_randomize_hexaco_traits_btn = gr.Button("Randomize")
                    with gr.Row():
                        with gr.Column():
                            gh_output_character_sheet_hexaco_honesty_humility = gr.Number(label="Honesty-humility trait", value=5, minimum=1, maximum=10, interactive=True)
                        with gr.Column():
                            gh_output_character_sheet_hexaco_emotionality = gr.Number(label="Emotionality trait", value=5, minimum=1, maximum=10, interactive=True)
                        with gr.Column():
                            gh_output_character_sheet_hexaco_extraversion = gr.Number(label="Extraversion trait", value=5, minimum=1, maximum=10, interactive=True)
                    with gr.Row():
                        with gr.Column():
                            gh_output_character_sheet_hexaco_agreeableness = gr.Number(label="Agreeableness trait", value=5, minimum=1, maximum=10, interactive=True)
                        with gr.Column():
                            gh_output_character_sheet_hexaco_conscientiousness = gr.Number(label="Conscientiousness trait", value=5, minimum=1, maximum=10, interactive=True)
                        with gr.Column():
                            gh_output_character_sheet_hexaco_openness_to_experience = gr.Number(label="Openness to experience trait", value=5, minimum=1, maximum=10, interactive=True)
                with gr.Accordion("Environmental inheritance", open=True):
                    with gr.Row():
                        gh_output_character_sheet_family_systems_inheritance = gr.DataFrame(label="Character's family systems inheritance", wrap=True)
                    with gr.Row():
                        gh_output_character_sheet_family_systems_inheritance_btn = gr.Button("Generate family systems inheritance")
                    with gr.Row():
                        gh_output_character_sheet_grand_narratives = gr.DataFrame(label="Character's grand narratives", wrap=True)
                    with gr.Row():
                        gh_output_character_sheet_grand_narratives_btn = gr.Button("Generate grand narratives")
                    with gr.Row():
                        gh_output_character_sheet_pursued_identities = gr.DataFrame(label="Character's pursued identities", wrap=True)
                    with gr.Row():
                        gh_output_character_sheet_pursued_identities_btn = gr.Button("Generate pursued identities")
                    with gr.Row():
                        gh_output_character_sheet_avoided_identities = gr.DataFrame(label="Character's avoided identities", wrap=True)
                    with gr.Row():
                        gh_output_character_sheet_avoided_identities_btn = gr.Button("Generate avoided identities")
                    with gr.Row():
                        gh_output_character_sheet_values = gr.DataFrame(label="Character's values", wrap=True)
                    with gr.Row():
                        gh_output_character_sheet_values_btn = gr.Button("Generate values")
                    with gr.Row():
                        gh_output_character_sheet_behavioral_repertoire = gr.DataFrame(label="Character's behavioral repertoire", wrap=True)
                    with gr.Row():
                        gh_output_character_sheet_behavioral_repertoire_btn = gr.Button("Generate behavioral repertoire")
                    with gr.Row():
                        gh_output_character_sheet_language_and_vocabulary = gr.DataFrame(label="Character's language and vocabulary", wrap=True)
                    with gr.Row():
                        gh_output_character_sheet_language_and_vocabulary_btn = gr.Button("Generate language and vocabulary")

            with gr.TabItem("Character history"):
                gh_conditions_character = gr.Textbox(label="Character's final conditions (e.g. name, age, occupation, etc.)")
                gh_number_of_chapters = gr.Number(label="Number of chapters", value=5, maximum=10)
                gh_button_character = gr.Button("Generate")
                gh_output_history_character = gr.DataFrame(label="Character's history", wrap=True)

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

    gh_randomize_sex_sexuality_btn.click(
        fn=randomize_sex_sexuality,
        outputs=[
            gh_output_character_sheet_biological_sex,
            gh_output_character_sheet_gender_identity,
            gh_output_character_sheet_sexuality]
        )

    gh_randomize_hexaco_traits_btn.click(
        fn=randomize_hexaco_traits,
        outputs=[
            gh_output_character_sheet_hexaco_honesty_humility,
            gh_output_character_sheet_hexaco_emotionality,
            gh_output_character_sheet_hexaco_extraversion,
            gh_output_character_sheet_hexaco_agreeableness,
            gh_output_character_sheet_hexaco_conscientiousness,
            gh_output_character_sheet_hexaco_openness_to_experience]
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
        # Save to a uniquely named temporary file
        temp_file_obj = tempfile.NamedTemporaryFile(delete=False, prefix="loregen_", suffix=".save")
        save_state_to_file(state_json, temp_file_obj.name)
        return temp_file_obj.name

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

    gh_output_character_sheet_family_systems_inheritance_btn.click(
        fn=generate_family_systems_inheritance,
        inputs=[
            gh_output_history_city,
            gh_output_history_family,
            gh_output_character_sheet_biological_sex,
            gh_output_character_sheet_gender_identity,
            gh_output_character_sheet_sexuality,
            gh_output_character_sheet_hexaco_honesty_humility,
            gh_output_character_sheet_hexaco_emotionality,
            gh_output_character_sheet_hexaco_extraversion,
            gh_output_character_sheet_hexaco_agreeableness,
            gh_output_character_sheet_hexaco_conscientiousness,
            gh_output_character_sheet_hexaco_openness_to_experience
        ],
        outputs=[gh_output_character_sheet_family_systems_inheritance]
    )
