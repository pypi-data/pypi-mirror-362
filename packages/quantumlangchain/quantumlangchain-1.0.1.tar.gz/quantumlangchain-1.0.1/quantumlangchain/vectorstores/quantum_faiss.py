"""
Quantum-enhanced FAISS vector store with amplitude amplification and entangled indexing.
"""

import asyncio
import uuid
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json
import numpy as np
import pickle
import os

from quantumlangchain.core.base import QuantumBase, QuantumState

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False


@dataclass
class QuantumIndexEntry:
    """Entry in quantum-enhanced FAISS index."""
    entry_id: str
    vector: np.ndarray
    metadata: Dict[str, Any] = field(default_factory=dict)
    quantum_enhanced: bool = False
    entanglement_ids: List[str] = field(default_factory=list)
    coherence_amplitude: float = 1.0
    phase: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    
    def get_quantum_amplitude(self) -> complex:
        """Get quantum amplitude as complex number."""
        return self.coherence_amplitude * np.exp(1j * self.phase)
    
    def update_phase(self, phase_shift: float):
        """Update quantum phase."""
        self.phase = (self.phase + phase_shift) % (2 * np.pi)


class QuantumFAISS(QuantumBase):
    """
    Quantum-enhanced FAISS vector store with amplitude amplification,
    entangled indexing, and coherent search algorithms.
    """
    
    def __init__(
        self,
        dimension: int,
        index_type: str = "IVFFlat",
        metric: str = "L2",
        nlist: int = 100,
        persist_path: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__(config)
        
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS is not available. Install with: pip install faiss-cpu or faiss-gpu")
        
        self.dimension = dimension
        self.index_type = index_type
        self.metric = metric
        self.nlist = nlist
        self.persist_path = persist_path
        
        # FAISS index
        self.index = None
        self.is_trained = False
        
        # Quantum entries registry
        self.quantum_entries: Dict[int, QuantumIndexEntry] = {}
        self.id_to_faiss_id: Dict[str, int] = {}
        self.faiss_id_to_id: Dict[int, str] = {}
        self.next_faiss_id = 0
        
        # Entanglement relationships
        self.entangled_groups: Dict[str, List[str]] = {}
        
        # Configuration
        self.amplitude_boost_factor = config.get("amplitude_boost_factor", 1.5) if config else 1.5
        self.coherence_threshold = config.get("coherence_threshold", 0.8) if config else 0.8
        self.max_search_results = config.get("max_search_results", 1000) if config else 1000
        
    async def initialize(self):
        """Initialize the quantum FAISS index."""
        await super().initialize()
        
        # Create FAISS index based on type
        if self.index_type == "Flat":
            if self.metric == "L2":
                self.index = faiss.IndexFlatL2(self.dimension)
            else:
                self.index = faiss.IndexFlatIP(self.dimension)
            self.is_trained = True
            
        elif self.index_type == "IVFFlat":
            if self.metric == "L2":
                quantizer = faiss.IndexFlatL2(self.dimension)
                self.index = faiss.IndexIVFFlat(quantizer, self.dimension, self.nlist)
            else:
                quantizer = faiss.IndexFlatIP(self.dimension)
                self.index = faiss.IndexIVFFlat(quantizer, self.dimension, self.nlist)
            
        elif self.index_type == "HNSW":
            self.index = faiss.IndexHNSWFlat(self.dimension, 32)
            self.index.hnsw.efConstruction = 200
            self.index.hnsw.efSearch = 50
            self.is_trained = True
            
        else:
            # Default to Flat index
            self.index = faiss.IndexFlatL2(self.dimension)
            self.is_trained = True
        
        # Load persisted index if available
        if self.persist_path and os.path.exists(f"{self.persist_path}.index"):
            await self.load_index()
        
        self.quantum_state = QuantumState.COHERENT
        
    async def reset_quantum_state(self):
        """Reset quantum state and coherence amplitudes."""
        self.quantum_state = QuantumState.COHERENT
        self.decoherence_level = 0.0
        
        # Reset quantum amplitudes and phases
        for entry in self.quantum_entries.values():
            entry.coherence_amplitude = 1.0
            entry.phase = 0.0
        
        self.entangled_groups.clear()
    
    async def add_vectors(
        self,
        vectors: Union[np.ndarray, List[List[float]]],
        ids: Optional[List[str]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None,
        quantum_enhanced: bool = False
    ) -> List[str]:
        """Add vectors to the quantum index."""
        if isinstance(vectors, list):
            vectors = np.array(vectors, dtype=np.float32)
        
        if vectors.ndim == 1:
            vectors = vectors.reshape(1, -1)
        
        n_vectors = vectors.shape[0]
        
        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in range(n_vectors)]
        
        # Prepare metadatas
        if metadatas is None:
            metadatas = [{} for _ in range(n_vectors)]
        
        # Train index if needed
        if not self.is_trained and hasattr(self.index, 'train'):
            if n_vectors >= self.nlist:
                self.index.train(vectors)
                self.is_trained = True
            else:
                # Need more vectors for training
                pass
        
        # Add to FAISS index
        start_faiss_id = self.next_faiss_id
        faiss_ids = list(range(start_faiss_id, start_faiss_id + n_vectors))
        
        if self.is_trained:
            self.index.add_with_ids(vectors, np.array(faiss_ids, dtype=np.int64))
        
        # Create quantum entries
        for i, (vector, entry_id, metadata) in enumerate(zip(vectors, ids, metadatas)):
            faiss_id = faiss_ids[i]
            
            # Create quantum entry
            quantum_entry = QuantumIndexEntry(
                entry_id=entry_id,
                vector=vector,
                metadata=metadata,
                quantum_enhanced=quantum_enhanced
            )
            
            # Store mappings
            self.quantum_entries[faiss_id] = quantum_entry
            self.id_to_faiss_id[entry_id] = faiss_id
            self.faiss_id_to_id[faiss_id] = entry_id
        
        self.next_faiss_id += n_vectors
        
        # Update quantum state
        if quantum_enhanced:
            if self.quantum_state == QuantumState.COHERENT:
                self.quantum_state = QuantumState.SUPERPOSITION
        
        return ids
    
    async def search(
        self,
        query_vector: Union[np.ndarray, List[float]],
        k: int = 5,
        quantum_enhanced: bool = False,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Search the quantum index for similar vectors."""
        if not self.is_trained:
            return []
        
        if isinstance(query_vector, list):
            query_vector = np.array(query_vector, dtype=np.float32)
        
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)
        
        # Perform FAISS search with more results for quantum processing
        search_k = min(k * 5, self.max_search_results) if quantum_enhanced else k
        
        distances, indices = self.index.search(query_vector, search_k)
        
        # Convert results to quantum format
        results = []
        for i, (distance, faiss_id) in enumerate(zip(distances[0], indices[0])):
            if faiss_id == -1:  # No more results
                break
            
            if faiss_id in self.quantum_entries:
                entry = self.quantum_entries[faiss_id]
                
                # Apply metadata filter if specified
                if filter_metadata:
                    match = all(
                        entry.metadata.get(key) == value
                        for key, value in filter_metadata.items()
                    )
                    if not match:
                        continue
                
                # Convert distance to similarity score
                similarity = self._distance_to_similarity(distance)
                
                # Update access tracking
                entry.access_count += 1
                
                results.append((entry.entry_id, similarity, entry.metadata))
        
        # Apply quantum enhancements if requested
        if quantum_enhanced:
            results = await self._apply_quantum_search_enhancements(
                results, query_vector[0]
            )
        
        # Return top k results
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]
    
    def _distance_to_similarity(self, distance: float) -> float:
        """Convert distance to similarity score."""
        if self.metric == "L2":
            # For L2 distance, convert to similarity (higher is better)
            return 1.0 / (1.0 + distance)
        else:
            # For inner product, distance is already similarity-like
            return distance
    
    async def _apply_quantum_search_enhancements(
        self,
        results: List[Tuple[str, float, Dict[str, Any]]],
        query_vector: np.ndarray
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Apply quantum enhancements to search results."""
        enhanced_results = []
        
        for entry_id, similarity, metadata in results:
            faiss_id = self.id_to_faiss_id.get(entry_id)
            if faiss_id is None:
                enhanced_results.append((entry_id, similarity, metadata))
                continue
            
            entry = self.quantum_entries[faiss_id]
            enhanced_similarity = similarity
            
            # Quantum amplitude boost
            if entry.quantum_enhanced:
                amplitude = abs(entry.get_quantum_amplitude())
                enhanced_similarity *= amplitude * self.amplitude_boost_factor
            
            # Entanglement correlation boost
            entanglement_boost = await self._calculate_entanglement_boost(entry, results)
            enhanced_similarity *= (1 + entanglement_boost)
            
            # Coherence effects
            coherence_factor = 1 - self.decoherence_level * 0.1
            enhanced_similarity *= coherence_factor
            
            # Access frequency boost (quantum memory effect)
            if entry.access_count > 0:
                frequency_boost = min(0.1, entry.access_count / 1000)
                enhanced_similarity *= (1 + frequency_boost)
            
            enhanced_results.append((entry_id, enhanced_similarity, metadata))
        
        # Update decoherence from quantum search
        self.update_decoherence(0.02)
        
        return enhanced_results
    
    async def _calculate_entanglement_boost(
        self,
        target_entry: QuantumIndexEntry,
        all_results: List[Tuple[str, float, Dict[str, Any]]]
    ) -> float:
        """Calculate boost from entangled entries in results."""
        if not target_entry.entanglement_ids:
            return 0.0
        
        entanglement_boost = 0.0
        
        for entanglement_id in target_entry.entanglement_ids:
            if entanglement_id in self.entangled_groups:
                entangled_entry_ids = self.entangled_groups[entanglement_id]
                
                # Count entangled entries in search results
                entangled_in_results = 0
                for entry_id, _, _ in all_results:
                    if entry_id in entangled_entry_ids and entry_id != target_entry.entry_id:
                        entangled_in_results += 1
                
                # Boost based on entangled entry presence
                if entangled_in_results > 0:
                    entanglement_boost += entangled_in_results * 0.05
        
        return min(0.3, entanglement_boost)  # Cap at 30% boost
    
    async def entangle_vectors(
        self,
        entry_ids: List[str],
        entanglement_strength: float = 0.8
    ) -> str:
        """Create quantum entanglement between vectors."""
        # Verify all entries exist
        for entry_id in entry_ids:
            if entry_id not in self.id_to_faiss_id:
                raise ValueError(f"Entry '{entry_id}' not found")
        
        entanglement_id = str(uuid.uuid4())
        
        # Update entries with entanglement
        for entry_id in entry_ids:
            faiss_id = self.id_to_faiss_id[entry_id]
            entry = self.quantum_entries[faiss_id]
            entry.entanglement_ids.append(entanglement_id)
            
            # Synchronize quantum phases (simplified entanglement effect)
            entry.phase = 0.0  # Common phase for entangled vectors
        
        # Store entanglement relationship
        self.entangled_groups[entanglement_id] = entry_ids
        
        # Update quantum state
        self.quantum_state = QuantumState.ENTANGLED
        
        return entanglement_id
    
    async def amplitude_amplification_search(
        self,
        query_vector: Union[np.ndarray, List[float]],
        target_condition: Callable[[Dict[str, Any]], bool],
        k: int = 5,
        iterations: int = 3
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Perform amplitude amplification search to boost target results."""
        if isinstance(query_vector, list):
            query_vector = np.array(query_vector, dtype=np.float32)
        
        # Initial search with larger result set
        initial_results = await self.search(
            query_vector=query_vector,
            k=k * 10,  # Get 10x more for amplification
            quantum_enhanced=False
        )
        
        if not initial_results:
            return []
        
        # Apply amplitude amplification iterations
        amplified_results = initial_results.copy()
        
        for iteration in range(iterations):
            amplified_results = await self._amplitude_amplification_iteration(
                amplified_results, target_condition, query_vector
            )
        
        # Sort and return top k
        amplified_results.sort(key=lambda x: x[1], reverse=True)
        return amplified_results[:k]
    
    async def _amplitude_amplification_iteration(
        self,
        results: List[Tuple[str, float, Dict[str, Any]]],
        target_condition: Callable[[Dict[str, Any]], bool],
        query_vector: np.ndarray
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Single iteration of amplitude amplification."""
        amplified_results = []
        
        for entry_id, similarity, metadata in results:
            # Check if this result meets target condition
            is_target = target_condition(metadata)
            
            if is_target:
                # Amplify target results
                amplification_factor = 1.4  # Simulated amplitude boost
                amplified_similarity = min(1.0, similarity * amplification_factor)
            else:
                # Slightly suppress non-target results
                amplified_similarity = similarity * 0.95
            
            # Apply quantum coherence effects
            faiss_id = self.id_to_faiss_id.get(entry_id)
            if faiss_id and faiss_id in self.quantum_entries:
                entry = self.quantum_entries[faiss_id]
                if entry.quantum_enhanced:
                    coherence_factor = abs(entry.get_quantum_amplitude())
                    amplified_similarity *= coherence_factor
            
            amplified_results.append((entry_id, amplified_similarity, metadata))
        
        # Update decoherence from quantum operation
        self.update_decoherence(0.03)
        
        return amplified_results
    
    async def grovers_search(
        self,
        oracle_function: Callable[[str, Dict[str, Any]], bool],
        k: int = 5,
        max_iterations: int = 10
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Perform Grover's algorithm-inspired search."""
        if not self.is_trained or self.index.ntotal == 0:
            return []
        
        # Get all vectors for Grover's search
        all_vectors = []
        all_ids = []
        all_metadata = []
        
        for faiss_id, entry in self.quantum_entries.items():
            all_vectors.append(entry.vector)
            all_ids.append(entry.entry_id)
            all_metadata.append(entry.metadata)
        
        if not all_vectors:
            return []
        
        # Initialize uniform superposition (all equal amplitudes)
        n_items = len(all_vectors)
        amplitudes = np.ones(n_items) / np.sqrt(n_items)
        
        # Grover iterations
        optimal_iterations = min(max_iterations, int(np.pi * np.sqrt(n_items) / 4))
        
        for _ in range(optimal_iterations):
            # Oracle: mark target items
            for i, (entry_id, metadata) in enumerate(zip(all_ids, all_metadata)):
                if oracle_function(entry_id, metadata):
                    amplitudes[i] *= -1  # Flip amplitude of target items
            
            # Diffusion operator: invert about average
            average = np.mean(amplitudes)
            amplitudes = 2 * average - amplitudes
        
        # Convert amplitudes to probabilities and get top results
        probabilities = np.abs(amplitudes) ** 2
        
        # Create results with quantum-enhanced scores
        results = []
        for i, (entry_id, metadata) in enumerate(zip(all_ids, all_metadata)):
            quantum_score = probabilities[i]
            results.append((entry_id, quantum_score, metadata))
        
        # Sort by quantum score and return top k
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Update decoherence from quantum algorithm
        self.update_decoherence(0.05)
        
        return results[:k]
    
    async def delete_vectors(self, entry_ids: List[str]) -> int:
        """Delete vectors from the quantum index."""
        deleted_count = 0
        
        for entry_id in entry_ids:
            if entry_id in self.id_to_faiss_id:
                faiss_id = self.id_to_faiss_id[entry_id]
                
                # Remove from quantum registry
                if faiss_id in self.quantum_entries:
                    entry = self.quantum_entries[faiss_id]
                    
                    # Break entanglements
                    for entanglement_id in entry.entanglement_ids.copy():
                        await self.break_entanglement(entanglement_id)
                    
                    del self.quantum_entries[faiss_id]
                
                # Remove from mappings
                del self.id_to_faiss_id[entry_id]
                if faiss_id in self.faiss_id_to_id:
                    del self.faiss_id_to_id[faiss_id]
                
                deleted_count += 1
        
        # Note: FAISS doesn't support direct deletion, so we keep track
        # of deleted IDs to filter them out during search
        
        return deleted_count
    
    async def break_entanglement(self, entanglement_id: str) -> bool:
        """Break quantum entanglement between vectors."""
        if entanglement_id not in self.entangled_groups:
            return False
        
        entry_ids = self.entangled_groups[entanglement_id]
        
        # Remove entanglement from entries
        for entry_id in entry_ids:
            if entry_id in self.id_to_faiss_id:
                faiss_id = self.id_to_faiss_id[entry_id]
                if faiss_id in self.quantum_entries:
                    entry = self.quantum_entries[faiss_id]
                    if entanglement_id in entry.entanglement_ids:
                        entry.entanglement_ids.remove(entanglement_id)
        
        # Remove entanglement group
        del self.entangled_groups[entanglement_id]
        
        return True
    
    async def save_index(self, path: Optional[str] = None) -> bool:
        """Save the quantum index to disk."""
        save_path = path or self.persist_path
        if not save_path:
            return False
        
        try:
            # Save FAISS index
            faiss.write_index(self.index, f"{save_path}.index")
            
            # Save quantum metadata
            metadata = {
                "quantum_entries": {
                    str(faiss_id): {
                        "entry_id": entry.entry_id,
                        "metadata": entry.metadata,
                        "quantum_enhanced": entry.quantum_enhanced,
                        "entanglement_ids": entry.entanglement_ids,
                        "coherence_amplitude": entry.coherence_amplitude,
                        "phase": entry.phase,
                        "created_at": entry.created_at.isoformat(),
                        "access_count": entry.access_count
                    }
                    for faiss_id, entry in self.quantum_entries.items()
                },
                "id_mappings": {
                    "id_to_faiss_id": self.id_to_faiss_id,
                    "faiss_id_to_id": {str(k): v for k, v in self.faiss_id_to_id.items()}
                },
                "entangled_groups": self.entangled_groups,
                "next_faiss_id": self.next_faiss_id,
                "is_trained": self.is_trained,
                "quantum_state": self.quantum_state.value,
                "decoherence_level": self.decoherence_level
            }
            
            with open(f"{save_path}.metadata", 'wb') as f:
                pickle.dump(metadata, f)
            
            return True
            
        except Exception:
            return False
    
    async def load_index(self, path: Optional[str] = None) -> bool:
        """Load the quantum index from disk."""
        load_path = path or self.persist_path
        if not load_path:
            return False
        
        try:
            # Load FAISS index
            if os.path.exists(f"{load_path}.index"):
                self.index = faiss.read_index(f"{load_path}.index")
            
            # Load quantum metadata
            if os.path.exists(f"{load_path}.metadata"):
                with open(f"{load_path}.metadata", 'rb') as f:
                    metadata = pickle.load(f)
                
                # Restore quantum entries
                self.quantum_entries = {}
                for faiss_id_str, entry_data in metadata["quantum_entries"].items():
                    faiss_id = int(faiss_id_str)
                    entry = QuantumIndexEntry(
                        entry_id=entry_data["entry_id"],
                        vector=np.array([]),  # Vector not stored in metadata
                        metadata=entry_data["metadata"],
                        quantum_enhanced=entry_data["quantum_enhanced"],
                        entanglement_ids=entry_data["entanglement_ids"],
                        coherence_amplitude=entry_data["coherence_amplitude"],
                        phase=entry_data["phase"],
                        created_at=datetime.fromisoformat(entry_data["created_at"]),
                        access_count=entry_data["access_count"]
                    )
                    self.quantum_entries[faiss_id] = entry
                
                # Restore mappings
                self.id_to_faiss_id = metadata["id_mappings"]["id_to_faiss_id"]
                self.faiss_id_to_id = {
                    int(k): v for k, v in metadata["id_mappings"]["faiss_id_to_id"].items()
                }
                
                # Restore other data
                self.entangled_groups = metadata["entangled_groups"]
                self.next_faiss_id = metadata["next_faiss_id"]
                self.is_trained = metadata["is_trained"]
                self.quantum_state = QuantumState(metadata["quantum_state"])
                self.decoherence_level = metadata["decoherence_level"]
            
            return True
            
        except Exception:
            return False
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get comprehensive index statistics."""
        stats = {
            "total_vectors": self.index.ntotal if self.index else 0,
            "dimension": self.dimension,
            "index_type": self.index_type,
            "metric": self.metric,
            "is_trained": self.is_trained,
            "quantum_entries": len(self.quantum_entries),
            "quantum_enhanced_entries": len([
                entry for entry in self.quantum_entries.values()
                if entry.quantum_enhanced
            ]),
            "entangled_entries": len([
                entry for entry in self.quantum_entries.values()
                if entry.entanglement_ids
            ]),
            "entanglement_groups": len(self.entangled_groups),
            "quantum_state": self.quantum_state.value,
            "decoherence_level": self.decoherence_level,
            "average_coherence": 0.0,
            "total_access_count": sum(entry.access_count for entry in self.quantum_entries.values())
        }
        
        # Calculate average coherence amplitude
        if self.quantum_entries:
            total_coherence = sum(
                abs(entry.get_quantum_amplitude()) 
                for entry in self.quantum_entries.values()
            )
            stats["average_coherence"] = total_coherence / len(self.quantum_entries)
        
        return stats
