import json
from duckduckgo_search import DDGS
from griptape.artifacts import TextArtifact
from griptape.structures import Pipeline
from griptape.tasks import CodeExecutionTask
from griptape.drivers import LocalStructureRunDriver
from griptape.tools import StructureRunClient

def load_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

config = load_config()

def search_duckduckgo(task: CodeExecutionTask) -> TextArtifact:
    keywords = task.input.value
    results = DDGS().text(keywords, max_results=config['search_tool']['max_results'])
    return TextArtifact(results)

def build_search_pipeline() -> Pipeline:
    pipeline = Pipeline()
    pipeline.add_task(
        CodeExecutionTask(
            "{{ args[0] }}",
            run_fn=search_duckduckgo,
        ),
    )
    return pipeline

def get_search_tool():
    search_driver = LocalStructureRunDriver(structure_factory_fn=build_search_pipeline)
    return StructureRunClient(
        name="SearchTool",
        description="Search the web for information",
        driver=search_driver,
        off_prompt=True,
    )