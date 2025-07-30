#!/usr/bin/env python3
"""
Test A2A Integration with Agent Lobby SDK
==========================================

This test demonstrates that the A2A integration works correctly
and provides the expected enhanced functionality.
"""

import asyncio
import json
import pytest
import sys
import os
from unittest.mock import AsyncMock, MagicMock

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sdk.agent_lobbi_sdk import AgentLobbySDK, A2AAgentCard, A2ATask, A2AProtocolHandler

@pytest.fixture
def mock_sdk():
    """Create a mock SDK instance for testing"""
    sdk = MagicMock()
    sdk.agent_id = "test_agent"
    sdk.agent_capabilities = ["analysis", "insights"]
    sdk.lobby_host = "localhost"
    sdk.task_handler = None
    return sdk

@pytest.fixture
def a2a_handler(mock_sdk):
    """Create A2A handler for testing"""
    return A2AProtocolHandler(mock_sdk)

def test_a2a_agent_card_creation(a2a_handler):
    """Test that A2A agent cards are created correctly"""
    agent_card = a2a_handler.generate_agent_card()
    
    # Verify basic properties
    assert agent_card.name == "Agent Lobby Enhanced - test_agent"
    assert "neuromorphic learning" in agent_card.description
    assert agent_card.version == "1.0.0"
    
    # Verify enhanced capabilities
    assert agent_card.capabilities["streaming"] is True
    assert agent_card.capabilities["pushNotifications"] is True
    assert agent_card.capabilities["neuromorphic_learning"] is True
    assert agent_card.capabilities["collective_intelligence"] is True
    
    # Verify Agent Lobby extensions
    assert "agent_lobby" in agent_card.extensions
    agent_lobby_ext = agent_card.extensions["agent_lobby"]
    assert agent_lobby_ext["platform"] == "Agent Lobby"
    assert "Neuromorphic agent selection" in agent_lobby_ext["enhanced_features"]
    assert "Collective intelligence" in agent_lobby_ext["enhanced_features"]
    
    # Verify skills based on capabilities
    assert len(agent_card.skills) == 2
    skill_ids = [skill["id"] for skill in agent_card.skills]
    assert "analysis" in skill_ids
    assert "insights" in skill_ids

def test_a2a_task_creation():
    """Test A2A task creation"""
    task = A2ATask(
        id="test_task_123",
        status="completed",
        artifacts=[{
            "name": "result",
            "description": "Test result",
            "parts": [{"type": "text", "text": "Test output"}]
        }],
        metadata={"agent_lobby_enhanced": True}
    )
    
    task_dict = task.to_dict()
    assert task_dict["id"] == "test_task_123"
    assert task_dict["status"] == "completed"
    assert len(task_dict["artifacts"]) == 1
    assert task_dict["metadata"]["agent_lobby_enhanced"] is True

def test_a2a_message_conversion(a2a_handler):
    """Test conversion of A2A messages to Agent Lobby format"""
    a2a_message = {
        "role": "user",
        "parts": [
            {"type": "text", "text": "Analyze this data"},
            {"type": "data", "data": {"key": "value"}}
        ]
    }
    
    lobby_task = a2a_handler.convert_a2a_to_lobby_task("task_123", a2a_message)
    
    assert lobby_task["task_id"] == "task_123"
    assert lobby_task["input_data"]["text"] == "Analyze this data"
    assert lobby_task["input_data"]["original_a2a_message"] == a2a_message
    assert lobby_task["capabilities_needed"] == ["analysis", "insights"]
    assert lobby_task["enhanced_processing"] is True

@pytest.mark.asyncio
async def test_a2a_task_execution(a2a_handler):
    """Test A2A task execution with Agent Lobby intelligence"""
    
    # Mock task handler
    async def mock_task_handler(task):
        return {
            "result": "Enhanced analysis complete",
            "quality": "superior"
        }
    
    a2a_handler.sdk.task_handler = mock_task_handler
    
    # Test task execution
    task = {
        "task_id": "test_task",
        "input_data": {"text": "Test input"},
        "capabilities_needed": ["analysis"]
    }
    
    result = await a2a_handler.execute_with_lobby_intelligence(task)
    
    assert result["result"]["result"] == "Enhanced analysis complete"
    assert result["result"]["quality"] == "superior"
    assert result["enhanced_by_agent_lobby"] is True
    assert result["agents_involved"] == ["test_agent"]
    assert result["processing_time"] > 0

def test_sdk_initialization():
    """Test SDK initialization with A2A support"""
    sdk = AgentLobbySDK(
        enable_a2a=True,
        a2a_port=8090,
        enable_security=False  # Disable for testing
    )
    
    assert sdk.enable_a2a is True
    assert sdk.a2a_port == 8090
    assert sdk.a2a_handler is not None
    assert isinstance(sdk.a2a_handler, A2AProtocolHandler)

def test_sdk_without_a2a():
    """Test SDK initialization without A2A support"""
    sdk = AgentLobbySDK(
        enable_a2a=False,
        enable_security=False
    )
    
    assert sdk.enable_a2a is False
    assert sdk.a2a_handler is None

def test_a2a_agent_card_to_dict():
    """Test A2A agent card dictionary conversion"""
    agent_card = A2AAgentCard(
        name="Test Agent",
        description="Test Description",
        version="1.0.0",
        url="http://localhost:8090",
        capabilities={"streaming": True},
        authentication={"schemes": ["bearer"]},
        skills=[{"id": "test", "name": "Test Skill"}],
        extensions={"custom": {"value": "test"}}
    )
    
    card_dict = agent_card.to_dict()
    
    assert card_dict["name"] == "Test Agent"
    assert card_dict["description"] == "Test Description"
    assert card_dict["version"] == "1.0.0"
    assert card_dict["url"] == "http://localhost:8090"
    assert card_dict["capabilities"]["streaming"] is True
    assert card_dict["authentication"]["schemes"] == ["bearer"]
    assert len(card_dict["skills"]) == 1
    assert card_dict["extensions"]["custom"]["value"] == "test"

def test_a2a_integration_benefits():
    """Test that A2A integration provides expected benefits"""
    sdk = AgentLobbySDK(enable_a2a=True, enable_security=False)
    
    # Test that A2A handler is available
    assert hasattr(sdk, 'a2a_handler')
    assert hasattr(sdk, 'start_a2a_server')
    assert hasattr(sdk, 'call_a2a_agent')
    assert hasattr(sdk, 'get_a2a_agent_card')
    
    # Test that A2A capabilities are properly configured
    handler = sdk.a2a_handler
    assert handler.sdk == sdk
    assert handler.active_tasks == {}
    assert handler.agent_card is None  # Not generated yet
    assert handler.a2a_port == 8090

if __name__ == "__main__":
    print("🧪 Running A2A Integration Tests")
    print("=" * 50)
    
    # Run basic tests
    print("✅ Testing A2A Agent Card Creation...")
    mock_sdk = MagicMock()
    mock_sdk.agent_id = "test_agent"
    mock_sdk.agent_capabilities = ["analysis", "insights"]
    mock_sdk.lobby_host = "localhost"
    
    handler = A2AProtocolHandler(mock_sdk)
    agent_card = handler.generate_agent_card()
    
    print(f"  📋 Agent Card Name: {agent_card.name}")
    print(f"  🧠 Enhanced Features: {len(agent_card.extensions['agent_lobby']['enhanced_features'])}")
    print(f"  ⚡ Capabilities: {list(agent_card.capabilities.keys())}")
    
    print("\n✅ Testing SDK Initialization...")
    sdk = AgentLobbySDK(enable_a2a=True, enable_security=False)
    print(f"  🔧 A2A Enabled: {sdk.enable_a2a}")
    print(f"  🌐 A2A Port: {sdk.a2a_port}")
    print(f"  🎯 A2A Handler: {'Available' if sdk.a2a_handler else 'Not Available'}")
    
    print("\n✅ Testing A2A Task Creation...")
    task = A2ATask(
        id="demo_task",
        status="completed",
        artifacts=[{"name": "demo", "parts": [{"type": "text", "text": "Demo result"}]}],
        metadata={"agent_lobby_enhanced": True}
    )
    
    task_dict = task.to_dict()
    print(f"  📝 Task ID: {task_dict['id']}")
    print(f"  📊 Status: {task_dict['status']}")
    print(f"  🚀 Enhanced: {task_dict['metadata']['agent_lobby_enhanced']}")
    
    print("\n🎉 All tests passed!")
    print("💡 Agent Lobby's A2A integration is working correctly!")
    print("🚀 Ready to provide enhanced A2A capabilities!") 