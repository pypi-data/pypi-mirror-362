"""
Base classes and interfaces for QuantumLangChain.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, AsyncIterator
from pydantic import BaseModel, Field
import asyncio
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class QuantumState(Enum):
    """Quantum state enumeration."""
    COHERENT = "coherent"
    DECOHERENT = "decoherent"
    ENTANGLED = "entangled"
    SUPERPOSITION = "superposition"
    COLLAPSED = "collapsed"


class DecoherenceLevel(Enum):
    """Decoherence severity levels."""
    LOW = 0.1
    MEDIUM = 0.3
    HIGH = 0.7
    CRITICAL = 0.9


class QuantumConfig(BaseModel):
    """Configuration for quantum operations."""
    
    backend_type: str = Field(default="qiskit", description="Quantum backend to use")
    num_qubits: int = Field(default=8, description="Number of qubits")
    circuit_depth: int = Field(default=10, description="Maximum circuit depth")
    decoherence_threshold: float = Field(default=0.1, description="Decoherence threshold")
    entanglement_degree: int = Field(default=2, description="Degree of entanglement")
    measurement_shots: int = Field(default=1024, description="Number of measurement shots")
    noise_model: Optional[Dict[str, Any]] = Field(default=None, description="Noise model parameters")
    error_correction: bool = Field(default=True, description="Enable quantum error correction")
    
    class Config:
        """Pydantic configuration."""
        extra = "allow"


class QuantumBase(ABC, BaseModel):
    """
    Abstract base class for all quantum-enhanced components.
    
    Provides common functionality for quantum state management,
    decoherence tracking, and backend abstraction.
    """
    
    config: QuantumConfig = Field(default_factory=QuantumConfig)
    quantum_state: QuantumState = Field(default=QuantumState.COHERENT)
    decoherence_level: float = Field(default=0.0)
    entanglement_registry: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True
        extra = "allow"
    
    def __init__(self, **data):
        super().__init__(**data)
        self._setup_logging()
        
    def _setup_logging(self) -> None:
        """Setup component-specific logging."""
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the quantum component."""
        pass
    
    @abstractmethod
    async def reset_quantum_state(self) -> None:
        """Reset quantum state to initial conditions."""
        pass
    
    def update_decoherence(self, delta: float) -> None:
        """Update decoherence level."""
        self.decoherence_level = min(1.0, max(0.0, self.decoherence_level + delta))
        
        if self.decoherence_level > self.config.decoherence_threshold:
            self.quantum_state = QuantumState.DECOHERENT
            self.logger.warning(f"Decoherence threshold exceeded: {self.decoherence_level}")
    
    def create_entanglement(self, other: "QuantumBase", strength: float = 1.0) -> str:
        """Create entanglement with another quantum component."""
        entanglement_id = f"entangle_{id(self)}_{id(other)}"
        
        self.entanglement_registry[entanglement_id] = {
            "partner": other,
            "strength": strength,
            "creation_time": asyncio.get_event_loop().time()
        }
        
        other.entanglement_registry[entanglement_id] = {
            "partner": self,
            "strength": strength,
            "creation_time": asyncio.get_event_loop().time()
        }
        
        self.quantum_state = QuantumState.ENTANGLED
        other.quantum_state = QuantumState.ENTANGLED
        
        self.logger.info(f"Entanglement created: {entanglement_id}")
        return entanglement_id
    
    def break_entanglement(self, entanglement_id: str) -> None:
        """Break an existing entanglement."""
        if entanglement_id in self.entanglement_registry:
            partner = self.entanglement_registry[entanglement_id]["partner"]
            
            del self.entanglement_registry[entanglement_id]
            if entanglement_id in partner.entanglement_registry:
                del partner.entanglement_registry[entanglement_id]
            
            self.logger.info(f"Entanglement broken: {entanglement_id}")
    
    def is_entangled(self) -> bool:
        """Check if component is entangled."""
        return len(self.entanglement_registry) > 0
    
    def get_entangled_partners(self) -> List["QuantumBase"]:
        """Get list of entangled partners."""
        return [entry["partner"] for entry in self.entanglement_registry.values()]
    
    async def measure_quantum_state(self) -> Dict[str, Any]:
        """Measure current quantum state."""
        measurement = {
            "state": self.quantum_state.value,
            "decoherence_level": self.decoherence_level,
            "entanglement_count": len(self.entanglement_registry),
            "coherence_time": 1.0 - self.decoherence_level,
            "measurement_timestamp": asyncio.get_event_loop().time()
        }
        
        # Measurement causes state collapse in superposition
        if self.quantum_state == QuantumState.SUPERPOSITION:
            self.quantum_state = QuantumState.COLLAPSED
        
        return measurement
    
    def enter_superposition(self) -> None:
        """Enter quantum superposition state."""
        if self.decoherence_level < self.config.decoherence_threshold:
            self.quantum_state = QuantumState.SUPERPOSITION
            self.logger.debug("Entered superposition state")
        else:
            self.logger.warning("Cannot enter superposition: decoherence too high")
    
    def apply_noise(self, noise_strength: float = 0.1) -> None:
        """Apply quantum noise to the system."""
        self.update_decoherence(noise_strength)
        
        # Noise affects entangled partners
        for partner in self.get_entangled_partners():
            partner.update_decoherence(noise_strength * 0.5)  # Reduced effect on partners


class QuantumBackend(ABC):
    """Abstract base class for quantum computing backends."""
    
    @abstractmethod
    async def execute_circuit(self, circuit: Any, shots: int = 1024) -> Dict[str, Any]:
        """Execute a quantum circuit."""
        pass
    
    @abstractmethod
    async def create_entangling_circuit(self, qubits: List[int]) -> Any:
        """Create an entangling quantum circuit."""
        pass
    
    @abstractmethod
    async def measure_qubits(self, circuit: Any, qubits: List[int]) -> Dict[str, int]:
        """Measure specified qubits."""
        pass
    
    @abstractmethod
    def get_backend_info(self) -> Dict[str, Any]:
        """Get backend information."""
        pass


class QuantumMemoryInterface(ABC):
    """Interface for quantum memory systems."""
    
    @abstractmethod
    async def store(self, key: str, value: Any, quantum_enhanced: bool = True) -> None:
        """Store data with optional quantum enhancement."""
        pass
    
    @abstractmethod
    async def retrieve(self, key: str, quantum_search: bool = True) -> Any:
        """Retrieve data with optional quantum search."""
        pass
    
    @abstractmethod
    async def entangle_memories(self, keys: List[str]) -> str:
        """Create entanglement between memory entries."""
        pass
    
    @abstractmethod
    async def create_memory_snapshot(self) -> str:
        """Create a snapshot of current memory state."""
        pass
    
    @abstractmethod
    async def restore_memory_snapshot(self, snapshot_id: str) -> None:
        """Restore memory from a snapshot."""
        pass


class QuantumChainInterface(ABC):
    """Interface for quantum-enhanced chains."""
    
    @abstractmethod
    async def arun(self, input_data: Any) -> Any:
        """Run the chain asynchronously."""
        pass
    
    @abstractmethod
    async def abatch(self, inputs: List[Any]) -> List[Any]:
        """Run the chain on a batch of inputs."""
        pass
    
    @abstractmethod
    async def astream(self, input_data: Any) -> AsyncIterator[Any]:
        """Stream chain execution."""
        pass


class QuantumAgentInterface(ABC):
    """Interface for quantum-enhanced agents."""
    
    @abstractmethod
    async def act(self, observation: Any) -> Any:
        """Take action based on observation."""
        pass
    
    @abstractmethod
    async def collaborate(self, other_agents: List["QuantumAgentInterface"]) -> Any:
        """Collaborate with other agents."""
        pass
    
    @abstractmethod
    async def share_belief_state(self, belief: Any) -> None:
        """Share belief state with entangled agents."""
        pass
