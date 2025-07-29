"""Tests for the OllamaConversationService."""

import pytest
from unittest.mock import patch, MagicMock

from src.qv_ollama_sdk.domain.models import (
    MessageRole,
    Message,
    Conversation,
    ModelParameters,
    GenerationResponse
)
from src.qv_ollama_sdk.services.ollama_conversation_service import OllamaConversationService


@pytest.fixture
def conversation():
    """Create a test conversation."""
    conversation = Conversation(model_name="llama3")
    conversation.add_system_message("You are a helpful assistant.")
    conversation.add_user_message("What is the capital of France?")
    return conversation


@pytest.fixture
def parameters():
    """Create test model parameters."""
    return ModelParameters(
        temperature=0.7,
        max_tokens=500
    )


@patch("ollama.chat")
def test_generate_response(mock_chat, conversation, parameters):
    """Test generating a response."""
    # Setup the mock
    mock_response = {
        "model": "llama3",
        "message": {
            "role": "assistant",
            "content": "The capital of France is Paris."
        },
        "done": True,
        "prompt_eval_count": {"prompt_tokens": 20, "completion_tokens": 10}
    }
    mock_chat.return_value = mock_response
    
    # Create the service and generate a response
    service = OllamaConversationService()
    response = service.generate_response(conversation, parameters)
    
    # Check the mock was called correctly
    mock_chat.assert_called_once_with(
        model=conversation.model_name,
        messages=conversation.get_message_history(),
        options=parameters.to_dict()
    )
    
    # Check the response
    assert response.model_name == "llama3"
    assert response.content == "The capital of France is Paris."
    assert response.finish_reason == True
    assert response.raw_response == mock_response


@patch("ollama.chat")
def test_stream_response(mock_chat, conversation, parameters):
    """Test streaming a response."""
    # Setup the mock
    mock_chunks = [
        {"message": {"content": "The "}},
        {"message": {"content": "capital "}},
        {"message": {"content": "of "}},
        {"message": {"content": "France "}},
        {"message": {"content": "is "}},
        {"message": {"content": "Paris."}}
    ]
    mock_chat.return_value = mock_chunks
    
    # Create the service
    service = OllamaConversationService()
    
    # Call stream_response and collect the chunks
    chunks = list(service.stream_response(conversation, parameters))
    
    # Check the mock was called correctly
    mock_chat.assert_called_once_with(
        model=conversation.model_name,
        messages=conversation.get_message_history(),
        options=parameters.to_dict(),
        stream=True
    )
    
    # Check the chunks
    assert chunks == ["The ", "capital ", "of ", "France ", "is ", "Paris."]


@patch("ollama.chat")
def test_generate_response_without_parameters(mock_chat, conversation):
    """Test generating a response without parameters."""
    # Setup the mock
    mock_response = {
        "model": "llama3",
        "message": {
            "role": "assistant",
            "content": "The capital of France is Paris."
        }
    }
    mock_chat.return_value = mock_response
    
    # Create the service and generate a response
    service = OllamaConversationService()
    response = service.generate_response(conversation)
    
    # Check the mock was called with default parameters
    mock_chat.assert_called_once()
    call_args = mock_chat.call_args[1]
    assert call_args["model"] == conversation.model_name
    assert call_args["messages"] == conversation.get_message_history()
    
    # Check the response
    assert response.model_name == "llama3"
    assert response.content == "The capital of France is Paris." 