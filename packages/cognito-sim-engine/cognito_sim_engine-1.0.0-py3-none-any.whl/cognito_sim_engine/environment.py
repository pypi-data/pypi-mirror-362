"""
Environment System - Cognitive environments for agent interaction.

This module provides environments where cognitive agents can perceive, act,
and interact with simulated worlds for testing cognitive architectures.
"""

import time
import uuid
from typing import Dict, List, Optional, Any, Set, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random
import numpy as np
from collections import defaultdict, deque


class ActionType(Enum):
    """Types of actions agents can perform."""
    PHYSICAL = "physical"
    COGNITIVE = "cognitive"
    COMMUNICATION = "communication"
    OBSERVATION = "observation"
    MANIPULATION = "manipulation"


class PerceptionType(Enum):
    """Types of perceptions available to agents."""
    VISUAL = "visual"
    AUDITORY = "auditory"
    TACTILE = "tactile"
    COGNITIVE = "cognitive"
    INTERNAL = "internal"


@dataclass
class Action:
    """Represents an action that can be performed by an agent."""
    name: str
    action_type: ActionType = ActionType.PHYSICAL
    parameters: Dict[str, Any] = field(default_factory=dict)
    priority: float = 0.5
    duration: float = 1.0  # seconds
    energy_cost: float = 1.0
    description: str = ""
    preconditions: List[str] = field(default_factory=list)
    effects: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def can_execute(self, agent_state: Dict[str, Any]) -> bool:
        """Check if action can be executed given agent state."""
        # Check energy requirements
        if agent_state.get("energy", 0) < self.energy_cost:
            return False
        
        # Check preconditions (simplified)
        for precondition in self.preconditions:
            if precondition not in agent_state.get("capabilities", []):
                return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert action to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "action_type": self.action_type.value,
            "parameters": self.parameters,
            "priority": self.priority,
            "duration": self.duration,
            "energy_cost": self.energy_cost,
            "description": self.description,
            "preconditions": self.preconditions,
            "effects": self.effects,
            "metadata": self.metadata
        }


@dataclass
class Perception:
    """Represents a perception received by an agent."""
    type: PerceptionType
    data: Any
    salience: float = 0.5  # How attention-grabbing this perception is
    timestamp: float = field(default_factory=time.time)
    source: str = "environment"
    location: Optional[Dict[str, float]] = None  # Spatial location if relevant
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert perception to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "data": self.data,
            "salience": self.salience,
            "timestamp": self.timestamp,
            "source": self.source,
            "location": self.location,
            "metadata": self.metadata
        }


@dataclass
class EnvironmentObject:
    """Represents an object in the environment."""
    name: str
    object_type: str = "generic"
    position: Dict[str, float] = field(default_factory=lambda: {"x": 0, "y": 0, "z": 0})
    properties: Dict[str, Any] = field(default_factory=dict)
    state: Dict[str, Any] = field(default_factory=dict)
    interactable: bool = True
    visible: bool = True
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def interact(self, action: Action, agent_id: str) -> Dict[str, Any]:
        """Handle interaction with this object."""
        result = {
            "success": False,
            "message": "No interaction defined",
            "state_changes": {}
        }
        
        if not self.interactable:
            result["message"] = f"{self.name} cannot be interacted with"
            return result
        
        # Basic interaction logic
        if action.name == "examine":
            result["success"] = True
            result["message"] = f"You examine the {self.name}. {self.description}"
        elif action.name == "move" and "direction" in action.parameters:
            # Move object if possible
            if self.properties.get("movable", False):
                direction = action.parameters["direction"]
                if direction == "up":
                    self.position["z"] += 1
                elif direction == "down":
                    self.position["z"] -= 1
                # Add more directions as needed
                result["success"] = True
                result["message"] = f"Moved {self.name} {direction}"
                result["state_changes"] = {"position": self.position.copy()}
            else:
                result["message"] = f"{self.name} cannot be moved"
        
        return result
    
    def get_visual_perception(self, observer_position: Dict[str, float]) -> Optional[Perception]:
        """Generate visual perception of this object."""
        if not self.visible:
            return None
        
        # Calculate distance
        dx = self.position["x"] - observer_position["x"]
        dy = self.position["y"] - observer_position["y"]
        dz = self.position["z"] - observer_position["z"]
        distance = np.sqrt(dx*dx + dy*dy + dz*dz)
        
        # Salience decreases with distance
        salience = max(0.1, 1.0 / (1.0 + distance))
        
        return Perception(
            type=PerceptionType.VISUAL,
            data={
                "object_name": self.name,
                "object_type": self.object_type,
                "position": self.position.copy(),
                "distance": distance,
                "visible_properties": {k: v for k, v in self.properties.items() if k in ["color", "size", "shape"]}
            },
            salience=salience,
            source="environment",
            location=self.position.copy(),
            metadata={"object_id": self.id}
        )


class EnvironmentState:
    """Represents the current state of the environment."""
    
    def __init__(self):
        """Initialize environment state."""
        self.objects: Dict[str, EnvironmentObject] = {}
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.global_properties: Dict[str, Any] = {
            "time": 0.0,
            "weather": "clear",
            "lighting": 1.0,
            "temperature": 20.0
        }
        self.event_history: deque = deque(maxlen=1000)
        self.spatial_grid: Dict[Tuple[int, int, int], Set[str]] = defaultdict(set)
    
    def add_object(self, obj: EnvironmentObject) -> str:
        """Add object to environment."""
        self.objects[obj.id] = obj
        self._update_spatial_grid(obj)
        
        self.event_history.append({
            "type": "object_added",
            "object_id": obj.id,
            "timestamp": time.time()
        })
        
        return obj.id
    
    def remove_object(self, object_id: str) -> bool:
        """Remove object from environment."""
        if object_id in self.objects:
            obj = self.objects[object_id]
            self._remove_from_spatial_grid(obj)
            del self.objects[object_id]
            
            self.event_history.append({
                "type": "object_removed",
                "object_id": object_id,
                "timestamp": time.time()
            })
            
            return True
        return False
    
    def move_object(self, object_id: str, new_position: Dict[str, float]) -> bool:
        """Move object to new position."""
        if object_id in self.objects:
            obj = self.objects[object_id]
            old_position = obj.position.copy()
            
            self._remove_from_spatial_grid(obj)
            obj.position = new_position.copy()
            self._update_spatial_grid(obj)
            
            self.event_history.append({
                "type": "object_moved",
                "object_id": object_id,
                "old_position": old_position,
                "new_position": new_position,
                "timestamp": time.time()
            })
            
            return True
        return False
    
    def _update_spatial_grid(self, obj: EnvironmentObject) -> None:
        """Update spatial grid with object position."""
        grid_pos = (
            int(obj.position["x"]),
            int(obj.position["y"]),
            int(obj.position["z"])
        )
        self.spatial_grid[grid_pos].add(obj.id)
    
    def _remove_from_spatial_grid(self, obj: EnvironmentObject) -> None:
        """Remove object from spatial grid."""
        grid_pos = (
            int(obj.position["x"]),
            int(obj.position["y"]),
            int(obj.position["z"])
        )
        self.spatial_grid[grid_pos].discard(obj.id)
    
    def get_objects_near(self, position: Dict[str, float], radius: float = 5.0) -> List[EnvironmentObject]:
        """Get objects within radius of position."""
        nearby_objects = []
        
        for obj in self.objects.values():
            dx = obj.position["x"] - position["x"]
            dy = obj.position["y"] - position["y"]
            dz = obj.position["z"] - position["z"]
            distance = np.sqrt(dx*dx + dy*dy + dz*dz)
            
            if distance <= radius:
                nearby_objects.append(obj)
        
        return nearby_objects
    
    def update(self, delta_time: float) -> None:
        """Update environment state."""
        self.global_properties["time"] += delta_time
        
        # Simulate dynamic changes
        if random.random() < 0.001:  # 0.1% chance per update
            # Random weather change
            weathers = ["clear", "cloudy", "rainy", "foggy"]
            self.global_properties["weather"] = random.choice(weathers)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary."""
        return {
            "objects": {obj_id: obj.to_dict() for obj_id, obj in self.objects.items()},
            "agents": self.agents.copy(),
            "global_properties": self.global_properties.copy(),
            "event_count": len(self.event_history)
        }


class CognitiveEnvironment:
    """
    Main cognitive environment for agent interaction.
    
    This class provides a rich, interactive environment where cognitive agents
    can perceive, act, and learn from their experiences.
    """
    
    def __init__(self, name: str = "Default Environment"):
        """
        Initialize cognitive environment.
        
        Args:
            name: Name of the environment
        """
        self.name = name
        self.state = EnvironmentState()
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.perception_generators: List[Callable] = []
        self.action_handlers: Dict[str, Callable] = {}
        self.update_callbacks: List[Callable] = []
        
        # Environment configuration
        self.max_perception_distance = 10.0
        self.perception_update_rate = 0.1  # seconds
        self.action_success_rate = 0.9
        
        # Metrics
        self.total_actions_executed = 0
        self.total_perceptions_generated = 0
        self.simulation_time = 0.0
        
        # Initialize default environment
        self._setup_default_environment()
        self._register_default_actions()
    
    def _setup_default_environment(self) -> None:
        """Setup a default environment with some objects."""
        # Add some basic objects
        table = EnvironmentObject(
            name="table",
            object_type="furniture",
            position={"x": 5, "y": 5, "z": 0},
            properties={"color": "brown", "material": "wood", "size": "medium"},
            description="A sturdy wooden table"
        )
        self.state.add_object(table)
        
        chair = EnvironmentObject(
            name="chair",
            object_type="furniture",
            position={"x": 4, "y": 5, "z": 0},
            properties={"color": "black", "material": "plastic", "size": "small", "movable": True},
            description="A simple plastic chair"
        )
        self.state.add_object(chair)
        
        book = EnvironmentObject(
            name="book",
            object_type="item",
            position={"x": 5, "y": 5, "z": 1},
            properties={"color": "red", "size": "small", "movable": True},
            description="An interesting book about cognitive science"
        )
        self.state.add_object(book)
    
    def _register_default_actions(self) -> None:
        """Register default action handlers."""
        self.action_handlers["move"] = self._handle_move_action
        self.action_handlers["examine"] = self._handle_examine_action
        self.action_handlers["interact"] = self._handle_interact_action
        self.action_handlers["wait"] = self._handle_wait_action
        self.action_handlers["explore"] = self._handle_explore_action
    
    def add_agent(self, agent_id: str, initial_position: Optional[Dict[str, float]] = None) -> None:
        """Add an agent to the environment."""
        if initial_position is None:
            initial_position = {"x": 0, "y": 0, "z": 0}
        
        self.agents[agent_id] = {
            "position": initial_position.copy(),
            "energy": 100.0,
            "capabilities": ["move", "examine", "interact", "wait", "explore"],
            "inventory": [],
            "status": "active",
            "last_action": None,
            "perception_history": deque(maxlen=100)
        }
        
        self.state.agents[agent_id] = self.agents[agent_id].copy()
    
    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent from the environment."""
        if agent_id in self.agents:
            del self.agents[agent_id]
            if agent_id in self.state.agents:
                del self.state.agents[agent_id]
            return True
        return False
    
    def get_perceptions(self, agent_id: Optional[str] = None) -> List[Perception]:
        """
        Get current perceptions for an agent or all agents.
        
        Args:
            agent_id: Specific agent ID, or None for all agents
            
        Returns:
            List of current perceptions
        """
        perceptions = []
        
        if agent_id:
            if agent_id in self.agents:
                perceptions.extend(self._generate_agent_perceptions(agent_id))
        else:
            # Generate perceptions for all agents
            for aid in self.agents.keys():
                perceptions.extend(self._generate_agent_perceptions(aid))
        
        # Add global perceptions
        perceptions.extend(self._generate_global_perceptions())
        
        self.total_perceptions_generated += len(perceptions)
        return perceptions
    
    def _generate_agent_perceptions(self, agent_id: str) -> List[Perception]:
        """Generate perceptions for a specific agent."""
        if agent_id not in self.agents:
            return []
        
        agent = self.agents[agent_id]
        perceptions = []
        
        # Visual perceptions of nearby objects
        nearby_objects = self.state.get_objects_near(
            agent["position"], 
            self.max_perception_distance
        )
        
        for obj in nearby_objects:
            visual_perception = obj.get_visual_perception(agent["position"])
            if visual_perception:
                perceptions.append(visual_perception)
        
        # Internal state perceptions
        internal_perception = Perception(
            type=PerceptionType.INTERNAL,
            data={
                "energy": agent["energy"],
                "position": agent["position"].copy(),
                "inventory_count": len(agent["inventory"]),
                "status": agent["status"]
            },
            salience=0.3,
            source="internal"
        )
        perceptions.append(internal_perception)
        
        # Environmental perceptions
        env_perception = Perception(
            type=PerceptionType.COGNITIVE,
            data={
                "weather": self.state.global_properties["weather"],
                "lighting": self.state.global_properties["lighting"],
                "time": self.state.global_properties["time"]
            },
            salience=0.2,
            source="environment"
        )
        perceptions.append(env_perception)
        
        # Store in agent's history
        agent["perception_history"].extend(perceptions)
        
        return perceptions
    
    def _generate_global_perceptions(self) -> List[Perception]:
        """Generate global environment perceptions."""
        perceptions = []
        
        # Random events
        if random.random() < 0.05:  # 5% chance of random event
            event_perception = Perception(
                type=PerceptionType.AUDITORY,
                data={"event": "ambient_sound", "description": "You hear a distant sound"},
                salience=0.4,
                source="environment"
            )
            perceptions.append(event_perception)
        
        return perceptions
    
    def execute_action(self, action: Action, agent_id: Optional[str] = None) -> bool:
        """
        Execute an action in the environment.
        
        Args:
            action: The action to execute
            agent_id: ID of the agent performing the action
            
        Returns:
            True if action was successful
        """
        if agent_id and agent_id not in self.agents:
            return False
        
        # Check if action can be executed
        if agent_id:
            agent = self.agents[agent_id]
            if not action.can_execute(agent):
                return False
        
        # Handle the action
        success = False
        if action.name in self.action_handlers:
            success = self.action_handlers[action.name](action, agent_id)
        else:
            # Default handler
            success = self._handle_default_action(action, agent_id)
        
        # Update agent state
        if success and agent_id:
            agent = self.agents[agent_id]
            agent["energy"] -= action.energy_cost
            agent["last_action"] = action.name
            
            # Random chance of failure
            if random.random() > self.action_success_rate:
                success = False
        
        if success:
            self.total_actions_executed += 1
        
        return success
    
    def _handle_move_action(self, action: Action, agent_id: Optional[str]) -> bool:
        """Handle movement actions."""
        if not agent_id or agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        direction = action.parameters.get("direction", "forward")
        distance = action.parameters.get("distance", 1.0)
        
        # Calculate new position
        new_position = agent["position"].copy()
        
        if direction == "forward":
            new_position["y"] += distance
        elif direction == "backward":
            new_position["y"] -= distance
        elif direction == "left":
            new_position["x"] -= distance
        elif direction == "right":
            new_position["x"] += distance
        elif direction == "up":
            new_position["z"] += distance
        elif direction == "down":
            new_position["z"] = max(0, new_position["z"] - distance)
        
        # Check for collisions (simplified)
        nearby_objects = self.state.get_objects_near(new_position, 0.5)
        blocking_objects = [obj for obj in nearby_objects if not obj.properties.get("passable", False)]
        
        if blocking_objects:
            return False  # Movement blocked
        
        # Update position
        old_position = agent["position"].copy()
        agent["position"] = new_position
        self.state.agents[agent_id]["position"] = new_position
        
        # Log movement
        self.state.event_history.append({
            "type": "agent_moved",
            "agent_id": agent_id,
            "old_position": old_position,
            "new_position": new_position,
            "timestamp": time.time()
        })
        
        return True
    
    def _handle_examine_action(self, action: Action, agent_id: Optional[str]) -> bool:
        """Handle examination actions."""
        target = action.parameters.get("target", "")
        
        if agent_id:
            agent = self.agents[agent_id]
            nearby_objects = self.state.get_objects_near(agent["position"], 2.0)
            
            for obj in nearby_objects:
                if obj.name.lower() == target.lower():
                    # Generate detailed perception
                    detailed_perception = Perception(
                        type=PerceptionType.VISUAL,
                        data={
                            "object_name": obj.name,
                            "description": obj.description,
                            "properties": obj.properties.copy(),
                            "state": obj.state.copy()
                        },
                        salience=0.8,
                        source="examination",
                        metadata={"examined_object": obj.id}
                    )
                    agent["perception_history"].append(detailed_perception)
                    return True
        
        return False
    
    def _handle_interact_action(self, action: Action, agent_id: Optional[str]) -> bool:
        """Handle interaction actions."""
        target = action.parameters.get("target", "")
        
        if agent_id:
            agent = self.agents[agent_id]
            nearby_objects = self.state.get_objects_near(agent["position"], 2.0)
            
            for obj in nearby_objects:
                if obj.name.lower() == target.lower():
                    result = obj.interact(action, agent_id)
                    
                    # Generate interaction perception
                    interaction_perception = Perception(
                        type=PerceptionType.COGNITIVE,
                        data={
                            "interaction_result": result,
                            "object_name": obj.name
                        },
                        salience=0.7,
                        source="interaction",
                        metadata={"interaction_success": result["success"]}
                    )
                    agent["perception_history"].append(interaction_perception)
                    
                    return result["success"]
        
        return False
    
    def _handle_wait_action(self, action: Action, agent_id: Optional[str]) -> bool:
        """Handle wait actions."""
        duration = action.parameters.get("duration", 1.0)
        # Waiting always succeeds and just consumes time
        return True
    
    def _handle_explore_action(self, action: Action, agent_id: Optional[str]) -> bool:
        """Handle exploration actions."""
        if not agent_id:
            return False
        
        agent = self.agents[agent_id]
        exploration_radius = action.parameters.get("radius", 5.0)
        
        # Generate exploration perceptions
        nearby_objects = self.state.get_objects_near(agent["position"], exploration_radius)
        
        exploration_data = {
            "objects_found": len(nearby_objects),
            "object_types": list(set(obj.object_type for obj in nearby_objects)),
            "area_explored": exploration_radius
        }
        
        exploration_perception = Perception(
            type=PerceptionType.COGNITIVE,
            data=exploration_data,
            salience=0.6,
            source="exploration"
        )
        
        agent["perception_history"].append(exploration_perception)
        return True
    
    def _handle_default_action(self, action: Action, agent_id: Optional[str]) -> bool:
        """Default action handler for unknown actions."""
        # Unknown actions have a lower success rate
        return random.random() < 0.3
    
    def update(self, delta_time: float = 1.0) -> None:
        """Update the environment state."""
        self.simulation_time += delta_time
        self.state.update(delta_time)
        
        # Update all agents
        for agent_id, agent in self.agents.items():
            # Regenerate some energy over time
            agent["energy"] = min(100.0, agent["energy"] + delta_time * 0.5)
            
            # Update agent state in environment state
            self.state.agents[agent_id] = agent.copy()
        
        # Call update callbacks
        for callback in self.update_callbacks:
            callback(self, delta_time)
    
    def add_perception_generator(self, generator: Callable) -> None:
        """Add a custom perception generator."""
        self.perception_generators.append(generator)
    
    def add_action_handler(self, action_name: str, handler: Callable) -> None:
        """Add a custom action handler."""
        self.action_handlers[action_name] = handler
    
    def add_update_callback(self, callback: Callable) -> None:
        """Add an update callback."""
        self.update_callbacks.append(callback)
    
    def get_environment_summary(self) -> Dict[str, Any]:
        """Get summary of current environment state."""
        return {
            "name": self.name,
            "simulation_time": self.simulation_time,
            "agents": len(self.agents),
            "objects": len(self.state.objects),
            "total_actions": self.total_actions_executed,
            "total_perceptions": self.total_perceptions_generated,
            "global_properties": self.state.global_properties.copy()
        }
    
    def export_state(self) -> Dict[str, Any]:
        """Export complete environment state."""
        return {
            "name": self.name,
            "simulation_time": self.simulation_time,
            "agents": {aid: agent.copy() for aid, agent in self.agents.items()},
            "environment_state": self.state.to_dict(),
            "metrics": {
                "total_actions": self.total_actions_executed,
                "total_perceptions": self.total_perceptions_generated
            }
        }
    
    def load_state(self, state_data: Dict[str, Any]) -> None:
        """Load environment state from data."""
        self.name = state_data.get("name", "Loaded Environment")
        self.simulation_time = state_data.get("simulation_time", 0.0)
        
        # Load agents
        self.agents = {}
        for agent_id, agent_data in state_data.get("agents", {}).items():
            self.agents[agent_id] = agent_data.copy()
        
        # Load metrics
        metrics = state_data.get("metrics", {})
        self.total_actions_executed = metrics.get("total_actions", 0)
        self.total_perceptions_generated = metrics.get("total_perceptions", 0)
