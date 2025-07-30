from typing import Any, Callable, Dict, List, Optional, Union

try:
    from langgraph.graph import StateGraph
except ImportError:
    StateGraph = None

class EuriaiLangGraph:
    """
    Full-featured wrapper for LangGraph integration in the EURI SDK.
    Allows programmatic graph construction, node/edge management, and workflow execution.
    """
    def __init__(self, name: str = "EuriaiLangGraph", state: Optional[Dict[str, Any]] = None):
        """
        Initialize the LangGraph wrapper.
        Args:
            name: Name of the graph.
            state: Initial state dictionary.
        """
        if StateGraph is None:
            raise ImportError("LangGraph is not installed. Please install with `pip install langgraph`.")
        self.name = name
        self.state = state or {}
        self.graph = StateGraph()
        self.nodes: Dict[str, Callable] = {}
        self.edges: List[tuple] = []

    def add_node(self, node_name: str, node_fn: Callable) -> None:
        """Add a node to the graph."""
        self.graph.add_node(node_name, node_fn)
        self.nodes[node_name] = node_fn

    def add_edge(self, from_node: str, to_node: str) -> None:
        """Add an edge between two nodes."""
        self.graph.add_edge(from_node, to_node)
        self.edges.append((from_node, to_node))

    def set_state(self, state: Dict[str, Any]) -> None:
        """Set the initial state for the graph execution."""
        self.state = state

    def run(self, input_state: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """
        Run the graph workflow with the given state.
        Returns the final state/output.
        """
        state = input_state or self.state
        return self.graph.run(state, **kwargs)

    def get_nodes(self) -> Dict[str, Callable]:
        return self.nodes

    def get_edges(self) -> List[tuple]:
        return self.edges

    def get_graph(self) -> Any:
        return self.graph

    def reset(self):
        """Reset the graph, nodes, and edges."""
        self.graph = StateGraph()
        self.nodes = {}
        self.edges = []
        self.state = {} 