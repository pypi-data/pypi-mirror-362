"""
Agent System - Cognitive agents with various architectural patterns.

This module provides different types of cognitive agents that can interact
with environments, reason about goals, and learn from experience.
"""

import time
import uuid
from typing import Dict, List, Optional, Any, Set, Callable, Type
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import random
import json

from .memory import MemoryManager, MemoryItem, MemoryType
from .reasoning import InferenceEngine, Goal, Fact, ReasoningResult
from .environment import CognitiveEnvironment, Action, Perception, ActionType
from .licensing import LicensedClass, requires_license


class AgentState(Enum):
    """States of cognitive agents."""
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    LEARNING = "learning"
    REFLECTING = "reflecting"
    ERROR = "error"


class LearningStrategy(Enum):
    """Learning strategies for agents."""
    REINFORCEMENT = "reinforcement"
    IMITATION = "imitation"
    DISCOVERY = "discovery"
    INSTRUCTION = "instruction"
    METACOGNITIVE = "metacognitive"


@dataclass
class AgentPersonality:
    """Personality traits that influence agent behavior."""
    curiosity: float = 0.5  # Tendency to explore
    caution: float = 0.5    # Risk aversion
    persistence: float = 0.5  # Goal persistence
    sociability: float = 0.5  # Social interaction preference
    creativity: float = 0.5   # Novel solution generation
    analyticalness: float = 0.5  # Preference for logical reasoning
    
    def influence_action_selection(self, actions: List[Action]) -> List[Action]:
        """Influence action selection based on personality."""
        influenced_actions = []
        
        for action in actions:
            # Modify action priority based on personality
            new_priority = action.priority
            
            # Curious agents prefer exploration
            if action.name in ["explore", "examine"] and self.curiosity > 0.7:
                new_priority *= 1.3
            
            # Cautious agents avoid risky actions
            if action.metadata.get("risk_level", 0) > 0.5 and self.caution > 0.7:
                new_priority *= 0.7
            
            # Creative agents prefer novel actions
            if action.metadata.get("novelty", 0) > 0.5 and self.creativity > 0.7:
                new_priority *= 1.2
            
            # Copy action with modified priority
            influenced_action = Action(
                name=action.name,
                action_type=action.action_type,
                parameters=action.parameters.copy(),
                priority=min(1.0, new_priority),
                duration=action.duration,
                energy_cost=action.energy_cost,
                description=action.description,
                preconditions=action.preconditions.copy(),
                effects=action.effects.copy(),
                metadata=action.metadata.copy()
            )
            influenced_actions.append(influenced_action)
        
        return influenced_actions


class BaseAgent(ABC):
    """
    Abstract base class for all cognitive agents.
    
    Defines the core interface and common functionality for cognitive agents.
    """
    
    def __init__(
        self,
        agent_id: str,
        name: str = "",
        personality: Optional[AgentPersonality] = None
    ):
        """
        Initialize base agent.
        
        Args:
            agent_id: Unique identifier for the agent
            name: Human-readable name
            personality: Personality traits
        """
        self.agent_id = agent_id
        self.name = name or f"Agent-{agent_id[:8]}"
        self.personality = personality or AgentPersonality()
        
        # Core state
        self.state = AgentState.IDLE
        self.created_at = time.time()
        self.last_update = time.time()
        
        # Agent capabilities
        self.capabilities: Set[str] = {"perceive", "reason", "act", "learn"}
        
        # Metrics
        self.total_actions = 0
        self.total_perceptions = 0
        self.total_reasoning_cycles = 0
        self.success_rate = 0.0
        
        # Callbacks
        self.action_callbacks: List[Callable] = []
        self.perception_callbacks: List[Callable] = []
        self.learning_callbacks: List[Callable] = []
    
    @abstractmethod
    def perceive(self, perceptions: List[Perception]) -> None:
        """Process incoming perceptions."""
        pass
    
    @abstractmethod
    def reason(self) -> List[Action]:
        """Perform reasoning to determine next actions."""
        pass
    
    @abstractmethod
    def act(self, environment: CognitiveEnvironment) -> Optional[Action]:
        """Select and execute an action in the environment."""
        pass
    
    @abstractmethod
    def learn(self, feedback: Dict[str, Any]) -> None:
        """Learn from experience and feedback."""
        pass
    
    def update(self, delta_time: float = 1.0) -> None:
        """Update agent state."""
        self.last_update = time.time()
    
    def add_capability(self, capability: str) -> None:
        """Add a new capability to the agent."""
        self.capabilities.add(capability)
    
    def has_capability(self, capability: str) -> bool:
        """Check if agent has a specific capability."""
        return capability in self.capabilities
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "state": self.state.value,
            "uptime": time.time() - self.created_at,
            "capabilities": list(self.capabilities),
            "metrics": {
                "total_actions": self.total_actions,
                "total_perceptions": self.total_perceptions,
                "total_reasoning_cycles": self.total_reasoning_cycles,
                "success_rate": self.success_rate
            }
        }


class CognitiveAgent(BaseAgent, LicensedClass):
    """
    Full cognitive agent with memory, reasoning, and learning capabilities.
    
    This is the main cognitive agent class that integrates all cognitive systems.
    Requires Core license for basic functionality.
    """
    
    def __init__(
        self,
        agent_id: str,
        name: str = "",
        personality: Optional[AgentPersonality] = None,
        working_memory_capacity: int = 7,
        enable_metacognition: bool = True,
        license_tier: str = "core"
    ):
        """
        Initialize cognitive agent with license validation.
        
        Args:
            agent_id: Unique identifier
            name: Agent name
            personality: Personality traits
            working_memory_capacity: Working memory capacity
            enable_metacognition: Enable metacognitive capabilities
            license_tier: Required license tier (core, pro, enterprise, research)
        """
        # Initialize licensing first
        LicensedClass.__init__(self, license_tier=license_tier)
        BaseAgent.__init__(self, agent_id, name, personality)
        
        # Cognitive systems
        self.memory_manager = MemoryManager(
            working_capacity=working_memory_capacity,
            decay_rate=0.02
        )
        self.inference_engine = InferenceEngine(depth_limit=8)
        
        # Agent state
        self.current_goals: List[Goal] = []
        self.current_perceptions: List[Perception] = []
        self.action_history: List[Action] = []
        self.pending_actions: List[Action] = []
        
        # Learning system
        self.learning_strategy = LearningStrategy.REINFORCEMENT
        self.learning_rate = 0.1
        self.experience_buffer: List[Dict[str, Any]] = []
        
        # Metacognition
        self.enable_metacognition = enable_metacognition
        self.metacognitive_insights: List[str] = []
        self.self_model: Dict[str, Any] = {
            "strengths": [],
            "weaknesses": [],
            "preferences": [],
            "knowledge_gaps": []
        }
        
        # Add cognitive capabilities
        self.capabilities.update({
            "memory_management", "symbolic_reasoning", "goal_planning",
            "metacognition" if enable_metacognition else None
        })
        self.capabilities.discard(None)
        
        # Initialize basic knowledge
        self._initialize_knowledge()
    
    def _initialize_knowledge(self) -> None:
        """Initialize basic knowledge and capabilities."""
        # Add basic facts about self
        self_facts = [
            Fact("is_agent", [self.agent_id]),
            Fact("can_perceive", [self.agent_id]),
            Fact("can_reason", [self.agent_id]),
            Fact("can_act", [self.agent_id]),
            Fact("can_learn", [self.agent_id])
        ]
        
        for fact in self_facts:
            self.inference_engine.reasoner.add_fact(fact)
        
        # Add domain knowledge based on capabilities
        if self.has_capability("memory_management"):
            self.inference_engine.add_domain_knowledge("problem_solving")
        
        if self.has_capability("symbolic_reasoning"):
            self.inference_engine.add_domain_knowledge("learning")
    
    def perceive(self, perceptions: List[Perception]) -> None:
        """Process incoming perceptions."""
        self.state = AgentState.THINKING
        self.current_perceptions = perceptions
        self.total_perceptions += len(perceptions)
        
        # Store important perceptions in memory
        for perception in perceptions:
            if perception.salience > 0.4:  # Only store salient perceptions
                memory_item = MemoryItem(
                    content=f"Perceived: {perception.type.value} - {perception.data}",
                    memory_type=MemoryType.WORKING,
                    importance=perception.salience,
                    metadata={
                        "perception_id": perception.id,
                        "perception_type": perception.type.value,
                        "source": perception.source
                    }
                )
                self.memory_manager.store_memory(memory_item)
        
        # Extract facts from perceptions
        self._extract_facts_from_perceptions(perceptions)
        
        # Call perception callbacks
        for callback in self.perception_callbacks:
            callback(self, perceptions)
    
    def _extract_facts_from_perceptions(self, perceptions: List[Perception]) -> None:
        """Extract logical facts from perceptions."""
        for perception in perceptions:
            facts = []
            
            if perception.type.value == "visual":
                data = perception.data
                if isinstance(data, dict) and "object_name" in data:
                    facts.append(Fact("visible", [data["object_name"]]))
                    facts.append(Fact("object_type", [data["object_name"], data.get("object_type", "unknown")]))
            
            elif perception.type.value == "internal":
                data = perception.data
                if isinstance(data, dict):
                    if "energy" in data:
                        energy_level = "high" if data["energy"] > 70 else "medium" if data["energy"] > 30 else "low"
                        facts.append(Fact("energy_level", [self.agent_id, energy_level]))
            
            # Add facts to knowledge base
            for fact in facts:
                self.inference_engine.reasoner.add_fact(fact)
    
    def reason(self) -> List[Action]:
        """Perform reasoning to determine next actions."""
        self.state = AgentState.THINKING
        self.total_reasoning_cycles += 1
        
        possible_actions = []
        
        # Reason about each active goal
        for goal in self.current_goals:
            if goal.is_active():
                reasoning_result = self.inference_engine.infer(
                    goal,
                    list(self.inference_engine.reasoner.facts.values())
                )
                
                if reasoning_result.success:
                    possible_actions.extend(reasoning_result.recommended_actions)
        
        # If no goal-directed actions, generate exploratory actions
        if not possible_actions:
            possible_actions.extend(self._generate_exploratory_actions())
        
        # Apply personality influence
        possible_actions = self.personality.influence_action_selection(possible_actions)
        
        # Store reasoning results in memory
        if possible_actions:
            reasoning_memory = MemoryItem(
                content=f"Reasoning produced {len(possible_actions)} possible actions",
                memory_type=MemoryType.EPISODIC,
                importance=0.6,
                metadata={"reasoning_cycle": self.total_reasoning_cycles}
            )
            self.memory_manager.store_memory(reasoning_memory)
        
        return possible_actions
    
    def _generate_exploratory_actions(self) -> List[Action]:
        """Generate exploratory actions when no goals are active."""
        exploratory_actions = []
        
        # Basic exploration
        explore_action = Action(
            name="explore",
            action_type=ActionType.OBSERVATION,
            parameters={"radius": 5.0},
            priority=0.3 + self.personality.curiosity * 0.3,
            description="Explore the surrounding area"
        )
        exploratory_actions.append(explore_action)
        
        # Random movement (low priority)
        if random.random() < 0.3:
            directions = ["forward", "backward", "left", "right"]
            move_action = Action(
                name="move",
                action_type=ActionType.PHYSICAL,
                parameters={"direction": random.choice(directions), "distance": 1.0},
                priority=0.2,
                description="Move in a random direction"
            )
            exploratory_actions.append(move_action)
        
        return exploratory_actions
    
    def act(self, environment: CognitiveEnvironment) -> Optional[Action]:
        """Select and execute an action in the environment."""
        self.state = AgentState.ACTING
        
        # Get possible actions from reasoning
        possible_actions = self.reason()
        
        if not possible_actions:
            return None
        
        # Select best action (highest priority)
        selected_action = max(possible_actions, key=lambda a: a.priority)
        
        # Execute action in environment
        success = environment.execute_action(selected_action, self.agent_id)
        
        # Record action
        self.action_history.append(selected_action)
        self.total_actions += 1
        
        # Update success rate
        recent_actions = self.action_history[-10:]  # Last 10 actions
        recent_successes = sum(1 for _ in recent_actions)  # Simplified success counting
        self.success_rate = recent_successes / len(recent_actions) if recent_actions else 0.0
        
        # Store action result in memory
        action_memory = MemoryItem(
            content=f"Executed action '{selected_action.name}' with success: {success}",
            memory_type=MemoryType.EPISODIC,
            importance=0.7 if success else 0.9,  # Failures are more important to remember
            metadata={
                "action_name": selected_action.name,
                "success": success,
                "action_id": selected_action.id
            }
        )
        self.memory_manager.store_memory(action_memory)
        
        # Call action callbacks
        for callback in self.action_callbacks:
            callback(self, selected_action, success)
        
        return selected_action if success else None
    
    def learn(self, feedback: Dict[str, Any]) -> None:
        """Learn from experience and feedback."""
        self.state = AgentState.LEARNING
        
        # Store experience
        experience = {
            "timestamp": time.time(),
            "feedback": feedback.copy(),
            "context": {
                "recent_perceptions": len(self.current_perceptions),
                "active_goals": len([g for g in self.current_goals if g.is_active()]),
                "recent_actions": len(self.action_history[-5:])
            }
        }
        self.experience_buffer.append(experience)
        
        # Apply learning strategy
        if self.learning_strategy == LearningStrategy.REINFORCEMENT:
            self._reinforcement_learning(feedback)
        elif self.learning_strategy == LearningStrategy.DISCOVERY:
            self._discovery_learning(feedback)
        
        # Metacognitive learning
        if self.enable_metacognition:
            self._metacognitive_learning(feedback)
        
        # Call learning callbacks
        for callback in self.learning_callbacks:
            callback(self, feedback)
    
    def _reinforcement_learning(self, feedback: Dict[str, Any]) -> None:
        """Simple reinforcement learning from feedback."""
        reward = feedback.get("reward", 0.0)
        
        if reward > 0 and self.action_history:
            # Reinforce recent successful actions
            recent_action = self.action_history[-1]
            
            # Create positive memory association
            success_memory = MemoryItem(
                content=f"Action '{recent_action.name}' led to positive outcome",
                memory_type=MemoryType.LONG_TERM,
                importance=0.8 + reward * 0.2,
                metadata={"reward": reward, "action_type": recent_action.action_type.value}
            )
            self.memory_manager.store_memory(success_memory)
    
    def _discovery_learning(self, feedback: Dict[str, Any]) -> None:
        """Learning through discovery and pattern recognition."""
        # Look for patterns in recent experiences
        if len(self.experience_buffer) > 5:
            recent_experiences = self.experience_buffer[-5:]
            
            # Simple pattern detection: repeated successful action types
            action_types = []
            rewards = []
            
            for exp in recent_experiences:
                if "last_action_type" in exp["context"]:
                    action_types.append(exp["context"]["last_action_type"])
                    rewards.append(exp["feedback"].get("reward", 0))
            
            # If certain action types consistently lead to rewards, remember this
            if len(set(action_types)) < len(action_types):  # Some repetition
                pattern_memory = MemoryItem(
                    content=f"Pattern discovered: certain action types tend to be successful",
                    memory_type=MemoryType.SEMANTIC,
                    importance=0.7,
                    metadata={"pattern_type": "action_success", "action_types": action_types}
                )
                self.memory_manager.store_memory(pattern_memory)
    
    def _metacognitive_learning(self, feedback: Dict[str, Any]) -> None:
        """Metacognitive learning about own cognitive processes."""
        # Analyze own performance
        if self.total_actions > 0:
            current_success_rate = self.success_rate
            
            if current_success_rate < 0.3:
                insight = "Performance is low - may need to adjust strategy"
                self.metacognitive_insights.append(insight)
                self.self_model["weaknesses"].append("low_success_rate")
            elif current_success_rate > 0.8:
                insight = "Performance is high - current strategy is effective"
                self.metacognitive_insights.append(insight)
                self.self_model["strengths"].append("high_success_rate")
            
            # Store metacognitive insight
            meta_memory = MemoryItem(
                content=insight,
                memory_type=MemoryType.SEMANTIC,
                importance=0.8,
                metadata={"type": "metacognitive_insight", "success_rate": current_success_rate}
            )
            self.memory_manager.store_memory(meta_memory)
    
    def add_goal(self, goal: Goal) -> None:
        """Add a new goal to the agent."""
        self.current_goals.append(goal)
        
        # Store goal in memory
        goal_memory = MemoryItem(
            content=f"New goal added: {goal.description}",
            memory_type=MemoryType.EPISODIC,
            importance=goal.priority,
            metadata={"goal_id": goal.id, "goal_priority": goal.priority}
        )
        self.memory_manager.store_memory(goal_memory)
    
    def remove_goal(self, goal_id: str) -> bool:
        """Remove a goal by ID."""
        for i, goal in enumerate(self.current_goals):
            if goal.id == goal_id:
                removed_goal = self.current_goals.pop(i)
                
                # Store goal removal in memory
                removal_memory = MemoryItem(
                    content=f"Goal removed: {removed_goal.description}",
                    memory_type=MemoryType.EPISODIC,
                    importance=0.6,
                    metadata={"goal_id": goal_id, "reason": "manual_removal"}
                )
                self.memory_manager.store_memory(removal_memory)
                
                return True
        return False
    
    def update(self, delta_time: float = 1.0) -> None:
        """Update agent cognitive systems."""
        super().update(delta_time)
        
        # Update memory systems
        self.memory_manager.update_working_memory()
        
        # Update goal states
        self._update_goals()
        
        # Periodic metacognitive reflection
        if self.enable_metacognition and self.total_reasoning_cycles % 20 == 0:
            self._metacognitive_reflection()
        
        # Clean up old experiences
        if len(self.experience_buffer) > 100:
            self.experience_buffer = self.experience_buffer[-50:]  # Keep recent 50
    
    def _update_goals(self) -> None:
        """Update goal states and remove completed/expired goals."""
        current_time = time.time()
        updated_goals = []
        
        for goal in self.current_goals:
            if goal.is_achieved():
                # Store goal achievement
                achievement_memory = MemoryItem(
                    content=f"Goal achieved: {goal.description}",
                    memory_type=MemoryType.EPISODIC,
                    importance=0.9,
                    metadata={"goal_id": goal.id, "achievement_time": current_time}
                )
                self.memory_manager.store_memory(achievement_memory)
            elif goal.is_expired(current_time):
                # Store goal expiration
                expiration_memory = MemoryItem(
                    content=f"Goal expired: {goal.description}",
                    memory_type=MemoryType.EPISODIC,
                    importance=0.7,
                    metadata={"goal_id": goal.id, "expiration_time": current_time}
                )
                self.memory_manager.store_memory(expiration_memory)
            else:
                updated_goals.append(goal)
        
        self.current_goals = updated_goals
    
    def _metacognitive_reflection(self) -> None:
        """Perform metacognitive reflection on performance."""
        if not self.enable_metacognition:
            return
        
        # Analyze recent performance
        recent_actions = self.action_history[-10:] if len(self.action_history) >= 10 else self.action_history
        
        if recent_actions:
            # Analyze action diversity
            action_types = [action.action_type for action in recent_actions]
            diversity = len(set(action_types)) / len(action_types)
            
            if diversity < 0.3:
                insight = "Action selection lacks diversity - may be stuck in behavioral pattern"
                self.metacognitive_insights.append(insight)
                self.self_model["weaknesses"].append("low_behavioral_diversity")
            
            # Analyze goal progress
            active_goals = [g for g in self.current_goals if g.is_active()]
            if active_goals:
                avg_progress = sum(g.progress for g in active_goals) / len(active_goals)
                if avg_progress < 0.1 and len(recent_actions) > 5:
                    insight = "Goals are not making progress - may need new strategy"
                    self.metacognitive_insights.append(insight)
                    self.self_model["knowledge_gaps"].append("goal_achievement_strategies")
    
    def get_cognitive_state(self) -> Dict[str, Any]:
        """Get comprehensive cognitive state information."""
        memory_stats = self.memory_manager.get_memory_statistics()
        
        return {
            "agent_info": self.get_status(),
            "memory_state": memory_stats,
            "goals": {
                "total": len(self.current_goals),
                "active": len([g for g in self.current_goals if g.is_active()]),
                "achieved": len([g for g in self.current_goals if g.is_achieved()])
            },
            "reasoning": {
                "total_cycles": self.total_reasoning_cycles,
                "knowledge_facts": len(self.inference_engine.reasoner.facts),
                "rules": len(self.inference_engine.reasoner.rules)
            },
            "learning": {
                "strategy": self.learning_strategy.value,
                "experiences": len(self.experience_buffer),
                "learning_rate": self.learning_rate
            },
            "metacognition": {
                "enabled": self.enable_metacognition,
                "insights": len(self.metacognitive_insights),
                "self_model": self.self_model
            } if self.enable_metacognition else None
        }
    
    def export_agent_data(self) -> Dict[str, Any]:
        """Export complete agent data for persistence."""
        return {
            "agent_info": {
                "agent_id": self.agent_id,
                "name": self.name,
                "personality": self.personality.__dict__,
                "created_at": self.created_at,
                "capabilities": list(self.capabilities)
            },
            "cognitive_state": self.get_cognitive_state(),
            "memory_export": self.memory_manager.export_memories(),
            "goals": [goal.to_dict() for goal in self.current_goals],
            "action_history": [action.to_dict() for action in self.action_history[-20:]],  # Recent 20
            "experience_buffer": self.experience_buffer[-10:],  # Recent 10
            "metacognition": {
                "insights": self.metacognitive_insights[-10:],  # Recent 10
                "self_model": self.self_model
            } if self.enable_metacognition else None
        }


class ReasoningAgent(CognitiveAgent):
    """Specialized agent focused on symbolic reasoning and logical problem solving."""
    
    def __init__(self, agent_id: str, name: str = "", **kwargs):
        """Initialize reasoning agent."""
        super().__init__(agent_id, name, **kwargs)
        
        # Enhanced reasoning capabilities
        self.inference_engine = InferenceEngine(depth_limit=15)
        self.reasoning_strategies = ["forward_chaining", "backward_chaining", "abductive"]
        self.current_strategy = "forward_chaining"
        
        # Add specialized reasoning knowledge
        self.inference_engine.add_domain_knowledge("problem_solving")
        
        # Override personality for reasoning focus
        self.personality.analyticalness = 0.8
        self.personality.persistence = 0.7
    
    def reason(self) -> List[Action]:
        """Enhanced reasoning with multiple strategies."""
        possible_actions = super().reason()
        
        # Try different reasoning strategies if initial reasoning fails
        if not possible_actions and self.current_goals:
            for strategy in self.reasoning_strategies:
                if strategy != self.current_strategy:
                    # Try alternative reasoning approach
                    enhanced_actions = self._reason_with_strategy(strategy)
                    if enhanced_actions:
                        possible_actions.extend(enhanced_actions)
                        break
        
        return possible_actions
    
    def _reason_with_strategy(self, strategy: str) -> List[Action]:
        """Reason using a specific strategy."""
        # This is a simplified implementation
        # In a full system, each strategy would have different logic
        
        if strategy == "abductive" and self.current_goals:
            # Abductive reasoning: find best explanation for observations
            goal = self.current_goals[0]
            
            # Generate hypothesis actions
            hypothesis_action = Action(
                name="test_hypothesis",
                action_type=ActionType.COGNITIVE,
                priority=0.6,
                description=f"Test hypothesis related to goal: {goal.description}",
                metadata={"reasoning_strategy": "abductive"}
            )
            return [hypothesis_action]
        
        return []


class LearningAgent(CognitiveAgent):
    """Specialized agent focused on learning and adaptation."""
    
    def __init__(self, agent_id: str, name: str = "", **kwargs):
        """Initialize learning agent."""
        super().__init__(agent_id, name, **kwargs)
        
        # Enhanced learning capabilities
        self.learning_strategies = [LearningStrategy.REINFORCEMENT, LearningStrategy.DISCOVERY, LearningStrategy.IMITATION]
        self.current_learning_strategy = LearningStrategy.REINFORCEMENT
        self.learning_rate = 0.15
        
        # Learning-specific state
        self.skill_levels: Dict[str, float] = {}
        self.learning_progress: Dict[str, List[float]] = {}
        
        # Override personality for learning focus
        self.personality.curiosity = 0.8
        self.personality.creativity = 0.6
    
    def learn(self, feedback: Dict[str, Any]) -> None:
        """Enhanced learning with multiple strategies."""
        super().learn(feedback)
        
        # Update skill levels based on performance
        if "skill" in feedback:
            skill_name = feedback["skill"]
            performance = feedback.get("performance", 0.0)
            
            if skill_name not in self.skill_levels:
                self.skill_levels[skill_name] = 0.0
                self.learning_progress[skill_name] = []
            
            # Update skill level with learning rate
            old_level = self.skill_levels[skill_name]
            self.skill_levels[skill_name] += self.learning_rate * (performance - old_level)
            self.learning_progress[skill_name].append(self.skill_levels[skill_name])
        
        # Adapt learning strategy based on progress
        self._adapt_learning_strategy()
    
    def _adapt_learning_strategy(self) -> None:
        """Adapt learning strategy based on recent progress."""
        if len(self.experience_buffer) > 10:
            recent_rewards = [exp["feedback"].get("reward", 0) for exp in self.experience_buffer[-10:]]
            avg_reward = sum(recent_rewards) / len(recent_rewards)
            
            if avg_reward < 0.3:
                # Poor performance, try different strategy
                current_idx = self.learning_strategies.index(self.current_learning_strategy)
                new_idx = (current_idx + 1) % len(self.learning_strategies)
                self.current_learning_strategy = self.learning_strategies[new_idx]
                
                # Store strategy change in memory
                strategy_memory = MemoryItem(
                    content=f"Changed learning strategy to {self.current_learning_strategy.value}",
                    memory_type=MemoryType.EPISODIC,
                    importance=0.7,
                    metadata={"strategy_change": True, "avg_reward": avg_reward}
                )
                self.memory_manager.store_memory(strategy_memory)


class MetaCognitiveAgent(CognitiveAgent):
    """Advanced agent with sophisticated metacognitive capabilities."""
    
    def __init__(self, agent_id: str, name: str = "", **kwargs):
        """Initialize metacognitive agent."""
        kwargs["enable_metacognition"] = True
        super().__init__(agent_id, name, **kwargs)
        
        # Enhanced metacognitive capabilities
        self.metacognitive_strategies = ["performance_monitoring", "strategy_selection", "self_reflection"]
        self.cognitive_load_monitor = 0.0
        self.strategy_effectiveness: Dict[str, float] = {}
        
        # Override personality for metacognitive focus
        self.personality.analyticalness = 0.9
        self.personality.persistence = 0.8
    
    def _metacognitive_reflection(self) -> None:
        """Enhanced metacognitive reflection."""
        super()._metacognitive_reflection()
        
        # Monitor cognitive load
        self._monitor_cognitive_load()
        
        # Evaluate strategy effectiveness
        self._evaluate_strategies()
        
        # Self-model updating
        self._update_self_model()
    
    def _monitor_cognitive_load(self) -> None:
        """Monitor and manage cognitive load."""
        # Simple cognitive load estimation
        working_memory_load = len(self.memory_manager.get_working_memory()) / self.memory_manager.working_memory.capacity
        goal_load = len(self.current_goals) / 10.0  # Normalize to reasonable goal count
        reasoning_load = min(1.0, self.total_reasoning_cycles / 1000.0)
        
        self.cognitive_load_monitor = (working_memory_load + goal_load + reasoning_load) / 3.0
        
        # Take action if cognitive load is too high
        if self.cognitive_load_monitor > 0.8:
            insight = "Cognitive load is high - need to prioritize or simplify tasks"
            self.metacognitive_insights.append(insight)
            
            # Simplify goals if needed
            if len(self.current_goals) > 5:
                # Remove lowest priority goals
                self.current_goals.sort(key=lambda g: g.priority)
                removed_goals = self.current_goals[:2]
                self.current_goals = self.current_goals[2:]
                
                for goal in removed_goals:
                    load_memory = MemoryItem(
                        content=f"Removed goal due to high cognitive load: {goal.description}",
                        memory_type=MemoryType.EPISODIC,
                        importance=0.6,
                        metadata={"cognitive_load": self.cognitive_load_monitor}
                    )
                    self.memory_manager.store_memory(load_memory)
    
    def _evaluate_strategies(self) -> None:
        """Evaluate effectiveness of different strategies."""
        if len(self.action_history) > 10:
            # Group actions by type and evaluate success rates
            action_groups = {}
            for action in self.action_history[-20:]:
                action_type = action.action_type.value
                if action_type not in action_groups:
                    action_groups[action_type] = []
                action_groups[action_type].append(action)
            
            # Calculate effectiveness for each strategy/action type
            for action_type, actions in action_groups.items():
                if len(actions) > 3:  # Need sufficient data
                    # Simplified effectiveness calculation
                    effectiveness = min(1.0, len(actions) / 20.0 * self.success_rate)
                    self.strategy_effectiveness[action_type] = effectiveness
    
    def _update_self_model(self) -> None:
        """Update self-model based on recent performance and insights."""
        # Update strengths and weaknesses based on strategy effectiveness
        for strategy, effectiveness in self.strategy_effectiveness.items():
            if effectiveness > 0.7:
                if strategy not in self.self_model["strengths"]:
                    self.self_model["strengths"].append(strategy)
            elif effectiveness < 0.3:
                if strategy not in self.self_model["weaknesses"]:
                    self.self_model["weaknesses"].append(strategy)
        
        # Identify knowledge gaps from failed reasoning
        if self.total_reasoning_cycles > 50:
            recent_insights = self.metacognitive_insights[-5:]
            gap_indicators = ["unknown", "failed", "no solution", "stuck"]
            
            for insight in recent_insights:
                for indicator in gap_indicators:
                    if indicator in insight.lower():
                        gap = f"knowledge_gap_from_{indicator}"
                        if gap not in self.self_model["knowledge_gaps"]:
                            self.self_model["knowledge_gaps"].append(gap)
                        break

    @requires_license(tier="pro")
    def advanced_reasoning(self, problem: str, reasoning_depth: int = 15) -> Dict[str, Any]:
        """
        Perform advanced reasoning with enhanced depth and analytics.
        Requires Pro license.
        
        Args:
            problem: Problem description to reason about
            reasoning_depth: Maximum reasoning depth
            
        Returns:
            Dict containing reasoning results and analytics
        """
        self._ensure_feature_license("pro")
        
        # Create a complex reasoning goal
        reasoning_goal = Goal(
            goal_id=f"advanced_reasoning_{uuid.uuid4().hex[:8]}",
            description=f"Advanced reasoning about: {problem}",
            priority=0.9,
            conditions={"problem": problem, "depth": reasoning_depth}
        )
        
        # Perform enhanced reasoning with deeper search
        old_depth = self.inference_engine.depth_limit
        self.inference_engine.depth_limit = reasoning_depth
        
        try:
            # Gather enhanced context
            facts = []
            
            # Add memory-based facts
            memories = self.memory_manager.retrieve_memories(problem, limit=20)
            for memory in memories:
                facts.append(Fact(
                    predicate="knowledge",
                    arguments=[memory.content],
                    confidence=memory.importance
                ))
            
            # Add personality-based reasoning biases
            if self.personality.analyticalness > 0.7:
                facts.append(Fact("analytical_approach", ["detailed_analysis"], 0.8))
            if self.personality.creativity > 0.7:
                facts.append(Fact("creative_approach", ["novel_solutions"], 0.8))
            
            # Perform advanced inference
            reasoning_result = self.inference_engine.infer(reasoning_goal, facts)
            
            # Generate analytics
            analytics = {
                "reasoning_depth_used": reasoning_depth,
                "facts_considered": len(facts),
                "inference_steps": getattr(reasoning_result, 'steps', 0),
                "confidence": reasoning_result.confidence if reasoning_result.success else 0.0,
                "personality_influence": {
                    "analytical_bias": self.personality.analyticalness,
                    "creative_bias": self.personality.creativity
                }
            }
            
            return {
                "success": reasoning_result.success,
                "result": reasoning_result.conclusion if reasoning_result.success else None,
                "recommended_actions": reasoning_result.recommended_actions,
                "analytics": analytics,
                "machine_id": self.get_machine_id()
            }
            
        finally:
            # Restore original depth limit
            self.inference_engine.depth_limit = old_depth
    
    @requires_license(tier="research")
    def generate_research_insights(self, domain: str) -> Dict[str, Any]:
        """
        Generate research insights and novel hypotheses.
        Requires Research license.
        
        Args:
            domain: Research domain to analyze
            
        Returns:
            Dict containing research insights and hypotheses
        """
        self._ensure_feature_license("research")
        
        # Retrieve domain-relevant knowledge
        domain_memories = self.memory_manager.retrieve_memories(domain, limit=50)
        
        # Analyze knowledge patterns
        insights = []
        hypotheses = []
        
        # Knowledge gap analysis
        knowledge_areas = set()
        for memory in domain_memories:
            if 'domain' in memory.metadata:
                knowledge_areas.add(memory.metadata['domain'])
        
        # Generate insights based on knowledge patterns
        if self.personality.creativity > 0.6:
            insights.append(f"Creative pattern analysis in {domain} suggests novel approaches")
        
        if len(knowledge_areas) > 5:
            insights.append(f"Interdisciplinary connections identified across {len(knowledge_areas)} areas")
        
        # Generate testable hypotheses
        if self.personality.analyticalness > 0.7:
            hypotheses.append(f"Systematic analysis of {domain} could reveal measurable patterns")
        
        # Store research insights in memory
        insight_memory = MemoryItem(
            content=f"Research insights generated for {domain}",
            memory_type=MemoryType.SEMANTIC,
            importance=0.9,
            metadata={
                "domain": domain,
                "insights_count": len(insights),
                "hypotheses_count": len(hypotheses),
                "research_timestamp": time.time()
            }
        )
        self.memory_manager.store_memory(insight_memory)
        
        return {
            "domain": domain,
            "insights": insights,
            "hypotheses": hypotheses,
            "knowledge_areas": list(knowledge_areas),
            "novelty_score": self.personality.creativity,
            "analytical_rigor": self.personality.analyticalness,
            "machine_id": self.get_machine_id()
        }
    
    @requires_license(tier="enterprise")
    def collaborate_with_agents(self, other_agents: List['CognitiveAgent'], 
                               collaboration_goal: str) -> Dict[str, Any]:
        """
        Collaborate with other agents on complex tasks.
        Requires Enterprise license.
        
        Args:
            other_agents: List of other agents to collaborate with
            collaboration_goal: Shared goal for collaboration
            
        Returns:
            Dict containing collaboration results
        """
        self._ensure_feature_license("enterprise")
        
        # Initiate collaboration protocol
        collaboration_id = uuid.uuid4().hex[:8]
        
        # Share relevant knowledge with other agents
        shared_knowledge = []
        for memory in self.memory_manager.get_semantic_memory():
            if memory.importance > 0.7:  # Share high-importance knowledge
                shared_knowledge.append({
                    "content": memory.content,
                    "importance": memory.importance,
                    "source_agent": self.agent_id
                })
        
        # Analyze collaboration potential
        collaboration_score = 0.0
        for agent in other_agents:
            # Simple compatibility check based on personality
            compatibility = 1.0 - abs(self.personality.sociability - agent.personality.sociability)
            collaboration_score += compatibility
        
        collaboration_score /= len(other_agents) if other_agents else 1
        
        # Store collaboration experience
        collab_memory = MemoryItem(
            content=f"Collaborated with {len(other_agents)} agents on: {collaboration_goal}",
            memory_type=MemoryType.EPISODIC,
            importance=0.8,
            metadata={
                "collaboration_id": collaboration_id,
                "goal": collaboration_goal,
                "participants": [agent.agent_id for agent in other_agents],
                "compatibility_score": collaboration_score
            }
        )
        self.memory_manager.store_memory(collab_memory)
        
        return {
            "collaboration_id": collaboration_id,
            "participants": [self.agent_id] + [agent.agent_id for agent in other_agents],
            "shared_knowledge_items": len(shared_knowledge),
            "collaboration_score": collaboration_score,
            "goal": collaboration_goal,
            "machine_id": self.get_machine_id()
        }
