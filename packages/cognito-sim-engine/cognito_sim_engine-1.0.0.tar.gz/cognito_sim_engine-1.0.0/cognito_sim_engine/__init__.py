"""
Cognito Simulation Engine - A modular cognitive simulation framework for AGI research.

This package provides a comprehensive framework for modeling and testing advanced AI 
cognitive architectures, including symbolic reasoning, memory modeling, goal-directed 
behavior, and cognitive learning agents.

Author: Krishna Bajpai <bajpaikrishna715@gmail.com>
License: MIT
"""

from .engine import CognitiveEngine, SimulationConfig
from .memory import (
    WorkingMemory,
    EpisodicMemory,
    LongTermMemory,
    MemoryManager,
    MemoryItem,
    MemoryType
)
from .reasoning import (
    SymbolicReasoner,
    InferenceEngine,
    Rule,
    Fact,
    Goal,
    ReasoningResult
)
from .agents import (
    CognitiveAgent,
    BaseAgent,
    ReasoningAgent,
    LearningAgent,
    MetaCognitiveAgent
)
from .environment import (
    CognitiveEnvironment,
    EnvironmentState,
    Action,
    Perception
)

__version__ = "1.0.0"
__author__ = "Krishna Bajpai"
__email__ = "bajpaikrishna715@gmail.com"

# Import licensing system
from .licensing import (
    CognitoLicenseError,
    LicensedClass,
    requires_license,
    licensed_operation,
    get_license_info,
    display_license_info,
    get_machine_id
)


__all__ = [
    # Core Engine
    "CognitiveEngine",
    "SimulationConfig",
    
    # Memory System
    "WorkingMemory",
    "EpisodicMemory", 
    "LongTermMemory",
    "MemoryManager",
    "MemoryItem",
    "MemoryType",
    
    # Reasoning System
    "SymbolicReasoner",
    "InferenceEngine",
    "Rule",
    "Fact",
    "Goal",
    "ReasoningResult",
    
    # Agent System
    "CognitiveAgent",
    "BaseAgent",
    "ReasoningAgent",
    "LearningAgent",
    "MetaCognitiveAgent",
    
    # Environment System
    "CognitiveEnvironment",
    "EnvironmentState",
    "Action",
    "Perception",
    
    # Licensing System
    "CognitoLicenseError",
    "LicensedClass",
    "requires_license",
    "licensed_operation",
    "get_license_info",
    "display_license_info",
    "get_machine_id",
]
