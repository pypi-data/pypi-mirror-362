import os
from typing import Optional, Dict, Any, List, Union

# CrewAI imports (user must install crewai)
try:
    from crewai import Agent, Crew, Task, Process
except ImportError:
    Agent = Crew = Task = Process = None

class EuriaiCrewAI:
    """
    Full-featured wrapper for CrewAI integration in the EURI SDK.
    Allows programmatic and config-based crew creation, agent/task management, and workflow execution.
    """
    def __init__(self, agents: Optional[Dict[str, Any]] = None, tasks: Optional[Dict[str, Any]] = None, process: str = "sequential", verbose: bool = True):
        """
        Initialize the CrewAI wrapper.
        Args:
            agents: Dict of agent configs or Agent objects.
            tasks: Dict of task configs or Task objects.
            process: 'sequential' or 'parallel'.
            verbose: Print detailed logs.
        """
        if Agent is None:
            raise ImportError("CrewAI is not installed. Please install with `pip install crewai`.")
        self.agents_config = agents or {}
        self.tasks_config = tasks or {}
        self.process = Process.sequential if process == "sequential" else Process.parallel
        self.verbose = verbose
        self._agents: List[Agent] = []
        self._tasks: List[Task] = []
        self._crew: Optional[Crew] = None

    def add_agent(self, name: str, config: Dict[str, Any]) -> None:
        """Add an agent by config."""
        agent = Agent(**config)
        self._agents.append(agent)
        self.agents_config[name] = config

    def add_task(self, name: str, config: Dict[str, Any]) -> None:
        """Add a task by config."""
        task = Task(**config)
        self._tasks.append(task)
        self.tasks_config[name] = config

    def build_crew(self) -> Crew:
        """Build the Crew object from current agents and tasks."""
        if not self._agents:
            self._agents = [Agent(**cfg) for cfg in self.agents_config.values()]
        if not self._tasks:
            self._tasks = [Task(**cfg) for cfg in self.tasks_config.values()]
        self._crew = Crew(agents=self._agents, tasks=self._tasks, process=self.process, verbose=self.verbose)
        return self._crew

    def run(self, inputs: Optional[Dict[str, Any]] = None) -> Any:
        """
        Run the crew workflow. Optionally pass input variables for tasks.
        Returns the final result or report.
        """
        if self._crew is None:
            self.build_crew()
        return self._crew.kickoff(inputs=inputs or {})

    @classmethod
    def from_yaml(cls, agents_yaml: str, tasks_yaml: str, process: str = "sequential", verbose: bool = True):
        """
        Create a CrewAI wrapper from YAML config files.
        Args:
            agents_yaml: Path to agents.yaml
            tasks_yaml: Path to tasks.yaml
        """
        import yaml
        with open(agents_yaml, "r") as f:
            agents = yaml.safe_load(f)
        with open(tasks_yaml, "r") as f:
            tasks = yaml.safe_load(f)
        return cls(agents=agents, tasks=tasks, process=process, verbose=verbose)

    def get_agents(self) -> List[Agent]:
        return self._agents

    def get_tasks(self) -> List[Task]:
        return self._tasks

    def get_crew(self) -> Optional[Crew]:
        return self._crew

    def reset(self):
        """Reset agents, tasks, and crew."""
        self._agents = []
        self._tasks = []
        self._crew = None 