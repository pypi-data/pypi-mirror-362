"""
QuantumLangChain: A composable framework for quantum-inspired reasoning,
entangled memory systems, and multi-agent cooperation.

🔐 LICENSED SOFTWARE - All features require valid licensing
📧 Contact: bajpaikrishna715@gmail.com for licensing inquiries
⏰ 24-hour grace period available for evaluation

Author: Krishna Bajpai <bajpaikrishna715@gmail.com>
"""

__version__ = "0.1.0"
__author__ = "Krishna Bajpai"
__email__ = "bajpaikrishna715@gmail.com"
__license_package__ = "quantumlangchain"

# Initialize licensing system
from quantumlangchain.licensing import (
    LicenseManager,
    validate_license,
    requires_license,
    LicensedComponent,
    get_license_status,
    get_machine_id,
    display_license_info,
    QuantumLicenseError,
    LicenseExpiredError,
    FeatureNotLicensedError,
    GracePeriodExpiredError,
    LicenseNotFoundError,
    UsageLimitExceededError
)

# Core imports with license validation
from quantumlangchain.core.base import QuantumBase
from quantumlangchain.chains.qlchain import QLChain
from quantumlangchain.memory.quantum_memory import QuantumMemory, SharedQuantumMemory
from quantumlangchain.agents.entangled_agents import EntangledAgents
from quantumlangchain.tools.quantum_tool_executor import QuantumToolExecutor
from quantumlangchain.retrievers.quantum_retriever import QuantumRetriever
from quantumlangchain.context.quantum_context_manager import QuantumContextManager
from quantumlangchain.prompts.qprompt_chain import QPromptChain

# Backend imports
from quantumlangchain.backends.qiskit_backend import QiskitBackend
from quantumlangchain.backends.pennylane_backend import PennyLaneBackend
from quantumlangchain.backends.braket_backend import BraketBackend

# Vector store imports
from quantumlangchain.vectorstores.hybrid_chromadb import HybridChromaDB
from quantumlangchain.vectorstores.quantum_faiss import QuantumFAISS

__all__ = [
    # Licensing system
    "LicenseManager",
    "validate_license", 
    "requires_license",
    "LicensedComponent",
    "get_license_status",
    "get_machine_id",
    "display_license_info",
    "QuantumLicenseError",
    "LicenseExpiredError",
    "FeatureNotLicensedError", 
    "GracePeriodExpiredError",
    "LicenseNotFoundError",
    "UsageLimitExceededError",
    # Core classes
    "QuantumBase",
    "QLChain", 
    "QuantumMemory",
    "SharedQuantumMemory",
    "EntangledAgents",
    "QuantumToolExecutor",
    "QuantumRetriever",
    "QuantumContextManager",
    "QPromptChain",
    # Backends
    "QiskitBackend",
    "PennyLaneBackend", 
    "BraketBackend",
    # Vector stores
    "HybridChromaDB",
    "QuantumFAISS",
]
