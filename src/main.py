import logging
import sys
import json
import os
from griptape.config import StructureConfig
from griptape.drivers import OllamaPromptDriver
from src.workflow.team_workflow import create_team_workflow

def load_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

def run_workflow():
    config = load_config()
    workflow_config = StructureConfig(
        prompt_driver=OllamaPromptDriver(
            model=config['ollama']['model'],
        ),
    )

    team = create_team_workflow(workflow_config)

    # Set up logging to write to a file
    log_file = 'workflow_output.log'
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filemode='w')  # 'w' mode overwrites the file each time

    # Redirect stdout to the log file
    original_stdout = sys.stdout
    with open(log_file, 'w') as f:
        sys.stdout = f
        result = team.run()
        sys.stdout = original_stdout

    return result, log_file

if __name__ == "__main__":
    run_workflow()
