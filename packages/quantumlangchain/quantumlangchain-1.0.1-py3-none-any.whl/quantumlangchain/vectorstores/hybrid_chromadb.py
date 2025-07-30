"""
Hybrid ChromaDB with quantum-enhanced similarity search and entangled document relationships.
"""

import asyncio
import uuid
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime
import json
import numpy as np

from quantumlangchain.core.base import QuantumBase, QuantumState

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False


@dataclass
class QuantumDocument:
    """Document with quantum enhancement metadata."""
    doc_id: str
    content: str
    embedding: np.ndarray
    metadata: Dict[str, Any] = field(default_factory=dict)
    quantum_enhanced: bool = False
    entanglement_ids: List[str] = field(default_factory=list)
    coherence_score: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "doc_id": self.doc_id,
            "content": self.content,
            "embedding": self.embedding.tolist() if isinstance(self.embedding, np.ndarray) else self.embedding,
            "metadata": self.metadata,
            "quantum_enhanced": self.quantum_enhanced,
            "entanglement_ids": self.entanglement_ids,
            "coherence_score": self.coherence_score,
            "created_at": self.created_at.isoformat(),
            "access_count": self.access_count,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QuantumDocument':
        """Create from dictionary."""
        embedding = np.array(data["embedding"]) if data["embedding"] else None
        return cls(
            doc_id=data["doc_id"],
            content=data["content"],
            embedding=embedding,
            metadata=data.get("metadata", {}),
            quantum_enhanced=data.get("quantum_enhanced", False),
            entanglement_ids=data.get("entanglement_ids", []),
            coherence_score=data.get("coherence_score", 1.0),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now(),
            access_count=data.get("access_count", 0),
            last_accessed=datetime.fromisoformat(data["last_accessed"]) if data.get("last_accessed") else None
        )


class HybridChromaDB(QuantumBase):
    """
    Hybrid ChromaDB implementation with quantum-enhanced similarity search,
    entangled document relationships, and coherence-aware retrieval.
    """
    
    def __init__(
        self,
        collection_name: str = "quantum_documents",
        persist_directory: Optional[str] = None,
        embedding_function: Optional[Any] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__(config)
        
        if not CHROMADB_AVAILABLE:
            raise ImportError("ChromaDB is not available. Install with: pip install chromadb")
        
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embedding_function = embedding_function
        
        # ChromaDB client and collection
        self.client = None
        self.collection = None
        
        # Quantum document registry
        self.quantum_documents: Dict[str, QuantumDocument] = {}
        self.entangled_documents: Dict[str, List[str]] = {}
        
        # Configuration
        self.similarity_threshold = config.get("similarity_threshold", 0.7) if config else 0.7
        self.quantum_boost_factor = config.get("quantum_boost_factor", 1.2) if config else 1.2
        self.max_results = config.get("max_results", 100) if config else 100
        
    async def initialize(self):
        """Initialize the hybrid ChromaDB system."""
        await super().initialize()
        
        # Initialize ChromaDB client
        if self.persist_directory:
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(allow_reset=True)
            )
        else:
            self.client = chromadb.EphemeralClient()
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
        except ValueError:
            # Collection doesn't exist, create it
            self.collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function,
                metadata={"quantum_enhanced": True}
            )
        
        self.quantum_state = QuantumState.COHERENT
        
    async def reset_quantum_state(self):
        """Reset quantum state and clear entanglements."""
        self.quantum_state = QuantumState.COHERENT
        self.decoherence_level = 0.0
        self.entangled_documents.clear()
        
        # Reset coherence scores
        for doc in self.quantum_documents.values():
            doc.coherence_score = 1.0
    
    async def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
        embeddings: Optional[List[List[float]]] = None,
        quantum_enhanced: bool = False
    ) -> List[str]:
        """Add documents to the collection with optional quantum enhancement."""
        if not documents:
            return []
        
        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in documents]
        
        # Prepare metadatas
        if metadatas is None:
            metadatas = [{} for _ in documents]
        
        # Add quantum metadata
        enhanced_metadatas = []
        for i, metadata in enumerate(metadatas):
            enhanced_metadata = metadata.copy()
            enhanced_metadata.update({
                "quantum_enhanced": quantum_enhanced,
                "added_at": datetime.now().isoformat(),
                "doc_index": i
            })
            enhanced_metadatas.append(enhanced_metadata)
        
        # Add to ChromaDB
        self.collection.add(
            documents=documents,
            metadatas=enhanced_metadatas,
            ids=ids,
            embeddings=embeddings
        )
        
        # Create quantum documents
        for i, doc_id in enumerate(ids):
            embedding_vector = None
            if embeddings and i < len(embeddings):
                embedding_vector = np.array(embeddings[i])
            
            quantum_doc = QuantumDocument(
                doc_id=doc_id,
                content=documents[i],
                embedding=embedding_vector,
                metadata=enhanced_metadatas[i],
                quantum_enhanced=quantum_enhanced
            )
            
            self.quantum_documents[doc_id] = quantum_doc
        
        # Update quantum state
        if quantum_enhanced:
            if self.quantum_state == QuantumState.COHERENT:
                self.quantum_state = QuantumState.SUPERPOSITION
        
        return ids
    
    async def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
        quantum_enhanced: bool = False
    ) -> List[Tuple[QuantumDocument, float]]:
        """Perform similarity search with optional quantum enhancement."""
        # Basic ChromaDB search
        results = self.collection.query(
            query_texts=[query],
            n_results=min(k * 2, self.max_results),  # Get more for quantum processing
            where=filter
        )
        
        if not results["ids"] or not results["ids"][0]:
            return []
        
        # Convert to quantum documents with scores
        search_results = []
        ids = results["ids"][0]
        distances = results["distances"][0] if results["distances"] else [0.0] * len(ids)
        documents = results["documents"][0] if results["documents"] else [""] * len(ids)
        metadatas = results["metadatas"][0] if results["metadatas"] else [{}] * len(ids)
        
        for i, doc_id in enumerate(ids):
            # Convert distance to similarity score (ChromaDB returns distances)
            similarity_score = 1.0 - distances[i] if i < len(distances) else 0.0
            
            # Get or create quantum document
            if doc_id in self.quantum_documents:
                quantum_doc = self.quantum_documents[doc_id]
                quantum_doc.access_count += 1
                quantum_doc.last_accessed = datetime.now()
            else:
                # Create quantum document from search result
                quantum_doc = QuantumDocument(
                    doc_id=doc_id,
                    content=documents[i] if i < len(documents) else "",
                    embedding=None,  # Will be retrieved if needed
                    metadata=metadatas[i] if i < len(metadatas) else {},
                    quantum_enhanced=metadatas[i].get("quantum_enhanced", False) if i < len(metadatas) else False
                )
                self.quantum_documents[doc_id] = quantum_doc
            
            search_results.append((quantum_doc, similarity_score))
        
        # Apply quantum enhancements if requested
        if quantum_enhanced:
            search_results = await self._apply_quantum_search_enhancements(
                search_results, query, filter
            )
        
        # Sort by similarity score and return top k
        search_results.sort(key=lambda x: x[1], reverse=True)
        return search_results[:k]
    
    async def _apply_quantum_search_enhancements(
        self,
        results: List[Tuple[QuantumDocument, float]],
        query: str,
        filter: Optional[Dict[str, Any]]
    ) -> List[Tuple[QuantumDocument, float]]:
        """Apply quantum enhancements to search results."""
        enhanced_results = []
        
        for doc, score in results:
            enhanced_score = score
            
            # Quantum coherence boost
            if doc.quantum_enhanced:
                coherence_boost = doc.coherence_score * self.quantum_boost_factor
                enhanced_score *= coherence_boost
            
            # Entanglement correlation boost
            entanglement_boost = await self._calculate_entanglement_boost(doc, results)
            enhanced_score *= (1 + entanglement_boost)
            
            # Decoherence penalty
            decoherence_penalty = self.decoherence_level * 0.1
            enhanced_score *= (1 - decoherence_penalty)
            
            # Access frequency boost (quantum memory effect)
            if doc.access_count > 0:
                frequency_boost = min(0.1, doc.access_count / 100)
                enhanced_score *= (1 + frequency_boost)
            
            enhanced_results.append((doc, enhanced_score))
        
        # Update decoherence from quantum search
        self.update_decoherence(0.02)
        
        return enhanced_results
    
    async def _calculate_entanglement_boost(
        self,
        target_doc: QuantumDocument,
        all_results: List[Tuple[QuantumDocument, float]]
    ) -> float:
        """Calculate boost from entangled documents in results."""
        if not target_doc.entanglement_ids:
            return 0.0
        
        entanglement_boost = 0.0
        
        for entanglement_id in target_doc.entanglement_ids:
            if entanglement_id in self.entangled_documents:
                entangled_doc_ids = self.entangled_documents[entanglement_id]
                
                # Count entangled documents in search results
                entangled_in_results = 0
                for doc, _ in all_results:
                    if doc.doc_id in entangled_doc_ids and doc.doc_id != target_doc.doc_id:
                        entangled_in_results += 1
                
                # Boost based on entangled document presence
                if entangled_in_results > 0:
                    entanglement_boost += entangled_in_results * 0.05
        
        return min(0.3, entanglement_boost)  # Cap at 30% boost
    
    async def entangle_documents(
        self,
        doc_ids: List[str],
        entanglement_strength: float = 0.8
    ) -> str:
        """Create quantum entanglement between documents."""
        # Verify all documents exist
        for doc_id in doc_ids:
            if doc_id not in self.quantum_documents:
                # Try to load from ChromaDB
                try:
                    result = self.collection.get(ids=[doc_id])
                    if not result["ids"]:
                        raise ValueError(f"Document '{doc_id}' not found")
                except Exception:
                    raise ValueError(f"Document '{doc_id}' not found")
        
        entanglement_id = str(uuid.uuid4())
        
        # Update documents with entanglement
        for doc_id in doc_ids:
            if doc_id in self.quantum_documents:
                self.quantum_documents[doc_id].entanglement_ids.append(entanglement_id)
        
        # Store entanglement relationship
        self.entangled_documents[entanglement_id] = doc_ids
        
        # Update quantum state
        self.quantum_state = QuantumState.ENTANGLED
        
        return entanglement_id
    
    async def break_entanglement(self, entanglement_id: str) -> bool:
        """Break quantum entanglement between documents."""
        if entanglement_id not in self.entangled_documents:
            return False
        
        doc_ids = self.entangled_documents[entanglement_id]
        
        # Remove entanglement from documents
        for doc_id in doc_ids:
            if doc_id in self.quantum_documents:
                doc = self.quantum_documents[doc_id]
                if entanglement_id in doc.entanglement_ids:
                    doc.entanglement_ids.remove(entanglement_id)
        
        # Remove entanglement relationship
        del self.entangled_documents[entanglement_id]
        
        return True
    
    async def update_document(
        self,
        doc_id: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None
    ) -> bool:
        """Update a document in the collection."""
        if doc_id not in self.quantum_documents:
            return False
        
        quantum_doc = self.quantum_documents[doc_id]
        
        # Prepare update data
        update_data = {}
        if content is not None:
            update_data["documents"] = [content]
            quantum_doc.content = content
        
        if metadata is not None:
            enhanced_metadata = quantum_doc.metadata.copy()
            enhanced_metadata.update(metadata)
            enhanced_metadata["updated_at"] = datetime.now().isoformat()
            update_data["metadatas"] = [enhanced_metadata]
            quantum_doc.metadata = enhanced_metadata
        
        if embedding is not None:
            update_data["embeddings"] = [embedding]
            quantum_doc.embedding = np.array(embedding)
        
        # Update in ChromaDB
        if update_data:
            try:
                self.collection.update(ids=[doc_id], **update_data)
                return True
            except Exception:
                return False
        
        return True
    
    async def delete_documents(self, doc_ids: List[str]) -> int:
        """Delete documents from the collection."""
        existing_ids = []
        
        for doc_id in doc_ids:
            if doc_id in self.quantum_documents:
                existing_ids.append(doc_id)
        
        if not existing_ids:
            return 0
        
        # Remove from ChromaDB
        try:
            self.collection.delete(ids=existing_ids)
        except Exception:
            return 0
        
        # Clean up quantum documents and entanglements
        for doc_id in existing_ids:
            # Remove from quantum registry
            if doc_id in self.quantum_documents:
                doc = self.quantum_documents[doc_id]
                
                # Break entanglements
                for entanglement_id in doc.entanglement_ids.copy():
                    await self.break_entanglement(entanglement_id)
                
                del self.quantum_documents[doc_id]
        
        return len(existing_ids)
    
    async def get_document(self, doc_id: str) -> Optional[QuantumDocument]:
        """Get a specific document by ID."""
        if doc_id in self.quantum_documents:
            doc = self.quantum_documents[doc_id]
            doc.access_count += 1
            doc.last_accessed = datetime.now()
            return doc
        
        # Try to load from ChromaDB
        try:
            result = self.collection.get(
                ids=[doc_id],
                include=["documents", "metadatas", "embeddings"]
            )
            
            if result["ids"] and result["ids"][0]:
                # Create quantum document
                quantum_doc = QuantumDocument(
                    doc_id=doc_id,
                    content=result["documents"][0] if result["documents"] else "",
                    embedding=np.array(result["embeddings"][0]) if result["embeddings"] and result["embeddings"][0] else None,
                    metadata=result["metadatas"][0] if result["metadatas"] else {},
                    quantum_enhanced=result["metadatas"][0].get("quantum_enhanced", False) if result["metadatas"] else False
                )
                
                self.quantum_documents[doc_id] = quantum_doc
                return quantum_doc
                
        except Exception:
            pass
        
        return None
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get comprehensive collection statistics."""
        # Get ChromaDB collection count
        chroma_count = self.collection.count() if self.collection else 0
        
        stats = {
            "total_documents": chroma_count,
            "quantum_documents": len(self.quantum_documents),
            "quantum_enhanced_documents": len([
                doc for doc in self.quantum_documents.values() 
                if doc.quantum_enhanced
            ]),
            "entangled_documents": len([
                doc for doc in self.quantum_documents.values() 
                if doc.entanglement_ids
            ]),
            "entanglement_groups": len(self.entangled_documents),
            "quantum_state": self.quantum_state.value,
            "decoherence_level": self.decoherence_level,
            "average_coherence_score": 0.0,
            "total_access_count": sum(doc.access_count for doc in self.quantum_documents.values()),
            "collection_name": self.collection_name
        }
        
        # Calculate average coherence
        if self.quantum_documents:
            total_coherence = sum(doc.coherence_score for doc in self.quantum_documents.values())
            stats["average_coherence_score"] = total_coherence / len(self.quantum_documents)
        
        return stats
    
    async def quantum_similarity_search(
        self,
        query: str,
        k: int = 5,
        quantum_algorithm: str = "amplitude_amplification"
    ) -> List[Tuple[QuantumDocument, float]]:
        """Perform quantum-enhanced similarity search using quantum algorithms."""
        # Get initial candidates (more than needed for quantum processing)
        initial_results = await self.similarity_search(
            query=query,
            k=k * 3,  # Get 3x more for quantum selection
            quantum_enhanced=False  # Don't apply enhancements yet
        )
        
        if not initial_results:
            return []
        
        # Apply quantum algorithm
        if quantum_algorithm == "amplitude_amplification":
            quantum_results = await self._amplitude_amplification_search(initial_results, query)
        elif quantum_algorithm == "grovers_search":
            quantum_results = await self._grovers_inspired_search(initial_results, query)
        else:
            # Default quantum enhancement
            quantum_results = await self._apply_quantum_search_enhancements(
                initial_results, query, None
            )
        
        # Select top k results
        quantum_results.sort(key=lambda x: x[1], reverse=True)
        return quantum_results[:k]
    
    async def _amplitude_amplification_search(
        self,
        candidates: List[Tuple[QuantumDocument, float]],
        query: str
    ) -> List[Tuple[QuantumDocument, float]]:
        """Apply amplitude amplification to boost relevant results."""
        amplified_results = []
        
        # Calculate query relevance for amplification
        query_terms = query.lower().split()
        
        for doc, score in candidates:
            # Calculate content relevance
            content_terms = doc.content.lower().split()
            relevance_count = sum(1 for term in query_terms if term in content_terms)
            relevance_factor = relevance_count / len(query_terms) if query_terms else 0
            
            # Apply amplitude amplification
            amplification_factor = 1 + relevance_factor * 0.5
            
            # Additional quantum boost for quantum-enhanced docs
            if doc.quantum_enhanced:
                amplification_factor *= 1.2
            
            # Apply coherence effects
            coherence_factor = 1 - self.decoherence_level * 0.1
            
            amplified_score = score * amplification_factor * coherence_factor
            amplified_results.append((doc, amplified_score))
        
        return amplified_results
    
    async def _grovers_inspired_search(
        self,
        candidates: List[Tuple[QuantumDocument, float]],
        query: str
    ) -> List[Tuple[QuantumDocument, float]]:
        """Apply Grover's algorithm-inspired search enhancement."""
        # Simulate Grover's oracle for document selection
        target_threshold = self.similarity_threshold
        
        enhanced_results = []
        for doc, score in candidates:
            # Oracle function: boost if above threshold
            if score >= target_threshold:
                # Grover's amplification effect
                grover_boost = 1.4  # Simulated quadratic speedup effect
                enhanced_score = min(1.0, score * grover_boost)
            else:
                # Slight suppression for below-threshold results
                enhanced_score = score * 0.9
            
            # Apply quantum coherence
            coherence_factor = 1 - self.decoherence_level * 0.05
            final_score = enhanced_score * coherence_factor
            
            enhanced_results.append((doc, final_score))
        
        return enhanced_results
