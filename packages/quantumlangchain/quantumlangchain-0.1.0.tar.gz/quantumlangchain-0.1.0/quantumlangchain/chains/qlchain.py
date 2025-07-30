"""
QLChain: Quantum-ready chains with decoherence-aware control flows.

🔐 LICENSED COMPONENT - Requires valid QuantumLangChain license
📧 Contact: bajpaikrishna715@gmail.com for licensing
"""

from typing import Any, Dict, List, Optional, Union, AsyncIterator, Callable
import asyncio
import logging
from datetime import datetime
from pydantic import Field

from quantumlangchain.core.base import (
    QuantumBase, 
    QuantumChainInterface, 
    QuantumConfig,
    QuantumState,
    DecoherenceLevel
)
from quantumlangchain.memory.quantum_memory import QuantumMemory
from quantumlangchain.backends.qiskit_backend import QiskitBackend
from quantumlangchain.licensing import (
    LicensedComponent,
    requires_license,
    validate_license,
    FeatureNotLicensedError
)

logger = logging.getLogger(__name__)


class QLChainConfig(QuantumConfig):
    """Configuration for QLChain."""
    
    max_iterations: int = Field(default=10, description="Maximum chain iterations")
    decoherence_penalty: float = Field(default=0.1, description="Decoherence penalty factor")
    circuit_injection_enabled: bool = Field(default=True, description="Enable quantum circuit injection")
    hybrid_execution: bool = Field(default=True, description="Enable hybrid quantum-classical execution")
    error_correction_threshold: float = Field(default=0.8, description="Error correction activation threshold")
    adaptive_depth: bool = Field(default=True, description="Enable adaptive circuit depth")
    parallel_branches: int = Field(default=3, description="Number of parallel quantum branches")


class QLChain(QuantumBase, QuantumChainInterface, LicensedComponent):
    """
    Quantum-ready chain with decoherence-aware control flows and circuit injection.
    
    🔐 LICENSING: Requires Basic tier or higher license
    Features used: core, basic_chains, quantum_memory
    
    QLChain extends traditional chain concepts with quantum-enhanced reasoning,
    allowing for superposition of execution paths, entangled memory access,
    and decoherence-aware decision making.
    """
    
    config: QLChainConfig = Field(default_factory=QLChainConfig)
    memory: Optional[QuantumMemory] = Field(default=None)
    backend: Optional[Any] = Field(default=None)
    execution_history: List[Dict[str, Any]] = Field(default_factory=list)
    quantum_circuits: Dict[str, Any] = Field(default_factory=dict)
    branch_weights: Dict[str, float] = Field(default_factory=dict)
    
    def __init__(self, **data):
        # Initialize licensing first
        LicensedComponent.__init__(
            self, 
            required_features=["core", "basic_chains"],
            required_tier="basic",
            package="quantumlangchain"
        )
        
        super().__init__(**data)
        
        # Initialize backend if not provided
        if self.backend is None:
            self.backend = QiskitBackend()
        
        # Initialize memory if not provided
        if self.memory is None:
            self.memory = QuantumMemory(
                classical_dim=512,
                quantum_dim=self.config.num_qubits,
                backend=self.backend
            )
    
    async def initialize(self) -> None:
        """Initialize the quantum chain."""
        await self.memory.initialize()
        self.quantum_state = QuantumState.COHERENT
        self.decoherence_level = 0.0
        
        # Initialize quantum circuits
        await self._initialize_quantum_circuits()
        
        self.logger.info("QLChain initialized successfully")
    
    async def reset_quantum_state(self) -> None:
        """Reset quantum state to initial conditions."""
        self.quantum_state = QuantumState.COHERENT
        self.decoherence_level = 0.0
        self.execution_history.clear()
        self.quantum_circuits.clear()
        self.branch_weights.clear()
        
        if self.memory:
            await self.memory.reset_quantum_state()
        
        await self._initialize_quantum_circuits()
        
        self.logger.info("QLChain quantum state reset")
    
    async def _initialize_quantum_circuits(self) -> None:
        """Initialize quantum circuits for chain operations."""
        try:
            # Create entangling circuit for memory access
            entangling_qubits = list(range(min(4, self.config.num_qubits)))
            entangling_circuit = await self.backend.create_entangling_circuit(entangling_qubits)
            self.quantum_circuits["entangling"] = entangling_circuit
            
            # Create variational circuit for adaptive reasoning
            if hasattr(self.backend, 'create_variational_circuit'):
                variational_circuit = self.backend.create_variational_circuit(
                    self.config.num_qubits, 
                    self.config.circuit_depth
                )
                self.quantum_circuits["variational"] = variational_circuit
            
            self.logger.debug("Quantum circuits initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize quantum circuits: {e}")
    
    @requires_license(features=["core", "basic_chains"], tier="basic")
    async def arun(self, input_data: Any, **kwargs) -> Any:
        """Run the chain asynchronously with quantum enhancement.
        
        🔐 LICENSED METHOD - Requires Basic tier license
        Features: core, basic_chains
        
        Args:
            input_data: Input data for the chain
            **kwargs: Additional execution parameters
            
        Returns:
            Chain execution result with quantum enhancements
        """
        execution_id = f"exec_{datetime.now().isoformat()}_{id(input_data)}"
        
        try:
            # Check quantum state and apply decoherence penalty
            if self.decoherence_level > self.config.decoherence_threshold:
                await self._apply_error_correction()
            
            # Enter superposition for parallel reasoning
            if self.config.parallel_branches > 1:
                self.enter_superposition()
                result = await self._parallel_quantum_execution(input_data, execution_id, **kwargs)
            else:
                result = await self._sequential_quantum_execution(input_data, execution_id, **kwargs)
            
            # Store execution in quantum memory
            await self._store_execution_result(execution_id, input_data, result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"QLChain execution failed: {e}")
            # Apply decoherence penalty for errors
            self.update_decoherence(self.config.decoherence_penalty)
            
            # Fallback to classical execution
            return await self._classical_fallback(input_data, **kwargs)
    
    async def _parallel_quantum_execution(
        self, 
        input_data: Any, 
        execution_id: str, 
        **kwargs
    ) -> Any:
        """Execute chain with parallel quantum branches."""
        
        # Create parallel execution branches
        branches = []
        for i in range(self.config.parallel_branches):
            branch_id = f"{execution_id}_branch_{i}"
            branch_weight = 1.0 / self.config.parallel_branches
            self.branch_weights[branch_id] = branch_weight
            
            branch_task = self._execute_quantum_branch(
                input_data, 
                branch_id, 
                branch_weight,
                **kwargs
            )
            branches.append(branch_task)
        
        # Execute branches in parallel
        branch_results = await asyncio.gather(*branches, return_exceptions=True)
        
        # Quantum interference and measurement
        final_result = await self._measure_branch_results(branch_results, execution_id)
        
        return final_result
    
    async def _execute_quantum_branch(
        self,
        input_data: Any,
        branch_id: str,
        weight: float,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute a single quantum branch."""
        
        branch_start_time = asyncio.get_event_loop().time()
        
        try:
            # Apply quantum circuit injection if enabled
            if self.config.circuit_injection_enabled:
                enhanced_input = await self._inject_quantum_circuit(input_data, branch_id)
            else:
                enhanced_input = input_data
            
            # Classical processing with quantum memory access
            intermediate_result = await self._process_with_quantum_memory(
                enhanced_input, 
                branch_id
            )
            
            # Apply quantum enhancement to result
            if self.config.hybrid_execution:
                final_result = await self._apply_quantum_enhancement(
                    intermediate_result, 
                    branch_id
                )
            else:
                final_result = intermediate_result
            
            execution_time = asyncio.get_event_loop().time() - branch_start_time
            
            return {
                "branch_id": branch_id,
                "result": final_result,
                "weight": weight,
                "execution_time": execution_time,
                "success": True,
                "decoherence_contribution": self.decoherence_level * weight
            }
            
        except Exception as e:
            self.logger.error(f"Branch {branch_id} execution failed: {e}")
            return {
                "branch_id": branch_id,
                "result": None,
                "weight": weight,
                "execution_time": 0.0,
                "success": False,
                "error": str(e),
                "decoherence_contribution": self.config.decoherence_penalty * weight
            }
    
    async def _measure_branch_results(
        self, 
        branch_results: List[Dict[str, Any]], 
        execution_id: str
    ) -> Any:
        """Measure and collapse quantum branch results."""
        
        # Filter successful branches
        successful_branches = [
            result for result in branch_results 
            if isinstance(result, dict) and result.get("success", False)
        ]
        
        if not successful_branches:
            raise RuntimeError("All quantum branches failed")
        
        # Calculate total weight and normalize
        total_weight = sum(branch["weight"] for branch in successful_branches)
        
        if total_weight == 0:
            # Equal weights fallback
            for branch in successful_branches:
                branch["normalized_weight"] = 1.0 / len(successful_branches)
        else:
            for branch in successful_branches:
                branch["normalized_weight"] = branch["weight"] / total_weight
        
        # Quantum measurement simulation
        measurement_result = await self._simulate_quantum_measurement(successful_branches)
        
        # Collapse superposition
        if self.quantum_state == QuantumState.SUPERPOSITION:
            self.quantum_state = QuantumState.COLLAPSED
        
        # Update decoherence based on branch contributions
        total_decoherence = sum(
            branch.get("decoherence_contribution", 0) 
            for branch in branch_results
        )
        self.update_decoherence(total_decoherence)
        
        # Store measurement in execution history
        self.execution_history.append({
            "execution_id": execution_id,
            "branch_count": len(branch_results),
            "successful_branches": len(successful_branches),
            "measurement_result": measurement_result,
            "final_decoherence": self.decoherence_level,
            "timestamp": datetime.now().isoformat()
        })
        
        return measurement_result
    
    async def _simulate_quantum_measurement(
        self, 
        branches: List[Dict[str, Any]]
    ) -> Any:
        """Simulate quantum measurement to select branch result."""
        
        # Use quantum backend for measurement if available
        if hasattr(self.backend, 'execute_circuit') and "entangling" in self.quantum_circuits:
            try:
                # Execute entangling circuit
                circuit_result = await self.backend.execute_circuit(
                    self.quantum_circuits["entangling"]
                )
                
                if circuit_result.get("success", False):
                    probabilities = circuit_result.get("probabilities", {})
                    
                    # Map quantum probabilities to branch selection
                    if probabilities:
                        # Use first measurement outcome to select branch
                        states = list(probabilities.keys())
                        probs = list(probabilities.values())
                        
                        # Weighted selection based on quantum probabilities
                        selected_index = self._weighted_random_choice(probs)
                        if selected_index < len(branches):
                            return branches[selected_index]["result"]
            
            except Exception as e:
                self.logger.warning(f"Quantum measurement failed, using classical: {e}")
        
        # Classical fallback: weighted random selection
        weights = [branch["normalized_weight"] for branch in branches]
        selected_index = self._weighted_random_choice(weights)
        
        return branches[selected_index]["result"]
    
    def _weighted_random_choice(self, weights: List[float]) -> int:
        """Select index based on weights."""
        import random
        
        if not weights:
            return 0
        
        total = sum(weights)
        if total == 0:
            return random.randint(0, len(weights) - 1)
        
        normalized_weights = [w / total for w in weights]
        rand_val = random.random()
        cumulative = 0.0
        
        for i, weight in enumerate(normalized_weights):
            cumulative += weight
            if rand_val <= cumulative:
                return i
        
        return len(weights) - 1
    
    async def _sequential_quantum_execution(
        self, 
        input_data: Any, 
        execution_id: str, 
        **kwargs
    ) -> Any:
        """Execute chain sequentially with quantum enhancements."""
        
        # Apply quantum circuit injection
        if self.config.circuit_injection_enabled:
            enhanced_input = await self._inject_quantum_circuit(input_data, execution_id)
        else:
            enhanced_input = input_data
        
        # Process with quantum memory
        intermediate_result = await self._process_with_quantum_memory(
            enhanced_input, 
            execution_id
        )
        
        # Apply quantum enhancement
        if self.config.hybrid_execution:
            final_result = await self._apply_quantum_enhancement(
                intermediate_result, 
                execution_id
            )
        else:
            final_result = intermediate_result
        
        return final_result
    
    async def _inject_quantum_circuit(self, input_data: Any, execution_id: str) -> Any:
        """Inject quantum circuit processing into the input data."""
        
        # For demonstration, this would encode classical data into quantum states
        # and perform quantum operations before converting back to classical
        
        try:
            if isinstance(input_data, str):
                # Convert string to quantum-enhanced representation
                enhanced_data = {
                    "original": input_data,
                    "quantum_enhanced": True,
                    "execution_id": execution_id,
                    "quantum_signature": hash(input_data) % (2 ** self.config.num_qubits)
                }
                return enhanced_data
            
            elif isinstance(input_data, dict):
                # Add quantum enhancement metadata
                input_data["quantum_enhanced"] = True
                input_data["execution_id"] = execution_id
                return input_data
            
            else:
                # Wrap in quantum container
                return {
                    "data": input_data,
                    "quantum_enhanced": True,
                    "execution_id": execution_id
                }
        
        except Exception as e:
            self.logger.warning(f"Quantum circuit injection failed: {e}")
            return input_data
    
    async def _process_with_quantum_memory(self, input_data: Any, execution_id: str) -> Any:
        """Process data using quantum memory access."""
        
        try:
            # Store input in quantum memory
            memory_key = f"input_{execution_id}"
            await self.memory.store(memory_key, input_data, quantum_enhanced=True)
            
            # Retrieve with quantum enhancement (simulates quantum processing)
            enhanced_data = await self.memory.retrieve(memory_key, quantum_search=True)
            
            # Simulate processing logic
            if isinstance(enhanced_data, dict) and "original" in enhanced_data:
                processed_result = {
                    "processed": True,
                    "input": enhanced_data["original"],
                    "quantum_signature": enhanced_data.get("quantum_signature", 0),
                    "processing_timestamp": datetime.now().isoformat()
                }
            else:
                processed_result = {
                    "processed": True,
                    "input": enhanced_data,
                    "processing_timestamp": datetime.now().isoformat()
                }
            
            return processed_result
            
        except Exception as e:
            self.logger.error(f"Quantum memory processing failed: {e}")
            # Classical fallback
            return {
                "processed": True,
                "input": input_data,
                "fallback": "classical",
                "processing_timestamp": datetime.now().isoformat()
            }
    
    async def _apply_quantum_enhancement(self, result: Any, execution_id: str) -> Any:
        """Apply quantum enhancement to processing result."""
        
        try:
            # Simulate quantum enhancement through variational circuit
            if "variational" in self.quantum_circuits:
                # In a real implementation, this would run the variational circuit
                # with parameters derived from the result data
                
                enhancement_factor = 1.0 - self.decoherence_level
                
                if isinstance(result, dict):
                    result["quantum_enhancement"] = enhancement_factor
                    result["coherence_level"] = 1.0 - self.decoherence_level
                    result["entanglement_active"] = self.is_entangled()
                
                return result
            
            else:
                return result
                
        except Exception as e:
            self.logger.warning(f"Quantum enhancement failed: {e}")
            return result
    
    async def _apply_error_correction(self) -> None:
        """Apply quantum error correction when decoherence is high."""
        
        if self.decoherence_level > self.config.error_correction_threshold:
            self.logger.info("Applying quantum error correction")
            
            # Simulate error correction by reducing decoherence
            correction_factor = 0.5
            self.decoherence_level *= correction_factor
            
            # Reset quantum state if necessary
            if self.decoherence_level < self.config.decoherence_threshold:
                self.quantum_state = QuantumState.COHERENT
    
    async def _store_execution_result(
        self, 
        execution_id: str, 
        input_data: Any, 
        result: Any
    ) -> None:
        """Store execution result in quantum memory."""
        
        try:
            execution_record = {
                "execution_id": execution_id,
                "input": input_data,
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "decoherence_level": self.decoherence_level,
                "quantum_state": self.quantum_state.value
            }
            
            memory_key = f"execution_{execution_id}"
            await self.memory.store(memory_key, execution_record, quantum_enhanced=True)
            
        except Exception as e:
            self.logger.error(f"Failed to store execution result: {e}")
    
    async def _classical_fallback(self, input_data: Any, **kwargs) -> Any:
        """Classical fallback execution when quantum processing fails."""
        
        self.logger.info("Using classical fallback execution")
        
        # Simple classical processing
        if isinstance(input_data, str):
            return {
                "processed": True,
                "input": input_data,
                "method": "classical_fallback",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "processed": True,
                "input": input_data,
                "method": "classical_fallback",
                "timestamp": datetime.now().isoformat()
            }
    
    async def abatch(self, inputs: List[Any]) -> List[Any]:
        """Run the chain on a batch of inputs."""
        
        # Process inputs in parallel with quantum enhancement
        tasks = [self.arun(input_data) for input_data in inputs]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and log errors
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.error(f"Batch input {i} failed: {result}")
                processed_results.append(None)
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def astream(self, input_data: Any) -> AsyncIterator[Any]:
        """Stream chain execution with quantum state updates."""
        
        execution_id = f"stream_{datetime.now().isoformat()}_{id(input_data)}"
        
        # Yield initial state
        yield {
            "type": "quantum_state",
            "state": self.quantum_state.value,
            "decoherence": self.decoherence_level,
            "execution_id": execution_id
        }
        
        # Process and yield intermediate results
        try:
            if self.config.circuit_injection_enabled:
                enhanced_input = await self._inject_quantum_circuit(input_data, execution_id)
                yield {
                    "type": "circuit_injection",
                    "enhanced_input": enhanced_input,
                    "execution_id": execution_id
                }
            else:
                enhanced_input = input_data
            
            # Memory processing
            intermediate_result = await self._process_with_quantum_memory(
                enhanced_input, 
                execution_id
            )
            yield {
                "type": "memory_processing",
                "intermediate_result": intermediate_result,
                "execution_id": execution_id
            }
            
            # Final quantum enhancement
            if self.config.hybrid_execution:
                final_result = await self._apply_quantum_enhancement(
                    intermediate_result, 
                    execution_id
                )
            else:
                final_result = intermediate_result
            
            yield {
                "type": "final_result",
                "result": final_result,
                "execution_id": execution_id
            }
            
        except Exception as e:
            yield {
                "type": "error",
                "error": str(e),
                "execution_id": execution_id
            }
    
    async def get_execution_stats(self) -> Dict[str, Any]:
        """Get statistics about chain execution."""
        
        return {
            "total_executions": len(self.execution_history),
            "current_decoherence": self.decoherence_level,
            "quantum_state": self.quantum_state.value,
            "entanglement_count": len(self.entanglement_registry),
            "circuit_count": len(self.quantum_circuits),
            "branch_weights": self.branch_weights.copy(),
            "backend_info": self.backend.get_backend_info() if self.backend else None,
            "memory_stats": await self._get_memory_stats() if self.memory else None
        }
    
    async def _get_memory_stats(self) -> Dict[str, Any]:
        """Get quantum memory statistics."""
        if hasattr(self.memory, 'get_stats'):
            return await self.memory.get_stats()
        return {"available": False}
