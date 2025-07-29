"""Test script to validate A2A protocol compliance of Arc Multi-Agent Hub.

This script tests all standard A2A methods and validates our implementation
against the A2A v0.2.5 specification.
"""

import asyncio
import json
import uuid
from datetime import datetime
from pathlib import Path

# Add parent directory to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from arc_advisor.a2a_compliant_protocols import (
    JSONRPCRequest,
    Message,
    TextPart,
    DataPart,
    MessageSendParams,
    MessageSendConfiguration,
    TaskQueryParams,
    TaskIdParams,
    ArcAgentCard,
    AgentCapabilities,
    AgentSkill,
    ArcExtension
)
from arc_advisor.a2a_multi_agent_hub import ArcA2AMultiAgentHub


async def test_agent_registration():
    """Test agent registration with Arc hub."""
    print("\n=== Testing Agent Registration ===")
    
    hub = ArcA2AMultiAgentHub()
    
    # Create test agent card
    agent_card = ArcAgentCard(
        name="test-agent-001",
        description="Test agent for A2A compliance validation",
        url="http://localhost:8080/a2a",
        version="1.0.0",
        skills=[
            AgentSkill(
                id="code-generation",
                name="Code Generation",
                description="Generate code in multiple languages",
                tags=["coding", "generation"]
            )
        ],
        defaultInputModes=["text", "data"],
        defaultOutputModes=["text", "data", "file"],
        capabilities=AgentCapabilities(
            streaming=True,
            pushNotifications=True,
            extensions=[ArcExtension()]
        )
    )
    
    # Test registration
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "arc/agent/register",
        "params": {
            "agent_card": agent_card.model_dump()
        }
    }
    
    response = await hub.handle_jsonrpc_message(request, "test-agent-001")
    print(f"Registration response: {json.dumps(response, indent=2)}")
    
    assert response.get("result", {}).get("status") == "registered"
    return hub


async def test_message_send():
    """Test standard A2A message/send method."""
    print("\n=== Testing message/send ===")
    
    hub = await test_agent_registration()
    
    # Create test message
    message = Message(
        role="user",
        parts=[
            TextPart(text="Analyze this Python code for potential bugs"),
            DataPart(
                data={
                    "code": "def divide(a, b): return a / b",
                    "language": "python"
                }
            )
        ]
    )
    
    request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "message/send",
        "params": {
            "message": message.model_dump(),
            "configuration": {
                "acceptedOutputModes": ["text", "data"]
            }
        }
    }
    
    response = await hub.handle_jsonrpc_message(request, "test-agent-001")
    print(f"Message send response: {json.dumps(response, indent=2)}")
    
    assert "result" in response
    assert "id" in response["result"]
    return hub, response["result"]["id"]


async def test_task_get():
    """Test standard A2A tasks/get method."""
    print("\n=== Testing tasks/get ===")
    
    hub, task_id = await test_message_send()
    
    request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tasks/get",
        "params": {
            "id": task_id
        }
    }
    
    response = await hub.handle_jsonrpc_message(request, "test-agent-001")
    print(f"Task get response: {json.dumps(response, indent=2)}")
    
    assert "result" in response
    assert response["result"]["id"] == task_id
    return hub, task_id


async def test_task_cancel():
    """Test standard A2A tasks/cancel method."""
    print("\n=== Testing tasks/cancel ===")
    
    hub, task_id = await test_task_get()
    
    request = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tasks/cancel",
        "params": {
            "id": task_id
        }
    }
    
    response = await hub.handle_jsonrpc_message(request, "test-agent-001")
    print(f"Task cancel response: {json.dumps(response, indent=2)}")
    
    assert "result" in response
    assert response["result"]["status"] == "canceled"
    return hub


async def test_message_stream():
    """Test standard A2A message/stream method."""
    print("\n=== Testing message/stream ===")
    
    hub = await test_agent_registration()
    
    # Create Arc advice request message
    message = Message(
        role="user",
        parts=[
            DataPart(
                data={
                    "type": "ArcAdviceRequest",
                    "agent_id": "test-agent-001",
                    "task_description": "Implement a rate limiter in Python",
                    "context": {
                        "language": "python",
                        "requirements": ["thread-safe", "configurable limits"]
                    }
                }
            )
        ],
        extensions=["https://arc.computer/extensions/learning/v1"]
    )
    
    request = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "message/stream",
        "params": {
            "message": message.model_dump(),
            "configuration": {
                "acceptedOutputModes": ["text", "data"]
            }
        }
    }
    
    response = await hub.handle_jsonrpc_message(request, "test-agent-001")
    print(f"Message stream response: {json.dumps(response, indent=2)}")
    
    assert "result" in response
    assert "streamUrl" in response["result"]
    assert "taskId" in response["result"]
    
    # Wait a bit for streaming to process
    await asyncio.sleep(2)
    return hub


async def test_arc_advice_request():
    """Test Arc-specific advice request."""
    print("\n=== Testing Arc Advice Request ===")
    
    hub = await test_agent_registration()
    
    request = {
        "jsonrpc": "2.0",
        "id": 6,
        "method": "arc/advice/request",
        "params": {
            "task_description": "Optimize database query performance",
            "context": {
                "database": "PostgreSQL",
                "query_type": "complex joins",
                "table_sizes": "millions of rows"
            },
            "previous_attempts": []
        }
    }
    
    response = await hub.handle_jsonrpc_message(request, "test-agent-001")
    print(f"Arc advice response: {json.dumps(response, indent=2)}")
    
    assert "result" in response
    assert "strategy" in response["result"]
    assert "confidence_score" in response["result"]
    return hub


async def test_bidirectional_query():
    """Test Arc bidirectional advisor query."""
    print("\n=== Testing Bidirectional Query ===")
    
    hub = await test_agent_registration()
    
    request = {
        "jsonrpc": "2.0",
        "id": 7,
        "method": "arc/advisor/query",
        "params": {
            "query_type": "pattern_analysis",
            "query_context": {
                "error_type": "database_connection",
                "frequency": "intermittent"
            },
            "limit": 5,
            "min_confidence": 0.7
        }
    }
    
    response = await hub.handle_jsonrpc_message(request, "test-agent-001")
    print(f"Advisor query response: {json.dumps(response, indent=2)}")
    
    assert "result" in response
    assert "insights" in response["result"]
    assert "confidence_score" in response["result"]
    return hub


async def test_reward_signal():
    """Test Arc reward signal submission."""
    print("\n=== Testing Reward Signal ===")
    
    hub = await test_agent_registration()
    
    request = {
        "jsonrpc": "2.0",
        "id": 8,
        "method": "arc/reward/submit",
        "params": {
            "advisor_trace_id": str(uuid.uuid4()),
            "task_trace_id": str(uuid.uuid4()),
            "task_success": True,
            "advice_followed": True,
            "advice_quality_score": 0.9,
            "context_relevance": 0.85,
            "context_clarity": 0.9,
            "context_actionability": 0.95,
            "agent_confidence_before": 0.6,
            "agent_confidence_after": 0.9,
            "execution_time_ms": 1500
        }
    }
    
    response = await hub.handle_jsonrpc_message(request, "test-agent-001")
    print(f"Reward signal response: {json.dumps(response, indent=2)}")
    
    assert "result" in response
    assert response["result"]["status"] == "recorded"
    return hub


async def test_error_handling():
    """Test A2A error handling."""
    print("\n=== Testing Error Handling ===")
    
    hub = ArcA2AMultiAgentHub()
    
    # Test invalid method
    request = {
        "jsonrpc": "2.0",
        "id": 9,
        "method": "invalid/method",
        "params": {}
    }
    
    response = await hub.handle_jsonrpc_message(request)
    print(f"Invalid method response: {json.dumps(response, indent=2)}")
    
    assert "error" in response
    assert response["error"]["code"] == -32601  # Method not found
    
    # Test task not found
    request = {
        "jsonrpc": "2.0",
        "id": 10,
        "method": "tasks/get",
        "params": {
            "id": "non-existent-task"
        }
    }
    
    response = await hub.handle_jsonrpc_message(request)
    print(f"Task not found response: {json.dumps(response, indent=2)}")
    
    assert "error" in response
    assert response["error"]["code"] == -32001  # Task not found


async def run_all_tests():
    """Run all A2A compliance tests."""
    print("Starting A2A Compliance Tests")
    print("============================")
    
    try:
        await test_agent_registration()
        await test_message_send()
        await test_task_get()
        await test_task_cancel()
        await test_message_stream()
        await test_arc_advice_request()
        await test_bidirectional_query()
        await test_reward_signal()
        await test_error_handling()
        
        print("\n✅ All A2A compliance tests passed!")
        print("\nHub Statistics:")
        hub = ArcA2AMultiAgentHub()
        stats = hub.get_hub_statistics()
        print(json.dumps(stats, indent=2))
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run_all_tests())