"""High-level client for the QV Ollama SDK."""

from typing import Optional, Dict, Any, List, Iterator, Callable

from .domain.models import (
    Conversation,
    ModelParameters,
    MessageRole,
    GenerationResponse,
    ToolCall,
    ToolResult,
    ToolRegistry
)
from .services.ollama_conversation_service import OllamaConversationService


class OllamaChatClient:
    """A simplified client for chat interactions with Ollama models."""
    
    def __init__(
        self,
        model_name: str = "gemma2:2b",
        system_message: Optional[str] = None,
        parameters: Optional[ModelParameters] = None
    ):
        """Initialize the Ollama chat client.
        
        Args:
            model_name: The name of the model to use
            system_message: Optional system message to set the context
            parameters: Optional model parameters to use for generation
        """
        self.conversation = Conversation(model_name=model_name)
        self.service = OllamaConversationService()
        self.parameters = parameters or ModelParameters()
        self.tool_registry = ToolRegistry()  # Client's own tool registry
        
        # Add system message if provided
        if system_message:
            self.conversation.add_system_message(system_message)
    
    def chat(self, message: str, tools: Optional[List[Callable]] = None, auto_execute: bool = True) -> GenerationResponse:
        """Send a message and get a response.
        
        Args:
            message: The user message to send
            tools: Optional list of Python functions that can be called by the model
            auto_execute: Whether to automatically execute tool calls (default: True)
            
        Returns:
            A GenerationResponse containing content, thinking, tool calls, and results
        """
        # Add the user message
        self.conversation.add_user_message(message)
        
        if tools and auto_execute:
            # Generate response with automatic tool execution
            response = self.service.generate_response_with_tool_execution(
                self.conversation, self.parameters, tools, auto_execute=True, tool_registry=self.tool_registry
            )
        
            # Add the assistant's response to the conversation (including tool calls)
            assistant_message = self.conversation.add_assistant_message(response.content)
            if response.tool_calls:
                assistant_message.tool_calls = response.tool_calls
            
            # Add tool result messages if any
            if response.tool_results:
                self.conversation.add_tool_results(response.tool_results)
                
            return response
        else:
            # Generate a response without automatic tool execution
            response = self.service.generate_response(self.conversation, self.parameters, tools)
            
            # Add the assistant's response to the conversation (including tool calls)
            assistant_message = self.conversation.add_assistant_message(response.content)
            if response.tool_calls:
                assistant_message.tool_calls = response.tool_calls
            
            return response
    
    def stream_chat(self, message: str, tools: Optional[List[Callable]] = None, auto_execute: bool = True) -> Iterator[GenerationResponse]:
        """Send a message and stream the response.
        
        Args:
            message: The user message to send
            tools: Optional list of Python functions that can be called by the model
            auto_execute: Whether to automatically execute tool calls (default: True)
            
        Yields:
            GenerationResponse chunks as they become available, including content, thinking, and tool calls
        """
        # Add the user message
        self.conversation.add_user_message(message)
        
        if tools and auto_execute:
            # Collect responses for conversation history
            initial_content = ""
            final_content = ""
            all_tool_calls = []
            all_tool_results = []
            
            # Stream with automatic tool execution
            for chunk in self.service.stream_response_with_tool_execution(
                self.conversation, self.parameters, tools, auto_execute=True, tool_registry=self.tool_registry
            ):
                # Handle tool execution results
                if chunk.tool_results:
                    all_tool_results.extend(chunk.tool_results)
                
                # Handle content chunks
                if chunk.content:
                    if chunk.tool_calls or all_tool_calls:
                        initial_content += chunk.content
                    else:
                        final_content += chunk.content
                
                # Collect tool calls
                if chunk.tool_calls:
                    all_tool_calls.extend(chunk.tool_calls)
                
                yield chunk
            
            # Add messages to conversation history
            if initial_content or all_tool_calls:
                assistant_message = self.conversation.add_assistant_message(initial_content)
                if all_tool_calls:
                    assistant_message.tool_calls = all_tool_calls
            
            if all_tool_results:
                self.conversation.add_tool_results(all_tool_results)
            
            # If we have a final response, add it too
            if final_content:
                self.conversation.add_assistant_message(final_content)
        else:
            # Collect the full response and tool calls for conversation history
            full_response = ""
            all_tool_calls = []
        
            # Stream the response without automatic tool execution
            for chunk in self.service.stream_response(self.conversation, self.parameters, tools):
                if chunk.content:
                    full_response += chunk.content
                
                # Collect tool calls from chunks
                if chunk.tool_calls:
                    all_tool_calls.extend(chunk.tool_calls)
                yield chunk
        
            # Add the assistant's response to the conversation (including tool calls)
            assistant_message = self.conversation.add_assistant_message(full_response)
            if all_tool_calls:
                assistant_message.tool_calls = all_tool_calls
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get the conversation history.
        
        Returns:
            The conversation history as a list of message dictionaries
        """
        return self.conversation.get_message_history()
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation.clear()
    
    def set_system_message(self, message: str) -> None:
        """Set or update the system message.
        
        Args:
            message: The system message to set
        """
        # Clear existing system messages
        self.conversation.messages = [
            msg for msg in self.conversation.messages 
            if msg.role != MessageRole.SYSTEM
        ]
        
        # Add the new system message
        self.conversation.add_system_message(message)
    
    def set_parameters(self, **kwargs) -> None:
        """Update model parameters.
        
        Args:
            **kwargs: Parameter values to update
        """
        # Set each parameter individually
        for key, value in kwargs.items():
            setattr(self.parameters, key, value)
    
    # Convenience properties for common parameters
    
    @property
    def temperature(self) -> float:
        """Get the current temperature parameter if set."""
        try:
            return self.parameters.temperature
        except AttributeError:
            return None
        
    @temperature.setter
    def temperature(self, value: float) -> None:
        """Set the temperature parameter."""
        self.set_parameters(temperature=value)
    
    @property
    def max_tokens(self) -> int:
        """Get the current max_tokens parameter if set."""
        try:
            return self.parameters.max_tokens
        except AttributeError:
            return None
        
    @max_tokens.setter
    def max_tokens(self, value: int) -> None:
        """Set the max_tokens parameter."""
        self.set_parameters(max_tokens=value)
    
    @property
    def top_p(self) -> float:
        """Get the current top_p parameter if set."""
        try:
            return self.parameters.top_p
        except AttributeError:
            return None
        
    @top_p.setter
    def top_p(self, value: float) -> None:
        """Set the top_p parameter."""
        self.set_parameters(top_p=value)
    
    @property
    def num_ctx(self) -> int:
        """Get the current context window size if set."""
        try:
            return self.parameters.num_ctx
        except AttributeError:
            return None
        
    @num_ctx.setter
    def num_ctx(self, value: int) -> None:
        """Set the context window size."""
        self.set_parameters(num_ctx=value)
    
    @property
    def thinking_mode(self) -> bool:
        """Get the current thinking mode setting."""
        try:
            return self.parameters.think
        except AttributeError:
            return False
        
    @thinking_mode.setter
    def thinking_mode(self, value: bool) -> None:
        """Enable or disable thinking mode."""
        self.set_parameters(think=value)
    
    def enable_thinking(self) -> None:
        """Enable thinking mode for supported models."""
        self.thinking_mode = True
    
    def disable_thinking(self) -> None:
        """Disable thinking mode."""
        self.thinking_mode = False
    
    def register_mcp_executor(self, tool_name: str, executor: Any) -> None:
        """Register an MCP executor for a specific tool."""
        self.tool_registry.register_mcp_executor(tool_name, executor) 