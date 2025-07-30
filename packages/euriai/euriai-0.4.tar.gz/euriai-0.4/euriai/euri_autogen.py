from typing import Optional, Dict, Any, List

try:
    import autogen
except ImportError:
    autogen = None

class EuriaiAutoGen:
    """
    Full-featured wrapper for AutoGen integration in the EURI SDK.
    Allows programmatic agent, tool, and workflow management, and chat execution.
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the AutoGen wrapper.
        Args:
            config: Dict of config options (API keys, model, etc.)
        """
        if autogen is None:
            raise ImportError("AutoGen is not installed. Please install with `pip install pyautogen`.")
        self.config = config or {}
        self.agents: List[Any] = []
        self.tools: List[Any] = []
        self.memory: Optional[Any] = None
        self.workflow: Optional[Any] = None
        self.history: List[Dict[str, Any]] = []

    def add_agent(self, agent_config: Dict[str, Any]) -> Any:
        """Add an agent with config."""
        agent = autogen.Agent(**agent_config)
        self.agents.append(agent)
        return agent

    def add_tool(self, tool_config: Dict[str, Any]) -> Any:
        """Add a tool with config."""
        tool = autogen.Tool(**tool_config)
        self.tools.append(tool)
        return tool

    def set_memory(self, memory_config: Dict[str, Any]) -> None:
        """Set memory for the workflow."""
        self.memory = autogen.Memory(**memory_config)

    def run_chat(self, prompt: str, agent_idx: int = 0, **kwargs) -> str:
        """
        Run a chat with the specified agent and prompt.
        Returns the agent's response.
        """
        if not self.agents:
            raise ValueError("No agents defined. Use add_agent().")
        agent = self.agents[agent_idx]
        response = agent.chat(prompt, **kwargs)
        self.history.append({"agent": agent, "prompt": prompt, "response": response})
        return response

    def run_workflow(self, workflow_config: Dict[str, Any], **kwargs) -> Any:
        """
        Run a custom workflow (advanced usage).
        """
        workflow = autogen.Workflow(**workflow_config)
        self.workflow = workflow
        result = workflow.run(**kwargs)
        return result

    def get_history(self) -> List[Dict[str, Any]]:
        return self.history

    def reset(self):
        """Reset agents, tools, memory, and history."""
        self.agents = []
        self.tools = []
        self.memory = None
        self.workflow = None
        self.history = [] 