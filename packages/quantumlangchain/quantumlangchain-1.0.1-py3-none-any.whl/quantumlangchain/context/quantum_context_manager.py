"""
Quantum-enhanced context management with temporal snapshots and coherent state tracking.
"""

import asyncio
import uuid
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import copy

from quantumlangchain.core.base import QuantumBase, QuantumState


class ContextScope(Enum):
    """Context scope levels."""
    GLOBAL = "global"
    SESSION = "session"
    CONVERSATION = "conversation"
    TURN = "turn"
    QUANTUM_STATE = "quantum_state"


@dataclass
class ContextSnapshot:
    """Snapshot of context state at a specific point in time."""
    snapshot_id: str
    timestamp: datetime
    scope: ContextScope
    context_data: Dict[str, Any]
    quantum_state: QuantumState
    decoherence_level: float
    entanglement_registry: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert snapshot to dictionary."""
        return {
            "snapshot_id": self.snapshot_id,
            "timestamp": self.timestamp.isoformat(),
            "scope": self.scope.value,
            "context_data": self.context_data,
            "quantum_state": self.quantum_state.value,
            "decoherence_level": self.decoherence_level,
            "entanglement_registry": self.entanglement_registry,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextSnapshot':
        """Create snapshot from dictionary."""
        return cls(
            snapshot_id=data["snapshot_id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            scope=ContextScope(data["scope"]),
            context_data=data["context_data"],
            quantum_state=QuantumState(data["quantum_state"]),
            decoherence_level=data["decoherence_level"],
            entanglement_registry=data.get("entanglement_registry", {}),
            metadata=data.get("metadata", {})
        )


@dataclass
class ContextWindow:
    """Sliding context window with quantum coherence tracking."""
    window_id: str
    max_size: int
    current_size: int = 0
    items: List[Dict[str, Any]] = field(default_factory=list)
    coherence_threshold: float = 0.8
    last_access: datetime = field(default_factory=datetime.now)
    
    def add_item(self, item: Dict[str, Any]):
        """Add item to context window."""
        self.items.append({
            **item,
            "timestamp": datetime.now(),
            "window_position": len(self.items)
        })
        
        # Maintain window size
        if len(self.items) > self.max_size:
            self.items.pop(0)
            # Update positions
            for i, item in enumerate(self.items):
                item["window_position"] = i
        
        self.current_size = len(self.items)
        self.last_access = datetime.now()
    
    def get_recent_items(self, count: int) -> List[Dict[str, Any]]:
        """Get most recent items from window."""
        self.last_access = datetime.now()
        return self.items[-count:] if count <= len(self.items) else self.items
    
    def search_items(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search items in context window."""
        self.last_access = datetime.now()
        
        # Simple keyword search with relevance scoring
        scored_items = []
        query_words = query.lower().split()
        
        for item in self.items:
            content = str(item.get("content", "")).lower()
            score = sum(1 for word in query_words if word in content)
            
            if score > 0:
                # Add recency bonus
                age_hours = (datetime.now() - item["timestamp"]).total_seconds() / 3600
                recency_bonus = max(0, 1 - age_hours / 24)  # Decay over 24 hours
                
                scored_items.append({
                    **item,
                    "relevance_score": score + recency_bonus * 0.1
                })
        
        # Sort by relevance and return top results
        scored_items.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored_items[:top_k]


class QuantumContextManager(QuantumBase):
    """
    Quantum-enhanced context management system with temporal snapshots,
    coherent state tracking, and entangled context windows.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        
        # Context storage
        self.contexts: Dict[ContextScope, Dict[str, Any]] = {
            scope: {} for scope in ContextScope
        }
        
        # Context windows for different scopes
        self.context_windows: Dict[str, ContextWindow] = {}
        
        # Snapshot management
        self.snapshots: Dict[str, ContextSnapshot] = {}
        self.snapshot_history: List[str] = []
        
        # Entangled contexts
        self.entangled_contexts: Dict[str, List[str]] = {}
        
        # Configuration
        self.max_snapshots = config.get("max_snapshots", 100) if config else 100
        self.auto_snapshot_interval = config.get("auto_snapshot_interval", 300) if config else 300  # 5 minutes
        self.context_decay_hours = config.get("context_decay_hours", 24) if config else 24
        
        # State tracking
        self.last_auto_snapshot: Optional[datetime] = None
        
    async def initialize(self):
        """Initialize the quantum context manager."""
        await super().initialize()
        self.quantum_state = QuantumState.COHERENT
        
        # Create default context windows
        self.create_context_window("global", max_size=1000)
        self.create_context_window("session", max_size=500)
        self.create_context_window("conversation", max_size=200)
        self.create_context_window("turn", max_size=50)
        
        # Start auto-snapshot task
        asyncio.create_task(self._auto_snapshot_task())
        
    async def reset_quantum_state(self):
        """Reset quantum state and clear temporary contexts."""
        self.quantum_state = QuantumState.COHERENT
        self.decoherence_level = 0.0
        
        # Clear turn and conversation contexts
        self.contexts[ContextScope.TURN].clear()
        self.contexts[ContextScope.CONVERSATION].clear()
        
        # Reset context windows
        if "turn" in self.context_windows:
            self.context_windows["turn"].items.clear()
            self.context_windows["turn"].current_size = 0
        
    def create_context_window(
        self,
        window_id: str,
        max_size: int = 100,
        coherence_threshold: float = 0.8
    ) -> ContextWindow:
        """Create a new context window."""
        window = ContextWindow(
            window_id=window_id,
            max_size=max_size,
            coherence_threshold=coherence_threshold
        )
        self.context_windows[window_id] = window
        return window
    
    async def set_context(
        self,
        scope: ContextScope,
        key: str,
        value: Any,
        quantum_enhanced: bool = False,
        window_id: Optional[str] = None
    ):
        """Set context value with optional quantum enhancement."""
        # Store in main context
        self.contexts[scope][key] = {
            "value": value,
            "timestamp": datetime.now(),
            "quantum_enhanced": quantum_enhanced,
            "access_count": 0
        }
        
        # Add to context window if specified
        if window_id and window_id in self.context_windows:
            self.context_windows[window_id].add_item({
                "key": key,
                "content": str(value),
                "scope": scope.value,
                "quantum_enhanced": quantum_enhanced
            })
        
        # Update quantum state
        if quantum_enhanced:
            if self.quantum_state == QuantumState.COHERENT:
                self.quantum_state = QuantumState.SUPERPOSITION
            
            # Small decoherence from interaction
            self.update_decoherence(0.01)
    
    async def get_context(
        self,
        scope: ContextScope,
        key: str,
        default: Any = None,
        quantum_search: bool = False
    ) -> Any:
        """Get context value with optional quantum search."""
        # Direct lookup
        if key in self.contexts[scope]:
            context_item = self.contexts[scope][key]
            context_item["access_count"] += 1
            context_item["last_access"] = datetime.now()
            
            if quantum_search and context_item["quantum_enhanced"]:
                # Apply quantum coherence effects
                coherence_factor = 1 - self.decoherence_level
                self.update_decoherence(0.005)  # Small decoherence from measurement
            
            return context_item["value"]
        
        # Quantum search across related contexts if enabled
        if quantum_search:
            return await self._quantum_context_search(key, scope, default)
        
        return default
    
    async def _quantum_context_search(
        self,
        key: str,
        preferred_scope: ContextScope,
        default: Any
    ) -> Any:
        """Perform quantum-enhanced context search across scopes."""
        candidates = []
        
        # Search all scopes with quantum probability
        for scope in ContextScope:
            if scope == preferred_scope:
                continue
                
            if key in self.contexts[scope]:
                context_item = self.contexts[scope][key]
                
                # Calculate quantum probability based on coherence and recency
                age_hours = (datetime.now() - context_item["timestamp"]).total_seconds() / 3600
                recency_factor = max(0, 1 - age_hours / self.context_decay_hours)
                
                quantum_probability = recency_factor * (1 - self.decoherence_level)
                if context_item["quantum_enhanced"]:
                    quantum_probability *= 1.2  # Boost for quantum-enhanced items
                
                candidates.append({
                    "value": context_item["value"],
                    "scope": scope,
                    "probability": quantum_probability
                })
        
        if candidates:
            # Select candidate with highest quantum probability
            best_candidate = max(candidates, key=lambda x: x["probability"])
            if best_candidate["probability"] > 0.1:  # Minimum threshold
                self.update_decoherence(0.02)  # Decoherence from quantum search
                return best_candidate["value"]
        
        return default
    
    async def create_snapshot(
        self,
        scope: ContextScope = ContextScope.SESSION,
        include_windows: bool = True
    ) -> str:
        """Create a snapshot of current context state."""
        snapshot_id = str(uuid.uuid4())
        
        # Prepare context data
        context_data = {}
        if scope == ContextScope.GLOBAL:
            context_data = copy.deepcopy(self.contexts)
        else:
            context_data[scope.value] = copy.deepcopy(self.contexts[scope])
        
        # Include context windows if requested
        if include_windows:
            context_data["windows"] = {
                window_id: {
                    "items": window.items.copy(),
                    "current_size": window.current_size,
                    "max_size": window.max_size
                }
                for window_id, window in self.context_windows.items()
            }
        
        # Create snapshot
        snapshot = ContextSnapshot(
            snapshot_id=snapshot_id,
            timestamp=datetime.now(),
            scope=scope,
            context_data=context_data,
            quantum_state=self.quantum_state,
            decoherence_level=self.decoherence_level,
            entanglement_registry=copy.deepcopy(self.entanglement_registry),
            metadata={
                "total_contexts": sum(len(contexts) for contexts in self.contexts.values()),
                "active_windows": len(self.context_windows),
                "entangled_contexts": len(self.entangled_contexts)
            }
        )
        
        # Store snapshot
        self.snapshots[snapshot_id] = snapshot
        self.snapshot_history.append(snapshot_id)
        
        # Maintain snapshot limit
        if len(self.snapshots) > self.max_snapshots:
            oldest_id = self.snapshot_history.pop(0)
            del self.snapshots[oldest_id]
        
        return snapshot_id
    
    async def restore_snapshot(self, snapshot_id: str) -> bool:
        """Restore context from a snapshot."""
        if snapshot_id not in self.snapshots:
            return False
        
        snapshot = self.snapshots[snapshot_id]
        
        # Restore context data
        if snapshot.scope == ContextScope.GLOBAL:
            self.contexts = copy.deepcopy(snapshot.context_data)
        else:
            scope_key = snapshot.scope.value
            if scope_key in snapshot.context_data:
                self.contexts[snapshot.scope] = copy.deepcopy(snapshot.context_data[scope_key])
        
        # Restore context windows if present
        if "windows" in snapshot.context_data:
            for window_id, window_data in snapshot.context_data["windows"].items():
                if window_id in self.context_windows:
                    self.context_windows[window_id].items = window_data["items"].copy()
                    self.context_windows[window_id].current_size = window_data["current_size"]
        
        # Restore quantum state
        self.quantum_state = snapshot.quantum_state
        self.decoherence_level = snapshot.decoherence_level
        self.entanglement_registry = copy.deepcopy(snapshot.entanglement_registry)
        
        return True
    
    async def entangle_contexts(
        self,
        context_keys: List[Tuple[ContextScope, str]],
        entanglement_strength: float = 0.8
    ) -> str:
        """Create entanglement between context items."""
        entanglement_id = str(uuid.uuid4())
        
        # Verify all contexts exist
        for scope, key in context_keys:
            if key not in self.contexts[scope]:
                raise KeyError(f"Context '{key}' not found in scope '{scope.value}'")
        
        # Create entanglement
        for scope, key in context_keys:
            context_item = self.contexts[scope][key]
            if "entanglement_ids" not in context_item:
                context_item["entanglement_ids"] = []
            context_item["entanglement_ids"].append(entanglement_id)
        
        # Store entanglement info
        self.entangled_contexts[entanglement_id] = [
            f"{scope.value}:{key}" for scope, key in context_keys
        ]
        
        # Update quantum state
        self.quantum_state = QuantumState.ENTANGLED
        
        return entanglement_id
    
    async def measure_entangled_contexts(self, entanglement_id: str) -> Dict[str, Any]:
        """Measure entangled contexts and collapse their superposition."""
        if entanglement_id not in self.entangled_contexts:
            return {}
        
        context_refs = self.entangled_contexts[entanglement_id]
        measurements = {}
        
        for ref in context_refs:
            scope_str, key = ref.split(":", 1)
            scope = ContextScope(scope_str)
            
            if key in self.contexts[scope]:
                context_item = self.contexts[scope][key]
                measurements[ref] = {
                    "value": context_item["value"],
                    "timestamp": context_item["timestamp"],
                    "access_count": context_item["access_count"],
                    "quantum_enhanced": context_item["quantum_enhanced"]
                }
        
        # Collapse quantum state after measurement
        if self.quantum_state == QuantumState.ENTANGLED:
            self.quantum_state = QuantumState.COLLAPSED
        
        self.update_decoherence(0.1)  # Measurement causes decoherence
        
        return {
            "entanglement_id": entanglement_id,
            "measurements": measurements,
            "measurement_timestamp": datetime.now(),
            "decoherence_level": self.decoherence_level
        }
    
    def search_context_windows(
        self,
        query: str,
        window_ids: Optional[List[str]] = None,
        top_k: int = 10
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Search across context windows."""
        if window_ids is None:
            window_ids = list(self.context_windows.keys())
        
        results = {}
        for window_id in window_ids:
            if window_id in self.context_windows:
                window_results = self.context_windows[window_id].search_items(query, top_k)
                if window_results:
                    results[window_id] = window_results
        
        return results
    
    def get_context_statistics(self) -> Dict[str, Any]:
        """Get comprehensive context statistics."""
        stats = {
            "contexts_by_scope": {
                scope.value: len(contexts)
                for scope, contexts in self.contexts.items()
            },
            "total_contexts": sum(len(contexts) for contexts in self.contexts.values()),
            "quantum_enhanced_contexts": 0,
            "context_windows": {
                window_id: {
                    "current_size": window.current_size,
                    "max_size": window.max_size,
                    "last_access": window.last_access.isoformat()
                }
                for window_id, window in self.context_windows.items()
            },
            "snapshots": {
                "total_snapshots": len(self.snapshots),
                "oldest_snapshot": self.snapshot_history[0] if self.snapshot_history else None,
                "newest_snapshot": self.snapshot_history[-1] if self.snapshot_history else None
            },
            "entangled_contexts": len(self.entangled_contexts),
            "quantum_state": self.quantum_state.value,
            "decoherence_level": self.decoherence_level
        }
        
        # Count quantum-enhanced contexts
        for contexts in self.contexts.values():
            for context_item in contexts.values():
                if context_item.get("quantum_enhanced", False):
                    stats["quantum_enhanced_contexts"] += 1
        
        return stats
    
    async def cleanup_expired_contexts(self):
        """Clean up expired contexts based on decay settings."""
        cutoff_time = datetime.now() - timedelta(hours=self.context_decay_hours)
        cleaned_count = 0
        
        for scope, contexts in self.contexts.items():
            expired_keys = []
            for key, context_item in contexts.items():
                if context_item["timestamp"] < cutoff_time:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del contexts[key]
                cleaned_count += 1
        
        return cleaned_count
    
    async def _auto_snapshot_task(self):
        """Background task for automatic snapshots."""
        while True:
            try:
                await asyncio.sleep(self.auto_snapshot_interval)
                
                # Create automatic snapshot
                snapshot_id = await self.create_snapshot(
                    scope=ContextScope.SESSION,
                    include_windows=True
                )
                
                self.last_auto_snapshot = datetime.now()
                
                # Cleanup expired contexts
                await self.cleanup_expired_contexts()
                
            except Exception as e:
                # Log error but continue running
                continue
