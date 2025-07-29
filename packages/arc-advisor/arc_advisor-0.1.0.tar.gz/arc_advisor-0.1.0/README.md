# Arc Advisor - Learning Infrastructure for Agentic Systems

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org)
[![PyPI](https://img.shields.io/pypi/v/arc-advisor.svg)](https://pypi.org/project/arc-advisor/)

> **Reference Implementation**: This is an experimental reference implementation of the Arc methodology, designed for developers to extend. The library provides a complete infrastructure for building self-improving agents through the Executor-Advisor pattern, with full data collection pipelines for GRPO training and multi-agent orchestration.

Arc Advisor implements the **Executor-Advisor pattern** - an architecture for building self-improving AI agents through separation of reasoning and learning. This library provides production-ready infrastructure for deploying agents that learn from their failures.

## Key Innovation: The Executor-Advisor Pattern

Traditional AI agents fail at complex, multi-step tasks due to lack of specialization. The Executor-Advisor pattern addresses this through architectural separation:

- **Executor**: General-purpose reasoning model (e.g., GPT-4.1) that handles task execution
- **Advisor**: Smaller, specialized model providing strategic guidance based on learned patterns
- **Learning Loop**: Continuous improvement through failure analysis and model updates

This pattern enables agents to improve performance without modifying the base LLM, reducing risk while enabling specialization.

![Arc Advisor Architecture](public/arc-advisor.png)

## Multi-Agent Evolution Roadmap

![Arc Progression](public/roadmap-background.png)

Arc Advisor enables a progressive deployment strategy for agentic systems, where the next level of contextual intelligence is determined by the quality of orchestration. Each stage builds upon the previous, allowing teams to start with human oversight and evolve toward autonomous agent networks.

**Stage 1: Human-in-the-Loop** represents the foundation where humans orchestrate agent control flow through the Arc API. This stage uses the `ArcAdvisorClient` with local advisor models and the `@monitor_and_learn` decorator to provide safe deployment with human oversight. The learning infrastructure captures all interactions for future training while maintaining human control over critical decisions.

**Stage 2: Mediated Agent-to-Sub-Agent Interaction** introduces autonomous operation with learned pattern matching. Here, production agents query the Arc Sub Agent for strategic guidance using `ToolAugmentedAdvisor` with semantic search capabilities. The advisor actively uses tools like `get_remediation_plan` and `query_success_patterns` to provide data-driven strategies based on historical failure analysis and success patterns.

**Stage 3: Autonomous Agent Network with Shared Learning** represents the full vision where the Arc Sub Agent orchestrates multiple specialized agents. The `multi_agent_demo()` showcases A2A-compliant hub managing GPT-4.1, Claude Sonnet-4, and O4-Mini agents working in parallel on complex business scenarios. Each agent contributes its expertise while the Arc Sub Agent synthesizes results and collects reward signals for future GRPO training.

The open-source library provides the complete infrastructure for all three stages, with structured failure data collection preparing organizations for reinforcement learning-trained advisor models. This methodology combines semantic similarity clustering for failure pattern discovery with reward signal aggregation from multi-agent collaboration outcomes, creating a foundation for truly autonomous agentic systems.

## Technical Overview

Arc Advisor provides:

1. **Inference Pipeline**: Local execution of advisor models with automatic device optimization (CUDA/MPS/CPU)
2. **Vector Database**: Semantic search powered by ChromaDB for intelligent pattern discovery
3. **Failure Tracking**: Structured logging with automatic indexing for similarity search
4. **Tool-Augmented Reasoning**: Advisor actively queries its knowledge base for data-driven strategies
5. **Model Agnostic**: Support for any HuggingFace causal language model as advisor
6. **Production Ready**: Robust error handling, configurable failure modes, and comprehensive logging

## Installation

```bash
pip install arc-advisor
```

For development with latest features:
```bash
git clone https://github.com/arc-computer/arc-advisor.git
cd arc-advisor
pip install -e .
```

## Quick Start

### Try the Interactive Demos

Experience the Arc methodology across all three stages of the agentic evolution:

```bash
# Stage 1-2: Single agent with Arc Sub Agent advisor
arc-advisor single-agent

# Stage 3: Multi-agent autonomous network
arc-advisor multi-agent

# Export learning data for analysis
arc-advisor export
```

**Requirements for live inference:**
```bash
# Required for all demos
echo "OPENAI_API_KEY=your-key-here" > .env

# Additional requirement for multi-agent
echo "ANTHROPIC_API_KEY=your-key-here" >> .env
```

The demos showcase real learning infrastructure with:
- **Live streaming inference** - No mocks, only production AI models
- **Semantic failure analysis** - ChromaDB vector search for pattern discovery
- **GRPO reward collection** - Structured signals for future RL training
- **A2A protocol compliance** - Industry-standard agent communication

### Integrate in Your Code

```python
from arc_advisor import ArcAdvisorClient

# Initialize with pre-trained advisor model
advisor = ArcAdvisorClient(
    agent_id="my-agent-001",
    hf_repo_id="Qwen/Qwen3-4B"  # Default general advisor
    # hf_repo_id="arc-computer/qwen3-4b-grpo"  # RL-trained advisor (coming soon)
)

# Decorate your agent's task function
@advisor.monitor_and_learn
def execute_task(query: str, context: dict) -> dict:
    # Get strategic advice before execution
    advice = advisor.get_advice(
        task_description="Complex multi-step workflow",
        context={"query": query, "business_context": context}
    )
    
    # Execute with your primary model
    result = your_executor_model(
        prompt=f"Task: {query}\nStrategy: {advice['strategy']}\nExecute:"
    )
    
    # Return structured outcome
    return {
        "success": validate_result(result),
        "output": result,
        "metrics": {"latency_ms": 150}
    }
```

## Architecture Details

### System Components

The Arc Advisor system consists of three primary components:

1. **Advisor Model**: Provides strategic guidance based on task context
2. **Executor Agent**: Implements the actual task using advisor strategies  
3. **Learning Infrastructure**: Captures failures for continuous improvement

### Data Flow

1. Task request arrives with context
2. Advisor generates strategy based on learned patterns
3. Executor implements task using strategy
4. Outcome logged for learning
5. Failures trigger improvement requests

### Learning Loop

![Arc Learning Infrastructure](public/architecture-background.png)

The learning loop operates as follows:

- **Production Environment**: Agent traces collected during normal operation
- **Failure Bank**: Structured storage of failure patterns and context
- **Learning Orchestrator**: Converts failures into training data
- **RL Training**: Updates advisor model using policy gradient methods
- **Evaluation**: Validates improvements before deployment

**Note**: This open-source reference implementation provides complete data collection infrastructure including:
- Structured failure tracking with semantic embeddings
- GRPO reward signal collection with custom metrics
- A2A-compliant multi-agent orchestration
- Export pipelines for training data preparation

The full continuous learning loop with automated RL training shown above is available through Arc's managed cloud.

## Advanced Configuration

### Vector Database for Semantic Search

Arc Advisor includes a vector database that enables:
- **Semantic Similarity**: Find related failures beyond keyword matching
- **Failure Clustering**: Discover common patterns across failures
- **Intelligent Remediation**: Data-driven strategies based on historical patterns

```python
# Migrate existing events to vector DB
arc-advisor-migrate

# Use tool-augmented advisor with semantic search
from arc_advisor import ToolAugmentedAdvisor

advisor = ToolAugmentedAdvisor(
    agent_id="my-agent",
    on_failure="warn"
)

# Advisor now uses semantic search in its tools
advice = advisor.get_advice(
    task_description="Handle database connection timeout",
    context={"error": "Connection pool exhausted"},
    enable_tools=True
)
```

### Custom Advisor Models

Deploy your own trained advisor:

```python
advisor = ArcAdvisorClient(
    agent_id="domain-specific-agent",
    hf_repo_id="your-org/custom-advisor-7b",
    local_model_dir="~/.arc/models"
)
```

### Generation Parameters

Control advisor output characteristics:

```python
advice = advisor.get_advice(
    task_description="Generate SQL for complex join",
    context={"schema": database_schema},
    generation_config={
        "temperature": 0.3,
        "max_new_tokens": 512,
        "top_p": 0.9
    }
)
```

### Failure Handling

Configure behavior when advisor fails:

```python
# Default: Continue without advice
advisor = ArcAdvisorClient(agent_id="prod-agent", on_failure="warn")

# Strict: Raise exception on failure  
advisor = ArcAdvisorClient(agent_id="test-agent", on_failure="raise")
```

## Interactive Learning Methodology

Arc Advisor implements a novel training methodology inspired by Reinforcement Learning Teachers (RLT) and GRPO optimization, where **advisors learn to teach rather than solve**:

### Stage-Based Learning Architecture

```bash
# Stage 1-2: Single-agent with advisor learning
arc-advisor single-agent
```
- **ToolAugmentedAdvisor** queries semantic failure patterns 
- **Streaming inference** with real-time strategy generation
- **Semantic clustering** discovers failure categories automatically
- **Reward signal collection** for GRPO policy optimization

```bash  
# Stage 3: Multi-agent collaborative learning
arc-advisor multi-agent
```
- **A2A-compliant orchestration** of specialized agents (GPT-4.1, Claude, O4-Mini)
- **Competitive evaluation** through agent collaboration outcomes
- **Relative performance metrics** replace binary success/failure signals
- **Round-robin learning** where agents teach each other through shared experiences

### Learning Infrastructure Features

**Semantic Pattern Discovery:**
- Vector similarity search beyond keyword matching
- Automatic failure clustering using ChromaDB embeddings
- Context-aware remediation strategies from historical patterns

**GRPO Reward Collection:**
- Structured signals from multi-agent collaboration outcomes
- Comparative performance evaluation between agent strategies
- Policy gradient preparation for advisor model fine-tuning
- **Enhanced custom metrics capture** for domain-specific optimization

**Real-Time Learning:**
- Live streaming inference during strategy generation
- Immediate failure indexing and pattern recognition  
- Bidirectional A2A communication for collaborative improvement

## Data Export and Analysis

Export collected failure data for analysis:

```bash
# Export all events
arc-advisor export > agent_events.json

# Extract failure patterns
cat agent_events.json | jq '.[] | select(.event.message_type == "ArcImprovementRequest")'
```

## Example: CRM Automation

See [examples/crm_pro_example.py](examples/crm_pro_example.py) for a complete implementation of a Salesforce CPQ agent using the Executor-Advisor pattern, demonstrating:

- Integration with GPT-4 as executor
- Structured context building for CRM workflows
- Failure tracking for quote generation tasks
- BANT qualification and compliance checking

## Performance Characteristics

- **Advisor Latency**: <100ms on consumer GPUs (MPS/CUDA)
- **Memory Requirements**: 8GB RAM for 4B parameter models
- **Disk Storage**: 10GB for model weights
- **Logging Overhead**: <5ms per event
- **Reward Signal Storage**: ~1KB per interaction (JSONL format)

## API Reference

### ArcAdvisorClient

```python
ArcAdvisorClient(
    agent_id: str,                    # Unique identifier for agent instance
    api_key: Optional[str] = None,    # For future cloud integration
    hf_repo_id: str = "Qwen/Qwen3-4B", # HuggingFace model repository
    local_model_dir: str = "~/.arc/models",  # Local model cache
    on_failure: str = "warn"          # Failure mode: "warn" or "raise"
)
```

### Core Methods

- `get_advice(task_description, context, generation_config)` - Retrieve strategic guidance
- `@monitor_and_learn` - Decorator for automatic outcome tracking
- Event logs: `~/.arc/logs/events.log` (JSON Lines format)

## Protocol Specification

Arc Advisor implements A2A (Agent-to-Agent) protocol for learning communication:

- `ArcLearningReport`: Captures task execution outcomes
- `ArcImprovementRequest`: Signals need for learning from failures

See [arc_advisor/protocols.py](arc_advisor/protocols.py) for schema definitions.

## Contributing

We welcome contributions. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Apache 2.0. See [LICENSE](LICENSE) for details.

## Citation

If you use Arc Advisor in your research, please cite:

```bibtex
@software{arc_advisor,
  title = {Arc Advisor: Learning Infrastructure for Agentic Systems},
  author = {The Arc Intellgence Team},
  year = {2025},
  url = {https://github.com/arc-computer/arc-advisor}
}
```

---

Built by [The Arc Intelligence Team](https://arc.computer)