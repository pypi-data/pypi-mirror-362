"""
SE-AGI: Self-Evolving General AI
The Holy Grail of Autonomous Intelligence

A revolutionary modular AI system capable of autonomous learning,
adaptation, and intelligence evolution.
"""

from .__version__ import __version__, __version_info__, RELEASE_STAGE

__author__ = "Krishna Bajpai"
__email__ = "bajpaikrishna715@gmail.com"

# License validation on import
from .licensing.validation import validate_seagi_license, display_license_info
from .licensing.exceptions import SEAGILicenseError

def _check_seagi_license():
    """Check SE-AGI license on package import."""
    try:
        validate_seagi_license()
        print("✅ SE-AGI licensed - ready for autonomous intelligence!")
    except SEAGILicenseError as e:
        print(f"⚠️ SE-AGI License Notice: {e}")
        import uuid
        machine_id = uuid.getnode()
        print(f"� Contact: bajpaikrishna715@gmail.com")
        print(f"🔧 Machine ID: {machine_id} (include this in your request)")
    except Exception as e:
        print(f"⚠️ License check failed: {e}")
        print("📧 Contact: bajpaikrishna715@gmail.com for support")

# Perform license check on import
_check_seagi_license()

from .core.seagi import SEAGI
from .core.config import AgentConfig, SEAGIConfig
from .core.meta_learner import MetaLearner
from .core.reflection import ReflectionEngine
from .agents.base import BaseAgent
from .agents.meta_agent import MetaAgent
from .agents.research_agent import ResearchAgent
from .agents.creative_agent import CreativeAgent
from .agents.analysis_agent import AnalysisAgent
from .agents.tool_agent import ToolAgent
from .reasoning.multimodal import MultiModalReasoner
from .memory.episodic import EpisodicMemory
from .memory.semantic import SemanticMemory
from .evolution.capability_evolution import CapabilityEvolver
from .safety.monitor import SafetyMonitor
from .safety.alignment import AlignmentChecker

# Core components for easy access
__all__ = [
    "SEAGI",
    "AgentConfig", 
    "SEAGIConfig",
    "MetaLearner",
    "ReflectionEngine",
    "BaseAgent",
    "MetaAgent",
    "ResearchAgent",
    "CreativeAgent", 
    "AnalysisAgent",
    "ToolAgent",
    "MultiModalReasoner",
    "EpisodicMemory",
    "SemanticMemory",
    "CapabilityEvolver",
    "SafetyMonitor",
    "AlignmentChecker",
]

# Version info
VERSION = __version__
