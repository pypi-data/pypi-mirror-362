"""Comprehensive stress testing engine for credit risk models."""

from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Field
from enum import Enum
import numpy as np
import math


class StressTestType(str, Enum):
    """Types of stress tests available."""
    CCAR = "ccar"
    DFAST = "dfast"
    CUSTOM = "custom"
    MONTE_CARLO = "monte_carlo"
    SENSITIVITY = "sensitivity"


class StressTestResult(BaseModel):
    """Stress test result container."""
    test_type: StressTestType = Field(..., description="Type of stress test")
    scenario_name: str = Field(..., description="Name of stress scenario")
    baseline_metrics: Dict[str, float] = Field(..., description="Baseline portfolio metrics")
    stressed_metrics: Dict[str, float] = Field(..., description="Stressed portfolio metrics")
    impact_analysis: Dict[str, Any] = Field(..., description="Impact analysis results")
    compliance_status: Dict[str, bool] = Field(..., description="Regulatory compliance status")
    recommendations: List[str] = Field(default_factory=list, description="Risk management recommendations")
    confidence_interval: Optional[Dict[str, float]] = Field(None, description="Confidence intervals for results")


class StressTestingEngine:
    """Comprehensive stress testing engine with multiple scenario types."""
    
    def __init__(self):
        """Initialize stress testing engine with predefined scenarios."""
        
        # CCAR stress scenarios (simplified versions)
        self.ccar_scenarios = {
            "ccar_baseline": {
                "gdp_growth": [0.025, 0.024, 0.023],
                "unemployment_rate": [0.042, 0.041, 0.040],
                "fed_funds_rate": [0.035, 0.040, 0.045],
                "house_price_index": [1.03, 1.025, 1.02],
                "commercial_real_estate": [1.01, 1.005, 1.00],
                "equity_prices": [1.05, 1.04, 1.03],
                "credit_spread": [0.015, 0.016, 0.017]
            },
            "ccar_adverse": {
                "gdp_growth": [-0.005, -0.01, 0.005],
                "unemployment_rate": [0.055, 0.065, 0.060],
                "fed_funds_rate": [0.025, 0.015, 0.020],
                "house_price_index": [0.95, 0.92, 0.94],
                "commercial_real_estate": [0.92, 0.88, 0.90],
                "equity_prices": [0.85, 0.82, 0.88],
                "credit_spread": [0.025, 0.030, 0.028]
            },
            "ccar_severely_adverse": {
                "gdp_growth": [-0.035, -0.08, -0.04],
                "unemployment_rate": [0.075, 0.105, 0.095],
                "fed_funds_rate": [0.005, 0.005, 0.005],
                "house_price_index": [0.88, 0.75, 0.82],
                "commercial_real_estate": [0.85, 0.70, 0.78],
                "equity_prices": [0.65, 0.50, 0.60],
                "credit_spread": [0.045, 0.055, 0.050]
            }
        }
        
        # DFAST scenarios
        self.dfast_scenarios = {
            "dfast_baseline": self.ccar_scenarios["ccar_baseline"],
            "dfast_adverse": self.ccar_scenarios["ccar_adverse"],
            "dfast_severely_adverse": self.ccar_scenarios["ccar_severely_adverse"]
        }
        
        # Risk factor correlations (simplified)
        self.risk_correlations = {
            ("gdp_growth", "unemployment_rate"): -0.7,
            ("gdp_growth", "equity_prices"): 0.6,
            ("unemployment_rate", "credit_spread"): 0.5,
            ("house_price_index", "equity_prices"): 0.4,
            ("fed_funds_rate", "credit_spread"): -0.3
        }
        
        # Basel III minimum requirements for compliance checking
        self.basel_minimums = {
            "tier1_capital_ratio": 6.0,
            "total_capital_ratio": 8.0,
            "leverage_ratio": 3.0,
            "lcr": 100.0,
            "nsfr": 100.0
        }
    
    def run_stress_test(
        self,
        scenario_name: str,
        portfolio_data: Dict[str, float],
        model: Any,
        test_type: StressTestType = StressTestType.CCAR
    ) -> StressTestResult:
        """
        Run comprehensive stress test on portfolio.
        
        Args:
            scenario_name: Name of stress scenario
            portfolio_data: Portfolio metrics and exposures
            model: Credit risk model
            test_type: Type of stress test
            
        Returns:
            Stress test results
        """
        
        # Get scenario parameters
        if test_type == StressTestType.CCAR:
            scenario = self.ccar_scenarios.get(scenario_name)
        elif test_type == StressTestType.DFAST:
            scenario = self.dfast_scenarios.get(scenario_name)
        else:
            raise ValueError(f"Scenario {scenario_name} not found for test type {test_type}")
        
        if not scenario:
            raise ValueError(f"Unknown scenario: {scenario_name}")
        
        # Calculate baseline metrics
        baseline_metrics = self._calculate_baseline_metrics(portfolio_data)
        
        # Apply stress scenario
        stressed_metrics = self._apply_stress_scenario(
            portfolio_data, scenario, model, test_type
        )
        
        # Analyze impact
        impact_analysis = self._analyze_stress_impact(baseline_metrics, stressed_metrics)
        
        # Check compliance
        compliance_status = self._check_stress_compliance(stressed_metrics)
        
        # Generate recommendations
        recommendations = self._generate_stress_recommendations(
            impact_analysis, compliance_status, scenario_name
        )
        
        return StressTestResult(
            test_type=test_type,
            scenario_name=scenario_name,
            baseline_metrics=baseline_metrics,
            stressed_metrics=stressed_metrics,
            impact_analysis=impact_analysis,
            compliance_status=compliance_status,
            recommendations=recommendations
        )
    
    def _calculate_baseline_metrics(self, portfolio_data: Dict[str, float]) -> Dict[str, float]:
        """Calculate baseline portfolio metrics."""
        
        total_exposure = portfolio_data.get("total_exposure", 0)
        weighted_avg_pd = portfolio_data.get("weighted_avg_pd", 0.02)
        weighted_avg_lgd = portfolio_data.get("weighted_avg_lgd", 0.45)
        weighted_avg_ead = portfolio_data.get("weighted_avg_ead", total_exposure * 0.75)
        
        # Calculate expected loss
        expected_loss = weighted_avg_pd * weighted_avg_lgd * weighted_avg_ead
        
        # Calculate capital ratios
        tier1_capital = portfolio_data.get("tier1_capital", total_exposure * 0.08)
        total_capital = portfolio_data.get("total_capital", total_exposure * 0.12)
        rwa = portfolio_data.get("rwa", total_exposure * 0.8)
        
        tier1_ratio = (tier1_capital / rwa) * 100 if rwa > 0 else 0
        total_capital_ratio = (total_capital / rwa) * 100 if rwa > 0 else 0
        leverage_ratio = (tier1_capital / total_exposure) * 100 if total_exposure > 0 else 0
        
        # Liquidity ratios
        lcr = portfolio_data.get("lcr", 125.0)
        nsfr = portfolio_data.get("nsfr", 115.0)
        
        return {
            "total_exposure": total_exposure,
            "expected_loss": expected_loss,
            "tier1_capital_ratio": tier1_ratio,
            "total_capital_ratio": total_capital_ratio,
            "leverage_ratio": leverage_ratio,
            "lcr": lcr,
            "nsfr": nsfr,
            "rwa": rwa,
            "tier1_capital": tier1_capital,
            "total_capital": total_capital
        }
    
    def _apply_stress_scenario(
        self,
        portfolio_data: Dict[str, float],
        scenario: Dict[str, List[float]],
        model: Any,
        test_type: StressTestType
    ) -> Dict[str, float]:
        """Apply stress scenario to portfolio."""
        
        # Start with baseline metrics
        baseline = self._calculate_baseline_metrics(portfolio_data)
        stressed = baseline.copy()
        
        # Extract scenario values (using most severe year)
        gdp_growth = min(scenario.get("gdp_growth", [0]))
        unemployment_rate = max(scenario.get("unemployment_rate", [0.05]))
        house_price_index = min(scenario.get("house_price_index", [1.0]))
        equity_prices = min(scenario.get("equity_prices", [1.0]))
        credit_spread = max(scenario.get("credit_spread", [0.02]))
        
        # Calculate stress multipliers
        pd_multiplier = self._calculate_pd_stress_multiplier(
            gdp_growth, unemployment_rate, credit_spread
        )
        lgd_multiplier = self._calculate_lgd_stress_multiplier(
            house_price_index, equity_prices
        )
        
        # Apply stress to credit parameters
        stressed_pd = baseline["expected_loss"] / (baseline["total_exposure"] * 0.45) * pd_multiplier
        stressed_lgd = 0.45 * lgd_multiplier
        
        # Recalculate expected loss
        stressed["expected_loss"] = stressed_pd * stressed_lgd * baseline["total_exposure"] * 0.75
        
        # Apply capital impact
        capital_impact = stressed["expected_loss"] - baseline["expected_loss"]
        stressed["tier1_capital"] = max(0, baseline["tier1_capital"] - capital_impact * 1.5)
        stressed["total_capital"] = max(0, baseline["total_capital"] - capital_impact * 1.2)
        
        # Recalculate ratios
        stressed["tier1_capital_ratio"] = (stressed["tier1_capital"] / baseline["rwa"]) * 100
        stressed["total_capital_ratio"] = (stressed["total_capital"] / baseline["rwa"]) * 100
        stressed["leverage_ratio"] = (stressed["tier1_capital"] / baseline["total_exposure"]) * 100
        
        # Apply liquidity stress
        liquidity_stress_factor = 1 - (gdp_growth + 0.05) * 2  # More severe GDP decline = more liquidity stress
        stressed["lcr"] = baseline["lcr"] * max(0.7, liquidity_stress_factor)
        stressed["nsfr"] = baseline["nsfr"] * max(0.8, liquidity_stress_factor)
        
        return stressed
    
    def _calculate_pd_stress_multiplier(
        self, 
        gdp_growth: float, 
        unemployment_rate: float, 
        credit_spread: float
    ) -> float:
        """Calculate PD stress multiplier based on economic factors."""
        
        # Base multiplier
        multiplier = 1.0
        
        # GDP impact (negative growth increases PD)
        if gdp_growth < 0:
            multiplier += abs(gdp_growth) * 15  # 15x multiplier for GDP decline
        
        # Unemployment impact
        unemployment_stress = max(0, unemployment_rate - 0.04)  # Above 4% baseline
        multiplier += unemployment_stress * 10
        
        # Credit spread impact
        spread_stress = max(0, credit_spread - 0.015)  # Above 1.5% baseline
        multiplier += spread_stress * 20
        
        return min(5.0, multiplier)  # Cap at 5x
    
    def _calculate_lgd_stress_multiplier(
        self, 
        house_price_index: float, 
        equity_prices: float
    ) -> float:
        """Calculate LGD stress multiplier based on asset prices."""
        
        # Base multiplier
        multiplier = 1.0
        
        # House price impact
        if house_price_index < 1.0:
            house_price_stress = (1.0 - house_price_index) * 0.5
            multiplier += house_price_stress
        
        # Equity price impact
        if equity_prices < 1.0:
            equity_stress = (1.0 - equity_prices) * 0.3
            multiplier += equity_stress
        
        return min(2.0, multiplier)  # Cap at 2x
    
    def _analyze_stress_impact(
        self, 
        baseline: Dict[str, float], 
        stressed: Dict[str, float]
    ) -> Dict[str, Any]:
        """Analyze impact of stress scenario."""
        
        impact = {}
        
        # Calculate changes
        for metric in baseline:
            if metric in stressed:
                baseline_val = baseline[metric]
                stressed_val = stressed[metric]
                
                if baseline_val != 0:
                    change_pct = ((stressed_val - baseline_val) / baseline_val) * 100
                else:
                    change_pct = 0
                
                impact[f"{metric}_change"] = stressed_val - baseline_val
                impact[f"{metric}_change_pct"] = change_pct
        
        # Overall impact assessment
        capital_impact = impact.get("tier1_capital_ratio_change", 0)
        loss_impact = impact.get("expected_loss_change", 0)
        
        if capital_impact < -200:  # More than 2% decline in Tier 1
            overall_impact = "severe"
        elif capital_impact < -100:  # 1-2% decline
            overall_impact = "moderate"
        elif capital_impact < -50:   # 0.5-1% decline
            overall_impact = "mild"
        else:
            overall_impact = "minimal"
        
        impact["overall_impact"] = overall_impact
        impact["loss_multiple"] = loss_impact / baseline["expected_loss"] if baseline["expected_loss"] > 0 else 0
        
        return impact
    
    def _check_stress_compliance(self, stressed_metrics: Dict[str, float]) -> Dict[str, bool]:
        """Check regulatory compliance under stress."""
        
        compliance = {}
        
        # Check Basel III requirements
        compliance["tier1_capital_adequate"] = stressed_metrics.get("tier1_capital_ratio", 0) >= self.basel_minimums["tier1_capital_ratio"]
        compliance["total_capital_adequate"] = stressed_metrics.get("total_capital_ratio", 0) >= self.basel_minimums["total_capital_ratio"]
        compliance["leverage_adequate"] = stressed_metrics.get("leverage_ratio", 0) >= self.basel_minimums["leverage_ratio"]
        compliance["lcr_adequate"] = stressed_metrics.get("lcr", 0) >= self.basel_minimums["lcr"]
        compliance["nsfr_adequate"] = stressed_metrics.get("nsfr", 0) >= self.basel_minimums["nsfr"]
        
        # Overall compliance
        compliance["overall_compliant"] = all(compliance.values())
        
        return compliance
    
    def _generate_stress_recommendations(
        self,
        impact_analysis: Dict[str, Any],
        compliance_status: Dict[str, bool],
        scenario_name: str
    ) -> List[str]:
        """Generate recommendations based on stress test results."""
        
        recommendations = []
        
        # Capital recommendations
        if not compliance_status.get("tier1_capital_adequate", True):
            recommendations.append("Increase Tier 1 capital to meet regulatory minimums under stress")
        
        if not compliance_status.get("total_capital_adequate", True):
            recommendations.append("Raise additional capital to maintain total capital adequacy")
        
        # Liquidity recommendations
        if not compliance_status.get("lcr_adequate", True):
            recommendations.append("Increase high-quality liquid assets to improve LCR")
        
        if not compliance_status.get("nsfr_adequate", True):
            recommendations.append("Adjust funding profile to meet NSFR requirements")
        
        # Risk management recommendations
        overall_impact = impact_analysis.get("overall_impact", "minimal")
        
        if overall_impact == "severe":
            recommendations.extend([
                "Consider reducing risk exposures in vulnerable sectors",
                "Implement enhanced monitoring for early warning indicators",
                "Review and update risk appetite statements"
            ])
        elif overall_impact == "moderate":
            recommendations.extend([
                "Monitor portfolio concentration risks",
                "Consider hedging strategies for key risk factors"
            ])
        
        # Scenario-specific recommendations
        if "severely_adverse" in scenario_name:
            recommendations.append("Develop contingency plans for severe economic downturn")
        
        return recommendations
    
    def sensitivity_analysis(
        self,
        portfolio_data: Dict[str, float],
        model: Any,
        risk_factor: str,
        factor_range: Tuple[float, float],
        num_steps: int = 10
    ) -> Dict[str, Any]:
        """Perform sensitivity analysis on a specific risk factor."""
        
        baseline_metrics = self._calculate_baseline_metrics(portfolio_data)
        
        # Generate factor values
        min_val, max_val = factor_range
        factor_values = np.linspace(min_val, max_val, num_steps)
        
        results = []
        
        for factor_value in factor_values:
            # Create scenario with single factor stress
            scenario = {risk_factor: [factor_value]}
            
            # Apply stress
            stressed_metrics = self._apply_stress_scenario(
                portfolio_data, scenario, model, StressTestType.SENSITIVITY
            )
            
            # Calculate impact
            tier1_impact = stressed_metrics["tier1_capital_ratio"] - baseline_metrics["tier1_capital_ratio"]
            loss_impact = stressed_metrics["expected_loss"] - baseline_metrics["expected_loss"]
            
            results.append({
                "factor_value": factor_value,
                "tier1_impact": tier1_impact,
                "loss_impact": loss_impact,
                "tier1_ratio": stressed_metrics["tier1_capital_ratio"]
            })
        
        # Calculate sensitivity metrics
        tier1_sensitivity = self._calculate_sensitivity_coefficient(
            [r["factor_value"] for r in results],
            [r["tier1_impact"] for r in results]
        )
        
        loss_sensitivity = self._calculate_sensitivity_coefficient(
            [r["factor_value"] for r in results],
            [r["loss_impact"] for r in results]
        )
        
        return {
            "factor_name": risk_factor,
            "factor_range": factor_range,
            "baseline_metrics": baseline_metrics,
            "sensitivity_results": results,
            "sensitivity_metrics": {
                "tier1_sensitivity": tier1_sensitivity,
                "loss_sensitivity": loss_sensitivity
            }
        }
    
    def _calculate_sensitivity_coefficient(self, x_values: List[float], y_values: List[float]) -> float:
        """Calculate sensitivity coefficient (slope)."""
        if len(x_values) < 2:
            return 0.0
        
        # Simple linear regression slope
        n = len(x_values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        
        denominator = n * sum_x2 - sum_x * sum_x
        if denominator == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        return slope
    
    def run_monte_carlo_simulation(
        self,
        portfolio_data: Dict[str, float],
        model: Any,
        num_simulations: int = 1000,
        confidence_levels: List[float] = [0.95, 0.99]
    ) -> Dict[str, Any]:
        """Run Monte Carlo simulation for risk assessment."""
        
        baseline_metrics = self._calculate_baseline_metrics(portfolio_data)
        simulation_results = []
        
        for _ in range(num_simulations):
            # Generate random scenario
            random_scenario = self._generate_random_scenario()
            
            # Apply stress
            stressed_metrics = self._apply_stress_scenario(
                portfolio_data, random_scenario, model, StressTestType.MONTE_CARLO
            )
            
            simulation_results.append({
                "tier1_ratio": stressed_metrics["tier1_capital_ratio"],
                "expected_loss": stressed_metrics["expected_loss"],
                "scenario": random_scenario
            })
        
        # Calculate statistics
        tier1_ratios = [r["tier1_ratio"] for r in simulation_results]
        expected_losses = [r["expected_loss"] for r in simulation_results]
        
        # Calculate VaR and Expected Shortfall
        var_results = {}
        es_results = {}
        
        for confidence_level in confidence_levels:
            percentile = (1 - confidence_level) * 100
            
            tier1_var = np.percentile(tier1_ratios, percentile)
            loss_var = np.percentile(expected_losses, percentile)
            
            # Expected Shortfall (average of tail)
            tier1_tail = [r for r in tier1_ratios if r <= tier1_var]
            loss_tail = [r for r in expected_losses if r >= loss_var]
            
            tier1_es = np.mean(tier1_tail) if tier1_tail else tier1_var
            loss_es = np.mean(loss_tail) if loss_tail else loss_var
            
            var_results[f"{confidence_level*100}%"] = {
                "tier1_var": tier1_var,
                "loss_var": loss_var
            }
            
            es_results[f"{confidence_level*100}%"] = {
                "tier1_es": tier1_es,
                "loss_es": loss_es
            }
        
        return {
            "num_simulations": num_simulations,
            "baseline_metrics": baseline_metrics,
            "simulation_statistics": {
                "tier1_mean": np.mean(tier1_ratios),
                "tier1_std": np.std(tier1_ratios),
                "tier1_min": np.min(tier1_ratios),
                "tier1_max": np.max(tier1_ratios),
                "loss_mean": np.mean(expected_losses),
                "loss_std": np.std(expected_losses),
                "loss_min": np.min(expected_losses),
                "loss_max": np.max(expected_losses)
            },
            "var_expected_loss": {k: v["loss_var"] for k, v in var_results.items()},
            "var_tier1_ratio": {k: v["tier1_var"] for k, v in var_results.items()},
            "expected_shortfall_loss": {k: v["loss_es"] for k, v in es_results.items()},
            "expected_shortfall_tier1": {k: v["tier1_es"] for k, v in es_results.items()}
        }
    
    def _generate_random_scenario(self) -> Dict[str, List[float]]:
        """Generate random stress scenario for Monte Carlo."""
        
        # Use normal distributions with correlations
        gdp_growth = np.random.normal(-0.02, 0.03)
        unemployment_rate = max(0.03, np.random.normal(0.06, 0.02))
        fed_funds_rate = max(0.0, np.random.normal(0.025, 0.015))
        house_price_index = max(0.5, np.random.normal(0.9, 0.1))
        equity_prices = max(0.3, np.random.normal(0.8, 0.15))
        credit_spread = max(0.01, np.random.normal(0.03, 0.01))
        
        return {
            "gdp_growth": [gdp_growth],
            "unemployment_rate": [unemployment_rate],
            "fed_funds_rate": [fed_funds_rate],
            "house_price_index": [house_price_index],
            "equity_prices": [equity_prices],
            "credit_spread": [credit_spread]
        }
    
    def get_available_scenarios(self) -> Dict[str, List[str]]:
        """Get list of available stress test scenarios."""
        return {
            "ccar": list(self.ccar_scenarios.keys()),
            "dfast": list(self.dfast_scenarios.keys())
        }