"""Legacy compatibility classes for CRCreditum."""

from typing import Dict, Any, Optional
from .assessment import CreditAssessment


class CreditApplication:
    """Legacy CreditApplication class for backward compatibility."""
    
    def __init__(self):
        """Initialize legacy credit application."""
        self._assessment_engine = CreditAssessment()
    
    def assess_individual(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Legacy individual assessment method."""
        return self._assessment_engine.assess_individual(data)
    
    def assess_business(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Legacy business assessment method."""
        return self._assessment_engine.assess_business(data)
    
    def get_version(self) -> str:
        """Get version information."""
        return self._assessment_engine.version


class CreditConfig:
    """Legacy configuration class."""
    
    def __init__(self):
        """Initialize legacy configuration."""
        self.individual_approval_threshold = 0.7
        self.corporate_approval_threshold = 0.65
        self.enable_enhanced_features = True
        self.enable_cra_compliance = True
        self.enable_basel_integration = True
        
        # Economic weights for assessment
        self.economic_weights = {
            "gdp_growth": 0.25,
            "unemployment_rate": 0.20,
            "inflation_rate": 0.15,
            "federal_funds_rate": 0.15,
            "consumer_confidence": 0.10,
            "housing_starts": 0.10,
            "business_investment": 0.05
        }
        
        # Economic scenarios
        self.economic_scenarios = {
            "baseline": {
                "gdp_growth": 0.025,
                "unemployment_rate": 0.045,
                "inflation_rate": 0.025,
                "federal_funds_rate": 0.035
            },
            "recession": {
                "gdp_growth": -0.02,
                "unemployment_rate": 0.08,
                "inflation_rate": 0.01,
                "federal_funds_rate": 0.01
            },
            "expansion": {
                "gdp_growth": 0.04,
                "unemployment_rate": 0.035,
                "inflation_rate": 0.035,
                "federal_funds_rate": 0.05
            }
        }
        
        # Cache settings
        self.cache_ttl = 3600  # 1 hour
        
    def get_economic_scenario(self, scenario_name: str) -> Dict[str, float]:
        """Get economic scenario by name."""
        return self.economic_scenarios.get(scenario_name, self.economic_scenarios["baseline"])
    
    def update_threshold(self, assessment_type: str, threshold: float) -> None:
        """Update approval threshold."""
        if assessment_type == "individual":
            self.individual_approval_threshold = threshold
        elif assessment_type == "corporate":
            self.corporate_approval_threshold = threshold