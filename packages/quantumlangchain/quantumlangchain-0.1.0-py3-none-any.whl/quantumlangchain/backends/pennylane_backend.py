"""
PennyLane backend implementation for QuantumLangChain.
"""

from typing import Any, Dict, List, Optional
import logging
import numpy as np

try:
    import pennylane as qml
    from pennylane import numpy as pnp
    PENNYLANE_AVAILABLE = True
except ImportError:
    PENNYLANE_AVAILABLE = False
    qml = None
    pnp = None

from quantumlangchain.core.base import QuantumBackend

logger = logging.getLogger(__name__)


class PennyLaneBackend(QuantumBackend):
    """PennyLane-based quantum backend implementation."""
    
    def __init__(
        self,
        device_name: str = "default.qubit",
        num_wires: int = 8,
        shots: Optional[int] = None,
        device_options: Optional[Dict[str, Any]] = None
    ):
        """Initialize PennyLane backend.
        
        Args:
            device_name: Name of the PennyLane device
            num_wires: Number of qubits/wires
            shots: Number of measurement shots (None for exact)
            device_options: Additional device options
        """
        if not PENNYLANE_AVAILABLE:
            raise ImportError("PennyLane is not available. Install with: pip install pennylane")
        
        self.device_name = device_name
        self.num_wires = num_wires
        self.shots = shots
        self.device_options = device_options or {}
        
        # Initialize device
        self.device = qml.device(
            device_name,
            wires=num_wires,
            shots=shots,
            **self.device_options
        )
        
        logger.info(f"Initialized PennyLane backend: {device_name} with {num_wires} wires")
    
    async def execute_circuit(self, circuit_func: callable, shots: int = 1024) -> Dict[str, Any]:
        """Execute a quantum circuit function.
        
        Args:
            circuit_func: PennyLane quantum function to execute
            shots: Number of measurement shots
            
        Returns:
            Execution results with measurements and metadata
        """
        try:
            # Create QNode
            qnode = qml.QNode(circuit_func, self.device)
            
            # Execute the circuit
            if shots and hasattr(self.device, 'shots'):
                # Update device shots if supported
                old_shots = self.device.shots
                self.device.shots = shots
                
            result = qnode()
            
            # Restore original shots
            if shots and hasattr(self.device, 'shots'):
                self.device.shots = old_shots
            
            # Format results
            if isinstance(result, (list, tuple, np.ndarray)):
                measurements = result
            else:
                measurements = [result]
            
            return {
                "measurements": measurements,
                "shots": shots or 1,
                "num_wires": self.num_wires,
                "success": True,
                "device_name": self.device_name
            }
            
        except Exception as e:
            logger.error(f"Circuit execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "measurements": []
            }
    
    async def create_entangling_circuit(self, qubits: List[int]) -> callable:
        """Create an entangling quantum circuit function.
        
        Args:
            qubits: List of qubit indices to entangle
            
        Returns:
            PennyLane quantum function with entangling gates
        """
        def entangling_circuit():
            # Create entanglement pattern
            if len(qubits) >= 2:
                # Bell state preparation for pairs
                for i in range(0, len(qubits)-1, 2):
                    if i+1 < len(qubits):
                        qubit1, qubit2 = qubits[i], qubits[i+1]
                        qml.Hadamard(wires=qubit1)
                        qml.CNOT(wires=[qubit1, qubit2])
                
                # Additional entanglement for complex patterns
                if len(qubits) > 2:
                    for i in range(len(qubits)-1):
                        qml.CZ(wires=[qubits[i], qubits[(i+1) % len(qubits)]])
            
            # Return measurements
            return [qml.expval(qml.PauliZ(wires=q)) for q in qubits]
        
        return entangling_circuit
    
    async def measure_qubits(self, circuit_func: callable, qubits: List[int]) -> Dict[str, int]:
        """Measure specified qubits.
        
        Args:
            circuit_func: PennyLane circuit function
            qubits: List of qubit indices to measure
            
        Returns:
            Measurement results
        """
        def measuring_circuit():
            # Execute the original circuit
            circuit_func()
            
            # Return probability measurements
            return [qml.probs(wires=q) for q in qubits]
        
        # Execute and return results  
        result = await self.execute_circuit(measuring_circuit)
        
        # Convert probabilities to counts (simulated)
        if result.get("success", False):
            measurements = result.get("measurements", [])
            shots = result.get("shots", 1024)
            
            counts = {}
            for i, probs in enumerate(measurements):
                if len(probs) == 2:  # Single qubit
                    count_0 = int(probs[0] * shots)
                    count_1 = shots - count_0
                    counts[f"qubit_{qubits[i]}_0"] = count_0
                    counts[f"qubit_{qubits[i]}_1"] = count_1
            
            return counts
        
        return {}
    
    def get_backend_info(self) -> Dict[str, Any]:
        """Get backend information.
        
        Returns:
            Backend configuration and capabilities
        """
        return {
            "backend_name": self.device_name,
            "provider": "pennylane", 
            "num_wires": self.num_wires,
            "shots": self.shots,
            "supports_analytic": self.device.analytic,
            "supports_finite_shots": hasattr(self.device, 'shots'),
            "device_options": self.device_options,
            "short_name": getattr(self.device, 'short_name', self.device_name),
            "capabilities": getattr(self.device, 'capabilities', {}),
            "plugin_version": getattr(qml, '__version__', 'unknown') if qml else None
        }
    
    def create_variational_circuit(
        self, 
        num_qubits: int, 
        num_layers: int = 2,
        entangling_gates: str = "CNOT"
    ) -> callable:
        """Create a variational quantum circuit.
        
        Args:
            num_qubits: Number of qubits
            num_layers: Number of entangling layers
            entangling_gates: Type of entangling gates
            
        Returns:
            Parameterized variational circuit function
        """
        def variational_circuit(params):
            # Reshape parameters
            params = pnp.array(params).reshape(num_layers, num_qubits, 3)
            
            for layer in range(num_layers):
                # Rotation gates
                for qubit in range(num_qubits):
                    qml.RX(params[layer, qubit, 0], wires=qubit)
                    qml.RY(params[layer, qubit, 1], wires=qubit) 
                    qml.RZ(params[layer, qubit, 2], wires=qubit)
                
                # Entangling gates
                if entangling_gates.upper() == "CNOT":
                    for qubit in range(num_qubits - 1):
                        qml.CNOT(wires=[qubit, qubit + 1])
                elif entangling_gates.upper() == "CZ":
                    for qubit in range(num_qubits - 1):
                        qml.CZ(wires=[qubit, qubit + 1])
            
            # Return expectation values
            return [qml.expval(qml.PauliZ(wires=i)) for i in range(num_qubits)]
        
        return variational_circuit
    
    def create_quantum_embedding(self, data: List[float], num_qubits: int) -> callable:
        """Create quantum data embedding circuit.
        
        Args:
            data: Classical data to embed
            num_qubits: Number of qubits for embedding
            
        Returns:
            Quantum embedding circuit function
        """
        def embedding_circuit():
            # Normalize data to [0, 2π] range
            normalized_data = pnp.array(data) * 2 * pnp.pi
            
            # Amplitude embedding (simplified)
            for i, value in enumerate(normalized_data[:num_qubits]):
                qml.RY(value, wires=i)
            
            # Entangling embedding
            for i in range(min(len(normalized_data), num_qubits) - 1):
                qml.CNOT(wires=[i, i + 1])
            
            return [qml.expval(qml.PauliZ(wires=i)) for i in range(num_qubits)]
        
        return embedding_circuit
    
    def create_grover_diffusion_operator(self, num_qubits: int) -> callable:
        """Create Grover diffusion operator.
        
        Args:
            num_qubits: Number of qubits
            
        Returns:
            Diffusion operator circuit function
        """
        def diffusion_operator():
            # Apply Hadamard to all qubits
            for qubit in range(num_qubits):
                qml.Hadamard(wires=qubit)
            
            # Apply X to all qubits
            for qubit in range(num_qubits):
                qml.PauliX(wires=qubit)
            
            # Multi-controlled Z gate (phase flip)
            if num_qubits > 1:
                # Implement multi-controlled Z using CNOT and single Z
                controls = list(range(num_qubits - 1))
                target = num_qubits - 1
                
                # Build multi-controlled gate
                for i, control in enumerate(controls[:-1]):
                    qml.CNOT(wires=[control, controls[i+1]])
                
                qml.CZ(wires=[controls[-1], target])
                
                # Uncompute
                for i in reversed(range(len(controls)-1)):
                    qml.CNOT(wires=[controls[i], controls[i+1]])
            else:
                qml.PauliZ(wires=0)
            
            # Apply X to all qubits
            for qubit in range(num_qubits):
                qml.PauliX(wires=qubit)
            
            # Apply Hadamard to all qubits
            for qubit in range(num_qubits):
                qml.Hadamard(wires=qubit)
        
        return diffusion_operator
