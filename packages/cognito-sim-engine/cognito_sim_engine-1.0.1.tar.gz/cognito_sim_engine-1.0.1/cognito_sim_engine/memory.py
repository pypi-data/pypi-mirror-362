"""
Memory System - Advanced memory modeling for cognitive architectures.

This module implements working memory, episodic memory, and long-term memory systems
with realistic cognitive constraints and memory dynamics.
"""

import time
import uuid
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import heapq
import json
from collections import defaultdict, deque
import numpy as np


class MemoryType(Enum):
    """Types of memory in the cognitive system."""
    WORKING = "working"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    LONG_TERM = "long_term"


class MemoryStatus(Enum):
    """Status of memory items."""
    ACTIVE = "active"
    DORMANT = "dormant"
    DECAYED = "decayed"
    CONSOLIDATED = "consolidated"


@dataclass
class MemoryItem:
    """Individual memory item with cognitive properties."""
    content: str
    memory_type: MemoryType
    importance: float = 0.5  # 0.0 to 1.0
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    activation_level: float = 1.0
    status: MemoryStatus = MemoryStatus.ACTIVE
    tags: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Associations with other memories
    associations: Dict[str, float] = field(default_factory=dict)  # memory_id -> strength
    
    def access(self) -> None:
        """Record memory access and update activation."""
        self.last_accessed = time.time()
        self.access_count += 1
        self.activation_level = min(1.0, self.activation_level + 0.1)
    
    def decay(self, decay_rate: float, current_time: Optional[float] = None) -> None:
        """Apply time-based decay to the memory."""
        if current_time is None:
            current_time = time.time()
        
        time_since_access = current_time - self.last_accessed
        decay_factor = np.exp(-decay_rate * time_since_access)
        self.activation_level *= decay_factor
        
        # Update status based on activation level
        if self.activation_level < 0.1:
            self.status = MemoryStatus.DECAYED
        elif self.activation_level < 0.3:
            self.status = MemoryStatus.DORMANT
    
    def strengthen_association(self, other_memory_id: str, strength: float = 0.1) -> None:
        """Strengthen association with another memory."""
        current_strength = self.associations.get(other_memory_id, 0.0)
        self.associations[other_memory_id] = min(1.0, current_strength + strength)
    
    def get_effective_importance(self) -> float:
        """Calculate effective importance considering recency and frequency."""
        recency_factor = 1.0 / (1.0 + (time.time() - self.last_accessed) / 3600)  # Hour-based
        frequency_factor = min(1.0, self.access_count / 10.0)
        return self.importance * 0.5 + recency_factor * 0.3 + frequency_factor * 0.2
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert memory item to dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "memory_type": self.memory_type.value,
            "importance": self.importance,
            "created_at": self.created_at,
            "last_accessed": self.last_accessed,
            "access_count": self.access_count,
            "activation_level": self.activation_level,
            "status": self.status.value,
            "tags": list(self.tags),
            "metadata": self.metadata,
            "associations": self.associations
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryItem':
        """Create memory item from dictionary."""
        item = cls(
            content=data["content"],
            memory_type=MemoryType(data["memory_type"]),
            importance=data.get("importance", 0.5),
            created_at=data.get("created_at", time.time()),
            last_accessed=data.get("last_accessed", time.time()),
            access_count=data.get("access_count", 0),
            activation_level=data.get("activation_level", 1.0),
            status=MemoryStatus(data.get("status", "active")),
            tags=set(data.get("tags", [])),
            metadata=data.get("metadata", {}),
            id=data.get("id", str(uuid.uuid4()))
        )
        item.associations = data.get("associations", {})
        return item


class WorkingMemory:
    """Working memory with limited capacity and rapid decay."""
    
    def __init__(self, capacity: int = 7, decay_rate: float = 0.1):
        """
        Initialize working memory.
        
        Args:
            capacity: Maximum number of items (Miller's 7±2)
            decay_rate: Rate of activation decay
        """
        self.capacity = capacity
        self.decay_rate = decay_rate
        self.items: List[MemoryItem] = []
        self._last_update = time.time()
    
    def add_item(self, item: MemoryItem) -> bool:
        """
        Add item to working memory.
        
        Returns:
            True if item was added, False if capacity exceeded
        """
        # Update existing items first
        self.update()
        
        # Check if item already exists
        for existing in self.items:
            if existing.content == item.content:
                existing.access()
                return True
        
        # If at capacity, remove least important item
        if len(self.items) >= self.capacity:
            if not self._make_space():
                return False
        
        item.memory_type = MemoryType.WORKING
        self.items.append(item)
        return True
    
    def _make_space(self) -> bool:
        """Remove least important item to make space."""
        if not self.items:
            return True
        
        # Find item with lowest effective importance
        least_important = min(self.items, key=lambda x: x.get_effective_importance())
        self.items.remove(least_important)
        return True
    
    def get_items(self, active_only: bool = True) -> List[MemoryItem]:
        """Get current working memory items."""
        self.update()
        if active_only:
            return [item for item in self.items if item.status == MemoryStatus.ACTIVE]
        return self.items.copy()
    
    def update(self) -> None:
        """Update working memory, applying decay."""
        current_time = time.time()
        
        # Apply decay to all items
        for item in self.items:
            item.decay(self.decay_rate, current_time)
        
        # Remove decayed items
        self.items = [item for item in self.items if item.activation_level > 0.05]
        
        self._last_update = current_time
    
    def clear(self) -> None:
        """Clear all items from working memory."""
        self.items.clear()
    
    def get_capacity_usage(self) -> float:
        """Get current capacity usage (0.0 to 1.0)."""
        return len(self.items) / self.capacity


class EpisodicMemory:
    """Episodic memory for storing experiences and events."""
    
    def __init__(self, max_size: int = 10000):
        """
        Initialize episodic memory.
        
        Args:
            max_size: Maximum number of episodes to store
        """
        self.max_size = max_size
        self.episodes: deque = deque(maxlen=max_size)
        self.episode_index: Dict[str, MemoryItem] = {}
        self.temporal_clusters: Dict[str, List[str]] = defaultdict(list)  # time_bucket -> memory_ids
    
    def add_episode(self, item: MemoryItem) -> None:
        """Add an episodic memory."""
        item.memory_type = MemoryType.EPISODIC
        
        # Remove oldest if at capacity
        if len(self.episodes) >= self.max_size:
            oldest = self.episodes[0]
            if oldest.id in self.episode_index:
                del self.episode_index[oldest.id]
        
        self.episodes.append(item)
        self.episode_index[item.id] = item
        
        # Add to temporal cluster (hour-based)
        time_bucket = str(int(item.created_at // 3600))
        self.temporal_clusters[time_bucket].append(item.id)
    
    def retrieve_recent(self, limit: int = 10) -> List[MemoryItem]:
        """Retrieve most recent episodes."""
        recent_episodes = list(self.episodes)[-limit:]
        return recent_episodes
    
    def retrieve_by_timeframe(self, start_time: float, end_time: float) -> List[MemoryItem]:
        """Retrieve episodes within a time frame."""
        return [
            episode for episode in self.episodes
            if start_time <= episode.created_at <= end_time
        ]
    
    def search_episodes(self, query: str, limit: int = 10) -> List[MemoryItem]:
        """Search episodes by content."""
        query_lower = query.lower()
        matches = []
        
        for episode in self.episodes:
            if query_lower in episode.content.lower():
                matches.append(episode)
                if len(matches) >= limit:
                    break
        
        return matches
    
    def get_associated_episodes(self, memory_id: str, limit: int = 5) -> List[MemoryItem]:
        """Get episodes associated with a specific memory."""
        if memory_id not in self.episode_index:
            return []
        
        memory = self.episode_index[memory_id]
        associated = []
        
        for assoc_id, strength in memory.associations.items():
            if assoc_id in self.episode_index and strength > 0.3:
                associated.append((self.episode_index[assoc_id], strength))
        
        # Sort by association strength
        associated.sort(key=lambda x: x[1], reverse=True)
        return [item for item, _ in associated[:limit]]


class LongTermMemory:
    """Long-term memory for consolidated knowledge."""
    
    def __init__(self):
        """Initialize long-term memory."""
        self.semantic_memory: Dict[str, MemoryItem] = {}
        self.procedural_memory: Dict[str, MemoryItem] = {}
        self.knowledge_graph: Dict[str, Set[str]] = defaultdict(set)  # concept -> related_concepts
        self.concept_strengths: Dict[str, float] = defaultdict(float)
    
    def consolidate_memory(self, item: MemoryItem) -> None:
        """Consolidate memory from working/episodic to long-term."""
        if item.memory_type == MemoryType.EPISODIC:
            # Extract semantic content from episodic memory
            semantic_item = MemoryItem(
                content=f"Knowledge: {item.content}",
                memory_type=MemoryType.SEMANTIC,
                importance=item.importance,
                created_at=item.created_at,
                metadata=item.metadata.copy()
            )
            self.semantic_memory[semantic_item.id] = semantic_item
        else:
            item.memory_type = MemoryType.LONG_TERM
            item.status = MemoryStatus.CONSOLIDATED
            self.semantic_memory[item.id] = item
        
        # Update concept strengths
        for tag in item.tags:
            self.concept_strengths[tag] += item.importance
    
    def retrieve_semantic(self, concept: str) -> List[MemoryItem]:
        """Retrieve semantic memories related to a concept."""
        matches = []
        concept_lower = concept.lower()
        
        for memory in self.semantic_memory.values():
            if (concept_lower in memory.content.lower() or 
                concept_lower in memory.tags):
                matches.append(memory)
        
        # Sort by relevance (importance * activation)
        matches.sort(key=lambda x: x.importance * x.activation_level, reverse=True)
        return matches
    
    def add_knowledge(self, concept: str, description: str, importance: float = 0.7) -> MemoryItem:
        """Add explicit knowledge to semantic memory."""
        item = MemoryItem(
            content=description,
            memory_type=MemoryType.SEMANTIC,
            importance=importance,
            tags={concept}
        )
        self.semantic_memory[item.id] = item
        self.concept_strengths[concept] += importance
        return item
    
    def link_concepts(self, concept1: str, concept2: str, strength: float = 0.5) -> None:
        """Create bidirectional link between concepts."""
        self.knowledge_graph[concept1].add(concept2)
        self.knowledge_graph[concept2].add(concept1)
        
        # Update concept strengths
        self.concept_strengths[concept1] += strength * 0.1
        self.concept_strengths[concept2] += strength * 0.1
    
    def get_related_concepts(self, concept: str, depth: int = 2) -> Set[str]:
        """Get concepts related to the given concept."""
        if depth <= 0:
            return set()
        
        related = set()
        direct_relations = self.knowledge_graph.get(concept, set())
        related.update(direct_relations)
        
        if depth > 1:
            for related_concept in direct_relations:
                related.update(self.get_related_concepts(related_concept, depth - 1))
        
        return related


class MemoryManager:
    """Central manager for all memory systems."""
    
    def __init__(
        self,
        working_capacity: int = 7,
        episodic_capacity: int = 10000,
        decay_rate: float = 0.01
    ):
        """
        Initialize memory manager.
        
        Args:
            working_capacity: Working memory capacity
            episodic_capacity: Episodic memory capacity
            decay_rate: Global decay rate
        """
        self.working_memory = WorkingMemory(working_capacity, decay_rate)
        self.episodic_memory = EpisodicMemory(episodic_capacity)
        self.long_term_memory = LongTermMemory()
        
        self.consolidation_threshold = 5  # Access count for consolidation
        self.consolidation_interval = 100  # Update cycles between consolidation
        self._update_counter = 0
    
    def store_memory(self, item: MemoryItem) -> str:
        """
        Store memory in appropriate system.
        
        Returns:
            Memory ID
        """
        if item.memory_type == MemoryType.WORKING:
            self.working_memory.add_item(item)
        elif item.memory_type == MemoryType.EPISODIC:
            self.episodic_memory.add_episode(item)
        elif item.memory_type in [MemoryType.SEMANTIC, MemoryType.LONG_TERM]:
            self.long_term_memory.consolidate_memory(item)
        
        return item.id
    
    def retrieve_memory(self, memory_id: str) -> Optional[MemoryItem]:
        """Retrieve memory by ID from any system."""
        # Check working memory
        for item in self.working_memory.items:
            if item.id == memory_id:
                item.access()
                return item
        
        # Check episodic memory
        if memory_id in self.episodic_memory.episode_index:
            item = self.episodic_memory.episode_index[memory_id]
            item.access()
            return item
        
        # Check long-term memory
        if memory_id in self.long_term_memory.semantic_memory:
            item = self.long_term_memory.semantic_memory[memory_id]
            item.access()
            return item
        
        return None
    
    def search_memories(
        self,
        query: str,
        memory_types: Optional[List[MemoryType]] = None,
        limit: int = 10
    ) -> List[MemoryItem]:
        """Search across all memory systems."""
        if memory_types is None:
            memory_types = list(MemoryType)
        
        results = []
        
        # Search working memory
        if MemoryType.WORKING in memory_types:
            for item in self.working_memory.get_items():
                if query.lower() in item.content.lower():
                    results.append(item)
        
        # Search episodic memory
        if MemoryType.EPISODIC in memory_types:
            episodic_results = self.episodic_memory.search_episodes(query, limit)
            results.extend(episodic_results)
        
        # Search long-term memory
        if MemoryType.SEMANTIC in memory_types or MemoryType.LONG_TERM in memory_types:
            semantic_results = self.long_term_memory.retrieve_semantic(query)
            results.extend(semantic_results[:limit])
        
        # Sort by relevance and limit results
        results.sort(key=lambda x: x.get_effective_importance(), reverse=True)
        return results[:limit]
    
    def get_working_memory(self) -> List[MemoryItem]:
        """Get current working memory contents."""
        return self.working_memory.get_items()
    
    def update_working_memory(self) -> None:
        """Update working memory (apply decay, etc.)."""
        self.working_memory.update()
        self._update_counter += 1
        
        # Periodic consolidation
        if self._update_counter % self.consolidation_interval == 0:
            self._consolidate_memories()
    
    def _consolidate_memories(self) -> None:
        """Consolidate frequently accessed memories to long-term storage."""
        # Find episodic memories that should be consolidated
        candidates = []
        for episode in self.episodic_memory.episodes:
            if (episode.access_count >= self.consolidation_threshold and
                episode.importance > 0.5):
                candidates.append(episode)
        
        # Consolidate top candidates
        for memory in candidates[:5]:  # Limit consolidation per cycle
            self.long_term_memory.consolidate_memory(memory)
    
    def create_memory_association(
        self,
        memory_id1: str,
        memory_id2: str,
        strength: float = 0.3
    ) -> bool:
        """Create association between two memories."""
        memory1 = self.retrieve_memory(memory_id1)
        memory2 = self.retrieve_memory(memory_id2)
        
        if memory1 and memory2:
            memory1.strengthen_association(memory_id2, strength)
            memory2.strengthen_association(memory_id1, strength)
            return True
        
        return False
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics."""
        return {
            "working_memory": {
                "items": len(self.working_memory.items),
                "capacity": self.working_memory.capacity,
                "usage": self.working_memory.get_capacity_usage()
            },
            "episodic_memory": {
                "episodes": len(self.episodic_memory.episodes),
                "capacity": self.episodic_memory.max_size
            },
            "long_term_memory": {
                "semantic_items": len(self.long_term_memory.semantic_memory),
                "concepts": len(self.long_term_memory.concept_strengths),
                "knowledge_links": sum(len(links) for links in self.long_term_memory.knowledge_graph.values())
            },
            "total_memories": (
                len(self.working_memory.items) +
                len(self.episodic_memory.episodes) +
                len(self.long_term_memory.semantic_memory)
            )
        }
    
    def export_memories(self) -> Dict[str, Any]:
        """Export all memories for persistence."""
        return {
            "working_memory": [item.to_dict() for item in self.working_memory.items],
            "episodic_memory": [item.to_dict() for item in self.episodic_memory.episodes],
            "semantic_memory": [item.to_dict() for item in self.long_term_memory.semantic_memory.values()],
            "concept_strengths": dict(self.long_term_memory.concept_strengths),
            "knowledge_graph": {k: list(v) for k, v in self.long_term_memory.knowledge_graph.items()}
        }
    
    def import_memories(self, data: Dict[str, Any]) -> None:
        """Import memories from exported data."""
        # Clear existing memories
        self.working_memory.clear()
        self.episodic_memory.episodes.clear()
        self.episodic_memory.episode_index.clear()
        self.long_term_memory.semantic_memory.clear()
        
        # Import working memory
        for item_data in data.get("working_memory", []):
            item = MemoryItem.from_dict(item_data)
            self.working_memory.add_item(item)
        
        # Import episodic memory
        for item_data in data.get("episodic_memory", []):
            item = MemoryItem.from_dict(item_data)
            self.episodic_memory.add_episode(item)
        
        # Import semantic memory
        for item_data in data.get("semantic_memory", []):
            item = MemoryItem.from_dict(item_data)
            self.long_term_memory.semantic_memory[item.id] = item
        
        # Import concept strengths and knowledge graph
        self.long_term_memory.concept_strengths.update(data.get("concept_strengths", {}))
        knowledge_graph_data = data.get("knowledge_graph", {})
        for concept, links in knowledge_graph_data.items():
            self.long_term_memory.knowledge_graph[concept] = set(links)
