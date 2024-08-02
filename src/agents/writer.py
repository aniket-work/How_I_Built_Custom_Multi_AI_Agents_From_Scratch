import json
from griptape.structures import Agent
from griptape.rules import Rule
from griptape.config import StructureConfig
from griptape.drivers import OllamaPromptDriver

def load_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

config = load_config()

def build_writer(role: str, goal: str, backstory: str):
    """Builds a Writer Structure."""
    writer = Agent(
        config=StructureConfig(
            prompt_driver=OllamaPromptDriver(
                model=config['ollama']['model'],
            ),
        ),
        id=role.lower().replace(" ", "_"),
        rules=[
            Rule(f"Position: {role}"),
            Rule(f"Objective: {goal}"),
            Rule(f"Backstory: {backstory}"),
            Rule("Desired Outcome: Full blog post of at least 4 paragraphs"),
        ],
    )
    return writer