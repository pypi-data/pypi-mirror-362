"""Tests for the domain models."""

import pytest
from datetime import datetime
from uuid import UUID

from src.qv_ollama_sdk.domain.models import (
    MessageRole,
    Message,
    Conversation,
    ModelParameters,
    GenerationResponse
)


def test_message_creation():
    """Test creating a message."""
    message = Message(role=MessageRole.USER, content="Hello")
    
    assert isinstance(message.id, UUID)
    assert message.role == MessageRole.USER
    assert message.content == "Hello"
    assert isinstance(message.created_at, datetime)
    assert isinstance(message.metadata, dict)


def test_message_to_dict():
    """Test converting a message to a dictionary."""
    message = Message(role=MessageRole.SYSTEM, content="You are a helpful assistant.")
    
    message_dict = message.to_dict()
    assert message_dict["role"] == "system"
    assert message_dict["content"] == "You are a helpful assistant."


def test_conversation_creation():
    """Test creating a conversation."""
    conversation = Conversation(model_name="llama3")
    
    assert isinstance(conversation.id, UUID)
    assert conversation.model_name == "llama3"
    assert conversation.messages == []
    assert isinstance(conversation.created_at, datetime)
    assert isinstance(conversation.updated_at, datetime)
    assert isinstance(conversation.metadata, dict)


def test_conversation_add_messages():
    """Test adding messages to a conversation."""
    conversation = Conversation(model_name="llama3")
    
    system_msg = conversation.add_system_message("You are a helpful assistant.")
    assert len(conversation.messages) == 1
    assert conversation.messages[0].role == MessageRole.SYSTEM
    assert conversation.messages[0].content == "You are a helpful assistant."
    
    user_msg = conversation.add_user_message("Hello")
    assert len(conversation.messages) == 2
    assert conversation.messages[1].role == MessageRole.USER
    assert conversation.messages[1].content == "Hello"
    
    assistant_msg = conversation.add_assistant_message("Hi there!")
    assert len(conversation.messages) == 3
    assert conversation.messages[2].role == MessageRole.ASSISTANT
    assert conversation.messages[2].content == "Hi there!"


def test_conversation_get_message_history():
    """Test getting the message history from a conversation."""
    conversation = Conversation(model_name="llama3")
    
    conversation.add_system_message("You are a helpful assistant.")
    conversation.add_user_message("Hello")
    conversation.add_assistant_message("Hi there!")
    
    history = conversation.get_message_history()
    
    assert len(history) == 3
    assert history[0]["role"] == "system"
    assert history[0]["content"] == "You are a helpful assistant."
    assert history[1]["role"] == "user"
    assert history[1]["content"] == "Hello"
    assert history[2]["role"] == "assistant"
    assert history[2]["content"] == "Hi there!"


def test_conversation_clear():
    """Test clearing a conversation."""
    conversation = Conversation(model_name="llama3")
    
    conversation.add_system_message("You are a helpful assistant.")
    conversation.add_user_message("Hello")
    
    assert len(conversation.messages) == 2
    
    conversation.clear()
    
    assert len(conversation.messages) == 0


def test_model_parameters_creation():
    """Test creating model parameters."""
    params = ModelParameters(
        temperature=0.5,
        top_p=0.8,
        max_tokens=1000
    )
    
    assert params.temperature == 0.5
    assert params.top_p == 0.8
    assert params.max_tokens == 1000
    assert params.stop_sequences == []


def test_model_parameters_to_dict():
    """Test converting model parameters to a dictionary."""
    params = ModelParameters(
        temperature=0.5,
        top_p=0.8,
        max_tokens=1000,
        stop_sequences=["END", "STOP"]
    )
    
    params_dict = params.to_dict()
    
    assert params_dict["temperature"] == 0.5
    assert params_dict["top_p"] == 0.8
    assert params_dict["max_tokens"] == 1000
    assert params_dict["stop"] == ["END", "STOP"]


def test_generation_response_creation():
    """Test creating a generation response."""
    response = GenerationResponse(
        model_name="llama3",
        content="Hello, how can I help you?",
        finish_reason="stop",
        usage={"prompt_tokens": 10, "completion_tokens": 8}
    )
    
    assert isinstance(response.id, UUID)
    assert response.model_name == "llama3"
    assert response.content == "Hello, how can I help you?"
    assert response.finish_reason == "stop"
    assert response.usage == {"prompt_tokens": 10, "completion_tokens": 8}
    assert isinstance(response.created_at, datetime) 