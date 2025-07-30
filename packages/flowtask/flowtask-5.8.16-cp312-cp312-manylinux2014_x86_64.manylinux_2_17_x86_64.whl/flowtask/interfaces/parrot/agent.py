"""
Create a Parrot AI Agent for FlowTask.
"""
from abc import abstractmethod
from typing import Any, Dict, Optional, List, Union
import textwrap
from pathlib import Path
from datetime import datetime
import aiofiles
from langchain_core.tools import BaseTool
from datamodel import BaseModel, Field
from datamodel.parsers.json import json_decoder, json_encoder  # noqa  pylint: disable=E0611
from asyncdb import AsyncDB  # noqa  pylint: disable=E0611
from navconfig import config
from navconfig.logging import logging
from querysource.conf import default_dsn
# Parrot:
from parrot.llms.openai import OpenAILLM
from parrot.bots.agent import BasicAgent


class AgentAnswer(BaseModel):
    """
    AgentAnswer is a model that defines the structure of the response
    for Any Parrot agent.
    """
    user_id: str = Field(..., description="Unique identifier for the user")
    agent_name: str = Field(required=False, description="Name of the agent that processed the request")
    status: str = Field(default="success", description="Status of the agent response")
    # The data field is the main content returned by the agent:
    data: str = Field(..., description="Data returned by the agent")
    output: str = Field(required=False)
    transcript: str = Field(default=None, description="Transcript of the conversation with the agent")
    attributes: Dict[str, str] = Field(default_factory=dict, description="Attributes associated with the response")
    created_at: datetime = Field(default=datetime.now)
    podcast_path: str = Field(required=False, description="Path to the podcast associated with the session")
    pdf_path: str = Field(required=False, description="Path to the PDF associated with the session")
    document_path: str = Field(required=False, description="Path to document generated during session")
    documents: List[str] = Field(default_factory=list, description="List of documents associated with the session")


class AgentBase:
    """AgentBase.

    Interface for creating new Parrot AI Agents to be used directly as Flowtask Components.

    """
    _agent_name: str = 'ParrotAgent'
    agent_id: str = 'default_agent'
    _backstory: Optional[str] = None
    _response: BaseModel = AgentAnswer

    def __init__(self, *args, **kwargs):
        self._agent_name: str = kwargs.get('agent_name', self._agent_name)
        self.agent_id: str = kwargs.get('agent_id', self.agent_id)
        self.backstory: Optional[str] = kwargs.get('backstory_file', "backstory.txt")
        self._backstory: str = kwargs.get('backstory', None)
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self._use_taskstorage = kwargs.get('use_taskstorage', False)
        # Agent Configuration:
        self._agent: Optional[BasicAgent] = None
        self._llm: Optional[OpenAILLM] = kwargs.get('llm', None)
        self._tools: List[BaseTool] = []
        self._config: Dict[str, Any] = kwargs.get('config', {})
        super(AgentBase, self).__init__(*args, **kwargs)

    @abstractmethod
    def _define_tools(self, base_dir: Path) -> List[BaseTool]:
        """Define the tools for the agent."""
        raise NotImplementedError("Subclasses must implement _define_tools method.")

    def db_connection(
        self,
        driver: str = 'pg',
        dsn: str = None,
        credentials: dict = None
    ) -> AsyncDB:
        """Return a database connection."""
        if not dsn:
            dsn = config.get(f'{driver.upper()}_DSN', fallback=default_dsn)
        if not dsn and credentials:
            dsn = credentials.get('dsn', default_dsn)
        if not dsn:
            raise ValueError(
                f"DSN for {driver} is not provided."
            )
        return AsyncDB(driver, dsn=dsn, credentials=credentials)

    async def open_file(self, file: str, prefix: str = 'files') -> str:
        """
        Opens a prompt file and returns its content.
        """
        filename = self.directory.joinpath(prefix, self.agent_id, file)
        if not filename.exists() or not filename.is_file():
            raise FileNotFoundError(
                f"File {filename} does not exist in the directory {self.directory}."
            )
        try:
            async with aiofiles.open(filename, 'r') as f:
                content = await f.read()
            return content
        except Exception as e:
            self.logger.warning(
                f"Failed to read prompt file {filename}: {e}"
            )
            return None

    async def open_prompt(self, file: str) -> str:
        """
        Opens a prompt file and returns its content.
        """
        if not self.directory:
            raise ValueError(
                "Directory is not set. Please set the directory before opening a prompt."
            )
        return await self.open_file(f"{file}.txt", prefix='prompts')

    async def create_agent(
        self,
        llm: Any = None,
        tools: Optional[List[Any]] = None,
        backstory: Optional[str] = None,
        agent_type: Optional[str] = None
    ) -> BasicAgent:
        """Create and configure a BasicAgent instance."""
        if not llm:
            llm = OpenAILLM(
                model="gpt-4.1",
                temperature=0.2,
                max_tokens=4096,
                use_chat=True
            )
        try:
            tools = self._define_tools(self.destination)
            if not isinstance(tools, list):
                raise TypeError("Tools must be a list of BaseTool instances.")
            if not all(isinstance(tool, BaseTool) for tool in tools):
                raise TypeError("All tools must be instances of BaseTool.")
            agent = BasicAgent(
                name=self._agent_name,
                llm=llm,
                tools=tools,
                agent_type=agent_type or 'tool-calling',
                backstory=backstory or self._backstory,
            )
            await agent.configure()
            return agent
        except Exception as e:
            raise RuntimeError(
                f"Failed to create agent {self.agent_name}: {str(e)}"
            ) from e

    async def start(self, **kwargs):
        """Check for File and Directory information."""
        if hasattr(self, "directory"):
            self.directory = Path(self.directory).resolve()
        else:
            if self._use_taskstorage:
                self.directory = self._taskstore.get_path().joinpath(self._program)
            else:
                self.directory = self._filestore.get_directory('').parent
        # Define destination:
        if hasattr(self, 'destination'):
            self.destination = Path(self.destination).resolve()
        else:
            self.destination = self._filestore.get_directory('', program=self._program)
        if not self.destination.exists():
            self.destination.mkdir(parents=True, exist_ok=True)
            # Also, create the subdirectory for the agent:
            self.destination.joinpath(self._agent_name).mkdir(parents=True, exist_ok=True)
        await super().start(**kwargs)
        # Open the Backstory prompt if it exists
        backstory = await self.open_file(self.backstory)
        # Create the Agent:
        if not self._agent:
            self._agent = await self.create_agent(
                llm=self._llm,
                tools=self._tools,
                backstory=backstory,
                agent_type=self._config.get('agent_type', 'tool-calling')
            )
        if not self._agent:
            raise RuntimeError(
                f"Agent {self.agent_name} could not be created. "
                "Ensure that the LLM and tools are properly configured."
            )
        return True

    async def ask_agent(
        self,
        userid: str,
        query: str = None,
        prompt_file: str = None,
        *args,
        **kwargs
    ) -> tuple[AgentAnswer, BaseModel]:
        """
        Asks the agent a question and returns an Object response.
        """
        if not query:
            if prompt_file:
                query = await self.open_prompt(prompt_file)
            else:
                raise ValueError(
                    "Query or prompt file must be provided."
                )
        self.logger.info(
            f"Asking agent {self._agent_name} with query: {query}"
        )
        # Answer is the string version of the query:
        question = query.format(**kwargs)
        # response is a BaseModel instance with the response data
        # result is a dictionary with the result of the agent invocation, or an Exception if it failed
        answer, response, result = await self._agent.invoke(question)
        if isinstance(result, Exception):
            raise result

        # Create the response object
        final_report = answer
        # parse the intermediate steps if available to extract PDF and podcast paths:
        pdf_path = None
        podcast_path = None
        transcript = None
        document_path = None
        if response.intermediate_steps:
            for step in response.intermediate_steps:
                tool = step['tool']
                result = step['result']
                tool_input = step.get('tool_input', {})
                if 'text' in tool_input:
                    transcript = tool_input['text']
                if isinstance(result, dict):
                    # Extract the URL from the result if available
                    url = result.get('url', None)
                    if tool == 'pdf_print_tool':
                        pdf_path = url
                    elif tool == 'podcast_generator_tool':
                        podcast_path = url
                    else:
                        document_path = url
        response_data = self._response(
            user_id=userid,
            agent_name=self._agent_name,
            attributes=kwargs.pop('attributes', {}),
            data=final_report,
            status="success",
            created_at=datetime.now(),
            output=result.get('output', ''),
            transcript=transcript,
            pdf_path=str(pdf_path),
            podcast_path=str(podcast_path),
            document_path=str(document_path),
            documents=response.documents if hasattr(response, 'documents') else [],
            **kwargs
        )
        return response_data, response

    async def generate_files(
        self,
        userid: str,
        response: AgentAnswer,
        **kwargs
    ) -> tuple[AgentAnswer, BaseModel]:
        """
        Generate files based on the response from the agent.
        This method can be overridden by subclasses to implement custom file generation logic.
        """
        query = await self.open_prompt('for_pdf.txt')
        query = textwrap.dedent(query)
        final_report = response.output.strip()
        for_pdf = query.format(
            final_report=final_report
        )
        try:
            _, response, result = await self._agent.invoke(for_pdf)
            if isinstance(result, Exception):
                raise result
        except Exception as e:
            print(f"Error invoking agent: {e}")
            raise RuntimeError(
                f"Failed to generate report due to an error in the agent invocation: {e}"
            )

        # parse the intermediate steps if available to extract PDF and podcast paths:
        pdf_path = None
        podcast_path = None
        transcript = None
        document_path = None
        if response.intermediate_steps:
            for step in response.intermediate_steps:
                tool = step['tool']
                result = step['result']
                tool_input = step.get('tool_input', {})
                if 'text' in tool_input:
                    transcript = tool_input['text']
                if isinstance(result, dict):
                    # Extract the URL from the result if available
                    url = result.get('url', None)
                    if tool == 'pdf_print_tool':
                        pdf_path = url
                    elif tool == 'podcast_generator_tool':
                        podcast_path = url
                    else:
                        document_path = url
        response_data = self._response(
            user_id=userid,
            agent_name=self._agent_name,
            attributes=kwargs.pop('attributes', {}),
            data=final_report,
            status="success",
            created_at=datetime.now(),
            output=result.get('output', ''),
            transcript=transcript,
            pdf_path=str(pdf_path),
            podcast_path=str(podcast_path),
            document_path=str(document_path),
            documents=response.documents if hasattr(response, 'documents') else [],
            **kwargs
        )
        return response_data, response
