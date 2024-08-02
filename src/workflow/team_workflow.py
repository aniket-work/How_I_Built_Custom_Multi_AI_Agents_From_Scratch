import os
import json
from griptape.structures import Workflow
from griptape.tasks import StructureRunTask, PromptTask
from griptape.drivers import LocalStructureRunDriver
from src.agents.researcher import build_researcher
from src.agents.writer import build_writer

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

config = load_config()

def create_team_workflow(workflow_config):
    team = Workflow(config=workflow_config)

    research_task = team.add_task(
        StructureRunTask(
            (config['researcher']['task_prompt'],),
            id="research",
            driver=LocalStructureRunDriver(
                structure_factory_fn=build_researcher,
            ),
        ),
    )

    team_tasks = []
    for writer in config['writers']:
        team_tasks.append(
            StructureRunTask(
                (config['writer_task_prompt'],),
                driver=LocalStructureRunDriver(
                    structure_factory_fn=lambda w=writer: build_writer(
                        role=w["role"],
                        goal=w["goal"],
                        backstory=w["backstory"],
                    )
                ),
            )
        )

    end_task = team.add_task(
        PromptTask(
            config['end_task_prompt'],
        )
    )

    team.insert_tasks(research_task, team_tasks, end_task)
    return team