"""
Analysis Features Package

This package contains all analysis-related features for the SNID GUI.
"""

from .games_integration import GamesIntegration
from .analysis_controller import AnalysisController

# Wind velocity analysis (optional)
try:
    from .wind_velocity_controller import WindVelocityController
    WIND_VELOCITY_AVAILABLE = True
except ImportError:
    WindVelocityController = None
    WIND_VELOCITY_AVAILABLE = False

__all__ = ['GamesIntegration', 'AnalysisController']

# Add wind velocity controller if available
if WIND_VELOCITY_AVAILABLE:
    __all__.append('WindVelocityController') 
