"""CLI tool for Arc Advisor - export data and run interactive demos.

This module provides the command-line interface for Arc Advisor, including:
- Exporting failure data for analysis and migration to Arc Pro
- Interactive demo showcasing the Executor-Advisor pattern with failure-driven learning
"""

import json
import os
import sys
import asyncio
import time
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dotenv import load_dotenv

from .client import ArcAdvisorClient
from .tool_advisor import ToolAugmentedAdvisor
from .multi_agent_hub import ArcA2AMultiAgentHub
from .protocols import ArcAgentCard, AgentCapabilities, AgentSkill, ArcExtension

try:
    from rich.console import Console
    from rich.live import Live
    from rich.panel import Panel
    from rich.columns import Columns
    from rich.text import Text
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class AgentClient:
    """Base class for LLM agent clients."""
    
    def __init__(self, name: str, model: str, specialization: str):
        self.name = name
        self.model = model
        self.specialization = specialization
        self.agent_id = f"{name.lower()}-{uuid.uuid4().hex[:8]}"
    
    async def execute_task(self, prompt: str, context: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Execute a task and return success status and result."""
        raise NotImplementedError


class GPT4Agent(AgentClient):
    """GPT-4.1 agent specialized in structured data analysis."""
    
    def __init__(self, api_key: str):
        super().__init__("GPT-4.1", "gpt-4.1", "Structured Data Analysis & Code Generation")
        self.api_key = api_key
    
    async def execute_task(self, prompt: str, context: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": f"You are {self.specialization}. Focus on data structure, SQL, and technical implementation. Respond with JSON including 'success': true/false and 'result' fields."},
                    {"role": "user", "content": f"Context: {json.dumps(context)}\n\nTask: {prompt}"}
                ],
                temperature=0.3,  # Lower for structured tasks
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("success", True), result
            
        except Exception as e:
            return False, {"success": False, "error": str(e), "agent": self.name}


class ClaudeAgent(AgentClient):
    """Claude Sonnet-4 agent specialized in reasoning and problem-solving."""
    
    def __init__(self, api_key: str):
        super().__init__("Claude-Sonnet-4", "claude-sonnet-4-20250514", "Complex Reasoning & Problem Solving")
        self.api_key = api_key
    
    async def execute_task(self, prompt: str, context: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            
            response = client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.7,
                system=f"You are {self.specialization}. Focus on logical reasoning, policy analysis, and strategic thinking. Always respond with valid JSON including 'success': true/false and 'result' fields.",
                messages=[{
                    "role": "user", 
                    "content": f"Context: {json.dumps(context)}\n\nTask: {prompt}\n\nProvide your response as JSON."
                }]
            )
            
            # Parse JSON from response
            content = response.content[0].text
            # Try to extract JSON if wrapped in markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            return result.get("success", True), result
            
        except Exception as e:
            return False, {"success": False, "error": str(e), "agent": self.name}


class O4MiniAgent(AgentClient):
    """o4-mini agent specialized in rapid iteration and prototyping."""
    
    def __init__(self, api_key: str):
        super().__init__("o4-mini", "o4-mini-2025-04-16", "Rapid Prototyping & Quick Iterations")
        self.api_key = api_key
    
    async def execute_task(self, prompt: str, context: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are {self.specialization}. Focus on quick solutions, iterative improvements, and practical implementations. Respond with JSON including 'success': true/false and 'result' fields."},
                    {"role": "user", "content": f"Context: {json.dumps(context)}\n\nTask: {prompt}"}
                ],
                temperature=0.8,  # Higher for creative iteration
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("success", True), result
            
        except Exception as e:
            return False, {"success": False, "error": str(e), "agent": self.name}


def export():
    """Export Arc Advisor event logs as JSON.
    
    Reads the local event log file and outputs it as a JSON array to stdout.
    This enables developers to analyze their failure data and prepare it for
    upload to Arc's managed learning service.
    """
    log_file = Path.home() / ".arc" / "logs" / "events.log"
    
    if not log_file.exists():
        print(
            "No event log found. The Arc Advisor Client will create logs "
            "when you use the @monitor_and_learn decorator.",
            file=sys.stderr,
        )
        sys.exit(1)
    
    events = []
    
    try:
        with open(log_file, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
    except json.JSONDecodeError as e:
        print(f"Error parsing log file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading log file: {e}", file=sys.stderr)
        sys.exit(1)
    
    if not events:
        print("No events found in log file.", file=sys.stderr)
        sys.exit(0)
    
    # Output as JSON array to stdout
    print(json.dumps(events, indent=2))


def get_multi_agent_scenarios() -> List[Dict[str, Any]]:
    """Get CRMArena-Pro scenarios designed for multi-agent collaboration."""
    return [
        {
            "name": "B2B Enterprise Quote Generation (Multi-Agent)",
            "task": "Generate comprehensive enterprise quote with compliance check",
            "description": "Complex B2B deal requiring data analysis, policy compliance, and iterative refinement",
            "metadata": {
                "account_type": "Enterprise",
                "deal_size": 250000,
                "compliance_required": True,
                "approval_levels": 3
            },
            "context": {
                "query": "Fortune 500 client wants to upgrade 500 Sales Cloud licenses, add Service Cloud for 200 agents, implement CPQ for 50 users, plus custom integrations. Must comply with SOX requirements.",
                "constraints": {
                    "max_discount": 15,
                    "approval_required": True,
                    "compliance_check": "SOX",
                    "timeline": "30 days"
                }
            },
            "agent_collaboration": {
                "gpt4": "Calculate pricing structure and technical requirements",
                "claude": "Analyze compliance requirements and risk assessment", 
                "o4mini": "Iterate on package configurations and optimizations"
            },
            "expected_outcome": "success"
        },
        {
            "name": "Service Escalation with Multi-Policy Violation",
            "task": "Handle complex customer escalation involving multiple policy conflicts",
            "description": "Customer service case requiring cross-team coordination and policy analysis",
            "metadata": {
                "case_type": "Escalation",
                "customer_tier": "Premium",
                "priority": "High",
                "departments": ["Legal", "Finance", "Support"]
            },
            "context": {
                "query": "Premium customer demands immediate refund of $50K annual contract due to claimed data breach. Customer used system for 11 months, contract has no-refund clause, but customer threatens legal action and regulatory complaint.",
                "constraints": {
                    "legal_review_required": True,
                    "refund_authority_limit": 10000,
                    "time_limit_hours": 4,
                    "regulatory_risk": "High"
                }
            },
            "agent_collaboration": {
                "claude": "Analyze legal implications and policy conflicts",
                "gpt4": "Calculate financial impact and alternatives",
                "o4mini": "Develop rapid response options and communications"
            },
            "expected_outcome": "complex"
        },
        {
            "name": "CPQ Configuration with Dependency Resolution",
            "task": "Configure complex product bundle with multiple dependencies and conflicts",
            "description": "Multi-step product configuration requiring technical validation and business rule application",
            "metadata": {
                "cpq_complexity": "High",
                "product_count": 15,
                "rule_conflicts": 3,
                "custom_pricing": True
            },
            "context": {
                "query": "Global client needs Sales Cloud Enterprise (1000 users), Service Cloud Unlimited (500 users), Marketing Cloud (200K contacts), Tableau CRM (50 users), MuleSoft (10 connections), but has existing Pardot instance and custom Apex code that may conflict.",
                "constraints": {
                    "existing_systems": ["Pardot", "Custom Apex", "Legacy CRM"],
                    "integration_required": True,
                    "migration_timeline": "6 months",
                    "budget_limit": 500000
                }
            },
            "agent_collaboration": {
                "gpt4": "Analyze technical dependencies and integration requirements",
                "claude": "Evaluate business rules and conflict resolution strategies",
                "o4mini": "Generate configuration options and alternatives"
            },
            "expected_outcome": "complex"
        }
    ]


def get_crmarena_scenarios() -> List[Dict[str, Any]]:
    """Get realistic CRMArena-Pro inspired scenarios including failure cases."""
    return [
        {
            "name": "B2B Quote Generation (Success Case)",
            "task": "Generate a quote for upgrading CRM licenses",
            "metadata": {
                "account_type": "Enterprise",
                "current_licenses": 100,
                "renewal_date": "2024-06-30",
                "contact_role": "IT Director"
            },
            "context": {
                "query": "Customer wants to add 50 more CRM licenses and upgrade to Enterprise edition. Current contract expires in 6 months.",
                "constraints": {
                    "discount_limit": 20,
                    "approval_required": False,
                    "bundle_available": True
                }
            },
            "expected_outcome": "success"
        },
        {
            "name": "Service Case with Policy Violation (Failure Case)",
            "task": "Process refund request exceeding authority",
            "metadata": {
                "case_type": "Refund Request",
                "customer_tier": "Standard",
                "agent_authority": "Level 1"
            },
            "context": {
                "query": "Customer demanding full refund of $5,000 annual subscription after 8 months of usage due to missing features.",
                "constraints": {
                    "refund_authority_limit": 500,
                    "time_limit_days": 30,
                    "usage_threshold": 0.25
                }
            },
            "expected_outcome": "failure",
            "failure_reason": "Refund amount exceeds agent authority"
        },
        {
            "name": "Complex SQL on Non-Existent Data (Failure Case)",
            "task": "Generate SQL for multi-dimensional analysis",
            "metadata": {
                "database": "Salesforce",
                "api_version": "59.0"
            },
            "context": {
                "query": "Show me all opportunities with custom object 'ProjectTimeline__c' data grouped by quarter and industry vertical.",
                "tables": {
                    "Opportunity": ["Id", "Name", "Amount", "CloseDate", "StageName"],
                    "Account": ["Id", "Name", "Industry"]
                },
                "note": "ProjectTimeline__c does not exist in this org"
            },
            "expected_outcome": "failure",
            "failure_reason": "Referenced object does not exist"
        },
        {
            "name": "CPQ Bundle Configuration",
            "task": "Configure product bundle with dependencies",
            "metadata": {
                "cpq_rules": "active",
                "catalog": "2024-Q1"
            },
            "context": {
                "query": "Customer wants Service Cloud but hasn't purchased Sales Cloud which is a prerequisite.",
                "products": {
                    "Sales_Cloud": {"price": 125, "per": "user/month", "min_users": 10},
                    "Service_Cloud": {"price": 135, "per": "user/month", "requires": "Sales_Cloud"}
                }
            },
            "expected_outcome": "failure",
            "failure_reason": "Product dependency not satisfied"
        }
    ]


def execute_with_gpt4(prompt: str, api_key: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
    """Execute task with GPT-4.1. Requires API key"""
    if not api_key:
        return False, {
            "error": "OPENAI_API_KEY required for real execution", 
            "success": False,
            "details": "Add your OpenAI API key to .env file to enable live inference"
        }
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "developer", "content": "You are a Salesforce automation assistant. Respond with JSON including 'success': true/false and 'result' fields."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get("success", False), result
        
    except Exception as e:
        return False, {"error": str(e), "success": False}


def get_recent_failures(advisor: ArcAdvisorClient, trace_id: str) -> List[Dict[str, Any]]:
    """Get recent failure events from the log."""
    log_file = Path.home() / ".arc" / "logs" / "events.log"
    if not log_file.exists():
        return []
    
    failures = []
    try:
        with open(log_file, "r") as f:
            for line in f:
                if line.strip():
                    event = json.loads(line)
                    if (event.get("event", {}).get("message_type") == "ArcImprovementRequest" and
                        event.get("event", {}).get("agent_id") == advisor.agent_id):
                        failures.append(event["event"]["payload"])
                        if len(failures) >= 3:  # Get last 3 failures
                            break
    except Exception:
        pass
    
    return failures


def demo():
    """Interactive demo of the Executor-Advisor pattern with semantic search.
    
    This represents Stage 1-2 of the Arc roadmap (Human-in-Loop → Mediated Agent-to-Sub-Agent).
    """
    print("\n" + "="*60)
    print("Arc Advisor Interactive Demo with Semantic Search")
    print("="*60)
    print("\nThis demo showcases:")
    print("1. Single agent with Arc Sub Agent advisor (Stage 1-2)")
    print("2. Semantic similarity search across failures")
    print("3. Failure clustering and pattern discovery")
    print("4. Tool-augmented advisor with active learning\n")
    
    print("💡 For multi-agent collaboration demo (Stage 3), use: arc-advisor multi-agent")
    
    # Load environment
    load_dotenv()
    
    # Check for OpenAI API key - REQUIRED for real execution
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY required for live inference")
        print("   Add your OpenAI API key to .env file:")
        print("   echo 'OPENAI_API_KEY=your-key-here' > .env")
        sys.exit(1)
    else:
        print("✅ OpenAI API key detected - using real GPT-4.1 execution")
    
    # Initialize advisor
    print("Initializing Tool-Augmented Arc Advisor with Semantic Search...")
    try:
        advisor = ToolAugmentedAdvisor(
            agent_id="demo-agent-001",
            on_failure="warn"
        )
        print("Tool-augmented advisor model loaded successfully")
        print("Vector database initialized for semantic search")
        print("Available tools: get_remediation_plan, query_success_patterns, analyze_failure_trend")
        
        # Show vector store statistics
        stats = advisor.vector_store.get_statistics()
        print(f"\nVector Database Statistics:")
        print(f"  - Total events indexed: {stats['total_events']}")
        print(f"  - Failure patterns: {stats['failure_requests']}")
        print(f"  - Success patterns: {stats['successful_executions']}")
        print()
        
    except Exception as e:
        print(f"Failed to initialize advisor: {e}")
        sys.exit(1)
    
    # Get scenarios
    scenarios = get_crmarena_scenarios()
    
    print("Select a demo scenario:")
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['name']}")
    print(f"{len(scenarios) + 1}. Custom scenario")
    print("0. Exit\n")
    
    selected_scenario = None
    while True:
        try:
            choice = input(f"Enter your choice (0-{len(scenarios) + 1}): ").strip()
            if choice == "0":
                print("\nThank you for trying Arc Advisor!")
                sys.exit(0)
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(scenarios):
                selected_scenario = scenarios[choice_num - 1]
                break
            elif choice_num == len(scenarios) + 1:
                # Custom scenario
                selected_scenario = {
                    "name": "Custom Scenario",
                    "task": input("\nEnter task description: ").strip(),
                    "context": {"query": input("Enter query: ").strip()},
                    "metadata": {},
                    "expected_outcome": "unknown"
                }
                break
            else:
                print(f"Invalid choice. Please select 0-{len(scenarios) + 1}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Execute the scenario with learning loop
    print(f"\n{'='*60}")
    print(f"Scenario: {selected_scenario['name']}")
    print(f"{'='*60}\n")
    
    # Attempt 1: Initial execution
    print("ATTEMPT 1: Initial Execution")
    print("-" * 40)
    
    # Get initial advisor strategy
    print("\nADVISOR: Generating initial strategy with tool assistance...\n")
    
    initial_context = {
        **selected_scenario.get("context", {}),
        "metadata": selected_scenario.get("metadata", {})
    }
    
    advice = advisor.get_advice(
        task_description=selected_scenario["task"],
        context=initial_context,
        generation_config={
            "temperature": 0.7,
            "max_new_tokens": 400,  # Increased for thinking content
            "top_p": 0.9,
        },
        stream=True,
        enable_tools=True  # Enable tool use
    )
    
    print("\n\nStrategy ready.")
    
    # Show advisor's thinking and tool usage
    if advice and advice.get("thinking"):
        print("\nADVISOR THINKING PROCESS:")
        print("-" * 40)
        print(advice["thinking"])
        print("-" * 40)
    
    if advice and advice.get("tools_used"):
        print(f"\nTools used: {', '.join(advice['tools_used'])}")
        if advice.get("tool_results"):
            print("\nTool Results Summary:")
            for tool, result in advice["tool_results"].items():
                if isinstance(result, dict) and "pattern_analysis" in result:
                    print(f"  - {tool}: Found {result['pattern_analysis'].get('total_similar_failures', 0)} similar failures")
                elif isinstance(result, dict) and "total_successes" in result:
                    print(f"  - {tool}: Found {result['total_successes']} successful patterns")
                elif isinstance(result, dict) and "total_failures" in result:
                    print(f"  - {tool}: {result['total_failures']} failures in {result.get('timeframe', 'N/A')}")
    
    # Execute with the strategy
    print("\nEXECUTOR: Implementing task...")
    
    # Build executor prompt
    executor_prompt = f"""Task: {selected_scenario['task']}
Query: {selected_scenario.get('context', {}).get('query', '')}
Metadata: {json.dumps(selected_scenario.get('metadata', {}))}
Advisor Strategy: {advice['strategy'] if advice else 'No advisor guidance'}

Execute this task following the advisor's strategy."""
    
    # Simulate execution based on expected outcome
    if selected_scenario.get("expected_outcome") == "failure":
        # Simulate failure for demonstration
        success = False
        executor_result = {
            "success": False,
            "error": selected_scenario.get("failure_reason", "Task failed"),
            "details": "The task could not be completed due to constraints"
        }
        print(f"\nX Task failed: {executor_result['error']}")
    else:
        # Try real execution or simulate success
        success, executor_result = execute_with_gpt4(executor_prompt, api_key)
        if success:
            print("\nTask completed successfully")
        else:
            print(f"\nX Task failed: {executor_result.get('error', 'Unknown error')}")
    
    # Track outcome
    @advisor.monitor_and_learn
    def execute_task_with_monitoring(_task: str, _ctx: Dict[str, Any], exec_result: Dict[str, Any]) -> Dict[str, Any]:
        """Execute and monitor the task."""
        return {
            "success": exec_result.get("success", False),
            "output": exec_result,
            "error": exec_result.get("error", ""),
            "metrics": {
                "attempt": 1,
                "execution_time_ms": 250
            }
        }
    
    result = execute_task_with_monitoring(
        selected_scenario["task"], 
        initial_context,
        executor_result
    )
    
    # If task failed, demonstrate the learning loop
    if not result["success"]:
        print("\n" + "="*60)
        print("LEARNING LOOP: Failure Detected")
        print("="*60)
        
        print("\n1. FAILURE TRACKING")
        print("   - Logging failure to ~/.arc/logs/events.log")
        print(f"   - Failure type: {result.get('error', 'Unknown')}")
        print("   - ArcImprovementRequest generated")
        
        print("\n2. ADVISOR ADAPTATION")
        print("   - Analyzing failure context...")
        
        # Get recent failures for context
        recent_failures = get_recent_failures(advisor, "demo")
        
        print(f"   - Found {len(recent_failures)} recent failures to learn from")
        
        # Attempt 2: Retry with adapted strategy
        print("\n" + "-"*40)
        print("ATTEMPT 2: Retry with Adapted Strategy")
        print("-" * 40)
        
        # Build enhanced context with failure information
        enhanced_context = {
            **initial_context,
            "previous_failure": {
                "error": result.get("error", ""),
                "attempt": 1,
                "strategy_used": advice['strategy'] if advice else "None"
            },
            "recent_failures": recent_failures[:2]  # Include last 2 failures
        }
        
        print("\nADVISOR: Generating adapted strategy based on failure...\n")
        
        adapted_advice = advisor.get_advice(
            task_description=f"Retry: {selected_scenario['task']} (after failure: {result.get('error', '')})",
            context=enhanced_context,
            generation_config={
                "temperature": 0.6,  # Lower temperature for more focused retry
                "max_new_tokens": 400,
                "top_p": 0.85,
            },
            stream=True,
            enable_tools=True
        )
        
        print("\n\nAdapted strategy ready.")
        
        # Show advisor's thinking and tool usage for retry
        if adapted_advice and adapted_advice.get("thinking"):
            print("\nADVISOR THINKING PROCESS (RETRY):")
            print("-" * 40)
            print(adapted_advice["thinking"])
            print("-" * 40)
        
        if adapted_advice and adapted_advice.get("tools_used"):
            print(f"\nTools used for retry: {', '.join(adapted_advice['tools_used'])}")
            if adapted_advice.get("tool_results"):
                print("\nTool Results Summary:")
                for tool, result in adapted_advice["tool_results"].items():
                    if isinstance(result, dict) and "pattern_analysis" in result:
                        analysis = result["pattern_analysis"]
                        print(f"\n  {tool}:")
                        if analysis.get("semantic_search_used"):
                            print("    - Using SEMANTIC SEARCH (not just keywords)")
                            print(f"    - Similarity range: {analysis.get('similarity_range', {}).get('min', 0):.2f} - {analysis.get('similarity_range', {}).get('max', 0):.2f}")
                        print(f"    - Found {analysis.get('total_similar_failures', 0)} similar failures")
                        if analysis.get("common_error_keywords"):
                            print(f"    - Common keywords: {', '.join(analysis['common_error_keywords'][:3])}")
                        if analysis.get("cluster_info") and analysis["cluster_info"].get("belongs_to_cluster"):
                            cluster = analysis["cluster_info"]
                            print(f"    - Part of failure cluster with {cluster['cluster_size']} members")
                        if analysis.get("database_stats"):
                            stats = analysis["database_stats"]
                            print(f"    - Vector DB: {stats.get('total_failures_indexed', 0)} failures indexed")
        
        # Retry execution
        print("\nEXECUTOR: Retrying with adapted approach...")
        
        retry_prompt = f"""Task: {selected_scenario['task']}
Query: {selected_scenario.get('context', {}).get('query', '')}
Previous Error: {result.get('error', '')}
Adapted Strategy: {adapted_advice['strategy'] if adapted_advice else 'Proceed with caution'}

Learn from the previous failure and execute this task successfully."""
        
        # Retry with real execution
        retry_success, retry_result = execute_with_gpt4(retry_prompt, api_key)
        
        if retry_success:
            print("\nTask completed successfully on retry!")
        else:
            print(f"\nRetry also failed: {retry_result.get('error', 'Unknown error')}")
        
        # Track retry outcome
        retry_outcome = execute_task_with_monitoring(
            f"Retry: {selected_scenario['task']}", 
            enhanced_context,
            retry_result
        )
        
        print(f"\nFinal outcome: {'Success' if retry_outcome['success'] else 'Failed'}")
    
    # Summary
    print(f"\n{'='*60}")
    print("DEMO COMPLETE")
    print(f"{'='*60}\n")
    
    print("Key Takeaways:")
    print("- Advisor provides strategic guidance for tasks")
    if not result["success"]:
        print("- Failures are tracked and analyzed automatically")
        print("- Advisor adapts strategy based on failure context")
        print("- System learns and improves from productive struggle")
    else:
        print("- Successful executions are logged for pattern analysis")
    
    print("\nNext Steps:")
    print("1. View learning data:     arc-advisor export")
    print("2. Try failure scenarios:  Select options 2-4 in demo")
    print("3. Integration guide:      See examples/crm_pro_example.py")
    print("4. Train custom advisors:  Visit arc.computer\n")
    
    # Ask if they want to run another demo
    again = input("Run another demo? (y/N): ").strip().lower()
    if again == 'y':
        demo()


async def multi_agent_demo():
    """Interactive demo of multi-agent collaboration with Arc Sub Agent orchestration."""
    console = Console() if RICH_AVAILABLE else None
    
    # Print header
    if console:
        console.print("\n" + "="*80, style="bold blue")
        console.print("🌐 Arc Multi-Agent Learning Infrastructure Demo", style="bold cyan", justify="center")
        console.print("="*80, style="bold blue")
        console.print("\n🎯 Showcasing: Autonomous Agent Network with Shared Learning", style="bold green")
        console.print("📋 Agents: GPT-4.1, Claude Sonnet-4, O4-Mini + Arc Sub Agent", style="yellow")
    else:
        print("\n" + "="*80)
        print("Arc Multi-Agent Learning Infrastructure Demo")
        print("="*80)
        print("\nShowcasing: Autonomous Agent Network with Shared Learning")
        print("Agents: GPT-4.1, Claude Sonnet-4, O4-Mini + Arc Sub Agent")
    
    # Load environment
    load_dotenv()
    
    # Check API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not openai_key or not anthropic_key:
        if console:
            console.print("\n❌ Missing API keys. Please add to .env file:", style="bold red")
            console.print("   OPENAI_API_KEY=your_openai_key", style="red")
            console.print("   ANTHROPIC_API_KEY=your_anthropic_key", style="red")
        else:
            print("\nMissing API keys. Please add to .env file:")
            print("   OPENAI_API_KEY=your_openai_key")
            print("   ANTHROPIC_API_KEY=your_anthropic_key")
        return
    
    # Initialize Arc Sub Agent (Central Learning Hub)
    if console:
        console.print("\n🚀 Initializing Arc Learning Infrastructure...", style="bold blue")
    else:
        print("\nInitializing Arc Learning Infrastructure...")
    
    try:
        # Initialize A2A Hub and Arc Sub Agent
        hub = ArcA2AMultiAgentHub(
            hub_id="arc-demo-hub",
            enable_auto_broadcast=True,
            enable_bidirectional=True
        )
        
        # Initialize production agents
        agents = {
            "gpt4": GPT4Agent(openai_key),
            "claude": ClaudeAgent(anthropic_key),
            "o4mini": O4MiniAgent(openai_key)
        }
        
        # Register agents with hub
        for agent_name, agent in agents.items():
            agent_card = ArcAgentCard(
                name=agent.name,
                description=f"{agent.specialization} specialist",
                url=f"http://localhost:8080/{agent_name}",
                version="1.0.0",
                skills=[
                    AgentSkill(
                        id=f"{agent_name}-specialty",
                        name=agent.specialization,
                        description=f"Specialized in {agent.specialization.lower()}",
                        tags=["crm", "business", agent_name]
                    )
                ],
                defaultInputModes=["text", "data"],
                defaultOutputModes=["text", "data"],
                capabilities=AgentCapabilities(
                    streaming=True,
                    pushNotifications=True,
                    extensions=[ArcExtension()]
                )
            )
            
            # Register with hub via A2A protocol
            registration_msg = {
                "jsonrpc": "2.0",
                "id": f"reg-{agent.agent_id}",
                "method": "arc/agent/register",
                "params": {"agent_card": agent_card.model_dump()}
            }
            
            await hub.handle_jsonrpc_message(registration_msg, agent.agent_id)
        
        if console:
            console.print("✅ Arc Sub Agent initialized with semantic search and learning tools", style="green")
            console.print("✅ Three production agents registered in A2A network", style="green")
            
            # Show hub statistics
            stats = hub.get_hub_statistics()
            stats_table = Table(title="Arc Learning Hub Status")
            stats_table.add_column("Metric", style="cyan")
            stats_table.add_column("Value", style="green")
            stats_table.add_row("Active Agents", str(stats["hub_metrics"]["active_agents"]))
            stats_table.add_row("A2A Protocol", stats["protocol_versions"]["a2a"])
            stats_table.add_row("Arc Extension", stats["protocol_versions"]["arc"])
            stats_table.add_row("Bidirectional", "✅" if stats["features"]["bidirectional"] else "❌")
            console.print(stats_table)
        else:
            print("✅ Arc Sub Agent initialized")
            print("✅ Three production agents registered")
    
    except Exception as e:
        if console:
            console.print(f"❌ Failed to initialize: {e}", style="bold red")
        else:
            print(f"Failed to initialize: {e}")
        return
    
    # Select scenario
    scenarios = get_multi_agent_scenarios()
    
    if console:
        console.print("\n📋 Select Multi-Agent Business Scenario:", style="bold yellow")
        for i, scenario in enumerate(scenarios, 1):
            console.print(f"{i}. {scenario['name']}", style="cyan")
            console.print(f"   {scenario['description']}", style="dim")
    else:
        print("\nSelect Multi-Agent Business Scenario:")
        for i, scenario in enumerate(scenarios, 1):
            print(f"{i}. {scenario['name']}")
            print(f"   {scenario['description']}")
    
    # Get user choice
    while True:
        try:
            choice = input(f"\nEnter your choice (1-{len(scenarios)}): ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(scenarios):
                selected_scenario = scenarios[choice_num - 1]
                break
            else:
                print(f"Invalid choice. Please select 1-{len(scenarios)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Execute multi-agent collaboration
    await execute_multi_agent_scenario(hub, agents, selected_scenario, console)


async def execute_multi_agent_scenario(
    hub: ArcA2AMultiAgentHub, 
    agents: Dict[str, AgentClient], 
    scenario: Dict[str, Any],
    console: Optional[Console]
):
    """Execute a multi-agent scenario with real-time streaming display."""
    
    # Header
    if console:
        console.print(f"\n🎬 Executing: {scenario['name']}", style="bold magenta")
        console.print("=" * 80, style="magenta")
    else:
        print(f"\nExecuting: {scenario['name']}")
        print("=" * 80)
    
    # Stage 1: Arc Sub Agent Initial Strategy
    if console:
        console.print("\n🧠 STAGE 1: Arc Sub Agent Strategic Analysis", style="bold blue")
    else:
        print("\nSTAGE 1: Arc Sub Agent Strategic Analysis")
    
    # Get Arc Sub Agent's initial strategy
    strategy_request = {
        "jsonrpc": "2.0",
        "id": f"strategy-{uuid.uuid4().hex[:8]}",
        "method": "arc/advice/request",
        "params": {
            "task_description": scenario["task"],
            "context": scenario["context"],
            "previous_attempts": []
        }
    }
    
    strategy_response = await hub.handle_jsonrpc_message(strategy_request, "arc-orchestrator")
    strategy = strategy_response.get("result", {})
    
    if console:
        strategy_panel = Panel(
            strategy.get("strategy", "Coordinate agents based on their specializations"),
            title="🎯 Arc Sub Agent Strategy",
            border_style="blue"
        )
        console.print(strategy_panel)
        
        # Show tools used
        if strategy.get("tools_used"):
            tools_text = Text()
            tools_text.append("🔧 Tools Used: ", style="bold")
            tools_text.append(", ".join(strategy["tools_used"]), style="cyan")
            console.print(tools_text)
    else:
        print(f"\nArc Strategy: {strategy.get('strategy', 'Coordinate agents')}")
    
    # Stage 2: Multi-Agent Collaboration
    if console:
        console.print("\n🤝 STAGE 2: Multi-Agent Collaboration", style="bold green")
    else:
        print("\nSTAGE 2: Multi-Agent Collaboration")
    
    agent_results = {}
    agent_collaboration = scenario.get("agent_collaboration", {})
    
    # Execute tasks in parallel with real-time updates
    if console:
        with Live(console=console, refresh_per_second=2) as live:
            tasks = []
            for agent_key, task_desc in agent_collaboration.items():
                if agent_key in agents:
                    task = execute_agent_task(agents[agent_key], task_desc, scenario["context"], console)
                    tasks.append((agent_key, task))
            
            # Wait for all tasks with progress updates
            progress_table = Table(title="Agent Execution Progress")
            progress_table.add_column("Agent", style="cyan")
            progress_table.add_column("Status", style="yellow")
            progress_table.add_column("Specialization", style="green")
            
            for agent_key, task in tasks:
                agent = agents[agent_key]
                progress_table.add_row(
                    agent.name, 
                    "🔄 Working...", 
                    agent.specialization
                )
            
            live.update(progress_table)
            
            # Execute tasks and collect results
            for agent_key, task in tasks:
                try:
                    success, result = await task
                    agent_results[agent_key] = {"success": success, "result": result}
                    
                    # Update progress
                    progress_table = Table(title="Agent Execution Progress")
                    progress_table.add_column("Agent", style="cyan")
                    progress_table.add_column("Status", style="yellow")
                    progress_table.add_column("Specialization", style="green")
                    
                    for ak, _ in tasks:
                        agent = agents[ak]
                        status = "✅ Complete" if ak in agent_results else "🔄 Working..."
                        progress_table.add_row(agent.name, status, agent.specialization)
                    
                    live.update(progress_table)
                    await asyncio.sleep(0.5)  # Brief pause for visual effect
                    
                except Exception as e:
                    agent_results[agent_key] = {"success": False, "result": {"error": str(e)}}
    else:
        # Non-rich version
        tasks = []
        for agent_key, task_desc in agent_collaboration.items():
            if agent_key in agents:
                print(f"\n{agents[agent_key].name}: {task_desc}")
                task = execute_agent_task(agents[agent_key], task_desc, scenario["context"], None)
                tasks.append((agent_key, task))
        
        for agent_key, task in tasks:
            try:
                success, result = await task
                agent_results[agent_key] = {"success": success, "result": result}
                print(f"✅ {agents[agent_key].name} completed")
            except Exception as e:
                agent_results[agent_key] = {"success": False, "result": {"error": str(e)}}
                print(f"❌ {agents[agent_key].name} failed: {e}")
    
    # Stage 3: Arc Sub Agent Synthesis
    if console:
        console.print("\n🧩 STAGE 3: Arc Sub Agent Synthesis & Learning", style="bold purple")
    else:
        print("\nSTAGE 3: Arc Sub Agent Synthesis & Learning")
    
    # Collect agent outputs for synthesis
    synthesis_context = {
        **scenario["context"],
        "agent_results": agent_results,
        "collaboration_pattern": agent_collaboration
    }
    
    # Arc Sub Agent synthesizes the results
    synthesis_request = {
        "jsonrpc": "2.0",
        "id": f"synthesis-{uuid.uuid4().hex[:8]}",
        "method": "arc/advisor/query",
        "params": {
            "query_type": "pattern_analysis",
            "query_context": synthesis_context,
            "limit": 5
        }
    }
    
    synthesis_response = await hub.handle_jsonrpc_message(synthesis_request, "arc-orchestrator")
    synthesis = synthesis_response.get("result", {})
    
    # Submit reward signals for each agent
    for agent_key, result in agent_results.items():
        reward_request = {
            "jsonrpc": "2.0",
            "id": f"reward-{uuid.uuid4().hex[:8]}",
            "method": "arc/reward/submit",
            "params": {
                "advisor_trace_id": strategy_request["id"],
                "task_trace_id": f"task-{agent_key}-{uuid.uuid4().hex[:8]}",
                "task_success": result["success"],
                "advice_followed": True,
                "advice_quality_score": 0.9 if result["success"] else 0.6,
                "context_relevance": 0.85,
                "context_clarity": 0.9,
                "context_actionability": 0.8,
                "agent_confidence_before": 0.7,
                "agent_confidence_after": 0.9 if result["success"] else 0.6,
                "execution_time_ms": 2000
            }
        }
        await hub.handle_jsonrpc_message(reward_request, agents[agent_key].agent_id)
    
    # Display results
    if console:
        # Show agent results
        results_table = Table(title="Multi-Agent Collaboration Results")
        results_table.add_column("Agent", style="cyan")
        results_table.add_column("Status", style="yellow")
        results_table.add_column("Key Output", style="green")
        
        for agent_key, result in agent_results.items():
            agent = agents[agent_key]
            status = "✅ Success" if result["success"] else "❌ Failed"
            output = result["result"].get("result", result["result"].get("error", "No output"))[:60] + "..."
            results_table.add_row(agent.name, status, output)
        
        console.print(results_table)
        
        # Show synthesis
        synthesis_panel = Panel(
            f"Confidence: {synthesis.get('confidence_score', 0):.2f}\n" +
            f"Patterns Found: {synthesis.get('patterns_found', 0)}\n" +
            "Insights: " + str(synthesis.get('insights', [])[:2]),
            title="🎯 Arc Learning Synthesis",
            border_style="purple"
        )
        console.print(synthesis_panel)
        
        # Final statistics
        final_stats = hub.get_hub_statistics()
        console.print(f"\n📊 Learning Session Complete:", style="bold green")
        console.print(f"   • Reward Signals Collected: {final_stats['reward_signals_collected']}", style="green")
        console.print(f"   • Agent Collaborations: {len(agent_results)}", style="green")
        console.print(f"   • Knowledge Patterns: {synthesis.get('patterns_found', 0)}", style="green")
        
    else:
        print("\nMulti-Agent Results:")
        for agent_key, result in agent_results.items():
            status = "Success" if result["success"] else "Failed"
            print(f"  {agents[agent_key].name}: {status}")
        
        print(f"\nArc Learning: {synthesis.get('patterns_found', 0)} patterns discovered")
        print("Reward signals collected for future GRPO training")


async def execute_agent_task(
    agent: AgentClient, 
    task_description: str, 
    context: Dict[str, Any],
    console: Optional[Console]
) -> Tuple[bool, Dict[str, Any]]:
    """Execute a task for a specific agent."""
    
    # Add some realistic delay for demonstration
    await asyncio.sleep(1 + (hash(agent.name) % 3))  # 1-4 second delay
    
    # Build full prompt with agent specialization context
    full_prompt = f"""
{task_description}

Your specialization: {agent.specialization}
Focus on your expertise while considering the broader business context.
Provide practical, actionable results that other agents can build upon.
"""
    
    return await agent.execute_task(full_prompt, context)


def main():
    """Main CLI dispatcher."""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "export":
            export()
        elif command == "single-agent":
            demo()
        elif command == "multi-agent":
            # Run async multi-agent demo
            try:
                asyncio.run(multi_agent_demo())
            except KeyboardInterrupt:
                print("\n\nDemo interrupted by user")
            except Exception as e:
                print(f"\nDemo failed: {e}")
        else:
            print(f"Unknown command: {command}")
            print("Usage: arc-advisor [export|single-agent|multi-agent]")
            sys.exit(1)
    else:
        print("Arc Advisor CLI")
        print("\nCommands:")
        print("  export        - Export learning data as JSON")
        print("  single-agent  - Run single-agent demo (Stage 1-2)")
        print("  multi-agent   - Run multi-agent demo (Stage 3)")
        print("\nRoadmap Progression:")
        print("  Stage 1: Human-in-Loop (basic advisor)")
        print("  Stage 2: Mediated Agent-to-Sub-Agent (single-agent)")
        print("  Stage 3: Autonomous Agent Network (multi-agent)")
        print("\nUsage: arc-advisor [export|single-agent|multi-agent]")
        sys.exit(0)


if __name__ == "__main__":
    main()