"""
Quantum-enhanced prompt chaining with superposition-based prompt selection.
"""

import asyncio
import uuid
from typing import Any, Dict, List, Optional, Union, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import random
import re

from quantumlangchain.core.base import QuantumBase, QuantumState


class PromptType(Enum):
    """Types of prompts in quantum chains."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    QUANTUM_SUPERPOSITION = "quantum_superposition"
    ENTANGLED = "entangled"
    CONDITIONAL = "conditional"


@dataclass
class QuantumPrompt:
    """A quantum-enhanced prompt with superposition capabilities."""
    prompt_id: str
    content: str
    prompt_type: PromptType
    quantum_weight: float = 1.0
    entanglement_ids: List[str] = field(default_factory=list)
    conditions: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.prompt_id:
            self.prompt_id = str(uuid.uuid4())
    
    def apply_quantum_weight(self, base_probability: float) -> float:
        """Apply quantum weight to modify selection probability."""
        return min(1.0, base_probability * self.quantum_weight)
    
    def check_conditions(self, context: Dict[str, Any]) -> bool:
        """Check if prompt conditions are satisfied."""
        if not self.conditions:
            return True
        
        for condition_key, expected_value in self.conditions.items():
            if condition_key not in context:
                return False
            
            actual_value = context[condition_key]
            if isinstance(expected_value, dict):
                # Complex condition (e.g., {"operator": "gt", "value": 5})
                operator = expected_value.get("operator", "eq")
                value = expected_value.get("value")
                
                if operator == "eq" and actual_value != value:
                    return False
                elif operator == "gt" and actual_value <= value:
                    return False
                elif operator == "lt" and actual_value >= value:
                    return False
                elif operator == "contains" and value not in str(actual_value):
                    return False
            else:
                # Simple equality check
                if actual_value != expected_value:
                    return False
        
        return True


@dataclass
class PromptChainResult:
    """Result from prompt chain execution."""
    chain_id: str
    executed_prompts: List[QuantumPrompt]
    final_prompt: str
    quantum_effects: Dict[str, Any]
    execution_time: float
    success: bool
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class QPromptChain(QuantumBase):
    """
    Quantum-enhanced prompt chaining system with superposition-based prompt selection,
    entangled prompt relationships, and adaptive prompt evolution.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        
        # Prompt storage
        self.prompts: Dict[str, QuantumPrompt] = {}
        self.prompt_chains: Dict[str, List[str]] = {}
        self.prompt_templates: Dict[str, str] = {}
        
        # Quantum relationships
        self.entangled_prompts: Dict[str, List[str]] = {}
        self.superposition_groups: Dict[str, List[str]] = {}
        
        # Execution history
        self.execution_history: List[PromptChainResult] = []
        
        # Configuration
        self.max_chain_length = config.get("max_chain_length", 10) if config else 10
        self.quantum_selection_threshold = config.get("quantum_selection_threshold", 0.7) if config else 0.7
        self.adaptive_learning = config.get("adaptive_learning", True) if config else True
        
    async def initialize(self):
        """Initialize the quantum prompt chain."""
        await super().initialize()
        self.quantum_state = QuantumState.COHERENT
        
        # Load default prompt templates
        self._load_default_templates()
        
    async def reset_quantum_state(self):
        """Reset quantum state and clear execution history."""
        self.quantum_state = QuantumState.COHERENT
        self.decoherence_level = 0.0
        self.execution_history.clear()
        
    def _load_default_templates(self):
        """Load default prompt templates."""
        self.prompt_templates.update({
            "system_base": "You are a helpful AI assistant with quantum-enhanced reasoning capabilities.",
            "analysis_template": "Analyze the following information: {content}\n\nProvide insights on: {focus_areas}",
            "synthesis_template": "Synthesize the following concepts: {concepts}\n\nCreate a unified understanding that addresses: {objectives}",
            "quantum_reasoning": "Apply quantum reasoning principles to: {problem}\n\nConsider superposition, entanglement, and interference effects.",
            "chain_continuation": "Based on the previous context: {context}\n\nContinue the reasoning chain by: {next_action}",
            "error_correction": "The previous step encountered an issue: {error}\n\nApply quantum error correction by: {correction_strategy}"
        })
    
    def add_prompt(
        self,
        content: str,
        prompt_type: PromptType = PromptType.USER,
        quantum_weight: float = 1.0,
        conditions: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Add a prompt to the quantum collection."""
        prompt = QuantumPrompt(
            prompt_id=str(uuid.uuid4()),
            content=content,
            prompt_type=prompt_type,
            quantum_weight=quantum_weight,
            conditions=conditions or {},
            metadata=metadata or {}
        )
        
        self.prompts[prompt.prompt_id] = prompt
        return prompt.prompt_id
    
    def add_prompt_template(
        self,
        template_name: str,
        template_content: str,
        prompt_type: PromptType = PromptType.USER,
        quantum_weight: float = 1.0
    ) -> str:
        """Add a parameterized prompt template."""
        self.prompt_templates[template_name] = template_content
        
        # Create a prompt from the template
        return self.add_prompt(
            content=template_content,
            prompt_type=prompt_type,
            quantum_weight=quantum_weight,
            metadata={"template_name": template_name, "is_template": True}
        )
    
    def create_prompt_chain(
        self,
        chain_name: str,
        prompt_ids: List[str],
        allow_quantum_selection: bool = True
    ):
        """Create a named prompt chain."""
        # Validate all prompts exist
        for prompt_id in prompt_ids:
            if prompt_id not in self.prompts:
                raise ValueError(f"Prompt '{prompt_id}' not found")
        
        self.prompt_chains[chain_name] = prompt_ids
        
        if allow_quantum_selection:
            # Enable quantum effects for this chain
            self.quantum_state = QuantumState.SUPERPOSITION
    
    def create_superposition_group(
        self,
        group_name: str,
        prompt_ids: List[str],
        selection_method: str = "quantum_interference"
    ):
        """Create a superposition group where one prompt is selected quantum-mechanically."""
        for prompt_id in prompt_ids:
            if prompt_id not in self.prompts:
                raise ValueError(f"Prompt '{prompt_id}' not found")
        
        self.superposition_groups[group_name] = prompt_ids
        
        # Update quantum state
        self.quantum_state = QuantumState.SUPERPOSITION
    
    def entangle_prompts(
        self,
        prompt_ids: List[str],
        entanglement_strength: float = 0.8
    ) -> str:
        """Create quantum entanglement between prompts."""
        entanglement_id = str(uuid.uuid4())
        
        # Validate and update prompts
        for prompt_id in prompt_ids:
            if prompt_id not in self.prompts:
                raise ValueError(f"Prompt '{prompt_id}' not found")
            
            self.prompts[prompt_id].entanglement_ids.append(entanglement_id)
        
        # Store entanglement relationship
        self.entangled_prompts[entanglement_id] = prompt_ids
        
        # Update quantum state
        self.quantum_state = QuantumState.ENTANGLED
        
        return entanglement_id
    
    async def select_quantum_prompt(
        self,
        candidate_prompts: List[str],
        context: Dict[str, Any],
        selection_method: str = "amplitude_amplification"
    ) -> Optional[str]:
        """Select a prompt using quantum selection methods."""
        if not candidate_prompts:
            return None
        
        valid_prompts = []
        for prompt_id in candidate_prompts:
            if prompt_id in self.prompts:
                prompt = self.prompts[prompt_id]
                if prompt.check_conditions(context):
                    valid_prompts.append((prompt_id, prompt))
        
        if not valid_prompts:
            return None
        
        if len(valid_prompts) == 1:
            return valid_prompts[0][0]
        
        # Apply quantum selection
        if selection_method == "amplitude_amplification":
            return await self._amplitude_amplification_selection(valid_prompts, context)
        elif selection_method == "quantum_interference":
            return await self._quantum_interference_selection(valid_prompts, context)
        elif selection_method == "entanglement_correlation":
            return await self._entanglement_correlation_selection(valid_prompts, context)
        else:
            # Default: weighted random selection
            return await self._weighted_random_selection(valid_prompts)
    
    async def _amplitude_amplification_selection(
        self,
        prompts: List[Tuple[str, QuantumPrompt]],
        context: Dict[str, Any]
    ) -> str:
        """Select prompt using amplitude amplification principles."""
        # Calculate amplification factors based on context relevance
        amplified_weights = []
        
        for prompt_id, prompt in prompts:
            base_weight = prompt.quantum_weight
            
            # Amplify based on context matching
            relevance_score = self._calculate_context_relevance(prompt, context)
            amplification_factor = 1 + relevance_score
            
            # Apply decoherence effects
            coherence_factor = 1 - self.decoherence_level
            
            final_weight = base_weight * amplification_factor * coherence_factor
            amplified_weights.append(final_weight)
        
        # Select based on amplified probabilities
        total_weight = sum(amplified_weights)
        if total_weight == 0:
            return prompts[0][0]
        
        probabilities = [w / total_weight for w in amplified_weights]
        selected_index = self._quantum_random_choice(probabilities)
        
        # Add small decoherence from measurement
        self.update_decoherence(0.02)
        
        return prompts[selected_index][0]
    
    async def _quantum_interference_selection(
        self,
        prompts: List[Tuple[str, QuantumPrompt]],
        context: Dict[str, Any]
    ) -> str:
        """Select prompt using quantum interference patterns."""
        interference_amplitudes = []
        
        for i, (prompt_id, prompt) in enumerate(prompts):
            amplitude = prompt.quantum_weight
            
            # Calculate interference with other prompts
            for j, (other_id, other_prompt) in enumerate(prompts):
                if i != j:
                    # Check for entanglement
                    entangled = any(
                        eid in other_prompt.entanglement_ids 
                        for eid in prompt.entanglement_ids
                    )
                    
                    if entangled:
                        # Constructive or destructive interference
                        phase_difference = (i - j) * 0.1  # Simplified phase calculation
                        interference = 0.2 * random.cos(phase_difference)
                        amplitude += interference
            
            interference_amplitudes.append(max(0, amplitude))  # Ensure non-negative
        
        # Select based on interference-modified amplitudes
        total_amplitude = sum(interference_amplitudes)
        if total_amplitude == 0:
            return prompts[0][0]
        
        probabilities = [a / total_amplitude for a in interference_amplitudes]
        selected_index = self._quantum_random_choice(probabilities)
        
        return prompts[selected_index][0]
    
    async def _entanglement_correlation_selection(
        self,
        prompts: List[Tuple[str, QuantumPrompt]],
        context: Dict[str, Any]
    ) -> str:
        """Select prompt based on entanglement correlations."""
        correlation_scores = []
        
        for prompt_id, prompt in prompts:
            score = prompt.quantum_weight
            
            # Boost score based on entangled prompt activation
            for entanglement_id in prompt.entanglement_ids:
                if entanglement_id in self.entangled_prompts:
                    entangled_prompt_ids = self.entangled_prompts[entanglement_id]
                    
                    # Check if any entangled prompts were recently used
                    recent_usage = any(
                        self._was_prompt_recently_used(pid, context)
                        for pid in entangled_prompt_ids
                        if pid != prompt_id
                    )
                    
                    if recent_usage:
                        score *= 1.5  # Correlation boost
            
            correlation_scores.append(score)
        
        # Select based on correlation scores
        max_score = max(correlation_scores)
        if max_score == 0:
            return prompts[0][0]
        
        normalized_scores = [s / max_score for s in correlation_scores]
        selected_index = self._quantum_random_choice(normalized_scores)
        
        return prompts[selected_index][0]
    
    async def _weighted_random_selection(
        self,
        prompts: List[Tuple[str, QuantumPrompt]]
    ) -> str:
        """Simple weighted random selection."""
        weights = [prompt.quantum_weight for _, prompt in prompts]
        total_weight = sum(weights)
        
        if total_weight == 0:
            return prompts[0][0]
        
        probabilities = [w / total_weight for w in weights]
        selected_index = self._quantum_random_choice(probabilities)
        
        return prompts[selected_index][0]
    
    def _quantum_random_choice(self, probabilities: List[float]) -> int:
        """Quantum-inspired random choice with coherence effects."""
        # Apply quantum coherence effects to probabilities
        coherence_factor = 1 - self.decoherence_level
        adjusted_probs = [p * coherence_factor for p in probabilities]
        
        # Normalize
        total_prob = sum(adjusted_probs)
        if total_prob == 0:
            return 0
        
        adjusted_probs = [p / total_prob for p in adjusted_probs]
        
        # Random selection
        r = random.random()
        cumulative = 0
        for i, prob in enumerate(adjusted_probs):
            cumulative += prob
            if r <= cumulative:
                return i
        
        return len(adjusted_probs) - 1
    
    def _calculate_context_relevance(
        self,
        prompt: QuantumPrompt,
        context: Dict[str, Any]
    ) -> float:
        """Calculate how relevant a prompt is to the current context."""
        relevance = 0.0
        
        # Check metadata matches
        for key, value in prompt.metadata.items():
            if key in context and context[key] == value:
                relevance += 0.2
        
        # Check content keyword matches
        content_lower = prompt.content.lower()
        context_text = " ".join(str(v) for v in context.values()).lower()
        
        # Simple keyword matching
        words = context_text.split()
        matches = sum(1 for word in words if word in content_lower)
        if words:
            relevance += (matches / len(words)) * 0.5
        
        return min(1.0, relevance)
    
    def _was_prompt_recently_used(
        self,
        prompt_id: str,
        context: Dict[str, Any],
        recent_threshold: int = 3
    ) -> bool:
        """Check if a prompt was used in recent executions."""
        recent_executions = self.execution_history[-recent_threshold:]
        
        for execution in recent_executions:
            for executed_prompt in execution.executed_prompts:
                if executed_prompt.prompt_id == prompt_id:
                    return True
        
        return False
    
    async def execute_prompt_chain(
        self,
        chain_name: str,
        context: Dict[str, Any],
        variables: Optional[Dict[str, Any]] = None
    ) -> PromptChainResult:
        """Execute a named prompt chain with quantum effects."""
        start_time = datetime.now()
        
        if chain_name not in self.prompt_chains:
            return PromptChainResult(
                chain_id=chain_name,
                executed_prompts=[],
                final_prompt="",
                quantum_effects={},
                execution_time=0.0,
                success=False,
                error=f"Chain '{chain_name}' not found"
            )
        
        try:
            prompt_ids = self.prompt_chains[chain_name]
            executed_prompts = []
            final_prompt_parts = []
            quantum_effects = {
                "superposition_collapses": 0,
                "entanglement_correlations": 0,
                "decoherence_events": 0,
                "quantum_selections": 0
            }
            
            for prompt_id in prompt_ids:
                if prompt_id in self.prompts:
                    prompt = self.prompts[prompt_id]
                    
                    # Check if this is a superposition group
                    superposition_group = None
                    for group_name, group_prompts in self.superposition_groups.items():
                        if prompt_id in group_prompts:
                            superposition_group = group_name
                            break
                    
                    if superposition_group:
                        # Quantum selection from superposition
                        selected_id = await self.select_quantum_prompt(
                            self.superposition_groups[superposition_group],
                            context
                        )
                        if selected_id and selected_id in self.prompts:
                            prompt = self.prompts[selected_id]
                            quantum_effects["quantum_selections"] += 1
                    
                    # Apply variables to prompt content
                    formatted_content = self._format_prompt_content(
                        prompt.content,
                        variables or {},
                        context
                    )
                    
                    # Create execution copy
                    executed_prompt = QuantumPrompt(
                        prompt_id=prompt.prompt_id,
                        content=formatted_content,
                        prompt_type=prompt.prompt_type,
                        quantum_weight=prompt.quantum_weight,
                        entanglement_ids=prompt.entanglement_ids.copy(),
                        conditions=prompt.conditions.copy(),
                        metadata=prompt.metadata.copy()
                    )
                    
                    executed_prompts.append(executed_prompt)
                    final_prompt_parts.append(formatted_content)
                    
                    # Track quantum effects
                    if prompt.entanglement_ids:
                        quantum_effects["entanglement_correlations"] += 1
                    
                    # Apply decoherence
                    if prompt.prompt_type == PromptType.QUANTUM_SUPERPOSITION:
                        self.update_decoherence(0.05)
                        quantum_effects["decoherence_events"] += 1
            
            # Combine final prompt
            final_prompt = "\n\n".join(final_prompt_parts)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            result = PromptChainResult(
                chain_id=chain_name,
                executed_prompts=executed_prompts,
                final_prompt=final_prompt,
                quantum_effects=quantum_effects,
                execution_time=execution_time,
                success=True
            )
            
            # Store in execution history
            self.execution_history.append(result)
            
            # Adaptive learning
            if self.adaptive_learning:
                await self._update_prompt_weights(result, context)
            
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return PromptChainResult(
                chain_id=chain_name,
                executed_prompts=[],
                final_prompt="",
                quantum_effects={},
                execution_time=execution_time,
                success=False,
                error=str(e)
            )
    
    def _format_prompt_content(
        self,
        content: str,
        variables: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Format prompt content with variables and context."""
        formatted = content
        
        # Replace variables
        for key, value in variables.items():
            placeholder = "{" + key + "}"
            formatted = formatted.replace(placeholder, str(value))
        
        # Replace context variables
        for key, value in context.items():
            placeholder = "{" + key + "}"
            formatted = formatted.replace(placeholder, str(value))
        
        return formatted
    
    async def _update_prompt_weights(
        self,
        result: PromptChainResult,
        context: Dict[str, Any]
    ):
        """Update prompt weights based on execution success."""
        if not result.success:
            return
        
        learning_rate = 0.1
        
        for executed_prompt in result.executed_prompts:
            if executed_prompt.prompt_id in self.prompts:
                original_prompt = self.prompts[executed_prompt.prompt_id]
                
                # Increase weight for successful prompts
                weight_adjustment = learning_rate * (1 - self.decoherence_level)
                original_prompt.quantum_weight = min(
                    2.0,  # Maximum weight
                    original_prompt.quantum_weight + weight_adjustment
                )
    
    def get_chain_statistics(self) -> Dict[str, Any]:
        """Get comprehensive prompt chain statistics."""
        stats = {
            "total_prompts": len(self.prompts),
            "total_chains": len(self.prompt_chains),
            "superposition_groups": len(self.superposition_groups),
            "entangled_prompts": len(self.entangled_prompts),
            "total_executions": len(self.execution_history),
            "successful_executions": len([r for r in self.execution_history if r.success]),
            "quantum_state": self.quantum_state.value,
            "decoherence_level": self.decoherence_level,
            "prompt_types": {},
            "average_execution_time": 0.0,
            "quantum_effects_summary": {
                "total_superposition_collapses": 0,
                "total_entanglement_correlations": 0,
                "total_quantum_selections": 0
            }
        }
        
        # Count prompt types
        for prompt in self.prompts.values():
            prompt_type = prompt.prompt_type.value
            stats["prompt_types"][prompt_type] = stats["prompt_types"].get(prompt_type, 0) + 1
        
        # Calculate average execution time
        if self.execution_history:
            total_time = sum(r.execution_time for r in self.execution_history)
            stats["average_execution_time"] = total_time / len(self.execution_history)
            
            # Aggregate quantum effects
            for result in self.execution_history:
                for effect, count in result.quantum_effects.items():
                    effect_key = f"total_{effect}"
                    if effect_key in stats["quantum_effects_summary"]:
                        stats["quantum_effects_summary"][effect_key] += count
        
        return stats
