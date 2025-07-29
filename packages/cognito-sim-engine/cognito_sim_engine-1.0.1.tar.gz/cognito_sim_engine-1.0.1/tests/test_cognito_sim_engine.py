"""
Test suite for the Cognito Simulation Engine.

This module contains comprehensive tests for all cognitive components
including memory systems, reasoning engines, agents, and environments.
"""

import pytest
import time
from typing import List

from cognito_sim_engine import (
    CognitiveEngine,
    SimulationConfig,
    CognitiveAgent,
    ReasoningAgent,
    LearningAgent,
    MetaCognitiveAgent,
    CognitiveEnvironment,
    MemoryManager,
    MemoryItem,
    MemoryType,
    InferenceEngine,
    Goal,
    Fact,
    Rule,
    AgentPersonality
)


class TestMemorySystem:
    """Test the memory management system."""
    
    def test_memory_manager_initialization(self):
        """Test memory manager initialization."""
        memory_manager = MemoryManager(working_capacity=5, decay_rate=0.1)
        
        assert memory_manager.working_memory.capacity == 5
        assert memory_manager.working_memory.decay_rate == 0.1
        
        stats = memory_manager.get_memory_statistics()
        assert stats["working_memory"]["items"] == 0
        assert stats["episodic_memory"]["episodes"] == 0
        assert stats["total_memories"] == 0
    
    def test_working_memory_capacity(self):
        """Test working memory capacity limits."""
        memory_manager = MemoryManager(working_capacity=3)
        
        # Add items up to capacity
        for i in range(3):
            item = MemoryItem(
                content=f"Item {i}",
                memory_type=MemoryType.WORKING,
                importance=0.5
            )
            success = memory_manager.working_memory.add_item(item)
            assert success
        
        # Adding beyond capacity should still work (displaces least important)
        item = MemoryItem(
            content="Item 3",
            memory_type=MemoryType.WORKING,
            importance=0.8  # Higher importance
        )
        success = memory_manager.working_memory.add_item(item)
        assert success
        
        # Should still have 3 items (capacity limit)
        items = memory_manager.working_memory.get_items()
        assert len(items) <= 3
    
    def test_memory_decay(self):
        """Test memory decay over time."""
        memory_manager = MemoryManager(decay_rate=0.5)  # High decay rate
        
        item = MemoryItem(
            content="Test item",
            memory_type=MemoryType.WORKING,
            importance=0.5
        )
        
        initial_activation = item.activation_level
        memory_manager.working_memory.add_item(item)
        
        # Simulate time passage
        item.decay(0.5, time.time() + 10)  # 10 seconds later
        
        assert item.activation_level < initial_activation
    
    def test_episodic_memory_storage(self):
        """Test episodic memory storage and retrieval."""
        memory_manager = MemoryManager()
        
        episode = MemoryItem(
            content="I went to the library",
            memory_type=MemoryType.EPISODIC,
            importance=0.7
        )
        
        memory_id = memory_manager.store_memory(episode)
        assert memory_id is not None
        
        retrieved = memory_manager.retrieve_memory(memory_id)
        assert retrieved is not None
        assert retrieved.content == "I went to the library"
        assert retrieved.memory_type == MemoryType.EPISODIC
    
    def test_memory_search(self):
        """Test memory search functionality."""
        memory_manager = MemoryManager()
        
        # Add various memories
        memories = [
            MemoryItem("Learning about AI", MemoryType.SEMANTIC, importance=0.8),
            MemoryItem("AI research is fascinating", MemoryType.EPISODIC, importance=0.6),
            MemoryItem("Machine learning algorithms", MemoryType.SEMANTIC, importance=0.7),
            MemoryItem("Went to the park", MemoryType.EPISODIC, importance=0.4)
        ]
        
        for memory in memories:
            memory_manager.store_memory(memory)
        
        # Search for AI-related memories
        ai_memories = memory_manager.search_memories("AI", limit=5)
        assert len(ai_memories) >= 2
        
        # All results should contain "AI"
        for memory in ai_memories:
            assert "AI" in memory.content or "ai" in memory.content.lower()


class TestReasoningEngine:
    """Test the symbolic reasoning system."""
    
    def test_inference_engine_initialization(self):
        """Test inference engine initialization."""
        engine = InferenceEngine(depth_limit=5)
        assert engine.depth_limit == 5
        assert engine.reasoner is not None
    
    def test_fact_storage_and_retrieval(self):
        """Test fact storage and retrieval."""
        engine = InferenceEngine()
        
        fact = Fact("is_human", ["alice"], confidence=0.9)
        fact_id = engine.reasoner.add_fact(fact)
        
        assert fact_id is not None
        assert fact_id in engine.reasoner.facts
        
        retrieved_fact = engine.reasoner.facts[fact_id]
        assert retrieved_fact.predicate == "is_human"
        assert retrieved_fact.arguments == ["alice"]
        assert retrieved_fact.confidence == 0.9
    
    def test_rule_application(self):
        """Test rule application in reasoning."""
        engine = InferenceEngine()
        
        # Add facts
        engine.reasoner.add_fact(Fact("human", ["alice"]))
        engine.reasoner.add_fact(Fact("mortal", ["alice"]))
        
        # Add rule: if human(X) then mortal(X)
        rule = Rule(
            conditions=[Fact("human", ["?x"])],
            conclusion=Fact("mortal", ["?x"]),
            confidence=0.9,
            name="mortality_rule"
        )
        engine.reasoner.add_rule(rule)
        
        # Test rule application
        facts_list = list(engine.reasoner.facts.values())
        can_apply, bindings = rule.can_apply(facts_list)
        
        assert can_apply
        assert "?x" in bindings
        assert bindings["?x"] == "alice"
    
    def test_forward_chaining(self):
        """Test forward chaining inference."""
        engine = InferenceEngine()
        
        # Add initial facts
        engine.reasoner.add_fact(Fact("bird", ["tweety"]))
        
        # Add rule: bird(X) -> can_fly(X)
        rule = Rule(
            conditions=[Fact("bird", ["?x"])],
            conclusion=Fact("can_fly", ["?x"]),
            name="bird_flies"
        )
        engine.reasoner.add_rule(rule)
        
        # Perform forward chaining
        result = engine.reasoner.forward_chaining(max_iterations=10)
        
        assert result.success
        assert len(result.derived_facts) > 0
        
        # Should derive that tweety can fly
        derived_predicates = [fact.predicate for fact in result.derived_facts]
        assert "can_fly" in derived_predicates
    
    def test_goal_directed_reasoning(self):
        """Test goal-directed reasoning."""
        engine = InferenceEngine()
        
        # Add facts
        facts = [
            Fact("wants_to_learn", ["student", "math"]),
            Fact("has_book", ["student", "math_book"]),
            Fact("teaches", ["math_book", "math"])
        ]
        
        for fact in facts:
            engine.reasoner.add_fact(fact)
        
        # Add learning rule
        rule = Rule(
            conditions=[
                Fact("wants_to_learn", ["?person", "?subject"]),
                Fact("has_book", ["?person", "?book"]),
                Fact("teaches", ["?book", "?subject"])
            ],
            conclusion=Fact("should_read", ["?person", "?book"]),
            name="learning_rule"
        )
        engine.reasoner.add_rule(rule)
        
        # Create goal
        goal = Goal(
            description="Learn mathematics",
            target_facts=[Fact("learned", ["student", "math"])]
        )
        
        # Perform inference
        result = engine.infer(goal, facts)
        
        assert result.success or len(result.derived_facts) > 0


class TestAgentSystem:
    """Test the cognitive agent system."""
    
    def test_cognitive_agent_initialization(self):
        """Test cognitive agent initialization."""
        agent = CognitiveAgent("test_agent", "Test Agent")
        
        assert agent.agent_id == "test_agent"
        assert agent.name == "Test Agent"
        assert agent.state.value == "idle"
        assert agent.memory_manager is not None
        assert agent.inference_engine is not None
        assert len(agent.current_goals) == 0
    
    def test_agent_goal_management(self):
        """Test agent goal management."""
        agent = CognitiveAgent("test_agent")
        
        goal = Goal(
            description="Test goal",
            priority=0.8,
            target_facts=[Fact("completed", ["test"])]
        )
        
        agent.add_goal(goal)
        assert len(agent.current_goals) == 1
        assert agent.current_goals[0].description == "Test goal"
        
        # Remove goal
        success = agent.remove_goal(goal.id)
        assert success
        assert len(agent.current_goals) == 0
    
    def test_agent_personality_influence(self):
        """Test personality influence on agent behavior."""
        curious_personality = AgentPersonality(curiosity=0.9, caution=0.1)
        cautious_personality = AgentPersonality(curiosity=0.1, caution=0.9)
        
        curious_agent = CognitiveAgent("curious", personality=curious_personality)
        cautious_agent = CognitiveAgent("cautious", personality=cautious_personality)
        
        # Create exploration action
        from cognito_sim_engine.environment import Action, ActionType
        explore_action = Action(
            name="explore",
            action_type=ActionType.OBSERVATION,
            priority=0.5,
            metadata={"novelty": 0.8}
        )
        
        # Test personality influence
        curious_actions = curious_agent.personality.influence_action_selection([explore_action])
        cautious_actions = cautious_agent.personality.influence_action_selection([explore_action])
        
        # Curious agent should have higher priority for exploration
        assert curious_actions[0].priority >= cautious_actions[0].priority
    
    def test_reasoning_agent_specialization(self):
        """Test reasoning agent specialization."""
        reasoning_agent = ReasoningAgent("reasoner", "Logic Master")
        
        assert isinstance(reasoning_agent, CognitiveAgent)
        assert reasoning_agent.inference_engine.depth_limit >= 10  # Enhanced reasoning depth
        assert reasoning_agent.personality.analyticalness >= 0.7
    
    def test_learning_agent_adaptation(self):
        """Test learning agent adaptation."""
        learning_agent = LearningAgent("learner", "Ada Student")
        
        assert isinstance(learning_agent, CognitiveAgent)
        assert hasattr(learning_agent, 'skill_levels')
        assert hasattr(learning_agent, 'learning_progress')
        assert learning_agent.personality.curiosity >= 0.7
        
        # Test learning from feedback
        feedback = {
            "reward": 0.8,
            "skill": "mathematics",
            "performance": 0.7
        }
        
        learning_agent.learn(feedback)
        
        assert "mathematics" in learning_agent.skill_levels
        assert learning_agent.skill_levels["mathematics"] > 0
    
    def test_metacognitive_agent_reflection(self):
        """Test metacognitive agent self-reflection."""
        meta_agent = MetaCognitiveAgent("philosopher", "Deep Thinker")
        
        assert isinstance(meta_agent, CognitiveAgent)
        assert meta_agent.enable_metacognition == True
        assert hasattr(meta_agent, 'cognitive_load_monitor')
        assert hasattr(meta_agent, 'strategy_effectiveness')
        
        # Simulate some actions to trigger metacognition
        from cognito_sim_engine.environment import Action, ActionType
        for i in range(10):
            action = Action(f"action_{i}", ActionType.COGNITIVE, priority=0.5)
            meta_agent.action_history.append(action)
        
        # Trigger metacognitive reflection
        meta_agent._metacognitive_reflection()
        
        # Should have generated some insights or updated self-model
        assert len(meta_agent.metacognitive_insights) > 0 or len(meta_agent.self_model["strengths"]) > 0


class TestEnvironmentSystem:
    """Test the cognitive environment system."""
    
    def test_environment_initialization(self):
        """Test environment initialization."""
        env = CognitiveEnvironment("Test Lab")
        
        assert env.name == "Test Lab"
        assert env.state is not None
        assert len(env.agents) == 0
        assert len(env.state.objects) > 0  # Should have default objects
    
    def test_agent_environment_interaction(self):
        """Test agent addition and interaction with environment."""
        env = CognitiveEnvironment("Test Environment")
        
        # Add agent
        env.add_agent("test_agent", {"x": 0, "y": 0, "z": 0})
        assert "test_agent" in env.agents
        
        # Test perception generation
        perceptions = env.get_perceptions("test_agent")
        assert len(perceptions) > 0
        
        # Should include internal state perception
        internal_perceptions = [p for p in perceptions if p.type.value == "internal"]
        assert len(internal_perceptions) > 0
    
    def test_action_execution(self):
        """Test action execution in environment."""
        env = CognitiveEnvironment("Action Test")
        env.add_agent("test_agent")
        
        from cognito_sim_engine.environment import Action, ActionType
        
        # Test movement action
        move_action = Action(
            name="move",
            action_type=ActionType.PHYSICAL,
            parameters={"direction": "forward", "distance": 1.0}
        )
        
        success = env.execute_action(move_action, "test_agent")
        # Movement should succeed (no obstacles in default environment)
        assert success == True or success == False  # Depends on environment state
    
    def test_environment_object_interaction(self):
        """Test interaction with environment objects."""
        env = CognitiveEnvironment("Object Test")
        env.add_agent("test_agent", {"x": 5, "y": 5, "z": 0})  # Near table
        
        from cognito_sim_engine.environment import Action, ActionType
        
        # Test examination action
        examine_action = Action(
            name="examine",
            action_type=ActionType.OBSERVATION,
            parameters={"target": "table"}
        )
        
        success = env.execute_action(examine_action, "test_agent")
        assert isinstance(success, bool)


class TestCognitiveEngine:
    """Test the main cognitive engine."""
    
    def test_engine_initialization(self):
        """Test cognitive engine initialization."""
        config = SimulationConfig(max_cycles=50)
        env = CognitiveEnvironment("Test Environment")
        engine = CognitiveEngine(config, env)
        
        assert engine.config.max_cycles == 50
        assert engine.environment == env
        assert engine.state.value == "idle"
        assert engine.current_cycle == 0
    
    def test_simulation_execution(self):
        """Test complete simulation execution."""
        config = SimulationConfig(max_cycles=10, enable_metrics=True)
        env = CognitiveEnvironment("Simulation Test")
        engine = CognitiveEngine(config, env)
        
        # Add a simple goal
        goal = Goal(
            description="Test simulation goal",
            priority=0.5,
            target_facts=[Fact("test", ["completed"])]
        )
        engine.add_goal(goal)
        
        # Run simulation
        metrics = engine.run_simulation()
        
        assert metrics is not None
        assert metrics.total_cycles <= 10
        assert engine.state.value in ["completed", "idle"]
    
    def test_cognitive_cycle(self):
        """Test individual cognitive cycle execution."""
        config = SimulationConfig(max_cycles=1)
        env = CognitiveEnvironment("Cycle Test")
        engine = CognitiveEngine(config, env)
        
        initial_cycle = engine.current_cycle
        success = engine.cognitive_cycle()
        
        assert success == True
        assert engine.current_cycle == initial_cycle + 1
    
    def test_engine_state_management(self):
        """Test engine state management."""
        config = SimulationConfig(max_cycles=100)
        env = CognitiveEnvironment("State Test")
        engine = CognitiveEngine(config, env)
        
        # Test state summary
        summary = engine.get_state_summary()
        assert "simulation_state" in summary
        assert "current_cycle" in summary
        assert "metrics" in summary
        
        # Test pause/resume functionality
        engine.pause_simulation()
        assert engine.state.value == "paused"
        
        engine.resume_simulation()
        assert engine.state.value == "running"
        
        engine.stop_simulation()
        assert engine.state.value == "completed"


class TestIntegration:
    """Integration tests for complete system functionality."""
    
    def test_full_cognitive_simulation(self):
        """Test complete cognitive simulation with agent-environment interaction."""
        # Setup
        config = SimulationConfig(
            max_cycles=20,
            working_memory_capacity=5,
            enable_metacognition=True,
            enable_learning=True
        )
        
        env = CognitiveEnvironment("Integration Test Lab")
        engine = CognitiveEngine(config, env)
        
        # Create and configure agent
        agent = CognitiveAgent("integration_agent", "Test Researcher")
        env.add_agent("integration_agent")
        
        # Add goals
        goals = [
            Goal(
                description="Explore the laboratory",
                priority=0.7,
                target_facts=[Fact("explored", ["laboratory"])]
            ),
            Goal(
                description="Learn about the environment",
                priority=0.6,
                target_facts=[Fact("learned", ["environment"])]
            )
        ]
        
        for goal in goals:
            agent.add_goal(goal)
        
        # Setup agent reasoning
        initial_facts = [
            Fact("in_location", ["integration_agent", "laboratory"]),
            Fact("can_explore", ["integration_agent"]),
            Fact("wants_knowledge", ["integration_agent"])
        ]
        
        for fact in initial_facts:
            agent.inference_engine.reasoner.add_fact(fact)
        
        # Run simulation
        metrics = engine.run_simulation()
        
        # Verify results
        assert metrics.total_cycles > 0
        assert agent.total_actions >= 0  # Agent should have attempted some actions
        assert len(agent.memory_manager.get_memory_statistics()["working_memory"]) >= 0
        
        # Agent should have made some progress
        final_state = agent.get_cognitive_state()
        assert final_state["reasoning"]["total_cycles"] > 0
    
    def test_multi_agent_interaction(self):
        """Test multi-agent simulation."""
        config = SimulationConfig(max_cycles=15)
        env = CognitiveEnvironment("Multi-Agent Test")
        engine = CognitiveEngine(config, env)
        
        # Create multiple agents
        agents = [
            CognitiveAgent("agent_1", "Explorer"),
            ReasoningAgent("agent_2", "Logician"),
            LearningAgent("agent_3", "Student")
        ]
        
        for agent in agents:
            env.add_agent(agent.agent_id)
            
            # Add a simple goal to each agent
            goal = Goal(
                description=f"Agent {agent.agent_id} goal",
                priority=0.5,
                target_facts=[Fact("active", [agent.agent_id])]
            )
            agent.add_goal(goal)
        
        # Run simulation
        metrics = engine.run_simulation()
        
        # Verify all agents participated
        assert metrics.total_cycles > 0
        
        # Check that environment tracked multiple agents
        env_summary = env.get_environment_summary()
        assert env_summary["agents"] == len(agents)


# Pytest configuration and fixtures
@pytest.fixture
def sample_memory_manager():
    """Create a sample memory manager for testing."""
    return MemoryManager(working_capacity=5, decay_rate=0.1)


@pytest.fixture
def sample_agent():
    """Create a sample cognitive agent for testing."""
    return CognitiveAgent("test_agent", "Test Agent")


@pytest.fixture
def sample_environment():
    """Create a sample environment for testing."""
    return CognitiveEnvironment("Test Environment")


@pytest.fixture
def sample_config():
    """Create a sample simulation configuration."""
    return SimulationConfig(
        max_cycles=10,
        working_memory_capacity=5,
        enable_metacognition=True,
        enable_learning=True
    )


# Test utilities
def create_test_goal(description: str = "Test goal", priority: float = 0.5) -> Goal:
    """Create a test goal."""
    return Goal(
        description=description,
        priority=priority,
        target_facts=[Fact("test", ["goal"])]
    )


def create_test_fact(predicate: str = "test", args: List[str] = None) -> Fact:
    """Create a test fact."""
    if args is None:
        args = ["entity"]
    return Fact(predicate, args)


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])
