"""
Qiskit backend implementation for QuantumLangChain.
"""

from typing import Any, Dict, List, Optional
import logging
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer.noise import NoiseModel, depolarizing_error
import numpy as np

from quantumlangchain.core.base import QuantumBackend

logger = logging.getLogger(__name__)


class QiskitBackend(QuantumBackend):
    """Qiskit-based quantum backend implementation."""
    
    def __init__(
        self,
        backend_name: str = "aer_simulator",
        noise_model: Optional[NoiseModel] = None,
        optimization_level: int = 1,
        max_credits: int = 10
    ):
        """Initialize Qiskit backend.
        
        Args:
            backend_name: Name of the Qiskit backend
            noise_model: Optional noise model for simulation
            optimization_level: Circuit optimization level (0-3)
            max_credits: Maximum credits for IBM Quantum
        """
        self.backend_name = backend_name
        self.noise_model = noise_model
        self.optimization_level = optimization_level
        self.max_credits = max_credits
        
        # Initialize simulator
        self.simulator = AerSimulator()
        
        # Create default noise model if none provided
        if self.noise_model is None:
            self.noise_model = self._create_default_noise_model()
        
        logger.info(f"Initialized Qiskit backend: {backend_name}")
    
    def _create_default_noise_model(self) -> NoiseModel:
        """Create a default noise model for simulation."""
        noise_model = NoiseModel()
        
        # Add depolarizing error to all single and two-qubit gates
        single_qubit_error = depolarizing_error(0.001, 1)
        two_qubit_error = depolarizing_error(0.01, 2)
        
        # Single-qubit gates
        noise_model.add_all_qubit_quantum_error(single_qubit_error, ['u1', 'u2', 'u3', 'rz', 'ry', 'rx'])
        
        # Two-qubit gates  
        noise_model.add_all_qubit_quantum_error(two_qubit_error, ['cx', 'cy', 'cz'])
        
        return noise_model
    
    async def execute_circuit(self, circuit: QuantumCircuit, shots: int = 1024) -> Dict[str, Any]:
        """Execute a quantum circuit.
        
        Args:
            circuit: Quantum circuit to execute
            shots: Number of measurement shots
            
        Returns:
            Execution results with counts and metadata
        """
        try:
            # Transpile circuit for the backend
            transpiled_circuit = transpile(
                circuit,
                backend=self.simulator,
                optimization_level=self.optimization_level
            )
            
            # Execute the circuit
            job = self.simulator.run(
                transpiled_circuit,
                shots=shots,
                noise_model=self.noise_model
            )
            
            result = job.result()
            counts = result.get_counts()
            
            # Calculate measurement probabilities
            total_shots = sum(counts.values())
            probabilities = {state: count/total_shots for state, count in counts.items()}
            
            return {
                "counts": counts,
                "probabilities": probabilities,
                "shots": total_shots,
                "circuit_depth": transpiled_circuit.depth(),
                "num_qubits": transpiled_circuit.num_qubits,
                "success": True,
                "execution_time": getattr(result, 'time_taken', 0.0)
            }
            
        except Exception as e:
            logger.error(f"Circuit execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "counts": {},
                "probabilities": {}
            }
    
    async def create_entangling_circuit(self, qubits: List[int]) -> QuantumCircuit:
        """Create an entangling quantum circuit.
        
        Args:
            qubits: List of qubit indices to entangle
            
        Returns:
            Quantum circuit with entangling gates
        """
        num_qubits = max(qubits) + 1 if qubits else 2
        
        # Create quantum and classical registers
        qreg = QuantumRegister(num_qubits, 'q')
        creg = ClassicalRegister(len(qubits), 'c')
        circuit = QuantumCircuit(qreg, creg)
        
        # Create entanglement pattern
        if len(qubits) >= 2:
            # Bell state preparation for pairs
            for i in range(0, len(qubits)-1, 2):
                if i+1 < len(qubits):
                    qubit1, qubit2 = qubits[i], qubits[i+1]
                    circuit.h(qubit1)  # Hadamard gate
                    circuit.cx(qubit1, qubit2)  # CNOT gate
            
            # Additional entanglement for more complex patterns
            if len(qubits) > 2:
                for i in range(len(qubits)-1):
                    circuit.cz(qubits[i], qubits[(i+1) % len(qubits)])
        
        # Add measurements
        for i, qubit in enumerate(qubits):
            circuit.measure(qubit, i)
        
        return circuit
    
    async def measure_qubits(self, circuit: QuantumCircuit, qubits: List[int]) -> Dict[str, int]:
        """Measure specified qubits.
        
        Args:
            circuit: Quantum circuit to measure
            qubits: List of qubit indices to measure
            
        Returns:
            Measurement results
        """
        # Create a copy of the circuit with measurements
        measured_circuit = circuit.copy()
        
        # Add classical register if not present
        if not measured_circuit.cregs:
            creg = ClassicalRegister(len(qubits), 'measurement')
            measured_circuit.add_register(creg)
        
        # Add measurement operations
        for i, qubit in enumerate(qubits):
            measured_circuit.measure(qubit, i)
        
        # Execute and return results
        result = await self.execute_circuit(measured_circuit)
        return result.get("counts", {})
    
    def get_backend_info(self) -> Dict[str, Any]:
        """Get backend information.
        
        Returns:
            Backend configuration and capabilities
        """
        return {
            "backend_name": self.backend_name,
            "provider": "qiskit",
            "simulator": True,
            "num_qubits": getattr(self.simulator.configuration(), 'n_qubits', 32),
            "coupling_map": getattr(self.simulator.configuration(), 'coupling_map', None),
            "basis_gates": getattr(self.simulator.configuration(), 'basis_gates', []),
            "noise_model_enabled": self.noise_model is not None,
            "optimization_level": self.optimization_level,
            "supports_pulse": False,
            "max_shots": getattr(self.simulator.configuration(), 'max_shots', 1024000),
            "quantum_volume": 32  # Simulated quantum volume
        }
    
    def create_variational_circuit(self, num_qubits: int, num_layers: int = 2) -> QuantumCircuit:
        """Create a variational quantum circuit.
        
        Args:
            num_qubits: Number of qubits
            num_layers: Number of entangling layers
            
        Returns:
            Parameterized variational circuit
        """
        # Use EfficientSU2 ansatz
        circuit = EfficientSU2(num_qubits, reps=num_layers, entanglement='linear')
        
        # Add classical register for measurements
        creg = ClassicalRegister(num_qubits, 'c')
        circuit.add_register(creg)
        
        return circuit
    
    def create_grover_oracle(self, marked_items: List[str], num_qubits: int) -> QuantumCircuit:
        """Create a Grover search oracle.
        
        Args:
            marked_items: Items to mark in the search space
            num_qubits: Number of qubits in the search space
            
        Returns:
            Oracle circuit for Grover's algorithm
        """
        qreg = QuantumRegister(num_qubits, 'q')
        oracle = QuantumCircuit(qreg, name='oracle')
        
        # Convert marked items to binary representations
        for item in marked_items:
            if isinstance(item, str) and item.startswith('0b'):
                # Binary string format
                binary = item[2:].zfill(num_qubits)
            elif isinstance(item, int):
                # Integer format
                binary = format(item, f'0{num_qubits}b')
            else:
                # Hash to binary
                binary = format(hash(item) % (2**num_qubits), f'0{num_qubits}b')
            
            # Apply phase flip for marked item
            for i, bit in enumerate(reversed(binary)):
                if bit == '0':
                    oracle.x(i)
            
            # Multi-controlled Z gate
            if num_qubits > 1:
                oracle.mcrz(np.pi, list(range(num_qubits-1)), num_qubits-1)
            else:
                oracle.z(0)
            
            # Undo X gates
            for i, bit in enumerate(reversed(binary)):
                if bit == '0':
                    oracle.x(i)
        
        return oracle
    
    def create_amplitude_amplification_circuit(
        self, 
        oracle: QuantumCircuit, 
        iterations: int = 1
    ) -> QuantumCircuit:
        """Create amplitude amplification circuit.
        
        Args:
            oracle: Oracle circuit to amplify
            iterations: Number of amplification iterations
            
        Returns:
            Complete amplitude amplification circuit
        """
        num_qubits = oracle.num_qubits
        qreg = QuantumRegister(num_qubits, 'q')
        creg = ClassicalRegister(num_qubits, 'c')
        circuit = QuantumCircuit(qreg, creg)
        
        # Initialize superposition
        circuit.h(range(num_qubits))
        
        # Grover iterations
        for _ in range(iterations):
            # Apply oracle
            circuit.compose(oracle, inplace=True)
            
            # Diffusion operator
            circuit.h(range(num_qubits))
            circuit.x(range(num_qubits))
            
            if num_qubits > 1:
                circuit.mcrz(np.pi, list(range(num_qubits-1)), num_qubits-1)
            else:
                circuit.z(0)
                
            circuit.x(range(num_qubits))
            circuit.h(range(num_qubits))
        
        # Final measurements
        circuit.measure_all()
        
        return circuit
