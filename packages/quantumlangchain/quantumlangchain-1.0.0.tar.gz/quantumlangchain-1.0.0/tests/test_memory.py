"""
Test cases for QuantumMemory functionality.
"""

import pytest
import asyncio
import numpy as np
from unittest.mock import AsyncMock, Mock, patch

from quantumlangchain.memory.quantum_memory import (
    QuantumMemory,
    MemoryEntry,
    MemorySnapshot
)
from quantumlangchain.core.base import QuantumState


class TestMemoryEntry:
    """Test cases for MemoryEntry class."""
    
    def test_memory_entry_creation(self):
        """Test MemoryEntry initialization."""
        entry = MemoryEntry(
            key="test_key",
            value="test_value",
            embedding=np.array([0.1, 0.2, 0.3]),
            quantum_enhanced=True
        )
        
        assert entry.key == "test_key"
        assert entry.value == "test_value"
        assert np.array_equal(entry.embedding, np.array([0.1, 0.2, 0.3]))
        assert entry.quantum_enhanced is True
        assert entry.timestamp is not None
        assert entry.retrieval_count == 0
    
    def test_memory_entry_retrieval_tracking(self):
        """Test retrieval count tracking."""
        entry = MemoryEntry("key", "value")
        
        # Initial state
        assert entry.retrieval_count == 0
        assert entry.last_retrieved is None
        
        # After retrieval
        entry.increment_retrieval()
        assert entry.retrieval_count == 1
        assert entry.last_retrieved is not None
        
        # Multiple retrievals
        entry.increment_retrieval()
        entry.increment_retrieval()
        assert entry.retrieval_count == 3


class TestQuantumMemory:
    """Test cases for QuantumMemory class."""
    
    @pytest.fixture
    async def memory(self, mock_quantum_backend):
        """Create QuantumMemory instance for testing."""
        memory = QuantumMemory(
            classical_dim=64,
            quantum_dim=3,
            backend=mock_quantum_backend
        )
        await memory.initialize()
        return memory
    
    @pytest.mark.asyncio
    async def test_memory_initialization(self, memory):
        """Test QuantumMemory initialization."""
        assert memory.classical_dim == 64
        assert memory.quantum_dim == 3
        assert len(memory.quantum_registers) == 3
        assert memory.quantum_state == QuantumState.COHERENT
        assert len(memory.memory_store) == 0
    
    @pytest.mark.asyncio
    async def test_basic_store_retrieve(self, memory):
        """Test basic store and retrieve operations."""
        # Store without quantum enhancement
        await memory.store("key1", "value1", quantum_enhanced=False)
        
        # Store with quantum enhancement
        await memory.store("key2", "value2", quantum_enhanced=True)
        
        # Retrieve data
        value1 = await memory.retrieve("key1")
        value2 = await memory.retrieve("key2", quantum_search=True)
        
        assert value1 == "value1"
        assert value2 == "value2"
        
        # Check memory stats
        stats = await memory.get_stats()
        assert stats["total_entries"] == 2
        assert stats["quantum_enhanced_entries"] == 1
    
    @pytest.mark.asyncio
    async def test_similarity_search(self, memory):
        """Test similarity-based retrieval."""
        # Store multiple similar entries
        entries = [
            ("quantum_physics", "Quantum mechanics principles"),
            ("classical_physics", "Newton's laws of motion"),
            ("quantum_computing", "Quantum algorithms and circuits"),
            ("machine_learning", "Neural networks and AI")
        ]
        
        for key, value in entries:
            await memory.store(key, value, quantum_enhanced=True)
        
        # Search for quantum-related content
        results = await memory.similarity_search(
            query="quantum superposition",
            top_k=2
        )
        
        assert len(results) <= 2
        assert all(isinstance(result, dict) for result in results)
        
        # Check that quantum-related entries rank higher
        quantum_keys = ["quantum_physics", "quantum_computing"]
        found_keys = [result["key"] for result in results if result["key"] in quantum_keys]
        assert len(found_keys) > 0
    
    @pytest.mark.asyncio
    async def test_memory_entanglement(self, memory):
        """Test memory entanglement functionality."""
        # Store test entries
        keys = ["concept1", "concept2", "concept3"]
        values = ["Value 1", "Value 2", "Value 3"]
        
        for key, value in zip(keys, values):
            await memory.store(key, value, quantum_enhanced=True)
        
        # Create entanglement
        entanglement_id = await memory.entangle_memories(keys)
        
        assert entanglement_id is not None
        assert memory.quantum_state == QuantumState.ENTANGLED
        
        # Verify entanglement in memory entries
        for key in keys:
            entry = memory.memory_store[key]
            assert entanglement_id in entry.entanglement_ids
        
        # Break entanglement
        await memory.break_entanglement(entanglement_id)
        
        # Verify entanglement is broken
        for key in keys:
            entry = memory.memory_store[key]
            assert entanglement_id not in entry.entanglement_ids
    
    @pytest.mark.asyncio
    async def test_memory_snapshots(self, memory):
        """Test memory snapshot and restore functionality."""
        # Store initial data
        await memory.store("initial1", "value1", quantum_enhanced=True)
        await memory.store("initial2", "value2", quantum_enhanced=False)
        
        # Create snapshot
        snapshot_id = await memory.create_memory_snapshot()
        assert snapshot_id is not None
        
        # Modify memory after snapshot
        await memory.store("new_entry", "new_value", quantum_enhanced=True)
        await memory.delete("initial1")
        
        # Verify modified state
        assert await memory.retrieve("new_entry") == "new_value"
        assert await memory.retrieve("initial1") is None
        assert await memory.retrieve("initial2") == "value2"
        
        # Restore snapshot
        await memory.restore_memory_snapshot(snapshot_id)
        
        # Verify restored state
        assert await memory.retrieve("initial1") == "value1"
        assert await memory.retrieve("initial2") == "value2"
        assert await memory.retrieve("new_entry") is None
    
    @pytest.mark.asyncio
    async def test_memory_delete(self, memory):
        """Test memory deletion functionality."""
        # Store test data
        await memory.store("delete_me", "test_value", quantum_enhanced=True)
        await memory.store("keep_me", "keep_value", quantum_enhanced=False)
        
        # Verify data exists
        assert await memory.retrieve("delete_me") == "test_value"
        assert await memory.retrieve("keep_me") == "keep_value"
        
        # Delete one entry
        success = await memory.delete("delete_me")
        assert success is True
        
        # Verify deletion
        assert await memory.retrieve("delete_me") is None
        assert await memory.retrieve("keep_me") == "keep_value"
        
        # Try to delete non-existent entry
        success = await memory.delete("non_existent")
        assert success is False
    
    @pytest.mark.asyncio
    async def test_memory_clear(self, memory):
        """Test memory clearing functionality."""
        # Store test data
        await memory.store("key1", "value1")
        await memory.store("key2", "value2")
        await memory.store("key3", "value3")
        
        # Verify data exists
        stats_before = await memory.get_stats()
        assert stats_before["total_entries"] == 3
        
        # Clear memory
        await memory.clear()
        
        # Verify memory is cleared
        stats_after = await memory.get_stats()
        assert stats_after["total_entries"] == 0
        
        # Verify quantum state is reset
        assert memory.quantum_state == QuantumState.COHERENT
        assert memory.decoherence_level == 0.0
    
    @pytest.mark.asyncio
    async def test_memory_update(self, memory):
        """Test memory update functionality."""
        # Store initial data
        await memory.store("update_key", "initial_value", quantum_enhanced=True)
        
        # Verify initial value
        assert await memory.retrieve("update_key") == "initial_value"
        
        # Update value
        await memory.update("update_key", "updated_value", quantum_enhanced=False)
        
        # Verify updated value
        assert await memory.retrieve("update_key") == "updated_value"
        
        # Try to update non-existent key
        with pytest.raises(KeyError):
            await memory.update("non_existent", "value")
    
    @pytest.mark.asyncio
    async def test_memory_stats(self, memory):
        """Test memory statistics functionality."""
        # Initial stats
        stats = await memory.get_stats()
        assert stats["total_entries"] == 0
        assert stats["quantum_enhanced_entries"] == 0
        assert stats["entangled_entries"] == 0
        assert stats["total_retrievals"] == 0
        
        # Add entries
        await memory.store("key1", "value1", quantum_enhanced=True)
        await memory.store("key2", "value2", quantum_enhanced=False)
        await memory.store("key3", "value3", quantum_enhanced=True)
        
        # Create entanglement
        await memory.entangle_memories(["key1", "key3"])
        
        # Perform retrievals
        await memory.retrieve("key1")
        await memory.retrieve("key2")
        await memory.retrieve("key1")  # Second retrieval
        
        # Check updated stats
        stats = await memory.get_stats()
        assert stats["total_entries"] == 3
        assert stats["quantum_enhanced_entries"] == 2
        assert stats["entangled_entries"] == 2
        assert stats["total_retrievals"] == 3
        assert stats["average_embedding_magnitude"] > 0
    
    @pytest.mark.asyncio
    async def test_quantum_coherence_tracking(self, memory):
        """Test quantum coherence tracking."""
        # Initial coherence should be high
        assert memory.decoherence_level == 0.0
        assert memory.quantum_state == QuantumState.COHERENT
        
        # Perform operations that cause decoherence
        for i in range(10):
            await memory.store(f"key{i}", f"value{i}", quantum_enhanced=True)
            await memory.retrieve(f"key{i}", quantum_search=True)
        
        # Decoherence should have increased
        assert memory.decoherence_level > 0.0
        
        # Reset quantum state
        await memory.reset_quantum_state()
        assert memory.decoherence_level == 0.0
        assert memory.quantum_state == QuantumState.COHERENT
    
    @pytest.mark.asyncio
    async def test_memory_persistence(self, memory, tmp_path):
        """Test memory persistence to disk."""
        # Store test data
        await memory.store("persist1", "value1", quantum_enhanced=True)
        await memory.store("persist2", "value2", quantum_enhanced=False)
        
        # Create snapshot for persistence
        snapshot_id = await memory.create_memory_snapshot()
        
        # Clear memory
        await memory.clear()
        assert (await memory.get_stats())["total_entries"] == 0
        
        # Restore from snapshot
        await memory.restore_memory_snapshot(snapshot_id)
        
        # Verify data is restored
        assert await memory.retrieve("persist1") == "value1"
        assert await memory.retrieve("persist2") == "value2"
        stats = await memory.get_stats()
        assert stats["total_entries"] == 2


class TestMemoryEdgeCases:
    """Test edge cases and error conditions."""
    
    @pytest.mark.asyncio
    async def test_invalid_operations(self, mock_quantum_backend):
        """Test invalid operations and error handling."""
        memory = QuantumMemory(classical_dim=32, quantum_dim=2, backend=mock_quantum_backend)
        await memory.initialize()
        
        # Try to retrieve non-existent key
        result = await memory.retrieve("non_existent")
        assert result is None
        
        # Try to entangle non-existent memories
        with pytest.raises(KeyError):
            await memory.entangle_memories(["non_existent1", "non_existent2"])
        
        # Try to restore non-existent snapshot
        with pytest.raises(KeyError):
            await memory.restore_memory_snapshot("invalid_snapshot_id")
    
    @pytest.mark.asyncio
    async def test_large_memory_operations(self, mock_quantum_backend):
        """Test operations with large amounts of data."""
        memory = QuantumMemory(classical_dim=128, quantum_dim=4, backend=mock_quantum_backend)
        await memory.initialize()
        
        # Store many entries
        num_entries = 100
        for i in range(num_entries):
            await memory.store(f"key_{i:03d}", f"value_{i}", quantum_enhanced=(i % 2 == 0))
        
        # Verify all entries
        stats = await memory.get_stats()
        assert stats["total_entries"] == num_entries
        assert stats["quantum_enhanced_entries"] == num_entries // 2
        
        # Test bulk retrieval
        retrieved_count = 0
        for i in range(num_entries):
            value = await memory.retrieve(f"key_{i:03d}")
            if value is not None:
                retrieved_count += 1
        
        assert retrieved_count == num_entries
    
    @pytest.mark.asyncio
    async def test_concurrent_operations(self, mock_quantum_backend):
        """Test concurrent memory operations."""
        memory = QuantumMemory(classical_dim=64, quantum_dim=3, backend=mock_quantum_backend)
        await memory.initialize()
        
        # Concurrent store operations
        store_tasks = [
            memory.store(f"concurrent_{i}", f"value_{i}", quantum_enhanced=True)
            for i in range(10)
        ]
        await asyncio.gather(*store_tasks)
        
        # Concurrent retrieve operations
        retrieve_tasks = [
            memory.retrieve(f"concurrent_{i}", quantum_search=True)
            for i in range(10)
        ]
        results = await asyncio.gather(*retrieve_tasks)
        
        # Verify results
        assert len(results) == 10
        assert all(result is not None for result in results)
        
        # Verify final state
        stats = await memory.get_stats()
        assert stats["total_entries"] == 10
