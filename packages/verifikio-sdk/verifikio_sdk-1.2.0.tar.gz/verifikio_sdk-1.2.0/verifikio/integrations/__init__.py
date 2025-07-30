"""
Verifik.io SDK Integrations

This module provides callback handlers for popular AI frameworks.
"""

from typing import TYPE_CHECKING

__all__ = []

# Conditional imports to avoid forcing dependencies
if TYPE_CHECKING:
    from .crewai import VerifikCrewAIHandler
    from .langchain import VerifikLangChainHandler
    __all__.extend(['VerifikCrewAIHandler', 'VerifikLangChainHandler'])