from typing import Optional, Dict, Any, List, Union
from types import SimpleNamespace
from euriai.client import EuriaiClient

try:
    import autogen
    from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
except ImportError:
    autogen = None
    AssistantAgent = UserProxyAgent = GroupChat = GroupChatManager = None

class EuriaiModelClient:
    """
    Custom model client that uses Euri API for AutoGen integration.
    Implements the ModelClient protocol required by AutoGen.
    """
    
    def __init__(self, config: Dict[str, Any], **kwargs):
        """
        Initialize the Euri model client.
        
        Args:
            config: Configuration dictionary containing:
                - model: Euri model name (e.g., 'gpt-4.1-nano', 'claude-3-5-sonnet')
                - api_key: Euri API key
                - temperature: Model temperature (optional)
                - max_tokens: Maximum tokens (optional)
        """
        self.config = config
        self.model = config["model"]
        self.api_key = config.get("api_key")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 1000)
        
        if not self.api_key:
            raise ValueError("Euri API key is required in config")
        
        # Initialize Euri client
        self.client = EuriaiClient(
            api_key=self.api_key,
            model=self.model
        )
        
        print(f"EuriaiModelClient initialized with model: {self.model}")
    
    def create(self, params: Dict[str, Any]) -> SimpleNamespace:
        """
        Create a response using the Euri API.
        
        Args:
            params: Parameters containing:
                - messages: List of message dictionaries
                - n: Number of responses (default 1)
                - temperature: Temperature override
                - max_tokens: Max tokens override
                
        Returns:
            Response object following AutoGen's ModelClientResponseProtocol
        """
        # Extract parameters
        messages = params.get("messages", [])
        n = params.get("n", 1)
        temperature = params.get("temperature", self.temperature)
        max_tokens = params.get("max_tokens", self.max_tokens)
        
        # Convert messages to prompt format
        prompt = self._convert_messages_to_prompt(messages)
        
        # Create response object
        response = SimpleNamespace()
        response.choices = []
        response.model = self.model
        response.usage = SimpleNamespace()
        
        # Generate responses
        for _ in range(n):
            try:
                # Call Euri API
                euri_response = self.client.generate_completion(
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                # Extract content
                content = euri_response.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # Create choice object
                choice = SimpleNamespace()
                choice.message = SimpleNamespace()
                choice.message.content = content
                choice.message.function_call = None
                choice.finish_reason = "stop"
                
                response.choices.append(choice)
                
                # Add usage info if available
                if "usage" in euri_response:
                    usage = euri_response["usage"]
                    response.usage.prompt_tokens = usage.get("prompt_tokens", 0)
                    response.usage.completion_tokens = usage.get("completion_tokens", 0)
                    response.usage.total_tokens = usage.get("total_tokens", 0)
                
            except Exception as e:
                print(f"Error calling Euri API: {e}")
                # Create error response
                choice = SimpleNamespace()
                choice.message = SimpleNamespace()
                choice.message.content = f"Error: {str(e)}"
                choice.message.function_call = None
                choice.finish_reason = "error"
                response.choices.append(choice)
        
        return response
    
    def message_retrieval(self, response: SimpleNamespace) -> List[str]:
        """
        Retrieve messages from the response.
        
        Args:
            response: Response object from create()
            
        Returns:
            List of response strings
        """
        return [choice.message.content for choice in response.choices]
    
    def cost(self, response: SimpleNamespace) -> float:
        """
        Calculate the cost of the response.
        
        Args:
            response: Response object from create()
            
        Returns:
            Cost of the response (0 for now)
        """
        return 0.0
    
    @staticmethod
    def get_usage(response: SimpleNamespace) -> Dict[str, Any]:
        """
        Get usage statistics from the response.
        
        Args:
            response: Response object from create()
            
        Returns:
            Usage statistics dictionary
        """
        usage = getattr(response, 'usage', SimpleNamespace())
        return {
            "prompt_tokens": getattr(usage, 'prompt_tokens', 0),
            "completion_tokens": getattr(usage, 'completion_tokens', 0),
            "total_tokens": getattr(usage, 'total_tokens', 0),
            "cost": 0.0,
            "model": response.model
        }
    
    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """
        Convert AutoGen messages to a prompt string.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Formatted prompt string
        """
        prompt_parts = []
        
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
            else:
                prompt_parts.append(f"{role}: {content}")
        
        return "\n".join(prompt_parts)

class EuriaiAutoGen:
    """
    Enhanced AutoGen integration that uses Euri API for all LLM calls.
    """
    
    def __init__(self, api_key: str, default_model: str = "gpt-4.1-nano"):
        """
        Initialize the EuriaiAutoGen wrapper.
        
        Args:
            api_key: Your Euri API key
            default_model: Default model to use
        """
        if autogen is None:
            raise ImportError("AutoGen is not installed. Please install with `pip install pyautogen`.")
        
        self.api_key = api_key
        self.default_model = default_model
        self.agents: List[Any] = []
        self.group_chat: Optional[GroupChat] = None
        self.group_chat_manager: Optional[GroupChatManager] = None
        self.history: List[Dict[str, Any]] = []
    
    def create_assistant_agent(
        self,
        name: str,
        system_message: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AssistantAgent:
        """
        Create an assistant agent with Euri API integration.
        
        Args:
            name: Agent name
            system_message: System message for the agent
            model: Euri model to use
            temperature: Model temperature
            max_tokens: Maximum tokens
            **kwargs: Additional arguments for AssistantAgent
            
        Returns:
            Configured AssistantAgent
        """
        # Create config for Euri API
        config_list = [{
            "model": model or self.default_model,
            "model_client_cls": "EuriaiModelClient",
            "api_key": self.api_key,
            "temperature": temperature,
            "max_tokens": max_tokens
        }]
        
        # Create agent
        agent = AssistantAgent(
            name=name,
            system_message=system_message,
            llm_config={"config_list": config_list},
            **kwargs
        )
        
        # Register the custom model client
        agent.register_model_client(model_client_cls=EuriaiModelClient)
        
        self.agents.append(agent)
        return agent
    
    def create_user_proxy_agent(
        self,
        name: str,
        is_termination_msg: Optional[callable] = None,
        code_execution_config: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> UserProxyAgent:
        """
        Create a user proxy agent.
        
        Args:
            name: Agent name
            is_termination_msg: Termination message function
            code_execution_config: Code execution configuration
            **kwargs: Additional arguments for UserProxyAgent
            
        Returns:
            Configured UserProxyAgent
        """
        agent = UserProxyAgent(
            name=name,
            is_termination_msg=is_termination_msg,
            code_execution_config=code_execution_config or {"use_docker": False},
            **kwargs
        )
        
        self.agents.append(agent)
        return agent
    
    def create_group_chat(
        self,
        agents: List[Any],
        messages: Optional[List[Dict[str, str]]] = None,
        max_round: int = 10,
        admin_name: str = "Admin",
        speaker_selection_method: str = "auto",
        **kwargs
    ) -> GroupChat:
        """
        Create a group chat with multiple agents.
        
        Args:
            agents: List of agents for the group chat
            messages: Initial messages
            max_round: Maximum number of rounds
            admin_name: Admin agent name
            speaker_selection_method: Speaker selection method
            **kwargs: Additional arguments for GroupChat
            
        Returns:
            Configured GroupChat
        """
        self.group_chat = GroupChat(
            agents=agents,
            messages=messages or [],
            max_round=max_round,
            admin_name=admin_name,
            speaker_selection_method=speaker_selection_method,
            **kwargs
        )
        
        return self.group_chat
    
    def create_group_chat_manager(
        self,
        groupchat: GroupChat,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> GroupChatManager:
        """
        Create a group chat manager.
        
        Args:
            groupchat: GroupChat instance
            model: Euri model to use
            temperature: Model temperature
            max_tokens: Maximum tokens
            **kwargs: Additional arguments for GroupChatManager
            
        Returns:
            Configured GroupChatManager
        """
        # Create config for Euri API
        config_list = [{
            "model": model or self.default_model,
            "model_client_cls": "EuriaiModelClient",
            "api_key": self.api_key,
            "temperature": temperature,
            "max_tokens": max_tokens
        }]
        
        # Create manager
        self.group_chat_manager = GroupChatManager(
            groupchat=groupchat,
            llm_config={"config_list": config_list},
            **kwargs
        )
        
        # Register the custom model client
        self.group_chat_manager.register_model_client(model_client_cls=EuriaiModelClient)
        
        return self.group_chat_manager
    
    def run_chat(
        self,
        agent1: Any,
        agent2: Any,
        message: str,
        max_turns: int = 10,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run a chat between two agents.
        
        Args:
            agent1: First agent
            agent2: Second agent
            message: Initial message
            max_turns: Maximum number of turns
            **kwargs: Additional arguments for initiate_chat
            
        Returns:
            Chat result
        """
        try:
            result = agent1.initiate_chat(
                agent2,
                message=message,
                max_turns=max_turns,
                **kwargs
            )
            
            # Store in history
            self.history.append({
                "type": "two_agent_chat",
                "agent1": agent1.name,
                "agent2": agent2.name,
                "message": message,
                "result": result
            })
            
            return result
            
        except Exception as e:
            print(f"Error in chat: {e}")
            return {"error": str(e)}
    
    def run_group_chat(
        self,
        message: str,
        max_turns: int = 10,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run a group chat with multiple agents.
        
        Args:
            message: Initial message
            max_turns: Maximum number of turns
            **kwargs: Additional arguments for initiate_chat
            
        Returns:
            Group chat result
        """
        if not self.group_chat_manager:
            raise ValueError("Group chat manager not created. Use create_group_chat_manager() first.")
        
        try:
            # Create a user proxy to start the conversation
            user_proxy = self.create_user_proxy_agent(
                name="User",
                human_input_mode="NEVER",
                max_consecutive_auto_reply=0
            )
            
            result = user_proxy.initiate_chat(
                self.group_chat_manager,
                message=message,
                max_turns=max_turns,
                **kwargs
            )
            
            # Store in history
            self.history.append({
                "type": "group_chat",
                "message": message,
                "result": result
            })
            
            return result
            
        except Exception as e:
            print(f"Error in group chat: {e}")
            return {"error": str(e)}
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available Euri models.
        
        Returns:
            List of available models
        """
        return [
            "gpt-4.1-nano",
            "gpt-4.1-turbo",
            "gpt-4.1-preview",
            "claude-3-5-sonnet",
            "claude-3-5-haiku",
            "gemini-2.5-flash",
            "gemini-2.5-pro"
        ]
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get chat history.
        
        Returns:
            List of chat history entries
        """
        return self.history
    
    def reset(self):
        """
        Reset agents, group chat, and history.
        """
        self.agents = []
        self.group_chat = None
        self.group_chat_manager = None
        self.history = []
    
    def create_config_list(
        self,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        Create a configuration list for manual agent creation.
        
        Args:
            model: Euri model name
            temperature: Model temperature
            max_tokens: Maximum tokens
            
        Returns:
            Configuration list for AutoGen
        """
        return [{
            "model": model,
            "model_client_cls": "EuriaiModelClient",
            "api_key": self.api_key,
            "temperature": temperature,
            "max_tokens": max_tokens
        }] 