from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import List, Optional, Dict, Any, Callable
from uuid import UUID, uuid4


class MessageRole(str, Enum):
    """Enumeration of possible message roles in a conversation."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class Function:
    """Represents a function definition for tool calling."""
    name: str
    arguments: Dict[str, Any]


@dataclass 
class ToolCall:
    """Represents a tool call made by the model."""
    function: Function
    id: Optional[str] = None  # Tool call ID for tracking


@dataclass
class ToolResult:
    """Represents the result of executing a tool call."""
    tool_call_id: Optional[str]
    function_name: str
    result: Any
    error: Optional[str] = None
    execution_time: Optional[float] = None


@dataclass
class ToolRegistry:
    """Registry of available functions for tool execution."""
    functions: Dict[str, Callable] = field(default_factory=dict)
    mcp_executors: Dict[str, Any] = field(default_factory=dict)  # MCP tool executors
    
    def register(self, func: Callable) -> None:
        """Register a function for tool calling."""
        self.functions[func.__name__] = func
    
    def get_function(self, name: str) -> Optional[Callable]:
        """Get a registered function by name."""
        return self.functions.get(name)
    
    def register_mcp_executor(self, tool_name: str, executor: Any) -> None:
        """Register an MCP executor for a specific tool."""
        self.mcp_executors[tool_name] = executor
    
    def execute_tool_call(self, tool_call: ToolCall) -> ToolResult:
        """Execute a tool call and return the result."""
        function_name = tool_call.function.name
        
        # Check if tool has MCP executor first
        if function_name in self.mcp_executors:
            try:
                executor = self.mcp_executors[function_name]
                
                # Threading wrapper to avoid deadlocks with async MCP execution
                import asyncio
                import threading
                
                result_container = []
                
                def thread_target():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        result = loop.run_until_complete(executor.execute_tool_call(tool_call))
                        result_container.append(result)
                    finally:
                        loop.close()
                
                thread = threading.Thread(target=thread_target)
                thread.start()
                thread.join(timeout=30)  # 30 second timeout
                
                return ToolResult(
                    tool_call_id=tool_call.id,
                    function_name=function_name,
                    result=result_container[0] if result_container else None,
                    error=None
                )
            except Exception as e:
                return ToolResult(
                    tool_call_id=tool_call.id,
                    function_name=function_name,
                    result=None,
                    error=f"MCP execution failed: {str(e)}"
                )
        
        # Fall back to regular Python function execution
        function = self.get_function(function_name)
        
        if not function:
            return ToolResult(
                tool_call_id=tool_call.id,
                function_name=function_name,
                result=None,
                error=f"Function '{function_name}' not found in registry"
            )
        
        try:
            # Execute the function with type casting for safety
            args = tool_call.function.arguments
            # Cast numeric arguments to appropriate types
            casted_args = {}
            for key, value in args.items():
                if isinstance(value, str) and value.isdigit():
                    casted_args[key] = int(value)
                elif isinstance(value, str):
                    try:
                        casted_args[key] = float(value)
                    except ValueError:
                        casted_args[key] = value
                else:
                    casted_args[key] = value
            
            result = function(**casted_args)
            return ToolResult(
                tool_call_id=tool_call.id,
                function_name=function_name,
                result=result,
                error=None
            )
        except Exception as e:
            return ToolResult(
                tool_call_id=tool_call.id,
                function_name=function_name,
                result=None,
                error=str(e)
            )


@dataclass
class Message:
    """Represents a single message in a conversation."""
    role: MessageRole
    content: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    tool_calls: Optional[List[ToolCall]] = None
    tool_call_id: Optional[str] = None  # For tool result messages
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to a dictionary format for the Ollama API."""
        message_dict = {
            "role": self.role.value,
            "content": self.content
        }
        
        # Add tool_calls for assistant messages
        if self.tool_calls:
            message_dict["tool_calls"] = [
                {
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in self.tool_calls
            ]
        
        # Add tool call reference for tool result messages
        if self.role == MessageRole.TOOL and self.tool_call_id:
            message_dict["tool_call_id"] = self.tool_call_id
        
        return message_dict
    
    def to_db_dict(self) -> Dict[str, Any]:
        """Convert message to a dictionary format for database storage."""
        db_dict = {
            "id": str(self.id),
            "role": self.role.value,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }
        
        if self.tool_calls:
            db_dict["tool_calls"] = [
                {
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    },
                    "id": tc.id
                }
                for tc in self.tool_calls
            ]
        
        if self.tool_call_id:
            db_dict["tool_call_id"] = self.tool_call_id
        
        return db_dict
    
    @classmethod
    def from_db_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create a Message instance from database dictionary format."""
        tool_calls = None
        if "tool_calls" in data and data["tool_calls"]:
            tool_calls = [
                ToolCall(
                    function=Function(
                        name=tc["function"]["name"],
                        arguments=tc["function"]["arguments"]
                    ),
                    id=tc.get("id")
                )
                for tc in data["tool_calls"]
            ]
        
        return cls(
            id=UUID(data["id"]),
            role=MessageRole(data["role"]),
            content=data["content"],
            created_at=datetime.fromisoformat(data["created_at"]),
            metadata=data.get("metadata", {}),
            tool_calls=tool_calls,
            tool_call_id=data.get("tool_call_id")
        )


@dataclass
class Conversation:
    """Represents a complete conversation consisting of multiple messages."""
    model_name: str = "llama3"
    id: UUID = field(default_factory=uuid4)
    title: Optional[str] = None
    messages: List[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_system_message(self, content: str) -> Message:
        """Add a system message to the conversation."""
        message = Message(role=MessageRole.SYSTEM, content=content)
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message
    
    def add_user_message(self, content: str) -> Message:
        """Add a user message to the conversation."""
        message = Message(role=MessageRole.USER, content=content)
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message
    
    def add_assistant_message(self, content: str) -> Message:
        """Add an assistant message to the conversation."""
        message = Message(role=MessageRole.ASSISTANT, content=content)
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message
    
    def add_tool_message(self, content: str, tool_call_id: str, function_name: str) -> Message:
        """Add a tool result message to the conversation."""
        message = Message(
            role=MessageRole.TOOL, 
            content=content,
            tool_call_id=tool_call_id,
            metadata={"function_name": function_name}
        )
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message
    
    def add_tool_results(self, tool_results: List[ToolResult]) -> List[Message]:
        """Add multiple tool result messages to the conversation."""
        messages = []
        for result in tool_results:
            if result.error:
                content = f"Error executing {result.function_name}: {result.error}"
            else:
                content = str(result.result)
            
            message = self.add_tool_message(
                content=content,
                tool_call_id=result.tool_call_id or "",
                function_name=result.function_name
            )
            messages.append(message)
        return messages
    
    def get_message_history(self) -> List[Dict[str, str]]:
        """Get the message history in a format suitable for the Ollama API."""
        return [message.to_dict() for message in self.messages]
    
    def clear(self) -> None:
        """Clear all messages from the conversation."""
        self.messages.clear()
        self.updated_at = datetime.now()
    
    def to_db_dict(self) -> Dict[str, Any]:
        """Convert conversation to a dictionary format for database storage.
        
        Note: Messages are stored separately and not included in this output.
        """
        return {
            "id": str(self.id),
            "model_name": self.model_name,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_db_dict(cls, data: Dict[str, Any]) -> 'Conversation':
        """Create a Conversation instance from database dictionary format.
        
        Note: Messages must be loaded separately and added to the conversation.
        """
        return cls(
            id=UUID(data["id"]),
            model_name=data["model_name"],
            title=data.get("title"),
            messages=[],  # Messages are loaded separately
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            metadata=data.get("metadata", {})
        )


class ModelParameters:
    """Parameters for controlling model generation behavior.
    
    Only parameters that are explicitly set will be sent to the API.
    The Ollama API will use its own defaults for any parameters not specified.
    
    Common parameters:
        temperature: Controls randomness. Higher values make output more random.
        max_tokens: Maximum number of tokens to generate.
        top_p: Nucleus sampling parameter.
        top_k: Limits token selection to top k options.
        stop: Sequences where the model should stop generating.
        frequency_penalty: Penalize frequent tokens.
        presence_penalty: Penalize tokens already used.
        repeat_penalty: How strongly to penalize repetitions.
        num_ctx: Context window size.
        think: Enable thinking mode for supported models.
        
    Any model-specific parameters can be provided through the constructor.
    """

    def __init__(self, **kwargs):
        """Initialize model parameters.
        
        Args:
            **kwargs: Parameter values to set. Only parameters explicitly
                     set here will be sent to the API.
        
        Common parameters include:
            temperature: Controls randomness (0.0-2.0)
            max_tokens: Maximum number of tokens to generate
            top_p: Nucleus sampling parameter (0.0-1.0) 
            top_k: Limits token selection to top k options
            stop: Sequences where the model should stop generating
            frequency_penalty: Penalize frequent tokens (0.0-2.0)
            presence_penalty: Penalize tokens already used (0.0-2.0)
            repeat_penalty: How strongly to penalize repetitions
            num_ctx: Context window size
            think: Enable thinking mode for supported models (True/False)
        """
        # Store parameters that were explicitly set
        self._parameters = {}
        
        # Common parameters
        self._common_params = [
            'temperature', 'max_tokens', 'top_p', 'top_k', 'stop',
            'frequency_penalty', 'presence_penalty', 'repeat_penalty', 'num_ctx', 'think'
        ]
        
        # Set provided parameters
        for key, value in kwargs.items():
            self._parameters[key] = value
        
    def __getattr__(self, name):
        """Get a parameter value."""
        if name in self._parameters:
            return self._parameters[name]
        raise AttributeError(f"'ModelParameters' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        """Set a parameter value."""
        if name.startswith('_'):
            # Private attributes
            super().__setattr__(name, value)
        else:
            # Parameters
            self._parameters[name] = value
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert parameters to a dictionary for API requests.
        
        Returns:
            Dictionary of explicitly set parameters
        """
        params = {}
        
        # Map special parameter names to their API equivalents
        api_param_mapping = {
            'max_tokens': 'num_predict'
        }
        
        for key, value in self._parameters.items():
            # Use API-specific name if it exists
            api_key = api_param_mapping.get(key, key)
            params[api_key] = value
            
        return params


@dataclass
class GenerationResponse:
    """Represents a response from the model generation."""
    model_name: str
    content: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    raw_response: Optional[Dict[str, Any]] = None
    finish_reason: Optional[str] = None
    usage: Optional[Dict[str, int]] = None 
    tool_calls: Optional[List[ToolCall]] = None
    tool_results: Optional[List[ToolResult]] = None
    thinking: Optional[str] = None  # Model's thinking process (thinking mode) 