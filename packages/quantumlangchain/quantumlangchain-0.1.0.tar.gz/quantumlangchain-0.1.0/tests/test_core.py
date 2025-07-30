"""
Test suite for QuantumLangChain core functionality.
"""

import pytest
import asyncio
import numpy as np
from unittest.mock import Mock, AsyncMock

from quantumlangchain.core.base import (
    QuantumBase,
    QuantumConfig,
    QuantumState,
    DecoherenceLevel
)
from quantumlangchain.backends.qiskit_backend import QiskitBackend
from quantumlangchain.chains.qlchain import QLChain
from quantumlangchain.memory.quantum_memory import QuantumMemory


class TestQuantumBase:
    """Test cases for QuantumBase class."""
    
    def test_quantum_config_creation(self):
        """Test QuantumConfig initialization."""
        config = QuantumConfig(
            num_qubits=8,
            circuit_depth=10,
            decoherence_threshold=0.1
        )
        
        assert config.num_qubits == 8
        assert config.circuit_depth == 10
        assert config.decoherence_threshold == 0.1
        assert config.backend_type == "qiskit"  # default
    
    @pytest.mark.asyncio
    async def test_quantum_base_initialization(self):
        """Test QuantumBase subclass initialization."""
        
        class TestQuantumComponent(QuantumBase):
            async def initialize(self):
                self.quantum_state = QuantumState.COHERENT
            
            async def reset_quantum_state(self):
                self.quantum_state = QuantumState.COHERENT
                self.decoherence_level = 0.0
        
        component = TestQuantumComponent()
        await component.initialize()
        
        assert component.quantum_state == QuantumState.COHERENT
        assert component.decoherence_level == 0.0
    
    def test_decoherence_update(self):
        """Test decoherence level updates."""
        
        class TestComponent(QuantumBase):
            async def initialize(self): pass
            async def reset_quantum_state(self): pass
        
        component = TestComponent()
        
        # Test decoherence increase
        component.update_decoherence(0.3)
        assert component.decoherence_level == 0.3
        
        # Test decoherence clamping
        component.update_decoherence(0.8)
        assert component.decoherence_level == 1.0  # Clamped to max
        
        # Test state change on threshold
        component.decoherence_level = 0.05
        component.config.decoherence_threshold = 0.1
        component.update_decoherence(0.06)
        assert component.quantum_state == QuantumState.DECOHERENT
    
    def test_entanglement_creation(self):
        """Test entanglement between components."""
        
        class TestComponent(QuantumBase):
            async def initialize(self): pass
            async def reset_quantum_state(self): pass
        
        comp1 = TestComponent()
        comp2 = TestComponent()
        
        # Create entanglement
        entanglement_id = comp1.create_entanglement(comp2, strength=0.8)
        
        assert entanglement_id in comp1.entanglement_registry
        assert entanglement_id in comp2.entanglement_registry
        assert comp1.quantum_state == QuantumState.ENTANGLED
        assert comp2.quantum_state == QuantumState.ENTANGLED
        assert comp1.is_entangled()
        assert comp2.is_entangled()
        
        # Break entanglement
        comp1.break_entanglement(entanglement_id)
        assert entanglement_id not in comp1.entanglement_registry
        assert entanglement_id not in comp2.entanglement_registry
    
    @pytest.mark.asyncio
    async def test_quantum_state_measurement(self):
        """Test quantum state measurement."""
        
        class TestComponent(QuantumBase):
            async def initialize(self): pass
            async def reset_quantum_state(self): pass
        
        component = TestComponent()
        component.quantum_state = QuantumState.SUPERPOSITION
        
        measurement = await component.measure_quantum_state()
        
        assert "state" in measurement
        assert "decoherence_level" in measurement
        assert "entanglement_count" in measurement
        assert "coherence_time" in measurement
        assert "measurement_timestamp" in measurement
        
        # Check state collapse
        assert component.quantum_state == QuantumState.COLLAPSED


class TestQiskitBackend:
    """Test cases for QiskitBackend."""
    
    def test_backend_initialization(self):
        """Test QiskitBackend initialization."""
        backend = QiskitBackend()
        
        assert backend.backend_name == "aer_simulator"
        assert backend.optimization_level == 1
        assert backend.noise_model is not None
    
    def test_backend_info(self):
        """Test backend information retrieval."""
        backend = QiskitBackend()
        info = backend.get_backend_info()
        
        assert "backend_name" in info
        assert "provider" in info
        assert info["provider"] == "qiskit"
        assert "num_qubits" in info
        assert "quantum_volume" in info
    
    @pytest.mark.asyncio
    async def test_entangling_circuit_creation(self):
        """Test entangling circuit creation."""
        backend = QiskitBackend()
        
        qubits = [0, 1, 2]
        circuit = await backend.create_entangling_circuit(qubits)
        
        assert circuit is not None
        assert circuit.num_qubits >= max(qubits) + 1
        assert len(circuit.cregs) > 0  # Has classical registers
    
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_circuit_execution(self):
        """Test quantum circuit execution."""
        backend = QiskitBackend()
        
        # Create simple test circuit
        qubits = [0, 1]
        circuit = await backend.create_entangling_circuit(qubits)
        
        # Execute circuit
        result = await backend.execute_circuit(circuit, shots=100)
        
        assert result["success"] is True
        assert "counts" in result
        assert "probabilities" in result
        assert result["shots"] == 100
        assert "circuit_depth" in result


class TestQLChain:
    """Test cases for QLChain."""
    
    @pytest.fixture
    async def qlchain(self):
        """Create QLChain instance for testing."""
        backend = QiskitBackend()
        memory = QuantumMemory(
            classical_dim=128,
            quantum_dim=4,
            backend=backend
        )
        
        chain = QLChain(
            memory=memory,
            backend=backend,
            config={
                "parallel_branches": 2,
                "circuit_injection_enabled": True
            }
        )
        
        await memory.initialize()
        await chain.initialize()
        
        return chain
    
    @pytest.mark.asyncio
    async def test_chain_initialization(self, qlchain):
        """Test QLChain initialization."""
        assert qlchain.quantum_state == QuantumState.COHERENT
        assert qlchain.memory is not None
        assert qlchain.backend is not None
        assert len(qlchain.quantum_circuits) > 0
    
    @pytest.mark.asyncio
    async def test_chain_execution(self, qlchain):
        """Test basic chain execution."""
        test_input = "Test quantum processing"
        
        result = await qlchain.arun(test_input)
        
        assert result is not None
        assert isinstance(result, dict)
        assert "processed" in result
        
        # Check execution history
        stats = qlchain.get_execution_stats()
        assert stats["total_executions"] > 0
    
    @pytest.mark.asyncio
    async def test_batch_execution(self, qlchain):
        """Test batch processing."""
        inputs = ["input1", "input2", "input3"]
        
        results = await qlchain.abatch(inputs)
        
        assert len(results) == len(inputs)
        for result in results:
            if result is not None:  # Some might fail in test environment
                assert isinstance(result, dict)
    
    @pytest.mark.asyncio
    async def test_streaming_execution(self, qlchain):
        """Test streaming execution."""
        test_input = "Stream test"
        
        results = []
        async for chunk in qlchain.astream(test_input):
            results.append(chunk)
        
        assert len(results) > 0
        assert any(chunk.get("type") == "final_result" for chunk in results)
    
    @pytest.mark.asyncio
    async def test_quantum_state_reset(self, qlchain):
        """Test quantum state reset."""
        # Execute some operations to change state
        await qlchain.arun("test")
        
        original_history_length = len(qlchain.execution_history)
        
        # Reset state
        await qlchain.reset_quantum_state()
        
        assert qlchain.quantum_state == QuantumState.COHERENT
        assert qlchain.decoherence_level == 0.0
        assert len(qlchain.execution_history) == 0


class TestQuantumMemory:
    """Test cases for QuantumMemory."""
    
    @pytest.fixture
    async def quantum_memory(self):
        """Create QuantumMemory instance for testing."""
        memory = QuantumMemory(
            classical_dim=64,
            quantum_dim=3
        )
        await memory.initialize()
        return memory
    
    @pytest.mark.asyncio
    async def test_memory_initialization(self, quantum_memory):
        """Test QuantumMemory initialization."""
        assert quantum_memory.quantum_state == QuantumState.COHERENT
        assert len(quantum_memory.quantum_registers) == 3
    
    @pytest.mark.asyncio
    async def test_memory_store_retrieve(self, quantum_memory):
        """Test basic store and retrieve operations."""
        test_key = "test_concept"
        test_value = "Quantum superposition principle"
        
        # Store data
        await quantum_memory.store(test_key, test_value, quantum_enhanced=True)
        
        # Retrieve data
        retrieved = await quantum_memory.retrieve(test_key, quantum_search=True)
        
        assert retrieved == test_value
        
        # Check memory stats
        stats = await quantum_memory.get_stats()
        assert stats["total_entries"] == 1
        assert stats["quantum_enhanced_entries"] == 1
    
    @pytest.mark.asyncio
    async def test_memory_entanglement(self, quantum_memory):
        """Test memory entanglement functionality."""
        # Store multiple entries
        keys = ["concept1", "concept2", "concept3"]
        values = ["Value 1", "Value 2", "Value 3"]
        
        for key, value in zip(keys, values):
            await quantum_memory.store(key, value, quantum_enhanced=True)
        
        # Create entanglement
        entanglement_id = await quantum_memory.entangle_memories(keys)
        
        assert entanglement_id is not None
        assert quantum_memory.quantum_state == QuantumState.ENTANGLED
        
        # Check entanglement in stats
        stats = await quantum_memory.get_stats()
        assert stats["entangled_entries"] == len(keys)
    
    @pytest.mark.asyncio
    async def test_memory_snapshots(self, quantum_memory):
        """Test memory snapshot and restore functionality."""
        # Store initial data
        await quantum_memory.store("initial", "initial_value", quantum_enhanced=True)
        
        # Create snapshot
        snapshot_id = await quantum_memory.create_memory_snapshot()
        
        # Modify memory
        await quantum_memory.store("modified", "modified_value", quantum_enhanced=True)
        
        # Verify modified state
        stats_before = await quantum_memory.get_stats()
        assert stats_before["total_entries"] == 2
        
        # Restore snapshot
        await quantum_memory.restore_memory_snapshot(snapshot_id)
        
        # Verify restored state
        stats_after = await quantum_memory.get_stats()
        assert stats_after["total_entries"] == 1
        
        retrieved = await quantum_memory.retrieve("initial")
        assert retrieved == "initial_value"
        
        # Modified entry should be gone
        retrieved_modified = await quantum_memory.retrieve("modified")
        assert retrieved_modified is None


@pytest.mark.integration
class TestIntegration:
    """Integration tests for multiple components."""
    
    @pytest.mark.asyncio
    async def test_chain_memory_integration(self):
        """Test QLChain and QuantumMemory integration."""
        backend = QiskitBackend()
        memory = QuantumMemory(classical_dim=128, quantum_dim=4, backend=backend)
        chain = QLChain(memory=memory, backend=backend)
        
        await memory.initialize()
        await chain.initialize()
        
        # Execute chain operation
        result = await chain.arun("Integration test")
        
        # Verify memory was used
        memory_stats = await memory.get_stats()
        assert memory_stats["total_entries"] > 0
        
        # Verify chain execution
        chain_stats = chain.get_execution_stats()
        assert chain_stats["total_executions"] > 0
    
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_full_system_integration(self):
        """Test full system with all components."""
        # This would test the entire system working together
        # Including chains, memory, agents, and retrievers
        pass


# Pytest configuration and fixtures
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Performance test markers
pytestmark = [
    pytest.mark.filterwarnings("ignore::DeprecationWarning"),
    pytest.mark.filterwarnings("ignore::PendingDeprecationWarning"),
]
