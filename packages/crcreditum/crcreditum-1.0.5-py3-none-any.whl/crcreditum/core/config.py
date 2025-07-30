"""Configuration management for CRCreditum."""

from typing import Dict, Any, Optional
import os
import json


class CreditConfig:
    """Central configuration manager for CRCreditum."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration with defaults and optional config file.
        
        Args:
            config_file: Path to JSON configuration file
        """
        # Default configuration
        self._load_defaults()
        
        # Load from file if provided
        if config_file and os.path.exists(config_file):
            self._load_from_file(config_file)
        
        # Override with environment variables
        self._load_from_environment()
    
    def _load_defaults(self):
        """Load default configuration values."""
        
        # Assessment thresholds
        self.individual_approval_threshold = 0.7
        self.corporate_approval_threshold = 0.65
        self.enhanced_assessment_threshold = 0.8
        
        # Feature flags
        self.enable_cra_enhancement = True
        self.enable_basel_compliance = True
        self.enable_explainability = True
        self.enable_stress_testing = True
        self.enable_monte_carlo = True
        
        # Economic factor weights
        self.economic_weights = {
            "gdp_growth": 0.25,
            "unemployment_rate": 0.20,
            "inflation_rate": 0.15,
            "federal_funds_rate": 0.15,
            "consumer_confidence": 0.10,
            "housing_starts": 0.10,
            "business_investment": 0.05
        }
        
        # Risk model parameters
        self.risk_model_config = {
            "default_model": "xgboost",
            "enable_ensemble": True,
            "cross_validation_folds": 5,
            "feature_selection_threshold": 0.01,
            "max_features": 50
        }
        
        # CRA configuration
        self.cra_config = {
            "lmi_income_threshold": 0.8,  # 80% of AMI
            "small_business_threshold": 1000000,  # $1M revenue
            "cra_test_weights": {
                "lending": 0.5,
                "investment": 0.25,
                "service": 0.25
            }
        }
        
        # Basel III configuration
        self.basel_config = {
            "min_cet1_ratio": 4.5,
            "min_tier1_ratio": 6.0,
            "min_total_capital_ratio": 8.0,
            "min_leverage_ratio": 3.0,
            "min_lcr": 100.0,
            "min_nsfr": 100.0,
            "capital_conservation_buffer": 2.5,
            "countercyclical_buffer": 0.0
        }
        
        # Stress testing configuration
        self.stress_test_config = {
            "default_scenarios": ["ccar_baseline", "ccar_adverse", "ccar_severely_adverse"],
            "monte_carlo_simulations": 1000,
            "confidence_levels": [0.95, 0.99],
            "correlation_adjustment": True
        }
        
        # Performance and caching
        self.cache_ttl = 3600  # 1 hour
        self.max_cache_size = 1000
        self.enable_async_processing = False
        self.batch_size = 100
        
        # Logging and monitoring
        self.log_level = "INFO"
        self.enable_metrics = True
        self.metrics_export_interval = 300  # 5 minutes
        
        # Economic scenarios
        self.economic_scenarios = {
            "baseline": {
                "gdp_growth": 0.025,
                "unemployment_rate": 0.045,
                "inflation_rate": 0.025,
                "federal_funds_rate": 0.035,
                "consumer_confidence": 100.0,
                "housing_starts": 1.2,
                "business_investment": 0.03
            },
            "recession": {
                "gdp_growth": -0.02,
                "unemployment_rate": 0.08,
                "inflation_rate": 0.01,
                "federal_funds_rate": 0.01,
                "consumer_confidence": 70.0,
                "housing_starts": 0.8,
                "business_investment": -0.05
            },
            "expansion": {
                "gdp_growth": 0.04,
                "unemployment_rate": 0.035,
                "inflation_rate": 0.035,
                "federal_funds_rate": 0.05,
                "consumer_confidence": 120.0,
                "housing_starts": 1.5,
                "business_investment": 0.06
            },
            "stagflation": {
                "gdp_growth": 0.005,
                "unemployment_rate": 0.07,
                "inflation_rate": 0.06,
                "federal_funds_rate": 0.06,
                "consumer_confidence": 80.0,
                "housing_starts": 0.9,
                "business_investment": 0.01
            }
        }
        
        # API configuration
        self.api_config = {
            "timeout": 30,
            "max_retries": 3,
            "rate_limit": 1000,  # requests per hour
            "enable_authentication": True
        }
    
    def _load_from_file(self, config_file: str):
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
            
            # Update configuration with file values
            for key, value in file_config.items():
                if hasattr(self, key):
                    if isinstance(getattr(self, key), dict) and isinstance(value, dict):
                        # Merge dictionaries
                        getattr(self, key).update(value)
                    else:
                        setattr(self, key, value)
        
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
    
    def _load_from_environment(self):
        """Load configuration from environment variables."""
        
        # Assessment thresholds
        if os.getenv("CRCREDITUM_INDIVIDUAL_THRESHOLD"):
            self.individual_approval_threshold = float(os.getenv("CRCREDITUM_INDIVIDUAL_THRESHOLD"))
        
        if os.getenv("CRCREDITUM_CORPORATE_THRESHOLD"):
            self.corporate_approval_threshold = float(os.getenv("CRCREDITUM_CORPORATE_THRESHOLD"))
        
        # Feature flags
        if os.getenv("CRCREDITUM_ENABLE_CRA"):
            self.enable_cra_enhancement = os.getenv("CRCREDITUM_ENABLE_CRA").lower() == "true"
        
        if os.getenv("CRCREDITUM_ENABLE_BASEL"):
            self.enable_basel_compliance = os.getenv("CRCREDITUM_ENABLE_BASEL").lower() == "true"
        
        # Cache settings
        if os.getenv("CRCREDITUM_CACHE_TTL"):
            self.cache_ttl = int(os.getenv("CRCREDITUM_CACHE_TTL"))
        
        # Logging
        if os.getenv("CRCREDITUM_LOG_LEVEL"):
            self.log_level = os.getenv("CRCREDITUM_LOG_LEVEL").upper()
    
    def get_economic_scenario(self, scenario_name: str) -> Dict[str, float]:
        """
        Get economic scenario by name.
        
        Args:
            scenario_name: Name of the scenario
            
        Returns:
            Economic scenario parameters
        """
        return self.economic_scenarios.get(scenario_name, self.economic_scenarios["baseline"])
    
    def update_threshold(self, assessment_type: str, threshold: float):
        """
        Update approval threshold for assessment type.
        
        Args:
            assessment_type: "individual" or "corporate"
            threshold: New threshold value (0-1)
        """
        if assessment_type == "individual":
            self.individual_approval_threshold = threshold
        elif assessment_type == "corporate":
            self.corporate_approval_threshold = threshold
        else:
            raise ValueError(f"Unknown assessment type: {assessment_type}")
    
    def update_economic_weights(self, weights: Dict[str, float]):
        """
        Update economic factor weights.
        
        Args:
            weights: Dictionary of factor weights
        """
        # Validate weights sum to 1.0 (approximately)
        total_weight = sum(weights.values())
        if abs(total_weight - 1.0) > 0.01:
            raise ValueError(f"Economic weights must sum to 1.0, got {total_weight}")
        
        self.economic_weights.update(weights)
    
    def add_custom_scenario(self, name: str, scenario: Dict[str, float]):
        """
        Add custom economic scenario.
        
        Args:
            name: Scenario name
            scenario: Economic parameters
        """
        required_factors = ["gdp_growth", "unemployment_rate", "inflation_rate", "federal_funds_rate"]
        
        for factor in required_factors:
            if factor not in scenario:
                raise ValueError(f"Missing required factor: {factor}")
        
        self.economic_scenarios[name] = scenario
    
    def get_feature_flag(self, flag_name: str) -> bool:
        """
        Get feature flag value.
        
        Args:
            flag_name: Name of the feature flag
            
        Returns:
            Feature flag value
        """
        return getattr(self, f"enable_{flag_name}", False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Export configuration as dictionary."""
        config_dict = {}
        
        for attr in dir(self):
            if not attr.startswith('_') and not callable(getattr(self, attr)):
                config_dict[attr] = getattr(self, attr)
        
        return config_dict
    
    def save_to_file(self, config_file: str):
        """
        Save current configuration to JSON file.
        
        Args:
            config_file: Path to save configuration
        """
        config_dict = self.to_dict()
        
        with open(config_file, 'w') as f:
            json.dump(config_dict, f, indent=2)
    
    def validate_configuration(self) -> Dict[str, Any]:
        """
        Validate current configuration.
        
        Returns:
            Validation results
        """
        issues = []
        warnings = []
        
        # Validate thresholds
        if not 0 <= self.individual_approval_threshold <= 1:
            issues.append("Individual approval threshold must be between 0 and 1")
        
        if not 0 <= self.corporate_approval_threshold <= 1:
            issues.append("Corporate approval threshold must be between 0 and 1")
        
        # Validate economic weights
        total_weight = sum(self.economic_weights.values())
        if abs(total_weight - 1.0) > 0.01:
            issues.append(f"Economic weights sum to {total_weight:.3f}, should be 1.0")
        
        # Validate Basel minimums
        if self.basel_config["min_cet1_ratio"] < 0:
            issues.append("Basel CET1 minimum ratio cannot be negative")
        
        # Check cache settings
        if self.cache_ttl < 0:
            warnings.append("Negative cache TTL will disable caching")
        
        # Check Monte Carlo settings
        if self.stress_test_config["monte_carlo_simulations"] < 100:
            warnings.append("Monte Carlo simulations below 100 may be unreliable")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "total_issues": len(issues),
            "total_warnings": len(warnings)
        }
    
    def reset_to_defaults(self):
        """Reset configuration to default values."""
        self._load_defaults()
    
    def __repr__(self) -> str:
        """String representation of configuration."""
        return f"CreditConfig(individual_threshold={self.individual_approval_threshold}, corporate_threshold={self.corporate_approval_threshold})"