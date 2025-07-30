"""
Test cases for EntangledAgents functionality.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, Mock, patch

from quantumlangchain.agents.entangled_agents import (
    EntangledAgents,
    AgentRole,
    SharedQuantumMemory,
    BeliefState
)
from quantumlangchain.memory.quantum_memory import QuantumMemory
from quantumlangchain.core.base import QuantumState


class TestAgentRole:
    """Test cases for AgentRole class."""
    
    def test_agent_role_creation(self):
        """Test AgentRole initialization."""
        role = AgentRole(
            name="researcher",
            description="Research and analysis specialist",
            capabilities=["search", "analyze", "synthesize"],
            priority=0.8
        )
        
        assert role.name == "researcher"
        assert role.description == "Research and analysis specialist"
        assert "search" in role.capabilities
        assert role.priority == 0.8
        assert role.active is True
    
    def test_agent_role_validation(self):
        """Test AgentRole validation."""
        # Test priority bounds
        with pytest.raises(ValueError):
            AgentRole(name="test", priority=1.5)  # Too high
        
        with pytest.raises(ValueError):
            AgentRole(name="test", priority=-0.1)  # Too low
        
        # Test empty capabilities
        role = AgentRole(name="test", capabilities=[])
        assert role.capabilities == []


class TestSharedQuantumMemory:
    """Test cases for SharedQuantumMemory class."""
    
    @pytest.fixture
    async def shared_memory(self, mock_quantum_backend):
        """Create SharedQuantumMemory instance for testing."""
        memory = SharedQuantumMemory(
            classical_dim=128,
            quantum_dim=4,
            backend=mock_quantum_backend
        )
        await memory.initialize()
        return memory
    
    @pytest.mark.asyncio
    async def test_shared_memory_initialization(self, shared_memory):
        """Test SharedQuantumMemory initialization."""
        assert shared_memory.classical_dim == 128
        assert shared_memory.quantum_dim == 4
        assert len(shared_memory.agent_access_log) == 0
        assert shared_memory.quantum_state == QuantumState.COHERENT
    
    @pytest.mark.asyncio
    async def test_agent_memory_access(self, shared_memory):
        """Test agent memory access tracking."""
        agent_id = "agent_001"
        
        # Store data as an agent
        await shared_memory.store_as_agent(
            agent_id=agent_id,
            key="test_knowledge",
            value="Important information",
            quantum_enhanced=True
        )
        
        # Retrieve data as an agent
        result = await shared_memory.retrieve_as_agent(
            agent_id=agent_id,
            key="test_knowledge",
            quantum_search=True
        )
        
        assert result == "Important information"
        
        # Check access log
        assert len(shared_memory.agent_access_log) >= 2  # Store + retrieve
        assert any(log["agent_id"] == agent_id for log in shared_memory.agent_access_log)
    
    @pytest.mark.asyncio
    async def test_collaborative_storage(self, shared_memory):
        """Test collaborative memory storage."""
        agents = ["agent_001", "agent_002", "agent_003"]
        
        # Multiple agents store related information
        for i, agent_id in enumerate(agents):
            await shared_memory.store_as_agent(
                agent_id=agent_id,
                key=f"research_finding_{i}",
                value=f"Finding {i} by {agent_id}",
                quantum_enhanced=True
            )
        
        # Create collaborative entanglement
        keys = [f"research_finding_{i}" for i in range(len(agents))]
        entanglement_id = await shared_memory.entangle_memories(keys)
        
        assert entanglement_id is not None
        assert shared_memory.quantum_state == QuantumState.ENTANGLED
        
        # Verify collaborative access
        for agent_id in agents:
            for key in keys:
                result = await shared_memory.retrieve_as_agent(agent_id, key)
                assert result is not None
    
    @pytest.mark.asyncio
    async def test_memory_conflict_resolution(self, shared_memory):
        """Test memory conflict resolution between agents."""
        key = "conflicted_knowledge"
        
        # Two agents store different values for same key
        await shared_memory.store_as_agent(
            agent_id="agent_001",
            key=key,
            value="Version A",
            quantum_enhanced=True
        )
        
        await shared_memory.store_as_agent(
            agent_id="agent_002",
            key=key,
            value="Version B",
            quantum_enhanced=True,
            allow_overwrite=False  # Should create conflict
        )
        
        # Retrieve should return the most recent or consensus value
        result = await shared_memory.retrieve_as_agent("agent_003", key)
        assert result in ["Version A", "Version B"]
        
        # Check conflict tracking
        stats = await shared_memory.get_agent_stats()
        assert "conflicts" in stats


class TestBeliefState:
    """Test cases for BeliefState class."""
    
    def test_belief_state_creation(self):
        """Test BeliefState initialization."""
        belief = BeliefState(
            agent_id="agent_001",
            belief="The solution involves quantum superposition",
            confidence=0.8,
            evidence=["observation_1", "calculation_2"]
        )
        
        assert belief.agent_id == "agent_001"
        assert belief.confidence == 0.8
        assert len(belief.evidence) == 2
        assert belief.timestamp is not None
    
    def test_belief_state_update(self):
        """Test BeliefState update functionality."""
        belief = BeliefState(
            agent_id="agent_001",
            belief="Initial hypothesis",
            confidence=0.6
        )
        
        original_timestamp = belief.timestamp
        
        # Update belief
        belief.update_belief(
            "Refined hypothesis",
            confidence=0.9,
            new_evidence=["new_data"]
        )
        
        assert belief.belief == "Refined hypothesis"
        assert belief.confidence == 0.9
        assert "new_data" in belief.evidence
        assert belief.timestamp > original_timestamp


class TestEntangledAgents:
    """Test cases for EntangledAgents class."""
    
    @pytest.fixture
    async def entangled_agents(self, mock_quantum_backend):
        """Create EntangledAgents instance for testing."""
        agents = EntangledAgents(
            agent_configs=[
                {
                    "name": "researcher",
                    "description": "Research specialist",
                    "capabilities": ["search", "analyze"],
                    "priority": 0.8
                },
                {
                    "name": "synthesizer", 
                    "description": "Information synthesis",
                    "capabilities": ["combine", "summarize"],
                    "priority": 0.7
                },
                {
                    "name": "validator",
                    "description": "Solution validation",
                    "capabilities": ["verify", "test"],
                    "priority": 0.9
                }
            ],
            backend=mock_quantum_backend
        )
        await agents.initialize()
        return agents
    
    @pytest.mark.asyncio
    async def test_agents_initialization(self, entangled_agents):
        """Test EntangledAgents initialization."""
        assert len(entangled_agents.agent_roles) == 3
        assert entangled_agents.shared_memory is not None
        assert entangled_agents.quantum_state == QuantumState.COHERENT
        
        # Check agent roles
        agent_names = [role.name for role in entangled_agents.agent_roles.values()]
        assert "researcher" in agent_names
        assert "synthesizer" in agent_names
        assert "validator" in agent_names
    
    @pytest.mark.asyncio
    async def test_single_agent_execution(self, entangled_agents):
        """Test single agent task execution."""
        problem = "Analyze quantum entanglement in multi-qubit systems"
        
        result = await entangled_agents.run_single_agent(
            agent_id="researcher",
            problem=problem
        )
        
        assert result is not None
        assert isinstance(result, dict)
        assert "agent_id" in result
        assert "solution" in result
        assert result["agent_id"] == "researcher"
        
        # Check memory was updated
        memory_stats = await entangled_agents.shared_memory.get_stats()
        assert memory_stats["total_entries"] > 0
    
    @pytest.mark.asyncio
    async def test_collaborative_problem_solving(self, entangled_agents):
        """Test collaborative problem solving."""
        problem = "Design a quantum algorithm for database search"
        
        result = await entangled_agents.collaborative_solve(
            problem=problem,
            max_iterations=3
        )
        
        assert result is not None
        assert isinstance(result, dict)
        assert "final_solution" in result
        assert "agent_contributions" in result
        assert "collaboration_history" in result
        
        # Verify all agents contributed
        contributions = result["agent_contributions"]
        assert len(contributions) > 0
        
        # Check entanglement was created
        assert entangled_agents.quantum_state in [
            QuantumState.ENTANGLED, 
            QuantumState.SUPERPOSITION
        ]
    
    @pytest.mark.asyncio
    async def test_belief_propagation(self, entangled_agents):
        """Test belief state propagation between agents."""
        # Agent creates initial belief
        initial_belief = BeliefState(
            agent_id="researcher",
            belief="Quantum interference patterns suggest optimal solution",
            confidence=0.7,
            evidence=["measurement_data", "theoretical_analysis"]
        )
        
        # Propagate belief to other agents
        propagated_beliefs = await entangled_agents.propagate_belief(initial_belief)
        
        assert len(propagated_beliefs) > 0
        
        # Check belief modifications by other agents
        for belief in propagated_beliefs:
            assert belief.agent_id != initial_belief.agent_id
            assert belief.timestamp >= initial_belief.timestamp
    
    @pytest.mark.asyncio
    async def test_quantum_consensus_building(self, entangled_agents):
        """Test quantum consensus building."""
        # Create conflicting beliefs
        beliefs = [
            BeliefState("researcher", "Solution A is optimal", 0.8),
            BeliefState("synthesizer", "Solution B is better", 0.7),
            BeliefState("validator", "Hybrid approach needed", 0.9)
        ]
        
        # Build consensus
        consensus = await entangled_agents.build_quantum_consensus(beliefs)
        
        assert consensus is not None
        assert isinstance(consensus, dict)
        assert "consensus_belief" in consensus
        assert "confidence" in consensus
        assert "supporting_agents" in consensus
        
        # Consensus confidence should be reasonable
        assert 0.0 <= consensus["confidence"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_agent_role_management(self, entangled_agents):
        """Test agent role management functionality."""
        # Add new agent role
        new_role = AgentRole(
            name="optimizer",
            description="Solution optimization specialist",
            capabilities=["optimize", "refine"],
            priority=0.85
        )
        
        entangled_agents.add_agent_role(new_role)
        assert "optimizer" in entangled_agents.agent_roles
        
        # Update existing role
        entangled_agents.update_agent_role("researcher", priority=0.95)
        updated_role = entangled_agents.agent_roles["researcher"]
        assert updated_role.priority == 0.95
        
        # Deactivate agent role
        entangled_agents.deactivate_agent_role("synthesizer")
        synthesizer_role = entangled_agents.agent_roles["synthesizer"]
        assert synthesizer_role.active is False
    
    @pytest.mark.asyncio
    async def test_parallel_agent_execution(self, entangled_agents):
        """Test parallel execution of multiple agents."""
        problem = "Optimize quantum circuit for error correction"
        
        # Get active agent IDs
        active_agents = [
            agent_id for agent_id, role in entangled_agents.agent_roles.items()
            if role.active
        ]
        
        # Execute in parallel
        results = await entangled_agents.run_parallel_agents(
            agent_ids=active_agents,
            problem=problem
        )
        
        assert len(results) == len(active_agents)
        assert all(isinstance(result, dict) for result in results)
        
        # Check for different perspectives
        solutions = [result.get("solution", "") for result in results]
        assert len(set(solutions)) > 1  # Different agents should provide different solutions
    
    @pytest.mark.asyncio
    async def test_quantum_interference_effects(self, entangled_agents):
        """Test quantum interference between agent solutions."""
        problem = "Find optimal parameters for quantum gate sequence"
        
        # Run collaborative solving with interference
        result = await entangled_agents.collaborative_solve(
            problem=problem,
            enable_interference=True,
            max_iterations=2
        )
        
        assert "interference_effects" in result
        assert "solution_superposition" in result
        
        # Interference should modify final solution
        interference_data = result["interference_effects"]
        assert len(interference_data) > 0
    
    @pytest.mark.asyncio
    async def test_agent_performance_tracking(self, entangled_agents):
        """Test agent performance tracking."""
        # Execute multiple problems
        problems = [
            "Problem 1: Quantum state preparation",
            "Problem 2: Error correction optimization", 
            "Problem 3: Algorithm complexity analysis"
        ]
        
        for problem in problems:
            await entangled_agents.run_single_agent("researcher", problem)
        
        # Get performance stats
        stats = await entangled_agents.get_performance_stats()
        
        assert "agent_performance" in stats
        assert "researcher" in stats["agent_performance"]
        
        researcher_stats = stats["agent_performance"]["researcher"]
        assert researcher_stats["total_executions"] == len(problems)
        assert researcher_stats["success_rate"] > 0
    
    @pytest.mark.asyncio
    async def test_memory_entanglement_effects(self, entangled_agents):
        """Test memory entanglement effects on agent collaboration."""
        # Store related knowledge from different agents
        knowledge_items = [
            ("quantum_gates", "Unitary transformations for quantum computation"),
            ("error_correction", "Protecting quantum information from decoherence"),
            ("optimization", "Finding optimal parameters for quantum circuits")
        ]
        
        agents = list(entangled_agents.agent_roles.keys())[:3]
        
        for i, (key, value) in enumerate(knowledge_items):
            await entangled_agents.shared_memory.store_as_agent(
                agent_id=agents[i],
                key=key,
                value=value,
                quantum_enhanced=True
            )
        
        # Create entanglement between memories
        entanglement_id = await entangled_agents.shared_memory.entangle_memories(
            [key for key, _ in knowledge_items]
        )
        
        # Test collaborative access
        problem = "Design quantum error correction using optimized gates"
        result = await entangled_agents.collaborative_solve(problem, max_iterations=2)
        
        # Solution should benefit from entangled knowledge
        assert "quantum_gates" in result["final_solution"].lower() or \
               "error_correction" in result["final_solution"].lower() or \
               "optimization" in result["final_solution"].lower()


class TestAgentEdgeCases:
    """Test edge cases and error conditions."""
    
    @pytest.mark.asyncio
    async def test_single_agent_system(self, mock_quantum_backend):
        """Test system with only one agent."""
        agents = EntangledAgents(
            agent_configs=[{
                "name": "solo_agent",
                "description": "Works alone",
                "capabilities": ["everything"],
                "priority": 1.0
            }],
            backend=mock_quantum_backend
        )
        await agents.initialize()
        
        # Collaborative solving should still work
        result = await agents.collaborative_solve("Test problem")
        assert result is not None
        assert len(result["agent_contributions"]) == 1
    
    @pytest.mark.asyncio
    async def test_no_active_agents(self, mock_quantum_backend):
        """Test behavior when no agents are active."""
        agents = EntangledAgents(
            agent_configs=[{
                "name": "inactive_agent",
                "description": "Inactive agent",
                "capabilities": ["nothing"],
                "priority": 0.5
            }],
            backend=mock_quantum_backend
        )
        await agents.initialize()
        
        # Deactivate the only agent
        agents.deactivate_agent_role("inactive_agent")
        
        # Should handle gracefully
        with pytest.raises(ValueError):
            await agents.collaborative_solve("Test problem")
    
    @pytest.mark.asyncio
    async def test_high_decoherence_handling(self, mock_quantum_backend):
        """Test behavior under high decoherence conditions."""
        agents = EntangledAgents(
            agent_configs=[
                {"name": "agent1", "description": "Test", "capabilities": ["test"], "priority": 0.5},
                {"name": "agent2", "description": "Test", "capabilities": ["test"], "priority": 0.5}
            ],
            backend=mock_quantum_backend
        )
        await agents.initialize()
        
        # Artificially increase decoherence
        agents.decoherence_level = 0.95
        agents.quantum_state = QuantumState.DECOHERENT
        
        # System should handle degraded quantum state
        result = await agents.collaborative_solve("Test under decoherence")
        assert result is not None  # Should fall back to classical methods
