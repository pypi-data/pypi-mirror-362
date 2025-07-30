from typing import Any, Callable, Dict, List, Optional

try:
    from smolagents import CodeAgent, HfApiModel, tool
except ImportError:
    CodeAgent = HfApiModel = tool = None

class EuriaiSmolAgent:
    """
    Full-featured wrapper for SmolAgents integration in the EURI SDK.
    Allows agent creation, tool integration, and task execution.
    """
    def __init__(self, model: Optional[Any] = None, tools: Optional[List[Callable]] = None):
        """
        Initialize the SmolAgent wrapper.
        Args:
            model: LLM model (default: HfApiModel())
            tools: List of tool functions (decorated with @tool)
        """
        if CodeAgent is None:
            raise ImportError("SmolAgents is not installed. Please install with `pip install smolagents`.")
        self.model = model or HfApiModel()
        self.tools = tools or []
        self.agent = CodeAgent(tools=self.tools, model=self.model)

    def add_tool(self, tool_fn: Callable) -> None:
        """Add a tool to the agent."""
        self.tools.append(tool_fn)
        self.agent = CodeAgent(tools=self.tools, model=self.model)

    def run(self, prompt: str, **kwargs) -> Any:
        """
        Run the agent on a prompt/task.
        Returns the agent's response.
        """
        return self.agent.run(prompt, **kwargs)

    def get_agent(self) -> Any:
        return self.agent

    def reset(self):
        """Reset the agent and tools."""
        self.tools = []
        self.agent = CodeAgent(tools=self.tools, model=self.model) 