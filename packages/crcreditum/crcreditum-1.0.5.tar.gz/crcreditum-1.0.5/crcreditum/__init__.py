"""
CRCreditum - Advanced Credit Risk Assessment Platform

A comprehensive credit risk assessment platform that integrates Community Reinvestment Act (CRA) 
compliance, Basel III regulatory frameworks, and advanced machine learning for financial institutions.
"""

__version__ = "1.0.5"
__author__ = "CRCreditum Team"
__email__ = "support@crcreditum.com"
__license__ = "MIT"

# Core imports for backward compatibility
from .schemas.legacy import CreditApplication, CreditConfig
from .schemas.assessment import CreditAssessment

# Main assessment classes
from .schemas.individual import IndividualAssessment
from .schemas.corporate import CorporateAssessment

# Model imports
from .models.cra import CRAAnalyzer
from .models.basel import BaselIIICalculator
from .models.explainability import ExplainabilityEngine
from .models.stress_testing import StressTestingEngine

# Configuration
from .core.config import CreditConfig as CoreConfig

__all__ = [
    # Core classes
    "CreditAssessment",
    "IndividualAssessment", 
    "CorporateAssessment",
    
    # Legacy compatibility
    "CreditApplication",
    "CreditConfig",
    
    # Model classes
    "CRAAnalyzer",
    "BaselIIICalculator", 
    "ExplainabilityEngine",
    "StressTestingEngine",
    
    # Configuration
    "CoreConfig",
    
    # Metadata
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]

# Package metadata
PACKAGE_INFO = {
    "name": "crcreditum",
    "version": __version__,
    "description": "Advanced Credit Risk Assessment with CRA Compliance and Basel III Integration",
    "features": [
        "Enhanced Credit Assessment (28+ individual, 32+ corporate fields)",
        "CRA Compliance Analysis (3-test framework)",
        "Basel III Integration (capital ratios, liquidity metrics)",
        "Explainable AI (SHAP-powered interpretability)",
        "Stress Testing (CCAR, DFAST, Monte Carlo)",
        "Real-time Analytics (economic factor integration)"
    ],
    "supported_types": ["individual", "business", "enhanced"],
    "compliance_frameworks": ["CRA", "Basel III", "CCAR", "DFAST"],
    "ml_models": ["XGBoost", "LightGBM", "Ensemble"],
    "total_assessments": 0  # Will be updated by assessment instances
}

def get_package_info():
    """Get comprehensive package information."""
    return PACKAGE_INFO.copy()

def get_version():
    """Get package version."""
    return __version__

def get_supported_features():
    """Get list of supported features."""
    return PACKAGE_INFO["features"]

# Initialize logging (optional)
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())