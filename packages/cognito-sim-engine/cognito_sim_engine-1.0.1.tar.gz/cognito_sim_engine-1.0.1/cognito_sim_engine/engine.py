"""
Cognitive Engine - Main simulation loop for cognitive architectures.

This module provides the core simulation engine that orchestrates cognitive cycles,
managing the interaction between memory, reasoning, and action systems.
"""

import time
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import uuid

from .memory import MemoryManager, MemoryItem, MemoryType
from .reasoning import InferenceEngine, Goal, Fact
from .environment import CognitiveEnvironment, Action, Perception
from .licensing import LicensedClass, requires_license


class SimulationState(Enum):
    """States of the cognitive simulation."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class CognitiveMetrics:
    """Metrics for cognitive performance analysis."""
    total_cycles: int = 0
    reasoning_time: float = 0.0
    memory_operations: int = 0
    goals_achieved: int = 0
    goals_failed: int = 0
    attention_switches: int = 0
    working_memory_load: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "total_cycles": self.total_cycles,
            "reasoning_time": self.reasoning_time,
            "memory_operations": self.memory_operations,
            "goals_achieved": self.goals_achieved,
            "goals_failed": self.goals_failed,
            "attention_switches": self.attention_switches,
            "working_memory_load": self.working_memory_load,
            "avg_reasoning_time": self.reasoning_time / max(1, self.total_cycles),
        }


@dataclass
class SimulationConfig:
    """Configuration for cognitive simulation."""
    max_cycles: int = 1000
    cycle_timeout: float = 1.0  # seconds
    working_memory_capacity: int = 7  # Miller's magical number
    attention_threshold: float = 0.5
    goal_timeout: float = 300.0  # seconds
    enable_metacognition: bool = True
    enable_learning: bool = True
    enable_visualization: bool = False
    log_level: str = "INFO"
    random_seed: Optional[int] = None
    
    # Cognitive parameters
    memory_decay_rate: float = 0.01
    attention_decay_rate: float = 0.05
    goal_priority_threshold: float = 0.3
    reasoning_depth_limit: int = 10
    
    # Performance monitoring
    enable_metrics: bool = True
    metrics_interval: int = 100  # cycles
    
    def __post_init__(self):
        """Validate configuration parameters."""
        if self.max_cycles <= 0:
            raise ValueError("max_cycles must be positive")
        if self.working_memory_capacity <= 0:
            raise ValueError("working_memory_capacity must be positive")
        if not 0 <= self.attention_threshold <= 1:
            raise ValueError("attention_threshold must be between 0 and 1")


class CognitiveEngine(LicensedClass):
    """
    Main cognitive simulation engine.
    
    This class orchestrates the cognitive cycle, managing the flow between
    perception, reasoning, memory operations, and action selection.
    
    Requires: Core license for basic functionality
    Pro license for advanced reasoning features
    Enterprise license for large-scale simulations
    """
    
    def __init__(
        self,
        config: Optional[SimulationConfig] = None,
        environment: Optional[CognitiveEnvironment] = None,
        license_tier: str = "core"
    ):
        """
        Initialize the cognitive engine with license validation.
        
        Args:
            config: Simulation configuration
            environment: Cognitive environment for agent interaction
            license_tier: Required license tier (core, pro, enterprise)
        """
        # Initialize licensing first
        super().__init__(license_tier=license_tier)
        
        self.config = config or SimulationConfig()
        self.environment = environment
        self.state = SimulationState.IDLE
        self.current_cycle = 0
        self.start_time = None
        
        # Core cognitive systems
        self.memory_manager = MemoryManager(
            working_capacity=self.config.working_memory_capacity,
            decay_rate=self.config.memory_decay_rate
        )
        self.inference_engine = InferenceEngine(
            depth_limit=self.config.reasoning_depth_limit
        )
        
        # Cognitive state
        self.current_goals = []
        self.attention_focus = None
        self.last_action = None
        self.current_perceptions = []
        
        # Metrics and monitoring
        self.metrics = CognitiveMetrics()
        self.cycle_callbacks = []
        
        # Setup logging
        logging.basicConfig(level=getattr(logging, self.config.log_level))
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"Cognitive Engine initialized with {license_tier} license")
    
    def add_cycle_callback(self, callback: Callable) -> None:
        """Add a callback function to be called after each cycle."""
        self.cycle_callbacks.append(callback)
    
    def set_environment(self, environment: CognitiveEnvironment) -> None:
        """Set the cognitive environment."""
        self.environment = environment
        self.logger.info("Environment set")
    
    def add_goal(self, goal: Goal) -> None:
        """Add a new goal to the system."""
        self.current_goals.append(goal)
        self.memory_manager.store_memory(
            MemoryItem(
                content=f"New goal: {goal.description}",
                memory_type=MemoryType.EPISODIC,
                importance=goal.priority,
                metadata={"goal_id": goal.id, "type": "goal_creation"}
            )
        )
        self.logger.info(f"Goal added: {goal.description}")
    
    def perceive(self) -> List[Perception]:
        """Perceive the current environment state."""
        if not self.environment:
            return []
        
        perceptions = self.environment.get_perceptions()
        self.current_perceptions = perceptions
        
        # Store perceptions in memory
        for perception in perceptions:
            self.memory_manager.store_memory(
                MemoryItem(
                    content=f"Perceived: {perception.data}",
                    memory_type=MemoryType.WORKING,
                    importance=perception.salience,
                    metadata={"type": "perception", "perception_type": perception.type}
                )
            )
        
        self.metrics.memory_operations += len(perceptions)
        return perceptions
    
    def reason(self) -> List[Action]:
        """Perform reasoning to determine next actions."""
        start_time = time.time()
        
        # Gather relevant facts from memory
        facts = []
        working_memories = self.memory_manager.get_working_memory()
        for memory in working_memories:
            facts.append(Fact(
                predicate="memory",
                arguments=[memory.content],
                confidence=memory.importance
            ))
        
        # Add perception facts
        for perception in self.current_perceptions:
            facts.append(Fact(
                predicate="perceived",
                arguments=[perception.type, str(perception.data)],
                confidence=perception.salience
            ))
        
        # Perform inference for each active goal
        possible_actions = []
        for goal in self.current_goals:
            if goal.is_active():
                result = self.inference_engine.infer(goal, facts)
                if result.success and result.recommended_actions:
                    possible_actions.extend(result.recommended_actions)
        
        # Update metrics
        reasoning_time = time.time() - start_time
        self.metrics.reasoning_time += reasoning_time
        
        return possible_actions
    
    def select_action(self, possible_actions: List[Action]) -> Optional[Action]:
        """Select the best action from possible actions."""
        if not possible_actions:
            return None
        
        # Simple action selection based on priority and context
        # In a more sophisticated system, this could use utility theory
        best_action = max(possible_actions, key=lambda a: a.priority)
        
        # Update attention focus
        if best_action.metadata.get("attention_target"):
            old_focus = self.attention_focus
            self.attention_focus = best_action.metadata["attention_target"]
            if old_focus != self.attention_focus:
                self.metrics.attention_switches += 1
        
        return best_action
    
    def execute_action(self, action: Action) -> bool:
        """Execute the selected action in the environment."""
        if not self.environment:
            self.logger.warning("No environment available for action execution")
            return False
        
        success = self.environment.execute_action(action)
        self.last_action = action
        
        # Store action in episodic memory
        self.memory_manager.store_memory(
            MemoryItem(
                content=f"Executed action: {action.name}",
                memory_type=MemoryType.EPISODIC,
                importance=action.priority,
                metadata={"type": "action", "success": success}
            )
        )
        
        self.metrics.memory_operations += 1
        return success
    
    def update_goals(self) -> None:
        """Update goal states and remove completed/expired goals."""
        current_time = time.time()
        updated_goals = []
        
        for goal in self.current_goals:
            if goal.is_achieved():
                self.metrics.goals_achieved += 1
                self.logger.info(f"Goal achieved: {goal.description}")
            elif goal.is_expired(current_time):
                self.metrics.goals_failed += 1
                self.logger.info(f"Goal expired: {goal.description}")
            else:
                updated_goals.append(goal)
        
        self.current_goals = updated_goals
    
    def cognitive_cycle(self) -> bool:
        """
        Execute one cognitive cycle.
        
        Returns:
            True if the cycle completed successfully, False if simulation should stop
        """
        try:
            self.current_cycle += 1
            
            # 1. Perceive environment
            perceptions = self.perceive()
            
            # 2. Update working memory and attention
            self.memory_manager.update_working_memory()
            self.metrics.working_memory_load = len(self.memory_manager.get_working_memory())
            
            # 3. Reason about current situation
            possible_actions = self.reason()
            
            # 4. Select best action
            selected_action = self.select_action(possible_actions)
            
            # 5. Execute action
            if selected_action:
                self.execute_action(selected_action)
            
            # 6. Update goals
            self.update_goals()
            
            # 7. Metacognitive reflection (if enabled)
            if self.config.enable_metacognition:
                self._metacognitive_reflection()
            
            # 8. Learning update (if enabled)
            if self.config.enable_learning:
                self._learning_update()
            
            # 9. Call cycle callbacks
            for callback in self.cycle_callbacks:
                callback(self)
            
            # 10. Update metrics
            self.metrics.total_cycles = self.current_cycle
            
            # Log progress periodically
            if self.current_cycle % self.config.metrics_interval == 0:
                self.logger.info(f"Cycle {self.current_cycle}: {len(self.current_goals)} active goals")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in cognitive cycle {self.current_cycle}: {e}")
            self.state = SimulationState.ERROR
            return False
    
    def _metacognitive_reflection(self) -> None:
        """Perform metacognitive reflection on recent performance."""
        # Simple metacognitive check: are we making progress on goals?
        if self.current_cycle % 50 == 0 and self.current_goals:
            # Check if goals are progressing
            stalled_goals = [g for g in self.current_goals if not g.has_recent_progress()]
            
            if stalled_goals:
                # Add metacognitive insight to memory
                self.memory_manager.store_memory(
                    MemoryItem(
                        content=f"Metacognitive insight: {len(stalled_goals)} goals may be stalled",
                        memory_type=MemoryType.EPISODIC,
                        importance=0.8,
                        metadata={"type": "metacognition", "stalled_goals": len(stalled_goals)}
                    )
                )
    
    def _learning_update(self) -> None:
        """Update learning mechanisms based on recent experience."""
        # Simple learning: reinforce successful action patterns
        if self.last_action and self.environment:
            # This is a placeholder for more sophisticated learning
            pass
    
    def run_simulation(self, max_cycles: Optional[int] = None) -> CognitiveMetrics:
        """
        Run the complete cognitive simulation.
        
        Args:
            max_cycles: Maximum number of cycles to run (overrides config)
            
        Returns:
            Final metrics from the simulation
        """
        max_cycles = max_cycles or self.config.max_cycles
        self.state = SimulationState.RUNNING
        self.start_time = time.time()
        
        self.logger.info(f"Starting cognitive simulation for {max_cycles} cycles")
        
        try:
            while (self.current_cycle < max_cycles and 
                   self.state == SimulationState.RUNNING):
                
                cycle_start = time.time()
                
                # Execute cognitive cycle
                if not self.cognitive_cycle():
                    break
                
                # Check for completion conditions
                if not self.current_goals and self.current_cycle > 10:
                    self.logger.info("No active goals remaining - simulation complete")
                    self.state = SimulationState.COMPLETED
                    break
                
                # Enforce cycle timeout
                cycle_time = time.time() - cycle_start
                if cycle_time < self.config.cycle_timeout:
                    time.sleep(self.config.cycle_timeout - cycle_time)
            
            if self.current_cycle >= max_cycles:
                self.state = SimulationState.COMPLETED
                self.logger.info(f"Simulation completed after {max_cycles} cycles")
            
        except KeyboardInterrupt:
            self.logger.info("Simulation interrupted by user")
            self.state = SimulationState.PAUSED
        except Exception as e:
            self.logger.error(f"Simulation error: {e}")
            self.state = SimulationState.ERROR
        
        # Final metrics calculation
        total_time = time.time() - (self.start_time or time.time())
        self.logger.info(f"Simulation ended. Total time: {total_time:.2f}s, Cycles: {self.current_cycle}")
        
        return self.metrics
    
    @requires_license(tier="pro")
    def run_advanced_simulation(self, duration: float = None, max_cycles: int = None) -> Dict[str, Any]:
        """
        Run advanced simulation with enhanced analytics and optimization.
        Requires Pro license.
        
        Args:
            duration: Maximum simulation duration in seconds
            max_cycles: Maximum number of cycles to run
            
        Returns:
            Dict containing detailed simulation results and analytics
        """
        self._ensure_feature_license("pro")
        
        # Advanced simulation with detailed analytics
        start_time = time.time()
        results = {
            "success": False,
            "cycles_completed": 0,
            "duration": 0.0,
            "advanced_metrics": {},
            "optimization_insights": []
        }
        
        try:
            # Run simulation with advanced monitoring
            self.run_simulation(duration=duration, max_cycles=max_cycles)
            
            results["success"] = True
            results["cycles_completed"] = self.current_cycle
            results["duration"] = time.time() - start_time
            results["advanced_metrics"] = self._generate_advanced_metrics()
            results["optimization_insights"] = self._generate_optimization_insights()
            
        except Exception as e:
            self.logger.error(f"Advanced simulation failed: {e}")
            results["error"] = str(e)
        
        return results
    
    @requires_license(tier="enterprise")
    def run_distributed_simulation(self, worker_count: int = 4, 
                                 load_balancing: str = "dynamic") -> Dict[str, Any]:
        """
        Run large-scale distributed simulation.
        Requires Enterprise license.
        
        Args:
            worker_count: Number of worker processes
            load_balancing: Load balancing strategy
            
        Returns:
            Dict containing distributed simulation results
        """
        self._ensure_feature_license("enterprise")
        
        return {
            "message": "Distributed simulation requires Enterprise license implementation",
            "worker_count": worker_count,
            "load_balancing": load_balancing,
            "machine_id": self.get_machine_id()
        }
    
    def _generate_advanced_metrics(self) -> Dict[str, Any]:
        """Generate advanced performance metrics (Pro feature)."""
        return {
            "cognitive_efficiency": self.metrics.goals_achieved / max(1, self.metrics.total_cycles),
            "memory_utilization": self.metrics.memory_operations / max(1, self.metrics.total_cycles),
            "attention_stability": 1.0 - (self.metrics.attention_switches / max(1, self.metrics.total_cycles)),
            "reasoning_efficiency": self.metrics.total_cycles / max(1, self.metrics.reasoning_time)
        }
    
    def _generate_optimization_insights(self) -> List[str]:
        """Generate optimization insights (Pro feature)."""
        insights = []
        
        if self.metrics.working_memory_load > 0.8:
            insights.append("Working memory utilization is high - consider optimizing memory management")
        
        if self.metrics.attention_switches > self.metrics.total_cycles * 0.3:
            insights.append("High attention switching detected - consider improving focus strategies")
        
        if self.metrics.reasoning_time > self.metrics.total_cycles * 0.1:
            insights.append("Reasoning overhead is high - consider simplifying inference rules")
        
        return insights

    # ...existing code...
    
    def pause_simulation(self) -> None:
        """Pause the running simulation."""
        if self.state == SimulationState.RUNNING:
            self.state = SimulationState.PAUSED
            self.logger.info("Simulation paused")
    
    def resume_simulation(self) -> None:
        """Resume a paused simulation."""
        if self.state == SimulationState.PAUSED:
            self.state = SimulationState.RUNNING
            self.logger.info("Simulation resumed")
    
    def stop_simulation(self) -> None:
        """Stop the simulation."""
        self.state = SimulationState.COMPLETED
        self.logger.info("Simulation stopped")
    
    def get_state_summary(self) -> Dict[str, Any]:
        """Get a summary of the current cognitive state."""
        return {
            "simulation_state": self.state.value,
            "current_cycle": self.current_cycle,
            "active_goals": len(self.current_goals),
            "working_memory_items": len(self.memory_manager.get_working_memory()),
            "attention_focus": self.attention_focus,
            "last_action": self.last_action.name if self.last_action else None,
            "metrics": self.metrics.to_dict()
        }
    
    def export_session(self, filepath: str) -> None:
        """Export the current session data to a file."""
        import json
        
        session_data = {
            "config": self.config.__dict__,
            "state_summary": self.get_state_summary(),
            "memory_dump": self.memory_manager.export_memories(),
            "goals": [goal.to_dict() for goal in self.current_goals],
            "timestamp": time.time()
        }
        
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2, default=str)
        
        self.logger.info(f"Session exported to {filepath}")
