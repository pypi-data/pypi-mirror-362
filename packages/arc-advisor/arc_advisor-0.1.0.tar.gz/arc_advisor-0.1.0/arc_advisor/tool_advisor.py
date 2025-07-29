"""Tool-Augmented Advisor - Extension of Arc Advisor with active tool use capabilities.

This module extends the base ArcAdvisorClient to enable the advisor to actively
query its own history and use tools to provide better, data-driven strategies.
"""

import json
import logging
from typing import Any, Dict, List, Optional

import torch

from .client import ArcAdvisorClient, ArcAdvisorError

logger = logging.getLogger("ToolAugmentedAdvisor")

# Tool-aware system prompt for Qwen3
TOOL_SYSTEM_PROMPT = """You are an expert advisor with access to these tools:

1. get_remediation_plan(failure_category, limit=5) - Analyze similar past failures to understand patterns
   Example: <tool>get_remediation_plan("SQLError", limit=3)</tool>
   
2. query_success_patterns(task_type) - Find successful strategies for similar tasks
   Example: <tool>query_success_patterns("quote_generation")</tool>
   
3. analyze_failure_trend(timeframe="7d") - Identify failure patterns over time
   Example: <tool>analyze_failure_trend(timeframe="24h")</tool>

When advising on a task, you should:
1. First check if similar tasks have failed before using get_remediation_plan
2. Query successful patterns if available
3. Synthesize a strategy based on historical data

Use tools by outputting: <tool>function_name(args)</tool>
Show your reasoning in <think>...</think> blocks.

Example thinking process:
<think>
This is a SQL query task. Let me check if we've had SQL-related failures recently.
<tool>get_remediation_plan("SQL", limit=3)</tool>
</think>

Based on the tool results, provide a concise, actionable strategy."""


class ToolAugmentedAdvisor(ArcAdvisorClient):
    """Extended advisor client with active tool-using capabilities.
    
    This advisor can actively query its own failure history and use various
    tools to provide better, data-driven strategies.
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize the tool-augmented advisor."""
        super().__init__(*args, **kwargs)
        
        # Register available tools
        self.tools = {
            "get_remediation_plan": self.get_remediation_plan,
            "query_success_patterns": self._query_success_patterns,
            "analyze_failure_trend": self._analyze_failure_trend,
        }
    
    def _query_success_patterns(self, task_type: str) -> Dict[str, Any]:
        """Query successful task executions using semantic search.
        
        Args:
            task_type: Type or description of task to search for.
            
        Returns:
            Dictionary with successful patterns, strategies, and similarity scores.
        """
        try:
            # Use vector store for semantic search
            success_patterns = self.vector_store.query_success_patterns(
                task_description=task_type,
                limit=5
            )
            
            if not success_patterns:
                return {"successful_patterns": [], "strategies_used": [], "total_successes": 0}
            
            # Extract detailed information
            successful_tasks = []
            strategies = []
            
            for pattern in success_patterns:
                metadata = pattern.get("metadata", {})
                
                # Parse document to extract context
                doc_text = pattern.get("document", "")
                
                task_info = {
                    "timestamp": metadata.get("timestamp", ""),
                    "trace_id": metadata.get("trace_id", ""),
                    "similarity_score": pattern.get("similarity", 0),
                    "success": True,
                }
                
                # Try to extract output/strategy from document
                if "Output:" in doc_text:
                    output_part = doc_text.split("Output:")[1].split("Metrics:")[0].strip()
                    try:
                        output_data = json.loads(output_part)
                        if isinstance(output_data, dict) and "strategy_used" in output_data:
                            strategies.append(output_data["strategy_used"])
                            task_info["strategy_used"] = output_data["strategy_used"]
                    except:
                        pass
                
                successful_tasks.append(task_info)
            
            # Get statistics from vector store
            stats = self.vector_store.get_statistics()
            
            return {
                "successful_patterns": successful_tasks,
                "strategies_used": strategies,
                "total_successes": stats.get("successful_executions", 0),
                "semantic_search_used": True,
                "similarity_range": {
                    "min": min(p["similarity_score"] for p in successful_tasks) if successful_tasks else 0,
                    "max": max(p["similarity_score"] for p in successful_tasks) if successful_tasks else 0,
                }
            }
            
        except Exception as e:
            logger.error(f"Error in semantic success pattern search: {e}")
            # Fallback to simple search
            return self._simple_success_search(task_type)
    
    def _analyze_failure_trend(self, timeframe: str = "7d") -> Dict[str, Any]:
        """Analyze failure trends over a specified timeframe.
        
        Args:
            timeframe: Time period to analyze (e.g., "24h", "7d", "30d").
            
        Returns:
            Dictionary with failure trend analysis.
        """
        from datetime import datetime, timedelta, timezone
        
        # Parse timeframe
        if timeframe.endswith("h"):
            hours = int(timeframe[:-1])
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        elif timeframe.endswith("d"):
            days = int(timeframe[:-1])
            cutoff_time = datetime.utcnow() - timedelta(days=days)
        else:
            cutoff_time = datetime.utcnow() - timedelta(days=7)  # Default 7 days
        
        failures_by_category = {}
        total_failures = 0
        
        if not self.log_file.exists():
            return {"failure_trends": {}, "total_failures": 0}
        
        try:
            with open(self.log_file, "r") as f:
                for line in f:
                    try:
                        log_entry = json.loads(line.strip())
                        # Parse timestamp and ensure it's timezone-aware
                        timestamp_str = log_entry.get("timestamp", "")
                        if timestamp_str.endswith("Z"):
                            # Replace Z with +00:00 for fromisoformat
                            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                        else:
                            timestamp = datetime.fromisoformat(timestamp_str)
                        
                        # Make cutoff_time timezone-aware if timestamp is
                        if timestamp.tzinfo is not None and cutoff_time.tzinfo is None:
                            # Make cutoff_time UTC-aware
                            cutoff_time_aware = cutoff_time.replace(tzinfo=timezone.utc)
                        else:
                            cutoff_time_aware = cutoff_time
                        
                        # Only consider events within timeframe
                        if timestamp > cutoff_time_aware:
                            event = log_entry.get("event", {})
                            
                            if event.get("message_type") == "ArcImprovementRequest":
                                payload = event.get("payload", {})
                                category = payload.get("failure_category", "Unknown")
                                
                                failures_by_category[category] = failures_by_category.get(category, 0) + 1
                                total_failures += 1
                    except (json.JSONDecodeError, ValueError):
                        continue
            
            # Sort by frequency
            sorted_failures = sorted(
                failures_by_category.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            return {
                "failure_trends": dict(sorted_failures),
                "total_failures": total_failures,
                "timeframe": timeframe,
                "most_common_failure": sorted_failures[0] if sorted_failures else None,
            }
            
        except Exception as e:
            logger.error(f"Error analyzing failure trends: {e}")
            return {"failure_trends": {}, "total_failures": 0}
    
    def _execute_tool(self, tool_call: Dict[str, Any]) -> Any:
        """Execute a tool call and return the result.
        
        Args:
            tool_call: Dictionary with 'name' and 'arguments'.
            
        Returns:
            Tool execution result.
        """
        tool_name = tool_call.get("name")
        args = tool_call.get("arguments", {})
        
        if tool_name not in self.tools:
            return {"error": f"Unknown tool: {tool_name}"}
        
        try:
            # Convert positional args to proper parameter names
            if tool_name == "get_remediation_plan":
                if "arg_0" in args:
                    args["failure_category"] = args.pop("arg_0")
                if "arg_1" in args:
                    args["limit"] = int(args.pop("arg_1"))
            elif tool_name == "query_success_patterns":
                if "arg_0" in args:
                    args["task_type"] = args.pop("arg_0")
            elif tool_name == "analyze_failure_trend":
                if "arg_0" in args:
                    args["timeframe"] = args.pop("arg_0")
            
            # Execute the tool
            result = self.tools[tool_name](**args)
            return result
            
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return {"error": str(e)}
    
    def get_advice(
        self,
        task_description: str,
        context: Dict[str, Any],
        generation_config: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        enable_tools: bool = True,
    ) -> Optional[Dict[str, Any]]:
        """Get strategic advice with active tool use.
        
        Args:
            task_description: A description of the task to be performed.
            context: Additional context about the task and environment.
            generation_config: Optional generation parameters.
            stream: If True, print tokens as they are generated.
            enable_tools: If True, allow the advisor to use tools.
        
        Returns:
            A dictionary containing the strategy, thinking content, tools used, and advisor ID.
        """
        if not enable_tools:
            # Fall back to base implementation
            return super().get_advice(
                task_description, context, generation_config, stream, enable_thinking=True
            )
        
        try:
            if self.endpoint == "local":
                if not self.model or not self.tokenizer:
                    raise ArcAdvisorError(
                        "Local advisor model is not loaded. Check installation."
                    )
                
                # Use tool-aware prompt
                if hasattr(self.tokenizer, 'apply_chat_template'):
                    messages = [
                        {"role": "system", "content": TOOL_SYSTEM_PROMPT},
                        {
                            "role": "user",
                            "content": f"Task: {task_description}\nContext: {json.dumps(context, indent=2)}"
                        }
                    ]
                    
                    # Apply chat template
                    try:
                        prompt = self.tokenizer.apply_chat_template(
                            messages,
                            tokenize=False,
                            add_generation_prompt=True,
                        )
                    except Exception:
                        # Fallback
                        prompt = f"{TOOL_SYSTEM_PROMPT}\n\nTask: {task_description}\nContext: {json.dumps(context, indent=2)}"
                else:
                    prompt = f"{TOOL_SYSTEM_PROMPT}\n\nTask: {task_description}\nContext: {json.dumps(context, indent=2)}"
                
                # Step 1: Initial generation with tool awareness
                initial_response = super().get_advice(
                    task_description="",  # We already included it in the prompt
                    context={},  # Already in prompt
                    generation_config=generation_config,
                    stream=stream,
                    enable_thinking=True,
                )
                
                if not initial_response:
                    return None
                
                # Step 2: Parse and execute tool calls
                tool_calls = initial_response.get("tool_calls", [])
                tool_results = {}
                
                for tool_call in tool_calls:
                    logger.info(f"Executing tool: {tool_call}")
                    result = self._execute_tool(tool_call)
                    tool_results[tool_call["name"]] = result
                
                # Step 3: Generate final advice with tool results if tools were used
                if tool_results:
                    # Prepare follow-up prompt with tool results
                    follow_up_messages = [
                        {"role": "system", "content": TOOL_SYSTEM_PROMPT},
                        {
                            "role": "user",
                            "content": f"Task: {task_description}\nContext: {json.dumps(context, indent=2)}"
                        },
                        {
                            "role": "assistant",
                            "content": f"<think>{initial_response.get('thinking', '')}</think>\n\nTool results: {json.dumps(tool_results, indent=2)}"
                        },
                        {
                            "role": "user",
                            "content": "Based on these tool results, provide your final strategy."
                        }
                    ]
                    
                    # Generate final response
                    final_response = self._generate_with_messages(
                        follow_up_messages, generation_config, stream
                    )
                    
                    if final_response:
                        thinking_content, final_strategy = self._extract_thinking_blocks(final_response)
                        
                        return {
                            "strategy": final_strategy.strip(),
                            "thinking": initial_response.get("thinking", "") + "\n" + thinking_content,
                            "tools_used": list(tool_results.keys()),
                            "tool_results": tool_results,
                            "advisor_id": self.hf_repo_id,
                        }
                
                # No tools used, return initial response
                return initial_response
                
            else:
                # Cloud mode with tool support
                return super().get_advice(
                    task_description, context, generation_config, stream, enable_thinking=True
                )
                
        except Exception as e:
            logger.error(f"Tool-augmented advisor failed: {e}", exc_info=True)
            if self.on_failure_mode == "raise":
                raise
            else:
                logger.warning("Falling back to base advisor without tools.")
                return super().get_advice(
                    task_description, context, generation_config, stream, enable_thinking=True
                )
    
    def _generate_with_messages(
        self, 
        messages: List[Dict[str, str]], 
        generation_config: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> str:
        """Generate response from messages using the model."""
        # Prepare prompt
        if hasattr(self.tokenizer, 'apply_chat_template'):
            try:
                prompt = self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True,
                )
            except Exception:
                # Fallback to simple format
                prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        else:
            prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        
        # Prepare generation config
        gen_config = {
            "max_new_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True,
        }
        if generation_config:
            gen_config.update(generation_config)
        
        # Tokenize and generate
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=2048,
        ).to(self.device)
        
        if stream:
            from transformers import TextStreamer
            streamer = TextStreamer(
                self.tokenizer,
                skip_prompt=True,
                skip_special_tokens=True,
            )
            gen_config["streamer"] = streamer
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                **gen_config,
                pad_token_id=self.tokenizer.pad_token_id,
            )
        
        # Decode the response
        response = self.tokenizer.decode(
            outputs[0][inputs.input_ids.shape[1]:],
            skip_special_tokens=True,
        )
        
        return response
    
    def _simple_success_search(self, task_type: str) -> Dict[str, Any]:
        """Fallback simple search for success patterns."""
        successful_tasks = []
        
        if not self.log_file.exists():
            return {"successful_patterns": [], "strategies_used": [], "total_successes": 0}
        
        try:
            with open(self.log_file, "r") as f:
                for line in f:
                    try:
                        log_entry = json.loads(line.strip())
                        event = log_entry.get("event", {})
                        
                        if event.get("message_type") == "ArcLearningReport":
                            payload = event.get("payload", {})
                            
                            if payload.get("success"):
                                task_context = str(payload)
                                if task_type.lower() in task_context.lower():
                                    successful_tasks.append({
                                        "timestamp": log_entry.get("timestamp"),
                                        "trace_id": event.get("trace_id"),
                                        "similarity_score": 1.0,
                                        "success": True,
                                    })
                    except json.JSONDecodeError:
                        continue
            
            return {
                "successful_patterns": successful_tasks[-5:],
                "strategies_used": [],
                "total_successes": len(successful_tasks),
                "semantic_search_used": False,
            }
            
        except Exception as e:
            logger.error(f"Error in simple success search: {e}")
            return {"successful_patterns": [], "strategies_used": [], "total_successes": 0}