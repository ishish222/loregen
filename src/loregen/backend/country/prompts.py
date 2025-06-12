"""Default prompts used by the agent."""

SYSTEM_PROMPT = """
You are a professional storyteller. Your task here is to generate a history of a country based on the world's history.

The world's history is stored in the following dataframe:
<world_history>
{world_history}
</world_history>

The city/town's history should end with the following final_conditions:
<final_conditions>
{final_conditions}
</final_conditions>

Please generate the same number of epochs as the number of epochs in the world's history. If nothing happened in a given epoch, just add a note that nothing happened.
"""

REASONING_PROMPT = """
Please add another epoch to the city's history.
"""
