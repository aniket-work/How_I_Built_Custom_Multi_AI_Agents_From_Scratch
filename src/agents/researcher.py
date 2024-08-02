import json
import os
from griptape.structures import Agent
from griptape.rules import Rule
from griptape.config import StructureConfig
from griptape.drivers import OllamaPromptDriver
from griptape.tools import WebScraper, TaskMemoryClient
from src.tools.search_tool import get_search_tool


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)


config = load_config()


def build_researcher():
    """Builds a Researcher Structure."""
    researcher_config = config['researcher']

    researcher = Agent(
        config=StructureConfig(
            prompt_driver=OllamaPromptDriver(
                model=config['ollama']['model'],
            ),
        ),
        id=researcher_config['id'],
        tools=[
            get_search_tool(),
            WebScraper(off_prompt=True),
            TaskMemoryClient(off_prompt=False),
        ],
        rules=[Rule(f"{rule['type']}: {rule['value']}") for rule in researcher_config['rules']],
    )
    return researcher