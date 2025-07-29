"""Arc Advisor Client - The core implementation of the Executor-Advisor pattern.

This module provides the main client for interacting with the Arc learning infrastructure,
enabling AI agents to receive strategic advice and track their performance for continuous improvement.
"""

import json
import logging
import os
import re
import uuid
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import requests
import torch
from huggingface_hub import snapshot_download
from transformers import AutoModelForCausalLM, AutoTokenizer

from .protocols import (
    ArcImprovementRequestMessage,
    ArcLearningReportMessage,
)
from .vector_store import ArcVectorStore

# Configure professional logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s",
)
logger = logging.getLogger("ArcAdvisorClient")


class ArcAdvisorError(Exception):
    """Custom exception for advisor failures."""
    pass


class ArcAdvisorClient:
    """The main client for interacting with the Arc learning infrastructure.
    
    Implements the Executor-Advisor pattern with a pluggable, learning co-pilot.
    This client can operate in two modes:
    - Local mode: Uses a downloaded model for inference (default for open-source users)
    - Cloud mode: Connects to Arc's managed service for continuous learning
    
    Attributes:
        agent_id: Unique identifier for this agent instance.
        api_key: Optional API key for cloud mode.
        endpoint: The service endpoint (local or cloud).
        hf_repo_id: HuggingFace repository ID for the advisor model.
        local_model_path: Directory for storing downloaded models.
        on_failure_mode: How to handle advisor failures ('warn' or 'raise').
    """
    
    def __init__(
        self,
        agent_id: str,
        api_key: Optional[str] = None,
        hf_repo_id: str = "Qwen/Qwen3-4B",
        local_model_dir: str = "~/.arc/models",
        on_failure: str = "warn",
    ):
        """Initialize the Arc Advisor Client.
        
        Args:
            agent_id: Unique identifier for this agent instance.
            api_key: Optional API key for cloud mode. If not provided, runs in local mode.
            hf_repo_id: HuggingFace model to use for local inference.
            local_model_dir: Directory to store downloaded models.
            on_failure: How to handle failures - 'warn' (default) or 'raise'.
        
        Raises:
            ValueError: If on_failure is not 'warn' or 'raise'.
        """
        self.agent_id = agent_id
        self.api_key = api_key
        self.endpoint = "https://api.arc.computer" if self.api_key else "local"
        self.hf_repo_id = hf_repo_id
        self.local_model_path = os.path.expanduser(local_model_dir)
        
        if on_failure not in ["warn", "raise"]:
            raise ValueError("on_failure must be either 'warn' or 'raise'")
        self.on_failure_mode = on_failure

        self.model = None
        self.tokenizer = None
        self.device = None
        
        # Ensure log directory exists
        self.log_dir = Path.home() / ".arc" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "events.log"
        
        # Initialize vector store for semantic search
        self.vector_store = ArcVectorStore(
            collection_name=f"arc_events_{agent_id}",
            embedding_model="all-MiniLM-L6-v2"  # Lightweight, effective model
        )
        logger.info(f"Vector store initialized for agent {agent_id}")

        if self.endpoint == "local":
            self._initialize_local_advisor()

    def _extract_thinking_blocks(self, text: str) -> Tuple[str, str]:
        """Extract thinking blocks and final response from model output.
        
        Args:
            text: The raw model output that may contain <think>...</think> blocks.
            
        Returns:
            Tuple of (thinking_content, final_response)
        """
        thinking_pattern = r'<think>(.*?)</think>'
        thinking_matches = re.findall(thinking_pattern, text, re.DOTALL)
        thinking_content = '\n'.join(thinking_matches) if thinking_matches else ""
        
        # Remove thinking blocks from the response
        final_response = re.sub(thinking_pattern, '', text, flags=re.DOTALL).strip()
        
        return thinking_content, final_response

    def _extract_tool_calls(self, thinking_content: str) -> List[Dict[str, Any]]:
        """Extract tool calls from thinking content.
        
        Args:
            thinking_content: The content from thinking blocks.
            
        Returns:
            List of tool calls with name and arguments.
        """
        tool_pattern = r'<tool>([^(]+)\((.*?)\)</tool>'
        tool_calls = []
        
        for match in re.finditer(tool_pattern, thinking_content):
            func_name = match.group(1).strip()
            args_str = match.group(2).strip()
            
            # Parse arguments - simple implementation for now
            args = {}
            if args_str:
                # Split by comma, handle both named and positional args
                arg_parts = args_str.split(',')
                for i, part in enumerate(arg_parts):
                    part = part.strip()
                    if '=' in part:
                        key, value = part.split('=', 1)
                        # Clean up quotes
                        value = value.strip().strip('"\'')
                        args[key.strip()] = value
                    else:
                        # Positional arg
                        args[f'arg_{i}'] = part.strip('"\'')
            
            tool_calls.append({
                "name": func_name,
                "arguments": args
            })
        
        return tool_calls

    def _initialize_local_advisor(self) -> None:
        """Initialize the local advisor by downloading the model from HuggingFace if not present."""
        try:
            model_path = os.path.join(self.local_model_path, self.hf_repo_id.replace("/", "--"))
            
            # Download model if not already present
            if not os.path.exists(model_path):
                logger.info(
                    f"Downloading advisor model '{self.hf_repo_id}' for the first time. "
                    "This may take a moment..."
                )
                os.makedirs(self.local_model_path, exist_ok=True)
                snapshot_download(
                    repo_id=self.hf_repo_id,
                    local_dir=model_path,
                    local_dir_use_symlinks=False,
                )
            
            # Load model and tokenizer
            # Check for available device - prefer MPS (Apple Silicon) over CPU
            if torch.cuda.is_available():
                self.device = "cuda"
            elif torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"
                
            logger.info(f"Loading advisor model on device: {self.device}")
            
            # First try to load from the downloaded path, fallback to downloading from HF
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            except Exception:
                logger.info(f"Loading tokenizer directly from HuggingFace: {self.hf_repo_id}")
                self.tokenizer = AutoTokenizer.from_pretrained(self.hf_repo_id)
            
            # Configure model loading based on device
            try:
                if self.device == "cuda":
                    self.model = AutoModelForCausalLM.from_pretrained(
                        model_path,
                        torch_dtype=torch.float16,
                        device_map="auto",
                    )
                elif self.device == "mps":
                    # MPS doesn't support float16 well, use float32
                    self.model = AutoModelForCausalLM.from_pretrained(
                        model_path,
                        torch_dtype=torch.float32,
                    )
                    self.model = self.model.to(self.device)
                else:
                    # CPU
                    self.model = AutoModelForCausalLM.from_pretrained(
                        model_path,
                        torch_dtype=torch.float32,
                    )
                    self.model = self.model.to(self.device)
            except Exception:
                # If loading from local path fails, download directly from HuggingFace
                logger.info(f"Loading model directly from HuggingFace: {self.hf_repo_id}")
                if self.device == "cuda":
                    self.model = AutoModelForCausalLM.from_pretrained(
                        self.hf_repo_id,
                        torch_dtype=torch.float16,
                        device_map="auto",
                    )
                elif self.device == "mps":
                    self.model = AutoModelForCausalLM.from_pretrained(
                        self.hf_repo_id,
                        torch_dtype=torch.float32,
                    )
                    self.model = self.model.to(self.device)
                else:
                    self.model = AutoModelForCausalLM.from_pretrained(
                        self.hf_repo_id,
                        torch_dtype=torch.float32,
                    )
                    self.model = self.model.to(self.device)
            
            # Set pad token if not set
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            logger.info(f"Local advisor model loaded successfully on device: {self.device}")
            
        except Exception as e:
            logger.error(f"Failed to initialize local advisor model: {e}")
            self.model = None
            self.tokenizer = None

    def get_advice(
        self,
        task_description: str,
        context: Dict[str, Any],
        generation_config: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        enable_thinking: bool = True,
    ) -> Optional[Dict[str, Any]]:
        """Get strategic advice from the advisor for a specific task.
        
        Args:
            task_description: A description of the task to be performed.
            context: Additional context about the task and environment.
            generation_config: Optional generation parameters (temperature, max_new_tokens, etc).
            stream: If True, print tokens as they are generated for visual feedback.
            enable_thinking: If True, enable thinking mode for the model.
        
        Returns:
            A dictionary containing the strategy, thinking content, and advisor ID, 
            or None if advisor fails and on_failure is set to 'warn'.
            
        Raises:
            ArcAdvisorError: If advisor fails and on_failure is set to 'raise'.
        """
        try:
            if self.endpoint == "local":
                if not self.model or not self.tokenizer:
                    raise ArcAdvisorError(
                        "Local advisor model is not loaded. Check installation."
                    )
                
                # Check if model supports chat template
                if hasattr(self.tokenizer, 'apply_chat_template'):
                    # Use chat template with thinking mode if supported
                    messages = [
                        {
                            "role": "system",
                            "content": "You are an expert advisor specializing in enterprise workflows. When reasoning about tasks, show your thinking process in <think>...</think> blocks."
                        },
                        {
                            "role": "user",
                            "content": f"Task: {task_description}\nContext: {json.dumps(context, indent=2)}\n\nProvide a concise, actionable strategy:"
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
                        # Fallback to simple format if chat template fails
                        prompt = f"""System: You are an expert advisor specializing in enterprise workflows. When reasoning about tasks, show your thinking process in <think>...</think> blocks.
Task: {task_description}
Context: {json.dumps(context, indent=2)}
Provide a concise, actionable strategy:"""
                else:
                    # Fallback for models without chat template
                    prompt = f"""System: You are an expert advisor specializing in enterprise workflows. When reasoning about tasks, show your thinking process in <think>...</think> blocks.
Task: {task_description}
Context: {json.dumps(context, indent=2)}
Provide a concise, actionable strategy:"""
                
                # Prepare generation config
                gen_config = {
                    "max_new_tokens": 512,  # Increased for thinking content
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
                    # Import TextStreamer for streaming output
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
                
                # Extract thinking content and final response
                thinking_content, final_strategy = self._extract_thinking_blocks(response)
                
                # Extract any tool calls from thinking
                tool_calls = self._extract_tool_calls(thinking_content) if thinking_content else []
                
                return {
                    "strategy": final_strategy.strip() if final_strategy else response.strip(),
                    "thinking": thinking_content,
                    "tool_calls": tool_calls,
                    "advisor_id": self.hf_repo_id,
                }
                
            else:
                # Commercial API call
                response = requests.post(
                    f"{self.endpoint}/v1/advice",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "agent_id": self.agent_id,
                        "task": task_description,
                        "context": context,
                        "enable_thinking": enable_thinking,
                    },
                    timeout=30,
                )
                response.raise_for_status()
                return response.json()

        except Exception as e:
            logger.error(f"ArcAdvisor failed to get advice: {e}", exc_info=True)
            if self.on_failure_mode == "raise":
                raise ArcAdvisorError(f"Advisor failed to generate advice: {e}") from e
            else:
                # Default 'warn' mode
                logger.warning(
                    "Proceeding without advisor strategy. Agent performance may be degraded."
                )
                return None

    def monitor_and_learn(self, func: Callable) -> Callable:
        """Decorator that wraps a task function to enable the learning loop.
        
        This decorator monitors the execution of a task, captures outcomes,
        and reports them to the learning system for continuous improvement.
        
        Args:
            func: The task function to wrap. Must return a dict with 'success' key.
            
        Returns:
            The wrapped function with learning capabilities.
            
        Example:
            @advisor.monitor_and_learn
            def my_task(query: str) -> dict:
                # Task implementation
                return {"success": True, "output": result}
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            trace_id = str(uuid.uuid4())
            
            try:
                # Execute the wrapped function
                outcome = func(*args, **kwargs)
                
                # Validate the return value
                if not isinstance(outcome, dict) or "success" not in outcome:
                    raise ValueError(
                        "Wrapped function must return a dictionary with a 'success' key."
                    )
                
                # Report the outcome
                self._report_outcome(trace_id, outcome)
                
                # Request improvement if the task failed
                if not outcome.get("success"):
                    self._request_improvement(trace_id, outcome)
                
                return outcome
                
            except Exception as e:
                # Create a failure outcome for exceptions
                failure_outcome = {
                    "success": False,
                    "error": type(e).__name__,
                    "error_message": str(e),
                }
                
                # Report the failure
                self._report_outcome(trace_id, failure_outcome)
                self._request_improvement(trace_id, failure_outcome)
                
                # Re-raise the exception
                raise
        
        return wrapper

    def _report_outcome(self, trace_id: str, outcome: Dict[str, Any]) -> None:
        """Report the outcome of a task execution.
        
        Args:
            trace_id: Unique identifier for this task execution.
            outcome: The task outcome containing success status and other data.
        """
        report = ArcLearningReportMessage(
            agent_id=self.agent_id,
            trace_id=trace_id,
            outcome=outcome,
        )
        
        # Create log entry with metadata
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "library_version": "0.1.0",
            "advisor_model_id": self.hf_repo_id,
            "event": report.model_dump(),
        }
        
        if self.endpoint == "local":
            # Write to local log file
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
            
            # Index in vector store for semantic search
            try:
                doc_id = self.vector_store.index_event(log_entry)
                logger.info(f"Outcome reported and indexed (trace_id: {trace_id}, doc_id: {doc_id})")
            except Exception as e:
                logger.warning(f"Failed to index event in vector store: {e}")
                logger.info(f"Outcome reported to local log (trace_id: {trace_id})")
        else:
            # Send to cloud service
            requests.post(
                f"{self.endpoint}/v1/report",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=report.model_dump(),
                timeout=10,
            )

    def _request_improvement(self, trace_id: str, outcome: Dict[str, Any]) -> None:
        """Request a learning improvement based on a task failure.
        
        Args:
            trace_id: Unique identifier for the failed task.
            outcome: The failure outcome containing error details.
        """
        request = ArcImprovementRequestMessage(
            agent_id=self.agent_id,
            trace_id=trace_id,
            failure_category=outcome.get("error", "UnknownFailure"),
            failure_context=outcome,
        )
        
        # Create log entry with metadata
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "library_version": "0.1.0",
            "advisor_model_id": self.hf_repo_id,
            "event": request.model_dump(),
        }
        
        if self.endpoint == "local":
            # Write to local log file
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
            
            # Index in vector store for semantic search
            try:
                doc_id = self.vector_store.index_event(log_entry)
                logger.warning(
                    f"Improvement request logged and indexed (trace_id: {trace_id}). "
                    "Semantic search now available for failure analysis."
                )
            except Exception as e:
                logger.warning(f"Failed to index failure in vector store: {e}")
                logger.warning(
                    f"Improvement request logged locally (trace_id: {trace_id}). "
                    "Run 'arc-advisor export' to analyze your failure data."
                )
        else:
            # Send to cloud service
            requests.post(
                f"{self.endpoint}/v1/request_improvement",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=request.model_dump(),
                timeout=10,
            )

    def get_remediation_plan(self, failure_category: str, limit: int = 5) -> Dict[str, Any]:
        """Query recent failures using semantic search for remediation insights.
        
        This tool uses vector similarity to find truly related failures,
        not just keyword matches, providing more intelligent remediation strategies.
        
        Args:
            failure_category: The category or description of failure to search for.
            limit: Maximum number of similar failures to analyze.
            
        Returns:
            Dictionary with similar failures, pattern analysis, and clusters.
        """
        try:
            # Use semantic search to find similar failures
            similar_failures = self.vector_store.search_similar_failures(
                query=failure_category,
                limit=limit,
                min_similarity=0.6  # Lower threshold for broader matches
            )
            
            if not similar_failures:
                # Fallback to searching without category filter
                similar_failures = self.vector_store.search_similar_failures(
                    query=failure_category,
                    failure_category=None,
                    limit=limit,
                    min_similarity=0.5
                )
            
            # Get failure clusters for broader pattern analysis
            clusters = self.vector_store.get_failure_clusters(
                min_cluster_size=2,
                similarity_threshold=0.75
            )
            
            # Find relevant cluster
            relevant_cluster = None
            for cluster in clusters:
                if any(failure_category.lower() in kw.lower() 
                       for kw in cluster.get("common_keywords", [])):
                    relevant_cluster = cluster
                    break
            
            # Extract detailed patterns
            error_messages = []
            failure_contexts = []
            
            for failure in similar_failures:
                # Parse the document text to extract error info
                doc_text = failure.get("document", "")
                if "Error:" in doc_text:
                    error_part = doc_text.split("Error:")[1].split("Context:")[0].strip()
                    if error_part:
                        error_messages.append(error_part)
                
                metadata = failure.get("metadata", {})
                failure_contexts.append({
                    "timestamp": metadata.get("timestamp", ""),
                    "trace_id": metadata.get("trace_id", ""),
                    "category": metadata.get("failure_category", ""),
                    "similarity_score": failure.get("similarity", 0),
                })
            
            # Build comprehensive analysis
            pattern_analysis = {
                "total_similar_failures": len(similar_failures),
                "semantic_search_used": True,
                "common_error_keywords": self._extract_common_keywords(error_messages),
                "similarity_range": {
                    "min": min(f["similarity"] for f in similar_failures) if similar_failures else 0,
                    "max": max(f["similarity"] for f in similar_failures) if similar_failures else 0,
                },
                "cluster_info": {
                    "belongs_to_cluster": relevant_cluster is not None,
                    "cluster_size": relevant_cluster["size"] if relevant_cluster else 0,
                    "cluster_keywords": relevant_cluster["common_keywords"] if relevant_cluster else [],
                } if relevant_cluster else None,
            }
            
            # Get vector store statistics
            stats = self.vector_store.get_statistics()
            pattern_analysis["database_stats"] = {
                "total_failures_indexed": stats.get("failure_requests", 0),
                "total_events": stats.get("total_events", 0),
            }
            
            return {
                "similar_failures": failure_contexts,
                "pattern_analysis": pattern_analysis,
                "detailed_matches": similar_failures[:3],  # Top 3 with full details
            }
            
        except Exception as e:
            logger.error(f"Error in semantic remediation search: {e}")
            # Fallback to simple search
            return self._simple_remediation_search(failure_category, limit)
    
    def _extract_common_keywords(self, messages: List[str]) -> List[str]:
        """Extract common keywords from error messages."""
        if not messages:
            return []
        
        # Simple keyword extraction - count word frequencies
        word_count = {}
        stop_words = {"the", "a", "an", "is", "in", "on", "at", "to", "for", "of", "with", "and", "or"}
        
        for msg in messages:
            words = msg.lower().split()
            for word in words:
                # Clean punctuation and filter stop words
                word = word.strip(".,!?;:")
                if word and word not in stop_words and len(word) > 2:
                    word_count[word] = word_count.get(word, 0) + 1
        
        # Return top keywords
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:5] if count > 1]
    
    def _simple_remediation_search(self, failure_category: str, limit: int) -> Dict[str, Any]:
        """Fallback simple search when vector store is not available."""
        similar_failures = []
        
        if not self.log_file.exists():
            return {"similar_failures": [], "pattern_analysis": {}}
        
        try:
            with open(self.log_file, "r") as f:
                for line in f:
                    try:
                        log_entry = json.loads(line.strip())
                        event = log_entry.get("event", {})
                        
                        if event.get("message_type") == "ArcImprovementRequest":
                            payload = event.get("payload", {})
                            category = payload.get("failure_category", "")
                            
                            if failure_category.lower() in category.lower():
                                similar_failures.append({
                                    "timestamp": log_entry.get("timestamp"),
                                    "trace_id": event.get("trace_id"),
                                    "category": category,
                                    "similarity_score": 1.0,  # Exact match
                                })
                                
                                if len(similar_failures) >= limit:
                                    break
                    except json.JSONDecodeError:
                        continue
            
            return {
                "similar_failures": similar_failures,
                "pattern_analysis": {
                    "total_similar_failures": len(similar_failures),
                    "semantic_search_used": False,
                },
            }
        except Exception as e:
            logger.error(f"Error in simple remediation search: {e}")
            return {"similar_failures": [], "pattern_analysis": {}}