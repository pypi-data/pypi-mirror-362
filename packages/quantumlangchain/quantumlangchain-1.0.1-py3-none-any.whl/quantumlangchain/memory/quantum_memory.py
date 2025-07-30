"""
QuantumMemory: Reversible, entangled memory layers with hybrid vector store support.

🔐 LICENSED COMPONENT - Requires valid QuantumLangChain license
📧 Contact: bajpaikrishna715@gmail.com for licensing
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import asyncio
import logging
import numpy as np
from datetime import datetime
import hashlib
import json
from pydantic import Field

from quantumlangchain.core.base import (
    QuantumBase,
    QuantumMemoryInterface,
    QuantumConfig,
    QuantumState
)
from quantumlangchain.licensing import (
    LicensedComponent,
    requires_license,
    validate_license,
    FeatureNotLicensedError
)

logger = logging.getLogger(__name__)


class QuantumMemoryConfig(QuantumConfig):
    """Configuration for QuantumMemory."""
    
    classical_dim: int = Field(default=512, description="Dimension of classical embeddings")
    quantum_dim: int = Field(default=8, description="Number of quantum memory qubits")
    max_entries: int = Field(default=10000, description="Maximum memory entries")
    entanglement_lifetime: float = Field(default=3600.0, description="Entanglement lifetime in seconds")
    compression_threshold: float = Field(default=0.8, description="Memory compression threshold")
    reversibility_enabled: bool = Field(default=True, description="Enable reversible operations")
    quantum_error_correction: bool = Field(default=True, description="Enable quantum error correction")
    hybrid_storage: bool = Field(default=True, description="Use hybrid classical-quantum storage")


class MemoryEntry:
    """Individual memory entry with quantum enhancement."""
    
    def __init__(
        self,
        key: str,
        value: Any,
        classical_embedding: Optional[np.ndarray] = None,
        quantum_state: Optional[Any] = None,
        timestamp: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.key = key
        self.value = value
        self.classical_embedding = classical_embedding
        self.quantum_state = quantum_state
        self.timestamp = timestamp or datetime.now()
        self.metadata = metadata or {}
        self.access_count = 0
        self.entanglement_links = set()
        self.is_quantum_enhanced = quantum_state is not None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to dictionary representation."""
        return {
            "key": self.key,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "access_count": self.access_count,
            "entanglement_links": list(self.entanglement_links),
            "is_quantum_enhanced": self.is_quantum_enhanced
        }


class QuantumMemory(QuantumBase, QuantumMemoryInterface, LicensedComponent):
    """
    Reversible, entangled memory system with hybrid classical-quantum storage.
    
    🔐 LICENSING: Requires Basic tier or higher license
    Features used: core, quantum_memory
    
    Provides quantum-enhanced memory operations including entanglement between
    memory entries, reversible transformations, and quantum error correction.
    """
    
    config: QuantumMemoryConfig = Field(default_factory=QuantumMemoryConfig)
    memory_store: Dict[str, MemoryEntry] = Field(default_factory=dict)
    entanglement_graph: Dict[str, List[str]] = Field(default_factory=dict)
    snapshots: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    quantum_registers: Dict[str, Any] = Field(default_factory=dict)
    classical_embeddings: Dict[str, np.ndarray] = Field(default_factory=dict)
    
    def __init__(self, **data):
        # Initialize licensing first
        LicensedComponent.__init__(
            self,
            required_features=["core", "quantum_memory"],
            required_tier="basic",
            package="quantumlangchain"
        )
        
        super().__init__(**data)
        self.backend = data.get('backend')
    
    async def initialize(self) -> None:
        """Initialize the quantum memory system."""
        
        # Initialize quantum registers
        await self._initialize_quantum_registers()
        
        # Setup error correction if enabled
        if self.config.quantum_error_correction:
            await self._setup_error_correction()
        
        self.quantum_state = QuantumState.COHERENT
        self.logger.info("QuantumMemory initialized successfully")
    
    async def reset_quantum_state(self) -> None:
        """Reset quantum memory to initial state."""
        
        # Clear all memory
        self.memory_store.clear()
        self.entanglement_graph.clear()
        self.snapshots.clear()
        self.quantum_registers.clear()
        self.classical_embeddings.clear()
        
        # Reset quantum state
        self.quantum_state = QuantumState.COHERENT
        self.decoherence_level = 0.0
        
        # Reinitialize
        await self.initialize()
        
        self.logger.info("QuantumMemory state reset")
    
    async def _initialize_quantum_registers(self) -> None:
        """Initialize quantum registers for memory operations."""
        
        try:
            # Create quantum register for each memory qubit
            for i in range(self.config.quantum_dim):
                register_name = f"qreg_{i}"
                # Initialize in |0⟩ state (simulated)
                self.quantum_registers[register_name] = {
                    "state": [1.0, 0.0],  # |0⟩ state amplitudes
                    "entangled_with": [],
                    "last_operation": "initialize",
                    "creation_time": datetime.now().isoformat()
                }
            
            self.logger.debug(f"Initialized {self.config.quantum_dim} quantum registers")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize quantum registers: {e}")
    
    async def _setup_error_correction(self) -> None:
        """Setup quantum error correction protocols."""
        
        # Implement basic error correction simulation
        self.error_correction_codes = {
            "bit_flip": {"syndrome_qubits": 2, "data_qubits": 1},
            "phase_flip": {"syndrome_qubits": 2, "data_qubits": 1},
            "shor_code": {"syndrome_qubits": 8, "data_qubits": 1}
        }
        
        self.logger.debug("Error correction protocols initialized")
    
    async def store(self, key: str, value: Any, quantum_enhanced: bool = True) -> None:
        """Store data with optional quantum enhancement.
        
        Args:
            key: Unique identifier for the memory entry
            value: Data to store
            quantum_enhanced: Whether to apply quantum enhancement
        """
        
        try:
            # Generate classical embedding
            classical_embedding = await self._generate_classical_embedding(value)
            
            # Generate quantum state if enhanced
            quantum_state = None
            if quantum_enhanced and self.quantum_state != QuantumState.DECOHERENT:
                quantum_state = await self._generate_quantum_state(value, key)
            
            # Create memory entry
            entry = MemoryEntry(
                key=key,
                value=value,
                classical_embedding=classical_embedding,
                quantum_state=quantum_state,
                metadata={
                    "storage_time": datetime.now().isoformat(),
                    "quantum_enhanced": quantum_enhanced,
                    "decoherence_level": self.decoherence_level
                }
            )
            
            # Store entry
            self.memory_store[key] = entry
            self.classical_embeddings[key] = classical_embedding
            
            # Update entanglement graph
            if key not in self.entanglement_graph:
                self.entanglement_graph[key] = []
            
            # Apply compression if threshold reached
            if len(self.memory_store) > self.config.max_entries * self.config.compression_threshold:
                await self._compress_memory()
            
            self.logger.debug(f"Stored entry: {key} (quantum_enhanced={quantum_enhanced})")
            
        except Exception as e:
            self.logger.error(f"Failed to store entry {key}: {e}")
            raise
    
    async def retrieve(self, key: str, quantum_search: bool = True) -> Any:
        """Retrieve data with optional quantum search.
        
        Args:
            key: Key to retrieve
            quantum_search: Whether to use quantum-enhanced search
            
        Returns:
            Retrieved data or None if not found
        """
        
        try:
            # Direct lookup first
            if key in self.memory_store:
                entry = self.memory_store[key]
                entry.access_count += 1
                
                # Apply quantum decoherence
                if entry.is_quantum_enhanced:
                    await self._apply_access_decoherence(entry)
                
                return entry.value
            
            # Quantum search if enabled
            if quantum_search and self.quantum_state != QuantumState.DECOHERENT:
                found_key = await self._quantum_similarity_search(key)
                if found_key and found_key in self.memory_store:
                    entry = self.memory_store[found_key]
                    entry.access_count += 1
                    return entry.value
            
            # Classical similarity search fallback
            similar_key = await self._classical_similarity_search(key)
            if similar_key and similar_key in self.memory_store:
                entry = self.memory_store[similar_key]
                entry.access_count += 1
                return entry.value
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve entry {key}: {e}")
            return None
    
    async def entangle_memories(self, keys: List[str]) -> str:
        """Create entanglement between memory entries.
        
        Args:
            keys: List of memory keys to entangle
            
        Returns:
            Entanglement ID
        """
        
        try:
            # Validate keys exist
            valid_keys = [key for key in keys if key in self.memory_store]
            if len(valid_keys) < 2:
                raise ValueError("Need at least 2 valid keys for entanglement")
            
            # Generate entanglement ID
            entanglement_id = f"entangle_{hash('_'.join(valid_keys)) % 1000000}"
            
            # Create quantum entanglement between entries
            await self._create_quantum_entanglement(valid_keys, entanglement_id)
            
            # Update entanglement graph
            for key in valid_keys:
                if key not in self.entanglement_graph:
                    self.entanglement_graph[key] = []
                
                # Add all other keys as entangled
                for other_key in valid_keys:
                    if other_key != key and other_key not in self.entanglement_graph[key]:
                        self.entanglement_graph[key].append(other_key)
                
                # Update memory entry
                if key in self.memory_store:
                    self.memory_store[key].entanglement_links.add(entanglement_id)
            
            self.quantum_state = QuantumState.ENTANGLED
            
            self.logger.info(f"Created entanglement {entanglement_id} between {len(valid_keys)} memories")
            return entanglement_id
            
        except Exception as e:
            self.logger.error(f"Failed to create entanglement: {e}")
            raise
    
    async def _create_quantum_entanglement(self, keys: List[str], entanglement_id: str) -> None:
        """Create quantum entanglement between memory entries."""
        
        # Simulate quantum entanglement by creating Bell states
        for i in range(0, len(keys) - 1, 2):
            if i + 1 < len(keys):
                key1, key2 = keys[i], keys[i + 1]
                
                # Create Bell state representation
                if key1 in self.memory_store and key2 in self.memory_store:
                    # Simulated entangled state
                    entangled_state = {
                        "type": "bell_state",
                        "qubits": [key1, key2],
                        "amplitudes": [0.7071, 0.0, 0.0, 0.7071],  # |00⟩ + |11⟩
                        "entanglement_id": entanglement_id,
                        "creation_time": datetime.now().isoformat()
                    }
                    
                    # Update quantum states
                    self.memory_store[key1].quantum_state = entangled_state
                    self.memory_store[key2].quantum_state = entangled_state
    
    async def create_memory_snapshot(self) -> str:
        """Create a snapshot of current memory state.
        
        Returns:
            Snapshot ID
        """
        
        try:
            snapshot_id = f"snapshot_{datetime.now().isoformat()}_{len(self.snapshots)}"
            
            # Create snapshot data
            snapshot_data = {
                "memory_store": {
                    key: entry.to_dict() for key, entry in self.memory_store.items()
                },
                "entanglement_graph": self.entanglement_graph.copy(),
                "quantum_state": self.quantum_state.value,
                "decoherence_level": self.decoherence_level,
                "quantum_registers": self.quantum_registers.copy(),
                "creation_time": datetime.now().isoformat(),
                "entry_count": len(self.memory_store)
            }
            
            # Store snapshot
            self.snapshots[snapshot_id] = snapshot_data
            
            self.logger.info(f"Created memory snapshot: {snapshot_id}")
            return snapshot_id
            
        except Exception as e:
            self.logger.error(f"Failed to create snapshot: {e}")
            raise
    
    async def restore_memory_snapshot(self, snapshot_id: str) -> None:
        """Restore memory from a snapshot.
        
        Args:
            snapshot_id: ID of the snapshot to restore
        """
        
        try:
            if snapshot_id not in self.snapshots:
                raise ValueError(f"Snapshot {snapshot_id} not found")
            
            snapshot_data = self.snapshots[snapshot_id]
            
            # Clear current state
            self.memory_store.clear()
            self.entanglement_graph.clear()
            self.quantum_registers.clear()
            self.classical_embeddings.clear()
            
            # Restore memory entries
            for key, entry_dict in snapshot_data["memory_store"].items():
                entry = MemoryEntry(
                    key=entry_dict["key"],
                    value=entry_dict["value"],
                    timestamp=datetime.fromisoformat(entry_dict["timestamp"]),
                    metadata=entry_dict["metadata"]
                )
                entry.access_count = entry_dict["access_count"]
                entry.entanglement_links = set(entry_dict["entanglement_links"])
                entry.is_quantum_enhanced = entry_dict["is_quantum_enhanced"]
                
                self.memory_store[key] = entry
                
                # Regenerate classical embedding
                self.classical_embeddings[key] = await self._generate_classical_embedding(entry.value)
            
            # Restore other state
            self.entanglement_graph = snapshot_data["entanglement_graph"]
            self.quantum_state = QuantumState(snapshot_data["quantum_state"])
            self.decoherence_level = snapshot_data["decoherence_level"]
            self.quantum_registers = snapshot_data["quantum_registers"]
            
            self.logger.info(f"Restored memory from snapshot: {snapshot_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to restore snapshot {snapshot_id}: {e}")
            raise
    
    async def _generate_classical_embedding(self, value: Any) -> np.ndarray:
        """Generate classical embedding for a value."""
        
        try:
            # Convert value to string representation
            if isinstance(value, (dict, list)):
                text = json.dumps(value, sort_keys=True)
            else:
                text = str(value)
            
            # Simple hash-based embedding (in production, use proper embeddings)
            hash_value = hashlib.sha256(text.encode()).hexdigest()
            
            # Convert hash to numerical embedding
            embedding = np.array([
                int(hash_value[i:i+2], 16) / 255.0 
                for i in range(0, min(len(hash_value), self.config.classical_dim * 2), 2)
            ])
            
            # Pad or truncate to desired dimension
            if len(embedding) < self.config.classical_dim:
                embedding = np.pad(embedding, (0, self.config.classical_dim - len(embedding)))
            else:
                embedding = embedding[:self.config.classical_dim]
            
            return embedding
            
        except Exception as e:
            self.logger.error(f"Failed to generate embedding: {e}")
            return np.random.random(self.config.classical_dim)
    
    async def _generate_quantum_state(self, value: Any, key: str) -> Dict[str, Any]:
        """Generate quantum state representation for a value."""
        
        try:
            # Simple quantum state encoding
            hash_val = hash(str(value)) % (2 ** self.config.quantum_dim)
            binary_rep = format(hash_val, f'0{self.config.quantum_dim}b')
            
            # Create quantum state amplitudes
            amplitudes = []
            for bit in binary_rep:
                if bit == '0':
                    amplitudes.extend([1.0, 0.0])  # |0⟩
                else:
                    amplitudes.extend([0.0, 1.0])  # |1⟩
            
            quantum_state = {
                "type": "computational_basis",
                "amplitudes": amplitudes[:2**self.config.quantum_dim],
                "qubits": self.config.quantum_dim,
                "encoding": binary_rep,
                "creation_time": datetime.now().isoformat()
            }
            
            return quantum_state
            
        except Exception as e:
            self.logger.error(f"Failed to generate quantum state: {e}")
            return {"type": "error", "amplitudes": [1.0] + [0.0] * (2**self.config.quantum_dim - 1)}
    
    async def _quantum_similarity_search(self, query_key: str) -> Optional[str]:
        """Perform quantum-enhanced similarity search."""
        
        try:
            if not self.memory_store:
                return None
            
            # Generate query embedding
            query_embedding = await self._generate_classical_embedding(query_key)
            
            # Simulate quantum speedup in similarity computation
            best_similarity = -1
            best_key = None
            
            for key, embedding in self.classical_embeddings.items():
                # Classical cosine similarity
                similarity = np.dot(query_embedding, embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
                )
                
                # Quantum enhancement factor (simulated)
                quantum_boost = 1.0 - self.decoherence_level * 0.1
                enhanced_similarity = similarity * quantum_boost
                
                if enhanced_similarity > best_similarity:
                    best_similarity = enhanced_similarity
                    best_key = key
            
            # Return result if similarity is above threshold
            threshold = 0.7
            if best_similarity > threshold:
                return best_key
            
            return None
            
        except Exception as e:
            self.logger.error(f"Quantum similarity search failed: {e}")
            return None
    
    async def _classical_similarity_search(self, query_key: str) -> Optional[str]:
        """Perform classical similarity search as fallback."""
        
        try:
            if not self.memory_store:
                return None
            
            # Simple string matching
            best_score = -1
            best_key = None
            
            for key in self.memory_store.keys():
                # Simple Levenshtein-like distance
                score = self._string_similarity(query_key, key)
                if score > best_score:
                    best_score = score
                    best_key = key
            
            # Return if above threshold
            if best_score > 0.5:
                return best_key
            
            return None
            
        except Exception as e:
            self.logger.error(f"Classical similarity search failed: {e}")
            return None
    
    def _string_similarity(self, s1: str, s2: str) -> float:
        """Calculate string similarity score."""
        
        if not s1 or not s2:
            return 0.0
        
        # Simple character overlap measure
        set1, set2 = set(s1.lower()), set(s2.lower())
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    async def _apply_access_decoherence(self, entry: MemoryEntry) -> None:
        """Apply decoherence effects on memory access."""
        
        # Memory access causes decoherence
        decoherence_delta = 0.01 * (1 + entry.access_count * 0.1)
        self.update_decoherence(decoherence_delta)
        
        # Update entry metadata
        entry.metadata["last_access"] = datetime.now().isoformat()
        entry.metadata["access_decoherence"] = decoherence_delta
    
    async def _compress_memory(self) -> None:
        """Compress memory by removing least accessed entries."""
        
        try:
            # Sort by access count
            sorted_entries = sorted(
                self.memory_store.items(),
                key=lambda x: x[1].access_count
            )
            
            # Remove bottom 20%
            removal_count = int(len(sorted_entries) * 0.2)
            for i in range(removal_count):
                key, _ = sorted_entries[i]
                del self.memory_store[key]
                if key in self.classical_embeddings:
                    del self.classical_embeddings[key]
                if key in self.entanglement_graph:
                    del self.entanglement_graph[key]
            
            self.logger.info(f"Compressed memory: removed {removal_count} entries")
            
        except Exception as e:
            self.logger.error(f"Memory compression failed: {e}")
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get memory system statistics."""
        
        total_entries = len(self.memory_store)
        quantum_enhanced_count = sum(
            1 for entry in self.memory_store.values() 
            if entry.is_quantum_enhanced
        )
        entangled_count = sum(
            1 for entry in self.memory_store.values()
            if entry.entanglement_links
        )
        
        return {
            "total_entries": total_entries,
            "quantum_enhanced_entries": quantum_enhanced_count,
            "entangled_entries": entangled_count,
            "snapshots_count": len(self.snapshots),
            "entanglement_groups": len(self.entanglement_graph),
            "quantum_state": self.quantum_state.value,
            "decoherence_level": self.decoherence_level,
            "quantum_registers": len(self.quantum_registers),
            "classical_dim": self.config.classical_dim,
            "quantum_dim": self.config.quantum_dim,
            "memory_efficiency": quantum_enhanced_count / total_entries if total_entries > 0 else 0
        }


class SharedQuantumMemory(QuantumMemory):
    """Shared quantum memory for multi-agent systems."""
    
    def __init__(self, agents: int = 3, entanglement_depth: int = 4, **data):
        super().__init__(**data)
        self.agent_count = agents
        self.entanglement_depth = entanglement_depth
        self.agent_memories = {}
        self.shared_entanglement_registry = {}
    
    async def initialize(self) -> None:
        """Initialize shared memory system."""
        await super().initialize()
        
        # Initialize per-agent memory spaces
        for i in range(self.agent_count):
            agent_id = f"agent_{i}"
            self.agent_memories[agent_id] = {}
        
        # Create shared entanglement between agents
        await self._create_shared_entanglement()
    
    async def _create_shared_entanglement(self) -> None:
        """Create entanglement between agent memory spaces."""
        
        # Create entanglement pattern between agents
        for i in range(self.agent_count):
            for j in range(i + 1, self.agent_count):
                agent1_id = f"agent_{i}"
                agent2_id = f"agent_{j}"
                
                entanglement_id = f"shared_{agent1_id}_{agent2_id}"
                self.shared_entanglement_registry[entanglement_id] = {
                    "agents": [agent1_id, agent2_id],
                    "strength": 1.0 / (abs(i - j) + 1),
                    "creation_time": datetime.now().isoformat()
                }
        
        self.quantum_state = QuantumState.ENTANGLED
        self.logger.info(f"Created shared entanglement for {self.agent_count} agents")
    
    async def store_for_agent(
        self, 
        agent_id: str, 
        key: str, 
        value: Any, 
        share_with_agents: Optional[List[str]] = None
    ) -> None:
        """Store data in agent-specific memory space with optional sharing."""
        
        # Store in main memory
        await self.store(key, value, quantum_enhanced=True)
        
        # Store in agent-specific space
        if agent_id not in self.agent_memories:
            self.agent_memories[agent_id] = {}
        
        self.agent_memories[agent_id][key] = {
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "shared_with": share_with_agents or []
        }
        
        # Create entanglement with shared agents
        if share_with_agents:
            all_keys = [f"{agent_id}_{key}"]
            for shared_agent in share_with_agents:
                shared_key = f"{shared_agent}_{key}"
                all_keys.append(shared_key)
                
                # Store in shared agent's space
                if shared_agent not in self.agent_memories:
                    self.agent_memories[shared_agent] = {}
                
                self.agent_memories[shared_agent][key] = {
                    "value": value,
                    "timestamp": datetime.now().isoformat(),
                    "shared_from": agent_id
                }
            
            # Create entanglement
            await self.entangle_memories(all_keys)
    
    async def retrieve_for_agent(self, agent_id: str, key: str) -> Any:
        """Retrieve data from agent's memory space."""
        
        # Check agent-specific memory first
        if agent_id in self.agent_memories and key in self.agent_memories[agent_id]:
            entry = self.agent_memories[agent_id][key]
            return entry["value"]
        
        # Fall back to shared memory
        return await self.retrieve(key, quantum_search=True)
    
    def get_shared_stats(self) -> Dict[str, Any]:
        """Get shared memory statistics."""
        
        agent_entry_counts = {
            agent_id: len(memories) 
            for agent_id, memories in self.agent_memories.items()
        }
        
        return {
            "agent_count": self.agent_count,
            "shared_entanglements": len(self.shared_entanglement_registry),
            "agent_entry_counts": agent_entry_counts,
            "total_agent_entries": sum(agent_entry_counts.values()),
            "entanglement_depth": self.entanglement_depth
        }
