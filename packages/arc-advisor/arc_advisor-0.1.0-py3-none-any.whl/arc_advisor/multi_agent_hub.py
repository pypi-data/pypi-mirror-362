"""A2A-compliant Multi-Agent Hub for Arc Advisory System.

This module implements a fully A2A-compliant hub that enables bidirectional
communication between production agents and the Arc Sub Agent advisor.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set, Any, Callable, Union
from pathlib import Path
import uuid
from collections import defaultdict

from .tool_advisor import ToolAugmentedAdvisor
from .protocols import (
    JSONRPCRequest,
    JSONRPCSuccessResponse,
    JSONRPCErrorResponse,
    JSONRPCError,
    Message,
    TextPart,
    DataPart,
    Task,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
    TaskArtifactUpdateEvent,
    A2AErrorCodes,
    MessageSendParams,
    MessageSendConfiguration,
    TaskQueryParams,
    TaskIdParams,
    ArcAdviceMessage,
    ArcLearningReportMessage,
    ArcImprovementRequestMessage,
    ArcAgentCard,
    ArcAdviceArtifact,
    is_arc_message
)

logger = logging.getLogger("ArcA2AHub")


class A2AAgentConnection:
    """Represents a connected A2A agent with bidirectional communication."""
    
    def __init__(self, agent_card: ArcAgentCard, websocket=None):
        self.agent_card = agent_card
        self.agent_id = agent_card.name  # Using name as ID per A2A spec
        self.websocket = websocket
        self.registration_time = datetime.utcnow()
        self.last_activity = datetime.utcnow()
        self.active_tasks: Set[str] = set()
        self.push_notification_configs: Dict[str, Any] = {}
        self.metrics = {
            "total_requests": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "advice_requests": 0,
            "improvements_reported": 0
        }


class ArcA2AMultiAgentHub:
    """A2A-compliant hub enabling bidirectional agent-advisor communication.
    
    Key Features:
    - Full A2A protocol compliance with JSON-RPC 2.0
    - Bidirectional communication between agents and advisor
    - Real-time learning and pattern sharing
    - Rich reward signal collection for GRPO training
    - Autonomous agent collaboration
    """
    
    def __init__(
        self,
        hub_id: str = "arc-a2a-hub-001",
        advisor: Optional[ToolAugmentedAdvisor] = None,
        enable_auto_broadcast: bool = True,
        enable_bidirectional: bool = True
    ):
        """Initialize the A2A-compliant Arc hub.
        
        Args:
            hub_id: Unique identifier for this hub
            advisor: The Arc advisor instance
            enable_auto_broadcast: Auto-broadcast insights to agents
            enable_bidirectional: Allow agents to query advisor
        """
        self.hub_id = hub_id
        self.advisor = advisor or ToolAugmentedAdvisor(
            agent_id=f"{hub_id}-advisor",
            on_failure="warn"
        )
        
        # Agent registry
        self.connected_agents: Dict[str, A2AAgentConnection] = {}
        
        # Task management
        self.tasks: Dict[str, Task] = {}
        self.task_contexts: Dict[str, str] = {}  # contextId -> agentId mapping
        self.streaming_tasks: Dict[str, asyncio.Queue] = {}  # For SSE streaming
        
        # Message routing
        self.method_handlers: Dict[str, Callable] = {
            # Standard A2A methods
            "message/send": self._handle_message_send,
            "message/stream": self._handle_message_stream,
            "tasks/get": self._handle_task_get,
            "tasks/cancel": self._handle_task_cancel,
            "tasks/pushNotificationConfig/add": self._handle_push_notification_add,
            "tasks/pushNotificationConfig/remove": self._handle_push_notification_remove,
            
            # Arc-specific extension methods
            "arc/advice/request": self._handle_advice_request,
            "arc/reward/submit": self._handle_reward_signal,
            "arc/advisor/query": self._handle_advisor_query,
            "arc/agent/register": self._handle_agent_registration,
        }
        
        # Configuration
        self.enable_auto_broadcast = enable_auto_broadcast
        self.enable_bidirectional = enable_bidirectional
        self.broadcast_threshold = 0.75
        
        # Metrics
        self.hub_metrics = {
            "total_messages": 0,
            "advice_requests": 0,
            "broadcasts_sent": 0,
            "reward_signals": 0,
            "active_agents": 0
        }
        
        # Reward aggregation
        self.reward_buffer: List[Dict[str, Any]] = []
        self.reward_file = Path.home() / ".arc" / "rewards" / f"{hub_id}_rewards.jsonl"
        self.reward_file.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Arc A2A Hub initialized: {hub_id}")
    
    async def handle_jsonrpc_message(
        self, 
        message: Dict[str, Any], 
        agent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Handle incoming JSON-RPC 2.0 message from an agent.
        
        Args:
            message: The JSON-RPC message
            agent_id: ID of the sending agent
            
        Returns:
            JSON-RPC response
        """
        self.hub_metrics["total_messages"] += 1
        
        # Validate JSON-RPC structure
        if message.get("jsonrpc") != "2.0":
            return JSONRPCErrorResponse(
                id=message.get("id"),
                error=JSONRPCError(
                    code=-32600,
                    message="Invalid Request",
                    data="Missing or invalid jsonrpc version"
                )
            ).model_dump()
        
        method = message.get("method")
        if not method:
            return JSONRPCErrorResponse(
                id=message.get("id"),
                error=JSONRPCError(
                    code=-32600,
                    message="Invalid Request",
                    data="Missing method"
                )
            ).model_dump()
        
        # Route to appropriate handler
        handler = self.method_handlers.get(method)
        if not handler:
            return JSONRPCErrorResponse(
                id=message.get("id"),
                error=JSONRPCError(
                    code=-32601,
                    message="Method not found",
                    data=f"Unknown method: {method}"
                )
            ).model_dump()
        
        try:
            # Execute handler
            result = await handler(message, agent_id)
            
            # Return success response
            return JSONRPCSuccessResponse(
                id=message.get("id"),
                result=result
            ).model_dump()
            
        except Exception as e:
            logger.error(f"Error handling {method}: {e}")
            return JSONRPCErrorResponse(
                id=message.get("id"),
                error=JSONRPCError(
                    code=-32603,
                    message="Internal error",
                    data=str(e)
                )
            ).model_dump()
    
    async def _handle_agent_registration(
        self, 
        message: Dict[str, Any], 
        agent_id: Optional[str]
    ) -> Dict[str, Any]:
        """Handle agent registration with Arc hub."""
        params = message.get("params", {})
        agent_card_data = params.get("agent_card")
        
        if not agent_card_data:
            raise ValueError("Missing agent_card in registration")
        
        agent_card = ArcAgentCard(**agent_card_data)
        
        # Create connection
        connection = A2AAgentConnection(agent_card)
        self.connected_agents[agent_card.name] = connection
        self.hub_metrics["active_agents"] = len(self.connected_agents)
        
        logger.info(f"Registered Arc agent: {agent_card.name} (v{agent_card.version})")
        
        # Log to advisor's learning system
        self.advisor._report_outcome(
            trace_id=str(uuid.uuid4()),
            outcome={
                "success": True,
                "event_type": "agent_registration",
                "agent_id": agent_card.name,
                "agent_version": agent_card.version,
                "capabilities": agent_card.capabilities.model_dump()
            }
        )
        
        return {
            "status": "registered",
            "hub_id": self.hub_id,
            "advisor_model": self.advisor.hf_repo_id,
            "arc_protocol_version": "0.1.0",
            "bidirectional_enabled": self.enable_bidirectional
        }
    
    async def _handle_advice_request(
        self, 
        message: Dict[str, Any], 
        agent_id: Optional[str]
    ) -> Dict[str, Any]:
        """Handle request for strategic advice."""
        params = message.get("params", {})
        
        self.hub_metrics["advice_requests"] += 1
        
        # Update agent metrics
        if agent_id and agent_id in self.connected_agents:
            agent = self.connected_agents[agent_id]
            agent.metrics["advice_requests"] += 1
            agent.last_activity = datetime.utcnow()
        
        # Build context with multi-agent awareness
        context = {
            **params.get("context", {}),
            "agent_name": agent_id,
            "previous_attempts": params.get("previous_attempts", []),
            "multi_agent_context": {
                "total_agents": len(self.connected_agents),
                "agent_versions": list(set(
                    f"{conn.agent_card.name}-v{conn.agent_card.version}" 
                    for conn in self.connected_agents.values()
                ))
            }
        }
        
        # Get advice from advisor
        advice = self.advisor.get_advice(
            task_description=params.get("task_description", ""),
            context=context,
            enable_tools=True,
            generation_config={
                "temperature": 0.7,
                "max_new_tokens": 400,
            }
        )
        
        if not advice:
            advice = {
                "strategy": "Proceed with standard approach",
                "tools_used": [],
                "thinking": None
            }
        
        # Extract patterns from semantic search
        relevant_patterns = []
        if advice.get("tool_results"):
            for tool, result in advice["tool_results"].items():
                if isinstance(result, dict) and "similar_failures" in result:
                    relevant_patterns.extend(result["similar_failures"][:3])
        
        # Build result
        return {
            "strategy": advice.get("strategy", ""),
            "confidence_score": 0.85 if advice.get("tools_used") else 0.65,
            "relevant_patterns": relevant_patterns,
            "tools_used": advice.get("tools_used", []),
            "thinking_trace": advice.get("thinking")
        }
    
    async def _handle_message_send(
        self, 
        message: Dict[str, Any], 
        agent_id: Optional[str]
    ) -> Dict[str, Any]:
        """Handle A2A message/send with Arc learning integration."""
        params = message.get("params", {})
        a2a_message = params.get("message", {})
        
        # Check if this contains Arc learning data
        extensions = a2a_message.get("extensions", [])
        if "https://arc.computer/extensions/learning/v1" in extensions:
            # Process Arc learning messages
            await self._process_arc_learning_message(a2a_message, agent_id)
        
        # Return task response
        task_id = a2a_message.get("taskId", str(uuid.uuid4()))
        return {
            "kind": "task",
            "id": task_id,
            "contextId": a2a_message.get("contextId", str(uuid.uuid4())),
            "status": {
                "state": "submitted",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
    
    async def _process_arc_learning_message(
        self, 
        message: Dict[str, Any], 
        agent_id: Optional[str]
    ) -> None:
        """Process Arc learning messages (reports, improvements)."""
        parts = message.get("parts", [])
        
        for part in parts:
            if part.get("kind") == "data":
                data = part.get("data", {})
                msg_type = data.get("type")
                
                if msg_type == "ArcLearningReport":
                    # Process learning report
                    self.advisor._report_outcome(
                        trace_id=data.get("trace_id"),
                        outcome=data.get("outcome", {})
                    )
                    
                    # Update agent metrics
                    if agent_id in self.connected_agents:
                        agent = self.connected_agents[agent_id]
                        if data.get("outcome", {}).get("success"):
                            agent.metrics["successful_tasks"] += 1
                        else:
                            agent.metrics["failed_tasks"] += 1
                
                elif msg_type == "ArcImprovementRequest":
                    # Process improvement request
                    self.advisor._request_improvement(
                        trace_id=data.get("trace_id"),
                        outcome=data.get("failure_context", {})
                    )
                    
                    # Update metrics
                    if agent_id in self.connected_agents:
                        self.connected_agents[agent_id].metrics["improvements_reported"] += 1
                    
                    # Check if we should broadcast
                    if self.enable_auto_broadcast:
                        await self._check_and_broadcast_patterns(data)
    
    async def _handle_reward_signal(
        self, 
        message: Dict[str, Any], 
        agent_id: Optional[str]
    ) -> Dict[str, Any]:
        """Handle reward signal for GRPO training with custom metrics support."""
        params = message.get("params", {})
        
        self.hub_metrics["reward_signals"] += 1
        
        # Define standard metrics that go in the main metrics field
        standard_metric_keys = {
            "task_success", "advice_followed", "advice_quality_score",
            "context_relevance", "context_clarity", "context_actionability",
            "agent_confidence_before", "agent_confidence_after", "execution_time_ms",
            "advisor_trace_id", "task_trace_id", "agent_id"
        }
        
        # Extract standard metrics
        metrics = {
            "task_success": params.get("task_success", False),
            "advice_followed": params.get("advice_followed", False),
            "advice_quality_score": params.get("advice_quality_score", 0.0),
            "context_relevance": params.get("context_relevance", 0.0),
            "context_clarity": params.get("context_clarity", 0.0),
            "context_actionability": params.get("context_actionability", 0.0),
            "confidence_delta": params.get("agent_confidence_after", 0.5) - params.get("agent_confidence_before", 0.5),
            "execution_time_ms": params.get("execution_time_ms", 0)
        }
        
        # Extract custom metrics (everything not in standard set)
        custom_metrics = {}
        for key, value in params.items():
            if key not in standard_metric_keys:
                custom_metrics[key] = value
        
        # Build reward data with enhanced structure
        reward_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent_id": agent_id or params.get("agent_id", "unknown"),
            "advisor_trace_id": params.get("advisor_trace_id", ""),
            "task_trace_id": params.get("task_trace_id", ""),
            "metrics": metrics
        }
        
        # Add custom metrics if any exist
        if custom_metrics:
            reward_data["custom_metrics"] = custom_metrics
        
        # Add competition context if present (special handling)
        if "competition_context" in params:
            reward_data["competition_context"] = params["competition_context"]
        
        self.reward_buffer.append(reward_data)
        
        # Persist immediately for training pipeline
        with open(self.reward_file, "a") as f:
            f.write(json.dumps(reward_data) + "\n")
        
        return {"status": "recorded", "buffer_size": len(self.reward_buffer)}
    
    async def _handle_advisor_query(
        self, 
        message: Dict[str, Any], 
        agent_id: Optional[str]
    ) -> Dict[str, Any]:
        """Handle bidirectional query from agent to advisor."""
        if not self.enable_bidirectional:
            raise ValueError("Bidirectional communication is disabled")
        
        params = message.get("params", {})
        
        # Route query based on type
        query_type = params.get("query_type", "pattern_analysis")
        if query_type == "pattern_analysis":
            # Use semantic search for patterns
            results = self.advisor.vector_store.search_similar_failures(
                query=json.dumps(params.get("query_context", {})),
                limit=params.get("limit", 10),
                min_similarity=params.get("min_confidence", 0.7)
            )
            
            insights = [
                {
                    "pattern": r.get("document", ""),
                    "similarity": r.get("similarity", 0),
                    "metadata": r.get("metadata", {})
                }
                for r in results
            ]
            
        elif query_type == "success_strategies":
            # Query successful patterns
            results = self.advisor.vector_store.search_similar_failures(
                query=json.dumps(params.get("query_context", {})),
                failure_category=None,  # Search all events
                limit=params.get("limit", 10),
                min_similarity=params.get("min_confidence", 0.7)
            )
            
            # Filter for successes
            insights = []
            for r in results:
                doc = r.get("document", "")
                if "Success: True" in doc:
                    insights.append({
                        "strategy": doc,
                        "similarity": r.get("similarity", 0),
                        "metadata": r.get("metadata", {})
                    })
        
        elif query_type == "failure_remediation":
            # Get remediation plan
            plan = self.advisor.get_remediation_plan(
                failure_category=params.get("query_context", {}).get("category", "general"),
                limit=params.get("limit", 10)
            )
            
            insights = plan.get("similar_failures", [])
        
        else:
            insights = []
        
        limit = params.get("limit", 10)
        return {
            "insights": insights[:limit],
            "patterns_found": len(insights),
            "confidence_score": sum(i.get("similarity", 0) for i in insights) / max(len(insights), 1),
            "recommended_strategies": [
                "Review similar patterns for insights",
                "Apply learned strategies from successful cases",
                "Monitor for recurring patterns"
            ]
        }
    
    async def _handle_task_get(
        self, 
        message: Dict[str, Any], 
        agent_id: Optional[str]
    ) -> Dict[str, Any]:
        """Handle standard A2A task/get request."""
        params = message.get("params", {})
        task_id = params.get("id")
        
        # For demo, return a simple task status
        return {
            "kind": "task",
            "id": task_id,
            "contextId": str(uuid.uuid4()),
            "status": {
                "state": "completed",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            },
            "artifacts": []
        }
    
    async def _check_and_broadcast_patterns(self, failure_data: Dict[str, Any]) -> None:
        """Check if failure patterns warrant broadcasting."""
        failure_category = failure_data.get("failure_category", "unknown")
        
        # Use semantic search to find patterns
        similar = self.advisor.vector_store.search_similar_failures(
            query=failure_category,
            limit=10,
            min_similarity=0.7
        )
        
        if len(similar) >= 3:
            # Calculate confidence
            avg_similarity = sum(s.get("similarity", 0) for s in similar) / len(similar)
            
            if avg_similarity >= self.broadcast_threshold:
                # Create broadcast
                broadcast = {
                    "jsonrpc": "2.0",
                    "method": "arc/broadcast/learning",
                    "params": {
                        "insight_type": "warning",
                        "affected_agents": ["*"],
                        "content": f"Pattern detected: {failure_category}. {len(similar)} similar cases found.",
                        "evidence_count": len(similar),
                        "confidence": avg_similarity,
                        "recommended_actions": [
                            f"Review pattern: {failure_category}",
                            "Apply preventive measures",
                            "Query advisor for remediation strategies"
                        ]
                    }
                }
                
                await self._broadcast_to_agents(broadcast)
    
    async def _broadcast_to_agents(self, message: Dict[str, Any]) -> None:
        """Broadcast message to all connected agents."""
        self.hub_metrics["broadcasts_sent"] += 1
        
        for agent_id, connection in self.connected_agents.items():
            try:
                if connection.websocket:
                    await connection.websocket.send_json(message)
                logger.info(f"Broadcast sent to {agent_id}")
            except Exception as e:
                logger.error(f"Failed to broadcast to {agent_id}: {e}")
    
    async def _handle_message_stream(
        self, 
        message: Dict[str, Any], 
        agent_id: Optional[str]
    ) -> Dict[str, Any]:
        """Handle A2A message/stream for real-time task updates via SSE."""
        params = message.get("params", {})
        msg_params = MessageSendParams(**params)
        
        # Create task with streaming enabled
        task_id = str(uuid.uuid4())
        context_id = str(uuid.uuid4())
        
        task = Task(
            id=task_id,
            contextId=context_id,
            status=TaskStatus(
                state=TaskState.SUBMITTED,
                timestamp=datetime.utcnow().isoformat() + "Z"
            ),
            artifacts=[],
            history=[msg_params.message]
        )
        
        self.tasks[task_id] = task
        self.task_contexts[context_id] = agent_id or "anonymous"
        
        # Create streaming queue
        stream_queue = asyncio.Queue()
        self.streaming_tasks[task_id] = stream_queue
        
        # Start async task processing
        asyncio.create_task(self._process_streaming_task(task_id, msg_params))
        
        return {
            "streamUrl": f"/tasks/{task_id}/stream",
            "taskId": task_id,
            "contextId": context_id
        }
    
    async def _handle_task_cancel(
        self, 
        message: Dict[str, Any], 
        agent_id: Optional[str]
    ) -> Dict[str, Any]:
        """Handle A2A tasks/cancel request."""
        params = TaskIdParams(**message.get("params", {}))
        task_id = params.id
        
        if task_id not in self.tasks:
            raise JSONRPCError(
                code=A2AErrorCodes.TASK_NOT_FOUND,
                message="Task not found",
                data={"taskId": task_id}
            )
        
        task = self.tasks[task_id]
        
        # Check if task can be canceled
        if task.status.state not in [TaskState.SUBMITTED, TaskState.WORKING]:
            raise JSONRPCError(
                code=A2AErrorCodes.TASK_NOT_CANCELABLE,
                message="Task cannot be canceled in current state",
                data={"taskId": task_id, "state": task.status.state}
            )
        
        # Update task state
        task.status.state = TaskState.CANCELED
        task.status.timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Clean up streaming if active
        if task_id in self.streaming_tasks:
            queue = self.streaming_tasks[task_id]
            await queue.put({"type": "done"})
            del self.streaming_tasks[task_id]
        
        return {"status": "canceled", "taskId": task_id}
    
    async def _handle_push_notification_add(
        self, 
        message: Dict[str, Any], 
        agent_id: Optional[str]
    ) -> Dict[str, Any]:
        """Handle push notification configuration addition."""
        if not agent_id or agent_id not in self.connected_agents:
            raise JSONRPCError(
                code=A2AErrorCodes.INVALID_REQUEST,
                message="Agent not registered",
                data={"agentId": agent_id}
            )
        
        params = message.get("params", {})
        config_id = str(uuid.uuid4())
        
        agent = self.connected_agents[agent_id]
        agent.push_notification_configs[config_id] = params
        
        return {
            "configId": config_id,
            "status": "added"
        }
    
    async def _handle_push_notification_remove(
        self, 
        message: Dict[str, Any], 
        agent_id: Optional[str]
    ) -> Dict[str, Any]:
        """Handle push notification configuration removal."""
        if not agent_id or agent_id not in self.connected_agents:
            raise JSONRPCError(
                code=A2AErrorCodes.INVALID_REQUEST,
                message="Agent not registered",
                data={"agentId": agent_id}
            )
        
        params = message.get("params", {})
        config_id = params.get("configId")
        
        if not config_id:
            raise JSONRPCError(
                code=A2AErrorCodes.INVALID_PARAMS,
                message="Missing configId",
                data=params
            )
        
        agent = self.connected_agents[agent_id]
        if config_id in agent.push_notification_configs:
            del agent.push_notification_configs[config_id]
            return {"status": "removed", "configId": config_id}
        else:
            return {"status": "not_found", "configId": config_id}
    
    async def _process_streaming_task(
        self, 
        task_id: str, 
        msg_params: MessageSendParams
    ) -> None:
        """Process a streaming task asynchronously."""
        try:
            task = self.tasks[task_id]
            queue = self.streaming_tasks[task_id]
            
            # Update task state to working
            task.status.state = TaskState.WORKING
            task.status.timestamp = datetime.utcnow().isoformat() + "Z"
            
            # Send status update
            status_event = TaskStatusUpdateEvent(
                taskId=task_id,
                contextId=task.contextId,
                status=task.status
            )
            await queue.put(status_event.model_dump())
            
            # Process Arc message if applicable
            if is_arc_message(msg_params.message):
                await self._process_arc_learning_message(
                    msg_params.message.model_dump(), 
                    self.task_contexts.get(task.contextId)
                )
                
                # Generate Arc advice artifact
                parts = msg_params.message.parts
                for part in parts:
                    if hasattr(part, 'kind') and part.kind == "data" and hasattr(part, 'data') and part.data.get("type") == "ArcAdviceRequest":
                        # Generate advice
                        advice = self.advisor.get_advice(
                            task_description=part.data.get("task_description", ""),
                            context=part.data.get("context", {}),
                            enable_tools=True
                        )
                        
                        # Create artifact
                        artifact = ArcAdviceArtifact(
                            strategy=advice.get("strategy", ""),
                            confidence=0.8 if advice.get("tools_used") else 0.6,
                            patterns=[]
                        )
                        
                        task.artifacts = [artifact]
                        
                        # Send artifact update
                        artifact_event = TaskArtifactUpdateEvent(
                            taskId=task_id,
                            contextId=task.contextId,
                            artifact=artifact,
                            lastChunk=True
                        )
                        await queue.put(artifact_event.model_dump())
            
            # Complete task
            task.status.state = TaskState.COMPLETED
            task.status.timestamp = datetime.utcnow().isoformat() + "Z"
            
            # Send final status
            final_event = TaskStatusUpdateEvent(
                taskId=task_id,
                contextId=task.contextId,
                status=task.status,
                final=True
            )
            await queue.put(final_event.model_dump())
            
            # Signal stream completion
            await queue.put({"type": "done"})
            
        except Exception as e:
            logger.error(f"Error processing streaming task {task_id}: {e}")
            task.status.state = TaskState.FAILED
            task.status.timestamp = datetime.utcnow().isoformat() + "Z"
            
            error_event = TaskStatusUpdateEvent(
                taskId=task_id,
                contextId=task.contextId,
                status=task.status,
                final=True
            )
            await queue.put(error_event.model_dump())
            await queue.put({"type": "done"})
    
    def get_hub_statistics(self) -> Dict[str, Any]:
        """Get comprehensive hub statistics."""
        agent_stats = {}
        for agent_id, conn in self.connected_agents.items():
            agent_stats[agent_id] = {
                "version": conn.agent_card.version,
                "metrics": conn.metrics,
                "last_activity": conn.last_activity.isoformat() + "Z"
            }
        
        return {
            "hub_id": self.hub_id,
            "protocol_versions": {
                "a2a": "0.2.5",
                "arc": "0.1.0"
            },
            "hub_metrics": self.hub_metrics,
            "connected_agents": agent_stats,
            "advisor_stats": self.advisor.vector_store.get_statistics(),
            "reward_signals_collected": len(self.reward_buffer),
            "features": {
                "auto_broadcast": self.enable_auto_broadcast,
                "bidirectional": self.enable_bidirectional
            }
        }