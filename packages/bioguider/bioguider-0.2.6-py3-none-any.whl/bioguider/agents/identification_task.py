
import os
import json
import logging
from enum import Enum
from typing import Callable
from pydantic import BaseModel, Field
from langchain_openai.chat_models.base import BaseChatOpenAI
from langchain.tools import Tool
from langgraph.graph import StateGraph, START, END

from bioguider.utils.constants import PrimaryLanguageEnum, ProjectTypeEnum
from bioguider.utils.file_utils import get_file_type
from bioguider.agents.agent_tools import (
    read_file_tool, 
    read_directory_tool, 
    summarize_file_tool,
)
from bioguider.agents.agent_utils import (
    read_directory,
)
from bioguider.agents.identification_execute_step import IdentificationExecuteStep
from bioguider.agents.identification_observe_step import IdentificationObserveStep
from bioguider.agents.identification_plan_step import IdentificationPlanStep
from bioguider.agents.identification_task_utils import IdentificationWorkflowState
from bioguider.agents.peo_common_step import PEOCommonStep
from bioguider.agents.prompt_utils import (
    IDENTIFICATION_GOAL_PROJECT_TYPE, 
    IDENTIFICATION_GOAL_PRIMARY_LANGUAGE,
    IDENTIFICATION_GOAL_META_DATA,
)
from bioguider.agents.python_ast_repl_tool import CustomPythonAstREPLTool
from bioguider.agents.agent_task import AgentTask
from bioguider.database.summarized_file_db import SummarizedFilesDb

logger = logging.getLogger(__name__)

META_DATA_FINAL_ANSWER_EXAMPLE = '{{"name": "repo name", ...}}'
PROJECT_TYPE_FINAL_ANSWER_EXAMPLE = '{{"project_type": "project type"}}'
PRIMARY_LANGUAGE_FINAL_ANSWER_EXAMPLE = '{{"primary_language": "primary language"}}'

class IdentificationPlanResult(BaseModel):
    """ Identification Plan Result """
    actions: list[dict] = Field(description="a list of action dictionary, e.g. [{'name': 'read_file', 'input': 'README.md'}, ...]")

IdentificationPlanResultJsonSchema = {
    "title": "identification_plan_result",
    "description": "plan result",
    "type": "object",
    "properties": {
        "actions": {
            "type": "array",
            "description": """a list of action dictionary, e.g. [{'name': 'read_file', 'input': 'README.md'}, ...]""",
            "title": "Actions",
            "items": {"type": "object"}
        },
    },
    "required": ["actions"],
}

class IdentificationTask(AgentTask):
    def __init__(
        self, 
        llm: BaseChatOpenAI,
        step_callback: Callable | None=None,
    ):
        super().__init__(llm=llm, step_callback=step_callback)
        self.repo_path: str | None = None
        self.gitignore_path: str | None = None
        self.repo_structure: str | None = None
        self.tools = []
        self.custom_tools = []
        self.steps: list[PEOCommonStep] = []

    def _initialize(self):        
        if not os.path.exists(self.repo_path):
            raise ValueError(f"Repository path {self.repo_path} does not exist.")
        files = read_directory(self.repo_path, os.path.join(self.repo_path, ".gitignore"))
        file_pairs = [(f, get_file_type(os.path.join(self.repo_path, f)).value) for f in files]
        self.repo_structure = ""
        for f, f_type in file_pairs:
            self.repo_structure += f"{f} - {f_type}\n"

        self.tools = [
            summarize_file_tool(
                llm=self.llm, 
                repo_path=self.repo_path, 
                output_callback=self._print_step,
                db=self.summary_file_db,
            ),
            read_directory_tool(repo_path=self.repo_path, gitignore_path=self.gitignore_path),
            read_file_tool(repo_path=self.repo_path),
        ]
        self.custom_tools = [Tool(
            name=tool.__class__.__name__,
            func=tool.run,
            description=tool.__class__.__doc__,
        ) for tool in self.tools]
        self.custom_tools.append(CustomPythonAstREPLTool())
        self.steps = [
            IdentificationPlanStep(
                llm=self.llm,
                repo_path=self.repo_path,
                repo_structure=self.repo_structure,
                gitignore_path=self.gitignore_path,
                custom_tools=self.custom_tools,
            ),
            IdentificationExecuteStep(
                llm=self.llm,
                repo_path=self.repo_path,
                repo_structure=self.repo_structure,
                gitignore_path=self.gitignore_path,
                custom_tools=self.custom_tools,
            ),
            IdentificationObserveStep(
                llm=self.llm,
                repo_path=self.repo_path,
                repo_structure=self.repo_structure,
                gitignore_path=self.gitignore_path,
                custom_tools=self.custom_tools,
            )
        ]
        
    
    def _compile(
        self, 
        repo_path: str,
        gitignore_path: str,
        **kwargs,
    ):
        self.repo_path = repo_path
        self.gitignore_path = gitignore_path
        self._initialize()
                
        def check_observation_step(state: IdentificationWorkflowState):
            if "final_answer" in state and state["final_answer"] is not None:
                return END
            return "plan_step"
        
        graph = StateGraph(IdentificationWorkflowState)
        graph.add_node("plan_step", self.steps[0].execute)
        graph.add_node("execute_step", self.steps[1].execute)
        graph.add_node("observe_step", self.steps[2].execute)
        graph.add_edge(START, "plan_step")
        graph.add_edge("plan_step", "execute_step")
        graph.add_edge("execute_step", "observe_step")
        graph.add_conditional_edges("observe_step", check_observation_step, {"plan_step", END})

        self.graph = graph.compile()
        
    def identify_project_type(self):
        s = self._go_graph({
            "goal": IDENTIFICATION_GOAL_PROJECT_TYPE,
            "final_answer_example": PROJECT_TYPE_FINAL_ANSWER_EXAMPLE,
        })
        proj_type = s["final_answer"] if "final_answer" in s else "unknown type"
        return self._parse_project_type(proj_type)
    
    def identify_primary_language(self):
        s = self._go_graph({
            "goal": IDENTIFICATION_GOAL_PRIMARY_LANGUAGE,
            "final_answer_example": PRIMARY_LANGUAGE_FINAL_ANSWER_EXAMPLE,
        })
        language = s["final_answer"] if "final_answer" in s else "unknown type"
        return self._parse_primary_language(language)
    
    def identify_meta_data(self):
        s = self._go_graph({
            "goal": IDENTIFICATION_GOAL_META_DATA,
            "final_answer_example": META_DATA_FINAL_ANSWER_EXAMPLE,
        })
        meta_data = s["final_answer"] if "final_answer" in s else "unknown type"
        return self._parse_meta_data(meta_data)
        
    
    def _parse_project_type(self, proj_type_obj: str) -> ProjectTypeEnum:
        try:
            json_obj = json.loads(proj_type_obj)
            proj_type = json_obj["project_type"]
        except Exception as e:
            logger.error(e)
            return ProjectTypeEnum.unknown
        proj_type = proj_type.strip()
        if proj_type == "application":
            return ProjectTypeEnum.application
        elif proj_type == "package":
            return ProjectTypeEnum.package
        elif proj_type == "pipeline":
            return ProjectTypeEnum.pipeline
        else:
            return ProjectTypeEnum.unknown
        
    def _parse_primary_language(self, language_obj: str) -> PrimaryLanguageEnum:
        try:
            json_obj = json.loads(language_obj)
            language = json_obj["primary_language"]
        except Exception as e:
            logger.error(e)
            return PrimaryLanguageEnum.unknown
        language = language.strip()
        if language == "python":
            return PrimaryLanguageEnum.python
        elif language == "R":
            return PrimaryLanguageEnum.R
        else:
            return PrimaryLanguageEnum.unknown
        
    def _parse_meta_data(self, meta_data_obj: str) -> dict:
        try:
            json_obj = json.loads(meta_data_obj)
            meta_data = json_obj
            return meta_data
        except Exception as e:
            logger.error(e)
            return {
                "name": "unknown",
                "description": "unknown",
                "license": "unknown",
                "owner": "unknown",
            }
