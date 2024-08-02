from griptape.config import StructureConfig
from griptape.drivers import OllamaPromptDriver
from griptape.tools import Calculator
from griptape.structures import Agent


agent = Agent(
    config=StructureConfig(
        prompt_driver=OllamaPromptDriver(
            model="llama3",
        ),
    ),
    tools=[Calculator()],
)
agent.run("What is (192 + 12) ^ 4")