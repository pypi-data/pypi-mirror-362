"""
Q-Memetic AI: Quantum-Inspired Memetic Computing System

A revolutionary AI system that evolves, mutates, and entangles memes
across users, systems, and timelines using quantum-inspired algorithms.

🔐 LICENSED SOFTWARE - QuantumMeta License Required
Grace Period: 24 hours from first use
License Support: bajpaikrishna715@gmail.com
"""

__version__ = "0.1.0"
__author__ = "Krishna Bajpai"
__email__ = "bajpaikrishna715@gmail.com"
__license_package__ = "qmemetic-ai"

# QuantumMeta License Integration
try:
    from quantummeta_license import validate_or_grace, LicenseError
    QUANTUMMETA_AVAILABLE = True
except ImportError:
    QUANTUMMETA_AVAILABLE = False

def _check_license():
    """Check license on package import."""
    if QUANTUMMETA_AVAILABLE:
        try:
            validate_or_grace(__license_package__, grace_days=1)  # 24 hour grace period
        except LicenseError as e:
            print("🔒 Q-MEMETIC AI LICENSE REQUIRED")
            print("=" * 50)
            print(f"License validation failed: {e}")
            print()
            print("To activate Q-Memetic AI:")
            print("1. Get license: https://krish567366.github.io/license-server/")
            print("2. Or email: bajpaikrishna715@gmail.com")
            print(f"   Include machine ID: {_get_machine_id()}")
            print()
            print("Grace period: 24 hours from first use")
            print("=" * 50)
            # Raise exception to prevent package use after grace period
            if "grace period expired" in str(e).lower():
                raise RuntimeError("Q-Memetic AI license required - grace period expired")
    else:
        print("⚠️  QuantumMeta license validation unavailable - running in limited mode")

def _get_machine_id():
    """Get machine ID for license support."""
    import platform
    import hashlib
    machine_info = f"{platform.machine()}_{platform.processor()}_{platform.system()}"
    return hashlib.sha256(machine_info.encode()).hexdigest()[:16]

# Automatic license check on import
_check_license()

# Import core classes (will be license-protected)
from .core.engine import MemeticEngine
from .core.meme import Meme, MemeVector
from .core.entanglement import QuantumEntangler
from .core.evolution import GeneticEvolver
from .licensing.manager import LicenseManager
from .federation.client import FederatedClient
from .visualization.noosphere import NoosphereVisualizer

__all__ = [
    "MemeticEngine",
    "Meme",
    "MemeVector", 
    "QuantumEntangler",
    "GeneticEvolver",
    "LicenseManager",
    "FederatedClient",
    "NoosphereVisualizer",
]
