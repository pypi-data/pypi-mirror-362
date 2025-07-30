"""
QuantumMetaGPT - Autonomous Quantum AI Research Agent
Copyright (C) 2025 - All rights reserved.

This software requires a valid license for operation.
For licensing information contact: bajpaikrishna715@gmail.com
"""

__version__ = "1.0.0"
__license_package__ = "quantummetagpt"

# Import licensing system first
from .licensing import LicenseEnforcer, show_license_info, get_machine_id

# Initialize licensing on package import
print("🔬 Initializing QuantumMetaGPT...")
print(f"🔧 Machine ID: {get_machine_id()}")

# Validate license immediately on import
_license_enforcer = LicenseEnforcer()
_license_enforcer.validate_license()

print("✅ QuantumMetaGPT licensed and ready!")
print("📋 Use show_license_info() to view license details")

# Import main modules after license validation
from .quantum_algorithm_generator import *
from .evaluation_engine import *
from .optimizer_engine import *
from .llm_paper_parser import *
from .report_generator import *
from .task_synthesizer import *
from .frontend_interface import *

__all__ = [
    'show_license_info',
    'get_machine_id'
]