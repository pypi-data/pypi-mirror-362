"""
Enhanced LangGraph Integration for Euri API
==========================================

This module provides a comprehensive LangGraph integration with the Euri API,
including AI-powered workflows, async operations, multi-model support, and
pre-built workflow patterns for common use cases.

Usage:
    from euriai.langgraph_enhanced import EuriaiLangGraph, EuriaiAINode
    
    # Create enhanced LangGraph with AI capabilities
    graph = EuriaiLangGraph(
        api_key="your_api_key",
        default_model="gpt-4.1-nano"
    )
    
    # Add AI-powered nodes
    graph.add_ai_node("analyzer", "Analyze the input and extract key insights")
    graph.add_ai_node("generator", "Generate a response based on the analysis")
    
    # Create workflow
    graph.add_edge("analyzer", "generator")
    graph.set_entry_point("analyzer")
    graph.set_finish_point("generator")
    
    # Run workflow
    result = graph.run({"input": "Your text here"})
    print(result)
"""

import asyncio
import json
import logging
from typing import (
    Any, Dict, List, Optional, Iterator, AsyncIterator, 
    Union, Callable, Sequence, TypeVar, Generic, Tuple
)
from concurrent.futures import ThreadPoolExecutor
import time
from functools import wraps
from enum import Enum

try:
    from langgraph.graph import StateGraph, START, END
    from langgraph.graph.state import CompiledStateGraph
    from langgraph.constants import Send
    from langgraph.checkpoint.memory import MemorySaver
    from pydantic import BaseModel, Field
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    # Fallback classes
    class StateGraph:
        pass
    class CompiledStateGraph:
        pass
    class Send:
        pass
    class MemorySaver:
        pass
    class BaseModel:
        pass
    class Field:
        pass
    START = "START"
    END = "END"

from euriai.client import EuriaiClient
from euriai.embedding import EuriaiEmbeddingClient

# Type definitions
StateType = TypeVar('StateType', bound=Dict[str, Any])
NodeOutput = Union[Dict[str, Any], List[Dict[str, Any]]]


class WorkflowType(Enum):
    """Predefined workflow types"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    AGENT_WORKFLOW = "agent_workflow"
    RAG_WORKFLOW = "rag_workflow"
    MULTI_AGENT = "multi_agent"


class NodeType(Enum):
    """Types of nodes in the workflow"""
    AI_NODE = "ai_node"
    FUNCTION_NODE = "function_node"
    CONDITION_NODE = "condition_node"
    AGGREGATOR_NODE = "aggregator_node"
    ROUTER_NODE = "router_node"
    EMBEDDING_NODE = "embedding_node"


class EuriaiAINode:
    """
    AI-powered node that uses Euri API for processing.
    
    This node can perform various AI tasks like text generation, analysis,
    summarization, and more using the Euri API.
    """
    
    def __init__(
        self,
        name: str,
        prompt_template: str,
        api_key: str,
        model: str = "gpt-4.1-nano",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        system_message: Optional[str] = None,
        output_parser: Optional[Callable[[str], Any]] = None,
        error_handler: Optional[Callable[[Exception], Any]] = None
    ):
        """
        Initialize an AI node.
        
        Args:
            name: Node name
            prompt_template: Template for generating prompts (can use {variable} placeholders)
            api_key: Euri API key
            model: Model to use for this node
            temperature: Model temperature
            max_tokens: Maximum tokens to generate
            system_message: Optional system message
            output_parser: Function to parse AI output
            error_handler: Function to handle errors
        """
        self.name = name
        self.prompt_template = prompt_template
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_message = system_message
        self.output_parser = output_parser
        self.error_handler = error_handler
        
        # Initialize client
        self.client = EuriaiClient(api_key=api_key, model=model)
        
        # Usage tracking
        self.usage_stats = {
            "total_calls": 0,
            "total_tokens": 0,
            "errors": 0,
            "avg_response_time": 0.0
        }
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the AI node."""
        start_time = time.time()
        
        try:
            # Format prompt with state variables
            formatted_prompt = self.prompt_template.format(**state)
            
            # Prepare messages
            messages = []
            if self.system_message:
                messages.append({"role": "system", "content": self.system_message})
            messages.append({"role": "user", "content": formatted_prompt})
            
            # Make API call
            response = self.client.generate_completion(
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Extract content
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Parse output if parser provided
            if self.output_parser:
                parsed_output = self.output_parser(content)
            else:
                parsed_output = content
            
            # Update usage stats
            self.usage_stats["total_calls"] += 1
            response_time = time.time() - start_time
            self.usage_stats["avg_response_time"] = (
                (self.usage_stats["avg_response_time"] * (self.usage_stats["total_calls"] - 1) + response_time)
                / self.usage_stats["total_calls"]
            )
            
            # Update state
            state[f"{self.name}_output"] = parsed_output
            state[f"{self.name}_raw_response"] = content
            
            return state
            
        except Exception as e:
            self.usage_stats["errors"] += 1
            
            if self.error_handler:
                return self.error_handler(e)
            else:
                logging.error(f"Error in AI node {self.name}: {e}")
                state[f"{self.name}_error"] = str(e)
                return state
    
    async def acall(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Async version of the AI node execution."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.__call__, state)


class EuriaiLangGraph:
    """
    Enhanced LangGraph integration that uses Euri API for AI-powered workflows.
    
    This implementation provides:
    - AI-powered nodes with Euri API integration
    - Pre-built workflow patterns
    - Async operations
    - Multi-model support
    - Usage tracking and monitoring
    - Error handling and recovery
    - Workflow visualization and debugging
    
    Example:
        graph = EuriaiLangGraph(
            api_key="your_api_key",
            default_model="gpt-4.1-nano"
        )
        
        # Add AI nodes
        graph.add_ai_node("analyzer", "Analyze this text: {input}")
        graph.add_ai_node("summarizer", "Summarize: {analyzer_output}")
        
        # Create workflow
        graph.add_edge("analyzer", "summarizer")
        graph.set_entry_point("analyzer")
        graph.set_finish_point("summarizer")
        
        # Run workflow
        result = graph.run({"input": "Your text here"})
    """
    
    def __init__(
        self,
        api_key: str,
        name: str = "EuriaiLangGraph",
        default_model: str = "gpt-4.1-nano",
        default_temperature: float = 0.7,
        default_max_tokens: int = 1000,
        enable_checkpointing: bool = True,
        verbose: bool = True
    ):
        """
        Initialize the enhanced LangGraph.
        
        Args:
            api_key: Euri API key
            name: Graph name
            default_model: Default model for AI nodes
            default_temperature: Default temperature
            default_max_tokens: Default max tokens
            enable_checkpointing: Enable workflow checkpointing
            verbose: Enable verbose logging
        """
        if not LANGGRAPH_AVAILABLE:
            raise ImportError(
                "LangGraph is not installed. Please install with: "
                "pip install langgraph"
            )
        
        self.api_key = api_key
        self.name = name
        self.default_model = default_model
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens
        self.verbose = verbose
        
        # Initialize graph
        self.graph = StateGraph(dict)
        self.compiled_graph: Optional[CompiledStateGraph] = None
        
        # Checkpointing
        self.checkpointer = MemorySaver() if enable_checkpointing else None
        
        # Node management
        self.nodes: Dict[str, Any] = {}
        self.ai_nodes: Dict[str, EuriaiAINode] = {}
        self.edges: List[Tuple[str, str]] = []
        self.conditional_edges: List[Dict[str, Any]] = []
        
        # Workflow state
        self.entry_point: Optional[str] = None
        self.finish_point: Optional[str] = None
        
        # Usage tracking
        self.usage_stats = {
            "total_runs": 0,
            "total_nodes_executed": 0,
            "avg_execution_time": 0.0,
            "errors": 0,
            "successful_runs": 0
        }
        
        # Thread pool for async operations
        self._executor = ThreadPoolExecutor(max_workers=4)
    
    def add_ai_node(
        self,
        name: str,
        prompt_template: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_message: Optional[str] = None,
        output_parser: Optional[Callable[[str], Any]] = None,
        error_handler: Optional[Callable[[Exception], Any]] = None
    ) -> None:
        """
        Add an AI-powered node to the graph.
        
        Args:
            name: Node name
            prompt_template: Prompt template with {variable} placeholders
            model: Model to use (defaults to graph default)
            temperature: Temperature (defaults to graph default)
            max_tokens: Max tokens (defaults to graph default)
            system_message: System message for the node
            output_parser: Function to parse AI output
            error_handler: Function to handle errors
        """
        ai_node = EuriaiAINode(
            name=name,
            prompt_template=prompt_template,
            api_key=self.api_key,
            model=model or self.default_model,
            temperature=temperature or self.default_temperature,
            max_tokens=max_tokens or self.default_max_tokens,
            system_message=system_message,
            output_parser=output_parser,
            error_handler=error_handler
        )
        
        self.ai_nodes[name] = ai_node
        self.nodes[name] = ai_node
        self.graph.add_node(name, ai_node)
        
        if self.verbose:
            print(f"Added AI node: {name} (model: {ai_node.model})")
    
    def add_function_node(self, name: str, func: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        """
        Add a function node to the graph.
        
        Args:
            name: Node name
            func: Function to execute (takes state dict, returns state dict)
        """
        self.nodes[name] = func
        self.graph.add_node(name, func)
        
        if self.verbose:
            print(f"Added function node: {name}")
    
    def add_condition_node(
        self,
        name: str,
        condition_func: Callable[[Dict[str, Any]], str],
        routes: Dict[str, str]
    ) -> None:
        """
        Add a conditional node that routes based on state.
        
        Args:
            name: Node name
            condition_func: Function that returns route key based on state
            routes: Mapping of route keys to target nodes
        """
        def condition_wrapper(state: Dict[str, Any]) -> str:
            route_key = condition_func(state)
            return routes.get(route_key, END)
        
        self.nodes[name] = condition_wrapper
        self.graph.add_node(name, condition_wrapper)
        
        # Add conditional edges
        for route_key, target_node in routes.items():
            self.graph.add_conditional_edges(
                name,
                condition_wrapper,
                {route_key: target_node}
            )
        
        self.conditional_edges.append({
            "source": name,
            "condition": condition_func,
            "routes": routes
        })
        
        if self.verbose:
            print(f"Added condition node: {name} with routes: {routes}")
    
    def add_embedding_node(
        self,
        name: str,
        embedding_model: str = "text-embedding-3-small",
        batch_size: int = 100
    ) -> None:
        """
        Add an embedding node that generates embeddings for text.
        
        Args:
            name: Node name
            embedding_model: Embedding model to use
            batch_size: Batch size for processing
        """
        embedding_client = EuriaiEmbeddingClient(
            api_key=self.api_key,
            model=embedding_model
        )
        
        def embedding_func(state: Dict[str, Any]) -> Dict[str, Any]:
            # Get text to embed (can be string or list)
            text_input = state.get(f"{name}_input", state.get("input", ""))
            
            if isinstance(text_input, str):
                embedding = embedding_client.embed(text_input)
                state[f"{name}_output"] = embedding.tolist()
            elif isinstance(text_input, list):
                embeddings = embedding_client.embed_batch(text_input)
                state[f"{name}_output"] = [emb.tolist() for emb in embeddings]
            else:
                state[f"{name}_error"] = "Invalid input type for embedding"
            
            return state
        
        self.nodes[name] = embedding_func
        self.graph.add_node(name, embedding_func)
        
        if self.verbose:
            print(f"Added embedding node: {name} (model: {embedding_model})")
    
    def add_edge(self, from_node: str, to_node: str) -> None:
        """
        Add an edge between two nodes.
        
        Args:
            from_node: Source node name
            to_node: Target node name
        """
        self.graph.add_edge(from_node, to_node)
        self.edges.append((from_node, to_node))
        
        if self.verbose:
            print(f"Added edge: {from_node} -> {to_node}")
    
    def set_entry_point(self, node_name: str) -> None:
        """
        Set the entry point for the workflow.
        
        Args:
            node_name: Name of the starting node
        """
        self.entry_point = node_name
        self.graph.add_edge(START, node_name)
        
        if self.verbose:
            print(f"Set entry point: {node_name}")
    
    def set_finish_point(self, node_name: str) -> None:
        """
        Set the finish point for the workflow.
        
        Args:
            node_name: Name of the ending node
        """
        self.finish_point = node_name
        self.graph.add_edge(node_name, END)
        
        if self.verbose:
            print(f"Set finish point: {node_name}")
    
    def compile_graph(self) -> CompiledStateGraph:
        """
        Compile the graph for execution.
        
        Returns:
            Compiled graph ready for execution
        """
        self.compiled_graph = self.graph.compile(
            checkpointer=self.checkpointer,
            debug=self.verbose
        )
        
        if self.verbose:
            print("Graph compiled successfully")
        
        return self.compiled_graph
    
    def run(
        self,
        input_state: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run the workflow with the given input state.
        
        Args:
            input_state: Initial state for the workflow
            config: Optional configuration for the run
            
        Returns:
            Final state after workflow execution
        """
        start_time = time.time()
        
        try:
            # Compile graph if not already compiled
            if self.compiled_graph is None:
                self.compile_graph()
            
            # Execute workflow
            result = self.compiled_graph.invoke(input_state, config=config)
            
            # Update usage stats
            self.usage_stats["total_runs"] += 1
            self.usage_stats["successful_runs"] += 1
            execution_time = time.time() - start_time
            self.usage_stats["avg_execution_time"] = (
                (self.usage_stats["avg_execution_time"] * (self.usage_stats["total_runs"] - 1) + execution_time)
                / self.usage_stats["total_runs"]
            )
            
            if self.verbose:
                print(f"Workflow completed in {execution_time:.2f}s")
            
            return result
            
        except Exception as e:
            self.usage_stats["errors"] += 1
            logging.error(f"Error running workflow: {e}")
            raise
    
    async def arun(
        self,
        input_state: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Async version of workflow execution.
        
        Args:
            input_state: Initial state for the workflow
            config: Optional configuration for the run
            
        Returns:
            Final state after workflow execution
        """
        start_time = time.time()
        
        try:
            # Compile graph if not already compiled
            if self.compiled_graph is None:
                self.compile_graph()
            
            # Execute workflow asynchronously
            result = await self.compiled_graph.ainvoke(input_state, config=config)
            
            # Update usage stats
            self.usage_stats["total_runs"] += 1
            self.usage_stats["successful_runs"] += 1
            execution_time = time.time() - start_time
            self.usage_stats["avg_execution_time"] = (
                (self.usage_stats["avg_execution_time"] * (self.usage_stats["total_runs"] - 1) + execution_time)
                / self.usage_stats["total_runs"]
            )
            
            if self.verbose:
                print(f"Async workflow completed in {execution_time:.2f}s")
            
            return result
            
        except Exception as e:
            self.usage_stats["errors"] += 1
            logging.error(f"Error running async workflow: {e}")
            raise
    
    def stream(
        self,
        input_state: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None
    ) -> Iterator[Dict[str, Any]]:
        """
        Stream workflow execution results.
        
        Args:
            input_state: Initial state for the workflow
            config: Optional configuration for the run
            
        Yields:
            Intermediate states during workflow execution
        """
        if self.compiled_graph is None:
            self.compile_graph()
        
        for chunk in self.compiled_graph.stream(input_state, config=config):
            yield chunk
    
    async def astream(
        self,
        input_state: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None
    ) -> AsyncIterator[Dict[str, Any]]:
        """
        Async stream workflow execution results.
        
        Args:
            input_state: Initial state for the workflow
            config: Optional configuration for the run
            
        Yields:
            Intermediate states during workflow execution
        """
        if self.compiled_graph is None:
            self.compile_graph()
        
        async for chunk in self.compiled_graph.astream(input_state, config=config):
            yield chunk
    
    def create_workflow_pattern(self, pattern_type: WorkflowType, **kwargs) -> None:
        """
        Create a pre-defined workflow pattern.
        
        Args:
            pattern_type: Type of workflow pattern to create
            **kwargs: Pattern-specific arguments
        """
        if pattern_type == WorkflowType.SEQUENTIAL:
            self._create_sequential_workflow(**kwargs)
        elif pattern_type == WorkflowType.PARALLEL:
            self._create_parallel_workflow(**kwargs)
        elif pattern_type == WorkflowType.CONDITIONAL:
            self._create_conditional_workflow(**kwargs)
        elif pattern_type == WorkflowType.AGENT_WORKFLOW:
            self._create_agent_workflow(**kwargs)
        elif pattern_type == WorkflowType.RAG_WORKFLOW:
            self._create_rag_workflow(**kwargs)
        elif pattern_type == WorkflowType.MULTI_AGENT:
            self._create_multi_agent_workflow(**kwargs)
        else:
            raise ValueError(f"Unknown workflow pattern: {pattern_type}")
    
    def _create_sequential_workflow(self, steps: List[Dict[str, Any]]) -> None:
        """Create a sequential workflow pattern."""
        previous_node = None
        
        for i, step in enumerate(steps):
            node_name = step.get("name", f"step_{i}")
            
            if step["type"] == "ai":
                self.add_ai_node(
                    node_name,
                    step["prompt_template"],
                    model=step.get("model"),
                    temperature=step.get("temperature"),
                    max_tokens=step.get("max_tokens")
                )
            elif step["type"] == "function":
                self.add_function_node(node_name, step["function"])
            
            if i == 0:
                self.set_entry_point(node_name)
            
            if previous_node:
                self.add_edge(previous_node, node_name)
            
            previous_node = node_name
        
        if previous_node:
            self.set_finish_point(previous_node)
    
    def _create_parallel_workflow(self, parallel_nodes: List[Dict[str, Any]], aggregator: Dict[str, Any]) -> None:
        """Create a parallel workflow pattern."""
        # Create dispatcher node
        def dispatcher(state: Dict[str, Any]) -> List[Send]:
            return [Send(node["name"], state) for node in parallel_nodes]
        
        self.add_function_node("dispatcher", dispatcher)
        self.set_entry_point("dispatcher")
        
        # Create parallel nodes
        for node in parallel_nodes:
            if node["type"] == "ai":
                self.add_ai_node(
                    node["name"],
                    node["prompt_template"],
                    model=node.get("model"),
                    temperature=node.get("temperature")
                )
            elif node["type"] == "function":
                self.add_function_node(node["name"], node["function"])
            
            # Connect to aggregator
            self.add_edge(node["name"], aggregator["name"])
        
        # Create aggregator node
        if aggregator["type"] == "ai":
            self.add_ai_node(
                aggregator["name"],
                aggregator["prompt_template"],
                model=aggregator.get("model")
            )
        elif aggregator["type"] == "function":
            self.add_function_node(aggregator["name"], aggregator["function"])
        
        self.set_finish_point(aggregator["name"])
    
    def _create_conditional_workflow(self, condition: Dict[str, Any], branches: Dict[str, List[Dict[str, Any]]]) -> None:
        """Create a conditional workflow pattern."""
        # Create condition node
        self.add_condition_node(
            condition["name"],
            condition["function"],
            {key: f"{key}_start" for key in branches.keys()}
        )
        self.set_entry_point(condition["name"])
        
        # Create branches
        for branch_name, steps in branches.items():
            previous_node = None
            
            for i, step in enumerate(steps):
                node_name = f"{branch_name}_{step.get('name', f'step_{i}')}"
                
                if step["type"] == "ai":
                    self.add_ai_node(
                        node_name,
                        step["prompt_template"],
                        model=step.get("model")
                    )
                elif step["type"] == "function":
                    self.add_function_node(node_name, step["function"])
                
                if i == 0:
                    # This is the start of the branch
                    self.add_function_node(f"{branch_name}_start", lambda state: state)
                    self.add_edge(f"{branch_name}_start", node_name)
                
                if previous_node:
                    self.add_edge(previous_node, node_name)
                
                previous_node = node_name
            
            # Connect last node to END
            if previous_node:
                self.set_finish_point(previous_node)
    
    def _create_agent_workflow(self, agent_config: Dict[str, Any]) -> None:
        """Create an agent workflow pattern."""
        # Planning node
        self.add_ai_node(
            "planner",
            agent_config.get("planning_prompt", "Create a plan to solve: {input}"),
            model=agent_config.get("planning_model", self.default_model)
        )
        
        # Execution node
        self.add_ai_node(
            "executor",
            agent_config.get("execution_prompt", "Execute this plan: {planner_output}"),
            model=agent_config.get("execution_model", self.default_model)
        )
        
        # Evaluation node
        self.add_ai_node(
            "evaluator",
            agent_config.get("evaluation_prompt", "Evaluate the result: {executor_output}"),
            model=agent_config.get("evaluation_model", self.default_model)
        )
        
        # Create workflow
        self.set_entry_point("planner")
        self.add_edge("planner", "executor")
        self.add_edge("executor", "evaluator")
        self.set_finish_point("evaluator")
    
    def _create_rag_workflow(self, rag_config: Dict[str, Any]) -> None:
        """Create a RAG (Retrieval-Augmented Generation) workflow pattern."""
        # Embedding node for query
        self.add_embedding_node(
            "query_embedder",
            embedding_model=rag_config.get("embedding_model", "text-embedding-3-small")
        )
        
        # Retrieval node (function that uses embeddings to find relevant docs)
        def retrieval_func(state: Dict[str, Any]) -> Dict[str, Any]:
            # This would typically interface with a vector database
            # For now, we'll use a simple placeholder
            query_embedding = state.get("query_embedder_output", [])
            # Simulate retrieval
            state["retrieved_docs"] = rag_config.get("sample_docs", ["Sample document content"])
            return state
        
        self.add_function_node("retriever", retrieval_func)
        
        # Generation node with context
        self.add_ai_node(
            "generator",
            rag_config.get(
                "generation_prompt",
                "Based on these documents: {retrieved_docs}\n\nAnswer the question: {input}"
            ),
            model=rag_config.get("generation_model", self.default_model)
        )
        
        # Create workflow
        self.set_entry_point("query_embedder")
        self.add_edge("query_embedder", "retriever")
        self.add_edge("retriever", "generator")
        self.set_finish_point("generator")
    
    def _create_multi_agent_workflow(self, agents: List[Dict[str, Any]]) -> None:
        """Create a multi-agent workflow pattern."""
        # Create agent nodes
        for agent in agents:
            self.add_ai_node(
                agent["name"],
                agent["prompt_template"],
                model=agent.get("model", self.default_model),
                system_message=agent.get("system_message")
            )
        
        # Create orchestrator
        def orchestrator(state: Dict[str, Any]) -> str:
            # Simple round-robin orchestration
            # In practice, this would be more sophisticated
            current_agent = state.get("current_agent", 0)
            next_agent = (current_agent + 1) % len(agents)
            state["current_agent"] = next_agent
            return agents[next_agent]["name"]
        
        self.add_condition_node(
            "orchestrator",
            orchestrator,
            {agent["name"]: agent["name"] for agent in agents}
        )
        
        # Connect agents back to orchestrator
        for agent in agents:
            self.add_edge(agent["name"], "orchestrator")
        
        self.set_entry_point("orchestrator")
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics for the workflow."""
        stats = self.usage_stats.copy()
        
        # Add AI node stats
        stats["ai_nodes"] = {}
        for name, node in self.ai_nodes.items():
            stats["ai_nodes"][name] = node.usage_stats.copy()
        
        return stats
    
    def get_graph_structure(self) -> Dict[str, Any]:
        """Get the structure of the graph."""
        return {
            "nodes": list(self.nodes.keys()),
            "ai_nodes": list(self.ai_nodes.keys()),
            "edges": self.edges,
            "conditional_edges": self.conditional_edges,
            "entry_point": self.entry_point,
            "finish_point": self.finish_point
        }
    
    def visualize_graph(self) -> str:
        """
        Generate a simple text visualization of the graph.
        
        Returns:
            Text representation of the graph structure
        """
        lines = []
        lines.append(f"Graph: {self.name}")
        lines.append("=" * 50)
        lines.append(f"Entry Point: {self.entry_point}")
        lines.append(f"Finish Point: {self.finish_point}")
        lines.append("")
        
        lines.append("Nodes:")
        for name, node in self.nodes.items():
            node_type = "AI" if name in self.ai_nodes else "Function"
            lines.append(f"  - {name} ({node_type})")
        
        lines.append("")
        lines.append("Edges:")
        for from_node, to_node in self.edges:
            lines.append(f"  {from_node} -> {to_node}")
        
        if self.conditional_edges:
            lines.append("")
            lines.append("Conditional Edges:")
            for edge in self.conditional_edges:
                lines.append(f"  {edge['source']} -> {edge['routes']}")
        
        return "\n".join(lines)
    
    def reset(self) -> None:
        """Reset the graph to initial state."""
        self.graph = StateGraph(dict)
        self.compiled_graph = None
        self.nodes = {}
        self.ai_nodes = {}
        self.edges = []
        self.conditional_edges = []
        self.entry_point = None
        self.finish_point = None
        
        # Reset usage stats
        self.usage_stats = {
            "total_runs": 0,
            "total_nodes_executed": 0,
            "avg_execution_time": 0.0,
            "errors": 0,
            "successful_runs": 0
        }
        
        if self.verbose:
            print("Graph reset")
    
    def update_model(self, node_name: str, model: str) -> None:
        """
        Update the model for a specific AI node.
        
        Args:
            node_name: Name of the AI node
            model: New model to use
        """
        if node_name in self.ai_nodes:
            self.ai_nodes[node_name].model = model
            self.ai_nodes[node_name].client = EuriaiClient(
                api_key=self.api_key,
                model=model
            )
            
            if self.verbose:
                print(f"Updated model for {node_name}: {model}")
        else:
            raise ValueError(f"AI node {node_name} not found")


# Helper functions for common patterns
def create_simple_workflow(
    api_key: str,
    steps: List[Dict[str, Any]],
    name: str = "SimpleWorkflow"
) -> EuriaiLangGraph:
    """
    Create a simple sequential workflow.
    
    Args:
        api_key: Euri API key
        steps: List of step configurations
        name: Workflow name
        
    Returns:
        Configured EuriaiLangGraph
    """
    graph = EuriaiLangGraph(api_key=api_key, name=name)
    graph.create_workflow_pattern(WorkflowType.SEQUENTIAL, steps=steps)
    return graph


def create_agent_workflow(
    api_key: str,
    agent_config: Dict[str, Any],
    name: str = "AgentWorkflow"
) -> EuriaiLangGraph:
    """
    Create an agent-based workflow.
    
    Args:
        api_key: Euri API key
        agent_config: Agent configuration
        name: Workflow name
        
    Returns:
        Configured EuriaiLangGraph
    """
    graph = EuriaiLangGraph(api_key=api_key, name=name)
    graph.create_workflow_pattern(WorkflowType.AGENT_WORKFLOW, agent_config=agent_config)
    return graph


def create_rag_workflow(
    api_key: str,
    rag_config: Dict[str, Any],
    name: str = "RAGWorkflow"
) -> EuriaiLangGraph:
    """
    Create a RAG (Retrieval-Augmented Generation) workflow.
    
    Args:
        api_key: Euri API key
        rag_config: RAG configuration
        name: Workflow name
        
    Returns:
        Configured EuriaiLangGraph
    """
    graph = EuriaiLangGraph(api_key=api_key, name=name)
    graph.create_workflow_pattern(WorkflowType.RAG_WORKFLOW, rag_config=rag_config)
    return graph 