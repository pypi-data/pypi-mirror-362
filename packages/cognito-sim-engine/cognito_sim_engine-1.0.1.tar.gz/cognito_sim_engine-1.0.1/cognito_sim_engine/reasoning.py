"""
Reasoning System - Symbolic reasoning and inference engine for cognitive architectures.

This module implements sophisticated reasoning capabilities including rule-based inference,
goal-directed reasoning, planning, and symbolic manipulation.
"""

from argparse import Action
import time
import uuid
from typing import Dict, List, Optional, Any, Set, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import itertools
from collections import defaultdict, deque
import json


class LogicalOperator(Enum):
    """Logical operators for reasoning."""
    AND = "and"
    OR = "or"
    NOT = "not"
    IMPLIES = "implies"
    EQUIVALENT = "equivalent"


class ConfidenceLevel(Enum):
    """Confidence levels for reasoning results."""
    VERY_LOW = 0.1
    LOW = 0.3
    MEDIUM = 0.5
    HIGH = 0.7
    VERY_HIGH = 0.9
    CERTAIN = 1.0


@dataclass
class Fact:
    """Represents a fact in the knowledge base."""
    predicate: str
    arguments: List[str] = field(default_factory=list)
    confidence: float = 1.0
    timestamp: float = field(default_factory=time.time)
    source: str = "user"
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def __str__(self) -> str:
        """String representation of the fact."""
        if self.arguments:
            args_str = "(" + ", ".join(self.arguments) + ")"
            return f"{self.predicate}{args_str}"
        return self.predicate
    
    def matches(self, pattern: 'Fact') -> bool:
        """Check if this fact matches a pattern (allowing variables)."""
        if self.predicate != pattern.predicate:
            return False
        
        if len(self.arguments) != len(pattern.arguments):
            return False
        
        for arg1, arg2 in zip(self.arguments, pattern.arguments):
            # Variables start with '?'
            if not (arg2.startswith('?') or arg1 == arg2):
                return False
        
        return True
    
    def substitute_variables(self, bindings: Dict[str, str]) -> 'Fact':
        """Create a new fact with variables substituted."""
        new_args = []
        for arg in self.arguments:
            if arg.startswith('?') and arg in bindings:
                new_args.append(bindings[arg])
            else:
                new_args.append(arg)
        
        return Fact(
            predicate=self.predicate,
            arguments=new_args,
            confidence=self.confidence,
            timestamp=self.timestamp,
            source=self.source,
            metadata=self.metadata.copy()
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert fact to dictionary."""
        return {
            "id": self.id,
            "predicate": self.predicate,
            "arguments": self.arguments,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "source": self.source,
            "metadata": self.metadata
        }


@dataclass
class Rule:
    """Represents an inference rule."""
    conditions: List[Fact]
    conclusion: Fact
    confidence: float = 1.0
    priority: int = 1
    name: str = ""
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def __post_init__(self):
        """Initialize rule name if not provided."""
        if not self.name:
            self.name = f"rule_{self.id[:8]}"
    
    def can_apply(self, facts: List[Fact]) -> Tuple[bool, Dict[str, str]]:
        """
        Check if this rule can be applied to the given facts.
        
        Returns:
            Tuple of (can_apply, variable_bindings)
        """
        if not self.conditions:
            return False, {}
        
        # Try to find a consistent binding for all conditions
        return self._find_bindings(facts, 0, {})
    
    def _find_bindings(
        self,
        facts: List[Fact],
        condition_idx: int,
        current_bindings: Dict[str, str]
    ) -> Tuple[bool, Dict[str, str]]:
        """Recursively find variable bindings for rule conditions."""
        if condition_idx >= len(self.conditions):
            return True, current_bindings
        
        condition = self.conditions[condition_idx]
        
        for fact in facts:
            if fact.matches(condition):
                # Try to bind variables
                new_bindings = current_bindings.copy()
                binding_success = True
                
                for cond_arg, fact_arg in zip(condition.arguments, fact.arguments):
                    if cond_arg.startswith('?'):  # Variable
                        if cond_arg in new_bindings:
                            if new_bindings[cond_arg] != fact_arg:
                                binding_success = False
                                break
                        else:
                            new_bindings[cond_arg] = fact_arg
                
                if binding_success:
                    success, final_bindings = self._find_bindings(
                        facts, condition_idx + 1, new_bindings
                    )
                    if success:
                        return True, final_bindings
        
        return False, {}
    
    def apply(self, bindings: Dict[str, str]) -> Fact:
        """Apply the rule with given variable bindings."""
        new_conclusion = self.conclusion.substitute_variables(bindings)
        new_conclusion.confidence *= self.confidence
        new_conclusion.source = f"rule_{self.name}"
        return new_conclusion
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert rule to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "conditions": [cond.to_dict() for cond in self.conditions],
            "conclusion": self.conclusion.to_dict(),
            "confidence": self.confidence,
            "priority": self.priority
        }


@dataclass
class Goal:
    """Represents a goal in goal-directed reasoning."""
    description: str
    target_facts: List[Fact] = field(default_factory=list)
    priority: float = 0.5
    deadline: Optional[float] = None
    created_at: float = field(default_factory=time.time)
    progress: float = 0.0
    status: str = "active"  # active, achieved, failed, suspended
    subgoals: List['Goal'] = field(default_factory=list)
    required_resources: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    last_progress_update: float = field(default_factory=time.time)
    
    def is_achieved(self) -> bool:
        """Check if the goal is achieved."""
        return self.status == "achieved" or self.progress >= 1.0
    
    def is_active(self) -> bool:
        """Check if the goal is currently active."""
        return self.status == "active"
    
    def is_expired(self, current_time: Optional[float] = None) -> bool:
        """Check if the goal has expired."""
        if self.deadline is None:
            return False
        
        if current_time is None:
            current_time = time.time()
        
        return current_time > self.deadline
    
    def has_recent_progress(self, time_window: float = 300.0) -> bool:
        """Check if goal has made recent progress."""
        current_time = time.time()
        return (current_time - self.last_progress_update) < time_window
    
    def update_progress(self, new_progress: float) -> None:
        """Update goal progress."""
        if 0.0 <= new_progress <= 1.0:
            self.progress = new_progress
            self.last_progress_update = time.time()
            
            if new_progress >= 1.0:
                self.status = "achieved"
    
    def add_subgoal(self, subgoal: 'Goal') -> None:
        """Add a subgoal."""
        self.subgoals.append(subgoal)
    
    def calculate_overall_progress(self) -> float:
        """Calculate progress including subgoals."""
        if not self.subgoals:
            return self.progress
        
        subgoal_progress = sum(g.calculate_overall_progress() for g in self.subgoals)
        avg_subgoal_progress = subgoal_progress / len(self.subgoals)
        
        # Weight: 70% own progress, 30% subgoals
        return 0.7 * self.progress + 0.3 * avg_subgoal_progress
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert goal to dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "target_facts": [fact.to_dict() for fact in self.target_facts],
            "priority": self.priority,
            "deadline": self.deadline,
            "created_at": self.created_at,
            "progress": self.progress,
            "status": self.status,
            "subgoals": [sg.to_dict() for sg in self.subgoals],
            "required_resources": list(self.required_resources),
            "metadata": self.metadata,
            "last_progress_update": self.last_progress_update
        }


@dataclass
class ReasoningResult:
    """Result of a reasoning operation."""
    success: bool
    derived_facts: List[Fact] = field(default_factory=list)
    applied_rules: List[str] = field(default_factory=list)
    reasoning_steps: List[str] = field(default_factory=list)
    confidence: float = 0.0
    recommended_actions: List['Action'] = field(default_factory=list)
    explanation: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_step(self, step: str) -> None:
        """Add a reasoning step to the explanation."""
        self.reasoning_steps.append(step)
    
    def add_derived_fact(self, fact: Fact, rule_name: str = "") -> None:
        """Add a derived fact from reasoning."""
        self.derived_facts.append(fact)
        if rule_name and rule_name not in self.applied_rules:
            self.applied_rules.append(rule_name)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "success": self.success,
            "derived_facts": [fact.to_dict() for fact in self.derived_facts],
            "applied_rules": self.applied_rules,
            "reasoning_steps": self.reasoning_steps,
            "confidence": self.confidence,
            "explanation": self.explanation,
            "metadata": self.metadata
        }


class SymbolicReasoner:
    """Core symbolic reasoning engine."""
    
    def __init__(self):
        """Initialize the symbolic reasoner."""
        self.facts: Dict[str, Fact] = {}
        self.rules: Dict[str, Rule] = {}
        self.reasoning_history: List[ReasoningResult] = []
        
        # Load default rules
        self._load_default_rules()
    
    def _load_default_rules(self) -> None:
        """Load default reasoning rules."""
        # Transitivity rule
        transitivity_rule = Rule(
            conditions=[
                Fact("related", ["?x", "?y"]),
                Fact("related", ["?y", "?z"])
            ],
            conclusion=Fact("related", ["?x", "?z"]),
            confidence=0.8,
            name="transitivity",
            description="If X is related to Y and Y is related to Z, then X is related to Z"
        )
        self.add_rule(transitivity_rule)
        
        # Inheritance rule
        inheritance_rule = Rule(
            conditions=[
                Fact("is_a", ["?x", "?type"]),
                Fact("property", ["?type", "?prop"])
            ],
            conclusion=Fact("has_property", ["?x", "?prop"]),
            confidence=0.9,
            name="inheritance",
            description="Objects inherit properties from their types"
        )
        self.add_rule(inheritance_rule)
        
        # Goal achievement rule
        goal_rule = Rule(
            conditions=[
                Fact("has_goal", ["?agent", "?goal"]),
                Fact("action_achieves", ["?action", "?goal"]),
                Fact("can_perform", ["?agent", "?action"])
            ],
            conclusion=Fact("should_do", ["?agent", "?action"]),
            confidence=0.8,
            name="goal_achievement",
            description="Agents should perform actions that achieve their goals"
        )
        self.add_rule(goal_rule)
    
    def add_fact(self, fact: Fact) -> str:
        """Add a fact to the knowledge base."""
        self.facts[fact.id] = fact
        return fact.id
    
    def add_rule(self, rule: Rule) -> str:
        """Add a rule to the rule base."""
        self.rules[rule.id] = rule
        return rule.id
    
    def remove_fact(self, fact_id: str) -> bool:
        """Remove a fact from the knowledge base."""
        if fact_id in self.facts:
            del self.facts[fact_id]
            return True
        return False
    
    def get_facts_by_predicate(self, predicate: str) -> List[Fact]:
        """Get all facts with a specific predicate."""
        return [fact for fact in self.facts.values() if fact.predicate == predicate]
    
    def query_fact(self, pattern: Fact) -> List[Fact]:
        """Query facts matching a pattern."""
        matches = []
        for fact in self.facts.values():
            if fact.matches(pattern):
                matches.append(fact)
        return matches
    
    def forward_chaining(self, max_iterations: int = 100) -> ReasoningResult:
        """
        Perform forward chaining inference.
        
        Args:
            max_iterations: Maximum number of inference iterations
            
        Returns:
            ReasoningResult with derived facts
        """
        result = ReasoningResult(success=True)
        facts_list = list(self.facts.values())
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            new_facts_derived = False
            
            for rule in self.rules.values():
                can_apply, bindings = rule.can_apply(facts_list)
                
                if can_apply:
                    new_fact = rule.apply(bindings)
                    
                    # Check if this fact already exists
                    if not any(existing.predicate == new_fact.predicate and 
                             existing.arguments == new_fact.arguments 
                             for existing in facts_list):
                        
                        fact_id = self.add_fact(new_fact)
                        facts_list.append(new_fact)
                        result.add_derived_fact(new_fact, rule.name)
                        result.add_step(f"Applied rule '{rule.name}' to derive: {new_fact}")
                        new_facts_derived = True
            
            if not new_facts_derived:
                break
        
        result.confidence = min(1.0, len(result.derived_facts) / max(1, len(self.rules)))
        result.explanation = f"Forward chaining completed in {iteration} iterations"
        
        self.reasoning_history.append(result)
        return result
    
    def backward_chaining(self, goal_fact: Fact, depth: int = 0, max_depth: int = 10) -> ReasoningResult:
        """
        Perform backward chaining to prove a goal.
        
        Args:
            goal_fact: The fact to prove
            depth: Current recursion depth
            max_depth: Maximum recursion depth
            
        Returns:
            ReasoningResult indicating if goal was proven
        """
        result = ReasoningResult(success=False)
        
        if depth > max_depth:
            result.add_step(f"Maximum depth {max_depth} reached")
            return result
        
        # Check if goal already exists in facts
        existing_facts = self.query_fact(goal_fact)
        if existing_facts:
            result.success = True
            result.confidence = max(fact.confidence for fact in existing_facts)
            result.add_step(f"Goal fact already exists: {goal_fact}")
            return result
        
        # Try to prove goal using rules
        for rule in self.rules.values():
            if rule.conclusion.matches(goal_fact):
                # Try to prove all conditions
                all_conditions_proven = True
                subresults = []
                
                for condition in rule.conditions:
                    subresult = self.backward_chaining(condition, depth + 1, max_depth)
                    subresults.append(subresult)
                    
                    if not subresult.success:
                        all_conditions_proven = False
                        break
                
                if all_conditions_proven:
                    result.success = True
                    result.confidence = min(subresult.confidence for subresult in subresults) * rule.confidence
                    result.add_step(f"Proved goal using rule '{rule.name}'")
                    
                    # Combine all reasoning steps
                    for subresult in subresults:
                        result.reasoning_steps.extend(subresult.reasoning_steps)
                        result.derived_facts.extend(subresult.derived_facts)
                    
                    break
        
        if not result.success:
            result.add_step(f"Could not prove goal: {goal_fact}")
        
        return result
    
    def explain_reasoning(self, fact: Fact) -> str:
        """Generate explanation for how a fact was derived."""
        explanation = [f"Explaining derivation of: {fact}"]
        
        # Find rules that could have derived this fact
        applicable_rules = []
        for rule in self.rules.values():
            if rule.conclusion.predicate == fact.predicate:
                applicable_rules.append(rule)
        
        if applicable_rules:
            explanation.append("Possible derivation rules:")
            for rule in applicable_rules:
                explanation.append(f"  - {rule.name}: {rule.description}")
        else:
            explanation.append("No rules found that could derive this fact.")
        
        return "\n".join(explanation)
    
    def get_knowledge_summary(self) -> Dict[str, Any]:
        """Get summary of current knowledge state."""
        predicates = defaultdict(int)
        for fact in self.facts.values():
            predicates[fact.predicate] += 1
        
        return {
            "total_facts": len(self.facts),
            "total_rules": len(self.rules),
            "predicates": dict(predicates),
            "reasoning_operations": len(self.reasoning_history)
        }


class InferenceEngine:
    """High-level inference engine for goal-directed reasoning."""
    
    def __init__(self, depth_limit: int = 10):
        """
        Initialize inference engine.
        
        Args:
            depth_limit: Maximum reasoning depth
        """
        self.reasoner = SymbolicReasoner()
        self.depth_limit = depth_limit
        self.planning_strategies = ["forward", "backward", "mixed"]
        
    def infer(self, goal: Goal, facts: List[Fact]) -> ReasoningResult:
        """
        Perform inference to achieve a goal.
        
        Args:
            goal: The goal to achieve
            facts: Current facts to reason with
            
        Returns:
            ReasoningResult with recommendations
        """
        # Add facts to reasoner
        for fact in facts:
            self.reasoner.add_fact(fact)
        
        result = ReasoningResult(success=False)
        
        # Try to achieve each target fact in the goal
        for target_fact in goal.target_facts:
            # First try backward chaining to see if we can prove the goal
            proof_result = self.reasoner.backward_chaining(target_fact, max_depth=self.depth_limit)
            
            if proof_result.success:
                result.success = True
                result.derived_facts.extend(proof_result.derived_facts)
                result.reasoning_steps.extend(proof_result.reasoning_steps)
                result.confidence = max(result.confidence, proof_result.confidence)
            else:
                # If we can't prove it directly, try forward chaining to see what we can derive
                forward_result = self.reasoner.forward_chaining(max_iterations=50)
                result.derived_facts.extend(forward_result.derived_facts)
                result.reasoning_steps.extend(forward_result.reasoning_steps)
        
        # Generate recommended actions based on reasoning
        result.recommended_actions = self._generate_actions(goal, result.derived_facts)
        
        if result.recommended_actions:
            result.success = True
            result.add_step(f"Generated {len(result.recommended_actions)} recommended actions")
        
        result.explanation = self._generate_explanation(goal, result)
        
        return result
    
    def _generate_actions(self, goal: Goal, derived_facts: List[Fact]) -> List['Action']:
        """Generate actions based on reasoning results."""
        from .environment import Action  # Import here to avoid circular dependency
        
        actions = []
        
        # Look for "should_do" facts generated by reasoning
        for fact in derived_facts:
            if fact.predicate == "should_do" and len(fact.arguments) >= 2:
                action = Action(
                    name=fact.arguments[1],
                    description=f"Action recommended for goal: {goal.description}",
                    priority=goal.priority * fact.confidence,
                    metadata={"goal_id": goal.id, "reasoning_confidence": fact.confidence}
                )
                actions.append(action)
        
        # If no specific actions derived, generate generic exploration actions
        if not actions and goal.target_facts:
            for target_fact in goal.target_facts:
                action = Action(
                    name=f"explore_{target_fact.predicate}",
                    description=f"Explore to achieve: {target_fact}",
                    priority=goal.priority * 0.5,
                    metadata={"goal_id": goal.id, "target_fact": str(target_fact)}
                )
                actions.append(action)
        
        return actions
    
    def _generate_explanation(self, goal: Goal, result: ReasoningResult) -> str:
        """Generate human-readable explanation of reasoning."""
        explanation = [f"Reasoning for goal: {goal.description}"]
        
        if result.success:
            explanation.append(f"Successfully generated {len(result.recommended_actions)} actions")
        else:
            explanation.append("Could not find direct path to goal achievement")
        
        if result.reasoning_steps:
            explanation.append("Reasoning steps:")
            for step in result.reasoning_steps[-5:]:  # Show last 5 steps
                explanation.append(f"  - {step}")
        
        if result.derived_facts:
            explanation.append(f"Derived {len(result.derived_facts)} new facts")
        
        return "\n".join(explanation)
    
    def add_domain_knowledge(self, domain: str) -> None:
        """Add domain-specific knowledge and rules."""
        if domain == "navigation":
            self._add_navigation_rules()
        elif domain == "problem_solving":
            self._add_problem_solving_rules()
        elif domain == "learning":
            self._add_learning_rules()
    
    def _add_navigation_rules(self) -> None:
        """Add navigation-specific rules."""
        # Rule: If you want to go somewhere and there's a path, follow it
        nav_rule = Rule(
            conditions=[
                Fact("wants_to_go", ["?agent", "?destination"]),
                Fact("path_exists", ["?current", "?destination"])
            ],
            conclusion=Fact("should_do", ["?agent", "follow_path"]),
            confidence=0.9,
            name="navigation",
            description="Follow path to reach destination"
        )
        self.reasoner.add_rule(nav_rule)
    
    def _add_problem_solving_rules(self) -> None:
        """Add problem-solving rules."""
        # Rule: If you have a problem and know a solution method, apply it
        solve_rule = Rule(
            conditions=[
                Fact("has_problem", ["?agent", "?problem"]),
                Fact("solution_method", ["?method", "?problem"])
            ],
            conclusion=Fact("should_do", ["?agent", "?method"]),
            confidence=0.8,
            name="problem_solving",
            description="Apply known solution methods to problems"
        )
        self.reasoner.add_rule(solve_rule)
    
    def _add_learning_rules(self) -> None:
        """Add learning-specific rules."""
        # Rule: If you encounter an unknown situation, explore it
        learn_rule = Rule(
            conditions=[
                Fact("unknown_situation", ["?agent", "?situation"]),
                Fact("can_explore", ["?agent", "?situation"])
            ],
            conclusion=Fact("should_do", ["?agent", "explore"]),
            confidence=0.7,
            name="learning",
            description="Explore unknown situations to learn"
        )
        self.reasoner.add_rule(learn_rule)
