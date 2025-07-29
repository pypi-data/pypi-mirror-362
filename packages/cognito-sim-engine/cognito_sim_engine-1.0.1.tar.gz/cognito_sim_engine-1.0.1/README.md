# 🧠 Cognito Simulation Engine

[![PyPI - Version](https://img.shields.io/pypi/v/cognito-sim-engine?color=green&label=PyPI&logo=pypi)](https://pypi.org/project/cognito-sim-engine/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-brightgreen.svg)](https://krish567366.github.io/cognito-sim-engine)
[![PyPI Downloads](https://static.pepy.tech/badge/cognito-sim-engine)](https://pepy.tech/projects/cognito-sim-engine)

**A modular cognitive simulation engine for modeling and testing advanced AI cognitive architectures.**

Cognito Simulation Engine is a groundbreaking framework designed for AGI research, providing sophisticated tools for simulating cognitive processes including symbolic reasoning, memory modeling, goal-directed behavior, and metacognitive learning agents.

## 🌟 Features

### Core Cognitive Systems

- **🧠 Advanced Memory Modeling**: Working memory, episodic memory, and long-term memory with realistic cognitive constraints
- **🎯 Goal-Directed Reasoning**: Symbolic reasoning engine with forward/backward chaining and abductive inference
- **🤖 Cognitive Agents**: Multiple agent architectures (Basic, Reasoning, Learning, MetaCognitive)
- **🌍 Interactive Environments**: Rich environments for agent perception, action, and learning
- **📊 Comprehensive Analytics**: Performance metrics, behavioral analysis, and cognitive load monitoring

### Advanced Capabilities

- **🔄 Metacognitive Reflection**: Agents that reason about their own cognitive processes
- **📚 Episodic Memory Simulation**: Realistic memory formation, consolidation, and retrieval
- **⚡ Working Memory Constraints**: Miller's 7±2 rule implementation with attention dynamics
- **🧩 Symbolic Reasoning**: Rule-based inference with uncertainty handling
- **🎓 Multiple Learning Strategies**: Reinforcement learning, discovery learning, and imitation learning

## 🚀 Quick Start

### Installation

```bash
pip install cognito-sim-engine
```

### Basic Usage

```python
from cognito_sim_engine import CognitiveEngine, CognitiveAgent, CognitiveEnvironment
from cognito_sim_engine import Goal, Fact, SimulationConfig

# Create a cognitive environment
env = CognitiveEnvironment("Research Lab")

# Configure the simulation
config = SimulationConfig(
    max_cycles=100,
    working_memory_capacity=7,
    enable_metacognition=True,
    enable_learning=True
)

# Create the cognitive engine
engine = CognitiveEngine(config=config, environment=env)

# Create a cognitive agent
agent = CognitiveAgent("researcher_01", "Dr. Cognitive")

# Add the agent to the environment
env.add_agent("researcher_01")

# Define a research goal
research_goal = Goal(
    description="Understand the cognitive architecture",
    priority=0.8,
    target_facts=[Fact("understood", ["cognitive_architecture"])]
)

# Add goal to the agent
agent.add_goal(research_goal)

# Run the simulation
metrics = engine.run_simulation()

print(f"Simulation completed in {metrics.total_cycles} cycles")
print(f"Goals achieved: {metrics.goals_achieved}")
```

### Command Line Interface

The package includes a powerful CLI for running simulations:

```bash
# Run a basic simulation
cogsim run --cycles 100 --agents 2 --agent-type cognitive

# Run an interactive simulation
cogsim run --interactive --cycles 50 --verbose

# Create a specialized reasoning agent
cogsim create-agent --type reasoning --name "LogicMaster"

# Run demonstration scenarios
cogsim demo --scenario reasoning --interactive

# Analyze simulation results
cogsim analyze session.json --format console

# Show system capabilities
cogsim info
```

## 🏗️ Architecture Overview

### Cognitive Engine

The central orchestrator that manages cognitive cycles:

- **Perception Processing**: Multi-modal sensory input handling
- **Memory Management**: Automatic consolidation and decay
- **Reasoning Coordination**: Goal-directed inference execution
- **Action Selection**: Priority-based decision making
- **Learning Integration**: Experience-based adaptation

### Memory System

Biologically-inspired memory architecture:

```python
from cognito_sim_engine import MemoryManager, MemoryItem, MemoryType

# Create memory manager
memory = MemoryManager(working_capacity=7, decay_rate=0.02)

# Store different types of memories
working_memory_item = MemoryItem(
    content="Current task: analyze data",
    memory_type=MemoryType.WORKING,
    importance=0.8
)

episodic_memory_item = MemoryItem(
    content="Yesterday I learned about neural networks",
    memory_type=MemoryType.EPISODIC,
    importance=0.6
)

memory.store_memory(working_memory_item)
memory.store_memory(episodic_memory_item)

# Retrieve memories
relevant_memories = memory.search_memories("neural networks")
```

### Reasoning Engine

Symbolic reasoning with multiple inference strategies:

```python
from cognito_sim_engine import InferenceEngine, Rule, Fact, Goal

# Create inference engine
reasoner = InferenceEngine(depth_limit=10)

# Define reasoning rules
learning_rule = Rule(
    conditions=[
        Fact("wants_to_learn", ["?agent", "?topic"]),
        Fact("has_resource", ["?agent", "?resource"]),
        Fact("teaches", ["?resource", "?topic"])
    ],
    conclusion=Fact("should_study", ["?agent", "?resource"]),
    confidence=0.9,
    name="learning_strategy"
)

reasoner.reasoner.add_rule(learning_rule)

# Define facts
reasoner.reasoner.add_fact(Fact("wants_to_learn", ["alice", "AI"]))
reasoner.reasoner.add_fact(Fact("has_resource", ["alice", "textbook"]))
reasoner.reasoner.add_fact(Fact("teaches", ["textbook", "AI"]))

# Perform inference
goal = Goal(
    description="Learn about AI",
    target_facts=[Fact("knows", ["alice", "AI"])]
)

result = reasoner.infer(goal, list(reasoner.reasoner.facts.values()))
print(f"Reasoning successful: {result.success}")
print(f"Recommended actions: {[a.name for a in result.recommended_actions]}")
```

## 🤖 Agent Types

### CognitiveAgent

Basic cognitive agent with memory, reasoning, and learning:

```python
from cognito_sim_engine import CognitiveAgent, AgentPersonality

# Create agent with custom personality
personality = AgentPersonality(
    curiosity=0.8,      # High exploration tendency
    analyticalness=0.7, # Prefers logical reasoning
    creativity=0.6      # Moderate creative problem solving
)

agent = CognitiveAgent(
    agent_id="explorer_01",
    name="Explorer",
    personality=personality,
    working_memory_capacity=7,
    enable_metacognition=True
)
```

### ReasoningAgent

Specialized for symbolic reasoning and logical problem solving:

```python
from cognito_sim_engine import ReasoningAgent

reasoning_agent = ReasoningAgent("logician_01", "Dr. Logic")
# Enhanced reasoning capabilities with multiple strategies
# Automatic domain knowledge loading for problem-solving
```

### LearningAgent

Focused on adaptive learning and skill acquisition:

```python
from cognito_sim_engine import LearningAgent

learning_agent = LearningAgent("student_01", "Ada Learner")
# Multiple learning strategies: reinforcement, discovery, imitation
# Skill level tracking and adaptive strategy selection
```

### MetaCognitiveAgent

Advanced agent with self-reflection and cognitive monitoring:

```python
from cognito_sim_engine import MetaCognitiveAgent

meta_agent = MetaCognitiveAgent("philosopher_01", "Meta Thinker")
# Cognitive load monitoring
# Strategy effectiveness evaluation
# Self-model updating
```

## 🌍 Environment System

Create rich, interactive environments for agent simulation:

```python
from cognito_sim_engine import CognitiveEnvironment, EnvironmentObject, Action

# Create environment
env = CognitiveEnvironment("Laboratory")

# Add interactive objects
microscope = EnvironmentObject(
    name="microscope",
    object_type="instrument",
    position={"x": 5, "y": 3, "z": 1},
    properties={"magnification": "1000x", "state": "available"},
    interactable=True,
    description="High-powered research microscope"
)

env.state.add_object(microscope)

# Add custom action handlers
def use_microscope(action, agent_id):
    return True  # Custom interaction logic

env.add_action_handler("use_microscope", use_microscope)
```

## 📚 Example Use Cases

### 1. Cognitive Architecture Research

```python
# Study working memory limitations
config = SimulationConfig(working_memory_capacity=5)  # Below normal capacity
agent = CognitiveAgent("test_subject", working_memory_capacity=5)

# Add multiple competing goals to test cognitive load
for i in range(10):
    goal = Goal(f"Task {i}", priority=random.uniform(0.3, 0.9))
    agent.add_goal(goal)

# Monitor performance degradation
metrics = engine.run_simulation()
```

### 2. Learning Strategy Comparison

```python
# Compare different learning approaches
reinforcement_agent = LearningAgent("rl_agent")
reinforcement_agent.learning_strategy = LearningStrategy.REINFORCEMENT

discovery_agent = LearningAgent("discovery_agent") 
discovery_agent.learning_strategy = LearningStrategy.DISCOVERY

# Run parallel simulations and compare performance
```

### 3. Metacognitive Development

```python
# Study metacognitive development
meta_agent = MetaCognitiveAgent("developing_mind")

# Add metacognitive learning callback
def track_metacognition(agent, feedback):
    insights = len(agent.metacognitive_insights)
    print(f"Metacognitive insights: {insights}")

meta_agent.learning_callbacks.append(track_metacognition)
```

## 🔧 Configuration

Comprehensive configuration options for fine-tuning simulations:

```python
config = SimulationConfig(
    max_cycles=1000,                    # Simulation length
    cycle_timeout=1.0,                  # Real-time cycle duration
    working_memory_capacity=7,          # Miller's magical number
    attention_threshold=0.5,            # Attention focus threshold
    goal_timeout=300.0,                 # Goal expiration time
    enable_metacognition=True,          # Metacognitive capabilities
    enable_learning=True,               # Learning mechanisms
    enable_visualization=False,         # Visual debugging
    memory_decay_rate=0.01,            # Memory decay rate
    attention_decay_rate=0.05,         # Attention decay
    reasoning_depth_limit=10,          # Maximum reasoning depth
    enable_metrics=True,               # Performance tracking
    random_seed=42                     # Reproducible results
)
```

## 📊 Analysis and Visualization

Built-in tools for analyzing cognitive behavior:

```python
# Get comprehensive agent state
cognitive_state = agent.get_cognitive_state()

# Export simulation data
session_data = engine.export_session("simulation.json")
agent_data = agent.export_agent_data()

# Memory system analysis
memory_stats = agent.memory_manager.get_memory_statistics()
print(f"Working memory usage: {memory_stats['working_memory']['usage']:.2f}")
print(f"Total memories: {memory_stats['total_memories']}")

# Reasoning analysis
reasoning_summary = agent.inference_engine.reasoner.get_knowledge_summary()
print(f"Facts: {reasoning_summary['total_facts']}")
print(f"Rules: {reasoning_summary['total_rules']}")
```

## 🧪 Research Applications

### AGI Development

- **Cognitive Architecture Testing**: Validate theoretical cognitive models
- **Scalability Studies**: Test cognitive systems under varying loads
- **Integration Research**: Study interaction between cognitive subsystems

### Psychology & Cognitive Science

- **Memory Research**: Investigate memory formation and retrieval patterns
- **Attention Studies**: Model attention allocation and switching
- **Learning Research**: Compare learning strategies and effectiveness

### AI Safety & Alignment

- **Goal Alignment**: Study how agents pursue and modify goals
- **Metacognitive Safety**: Research self-reflective AI behavior
- **Cognitive Containment**: Test cognitive limitation strategies

## 🛠️ Development & Extension

### Plugin Architecture

```python
# Create custom cognitive modules
from cognito_sim_engine import BaseAgent

class EmotionalAgent(BaseAgent):
    def __init__(self, agent_id, name=""):
        super().__init__(agent_id, name)
        self.emotions = {"joy": 0.5, "fear": 0.1, "anger": 0.0}
    
    def perceive(self, perceptions):
        # Custom emotional processing
        pass
    
    def reason(self):
        # Emotion-influenced reasoning
        pass
```

### Custom Environments

```python
# Create domain-specific environments
class SocialEnvironment(CognitiveEnvironment):
    def __init__(self):
        super().__init__("Social World")
        self.social_dynamics = SocialDynamicsEngine()
    
    def get_perceptions(self, agent_id=None):
        # Add social perceptions
        perceptions = super().get_perceptions(agent_id)
        social_perceptions = self.social_dynamics.get_social_cues(agent_id)
        return perceptions + social_perceptions
```

## 📖 Documentation

Comprehensive documentation is available at: [https://krish567366.github.io/cognito-sim-engine](https://krish567366.github.io/cognito-sim-engine)

### Documentation Sections

- **Getting Started**: Installation and basic usage
- **Cognitive Theory**: Theoretical foundations and design principles
- **API Reference**: Complete API documentation with examples
- **Advanced Usage**: Complex scenarios and customization
- **Research Applications**: Real-world research use cases
- **Contributing**: Development guidelines and contribution process

## 📦 Installation Options

### PyPI (Recommended)

```bash
pip install cognito-sim-engine
```

### Development Installation

```bash
git clone https://github.com/krish567366/cognito-sim-engine.git
cd cognito-sim-engine
pip install -e ".[dev,docs,visualization]"
```

### Optional Dependencies

```bash
# For visualization capabilities
pip install cognito-sim-engine[visualization]

# For development tools
pip install cognito-sim-engine[dev]

# For documentation building
pip install cognito-sim-engine[docs]
```

## 🤝 Contributing

We welcome contributions from the AGI research community!

### Areas for Contribution

- **New Agent Architectures**: Implement novel cognitive architectures
- **Memory Models**: Develop advanced memory systems
- **Reasoning Engines**: Create specialized reasoning capabilities
- **Environment Types**: Build domain-specific environments
- **Analysis Tools**: Develop cognitive behavior analysis tools
- **Documentation**: Improve documentation and tutorials

### Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Ensure all tests pass: `pytest`
5. Submit a pull request

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/krish567366/cognito-sim-engine.git
cd cognito-sim-engine

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run type checking
mypy cognito_sim_engine/

# Format code
black cognito_sim_engine/
isort cognito_sim_engine/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Krishna Bajpai**

- Email: bajpaikrishna715@gmail.com
- GitHub: [@krish567366](https://github.com/krish567366)

## 🙏 Acknowledgments

- Cognitive science research community for theoretical foundations
- Open source AI/ML community for inspiration and tools
- Beta testers and early adopters for valuable feedback

## 🔗 Links

- **Documentation**: [https://krish567366.github.io/cognito-sim-engine](https://krish567366.github.io/cognito-sim-engine)
- **PyPI Package**: [https://pypi.org/project/cognito-sim-engine/](https://pypi.org/project/cognito-sim-engine/)
- **GitHub Repository**: [https://github.com/krish567366/cognito-sim-engine](https://github.com/krish567366/cognito-sim-engine)
- **Issue Tracker**: [https://github.com/krish567366/cognito-sim-engine/issues](https://github.com/krish567366/cognito-sim-engine/issues)

## ⭐ Support

If you find this project useful for your research, please consider:

- Starring the repository ⭐
- Citing the project in your research papers
- Contributing to the codebase
- Reporting issues and suggesting improvements

---

*Cognito Simulation Engine - Pioneering the future of AGI research through advanced cognitive simulation.*
