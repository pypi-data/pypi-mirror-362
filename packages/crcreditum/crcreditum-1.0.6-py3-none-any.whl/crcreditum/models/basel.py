"""Basel III compliance calculator and risk assessment module."""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import math


class BankFinancials(BaseModel):
    """Bank financial data for Basel III calculations."""
    
    # Capital Components
    common_equity_tier1: float = Field(..., ge=0, description="Common Equity Tier 1 capital")
    additional_tier1: float = Field(..., ge=0, description="Additional Tier 1 capital")
    tier2_capital: float = Field(..., ge=0, description="Tier 2 capital")
    
    # Assets and Exposures
    cash_and_equivalents: float = Field(..., ge=0, description="Cash and cash equivalents")
    sovereign_exposures: float = Field(..., ge=0, description="Sovereign exposures")
    bank_exposures: float = Field(..., ge=0, description="Bank exposures")
    corporate_exposures: float = Field(..., ge=0, description="Corporate exposures")
    retail_exposures: float = Field(..., ge=0, description="Retail exposures")
    real_estate_residential: float = Field(..., ge=0, description="Residential real estate")
    real_estate_commercial: float = Field(..., ge=0, description="Commercial real estate")
    past_due_exposures: float = Field(..., ge=0, description="Past due exposures")
    other_exposures: float = Field(..., ge=0, description="Other exposures")
    off_balance_sheet_exposures: float = Field(..., ge=0, description="Off-balance sheet exposures")
    derivatives_exposure: float = Field(..., ge=0, description="Derivatives exposure")
    
    # Liquidity Components
    high_quality_liquid_assets: float = Field(..., ge=0, description="High Quality Liquid Assets")
    cash_outflows_30d: float = Field(..., ge=0, description="Net cash outflows over 30 days")
    cash_inflows_30d: float = Field(..., ge=0, description="Cash inflows over 30 days")
    available_stable_funding: float = Field(..., ge=0, description="Available stable funding")
    required_stable_funding: float = Field(..., ge=0, description="Required stable funding")
    
    # Balance Sheet Items
    total_assets: float = Field(..., ge=0, description="Total assets")
    total_liabilities: float = Field(..., ge=0, description="Total liabilities")
    
    # Income Statement Items
    operating_income: float = Field(..., description="Operating income")
    gross_income: float = Field(..., ge=0, description="Gross income")


class BaselMetrics(BaseModel):
    """Basel III calculated metrics."""
    
    # Capital Ratios
    cet1_ratio: float = Field(..., description="Common Equity Tier 1 ratio")
    tier1_capital_ratio: float = Field(..., description="Tier 1 capital ratio")
    total_capital_ratio: float = Field(..., description="Total capital ratio")
    leverage_ratio: float = Field(..., description="Leverage ratio")
    
    # Liquidity Ratios
    liquidity_coverage_ratio: float = Field(..., description="Liquidity Coverage Ratio (LCR)")
    net_stable_funding_ratio: float = Field(..., description="Net Stable Funding Ratio (NSFR)")
    
    # Risk-Weighted Assets
    total_rwa: float = Field(..., description="Total Risk-Weighted Assets")
    credit_rwa: float = Field(..., description="Credit Risk-Weighted Assets")
    market_rwa: float = Field(..., description="Market Risk-Weighted Assets")
    operational_rwa: float = Field(..., description="Operational Risk-Weighted Assets")
    
    # Compliance Status
    is_compliant: bool = Field(..., description="Overall Basel III compliance status")
    compliance_issues: List[str] = Field(default_factory=list, description="Compliance issues")
    capital_surpluses: Dict[str, float] = Field(default_factory=dict, description="Capital surpluses/deficits")
    
    # Additional Metrics
    capital_conservation_buffer: float = Field(..., description="Capital conservation buffer")
    countercyclical_buffer: float = Field(..., description="Countercyclical capital buffer")


class BaselIIICalculator:
    """Basel III compliance calculator."""
    
    def __init__(self):
        """Initialize Basel III calculator with regulatory requirements."""
        
        # Minimum capital requirements (as percentages)
        self.min_cet1_ratio = 4.5
        self.min_tier1_ratio = 6.0
        self.min_total_capital_ratio = 8.0
        self.min_leverage_ratio = 3.0
        
        # Buffer requirements
        self.capital_conservation_buffer = 2.5
        self.countercyclical_buffer = 0.0  # Variable, set by regulators
        
        # Liquidity requirements
        self.min_lcr = 100.0
        self.min_nsfr = 100.0
        
        # Risk weights for different asset classes
        self.risk_weights = {
            "cash": 0.0,
            "sovereign": 0.0,    # Assuming AAA-rated sovereign
            "bank": 20.0,        # Short-term bank exposures
            "corporate": 100.0,  # Standard corporate
            "retail": 75.0,      # Qualifying retail
            "residential_re": 35.0,  # Residential real estate
            "commercial_re": 100.0,  # Commercial real estate
            "past_due": 150.0,   # Past due exposures
            "other": 100.0,      # Other exposures
            "off_balance_sheet": 50.0,  # Credit conversion factor
            "derivatives": 100.0  # Simplified for derivatives
        }
    
    def calculate_basel_metrics(self, bank_data: BankFinancials) -> BaselMetrics:
        """Calculate comprehensive Basel III metrics."""
        
        # Calculate Risk-Weighted Assets
        rwa_breakdown = self._calculate_rwa(bank_data)
        total_rwa = rwa_breakdown["total"]
        
        # Calculate capital ratios
        cet1_ratio = (bank_data.common_equity_tier1 / total_rwa) * 100
        tier1_capital = bank_data.common_equity_tier1 + bank_data.additional_tier1
        tier1_ratio = (tier1_capital / total_rwa) * 100
        total_capital = tier1_capital + bank_data.tier2_capital
        total_capital_ratio = (total_capital / total_rwa) * 100
        
        # Calculate leverage ratio
        total_exposure = self._calculate_total_exposure(bank_data)
        leverage_ratio = (tier1_capital / total_exposure) * 100
        
        # Calculate liquidity ratios
        lcr = self._calculate_lcr(bank_data)
        nsfr = self._calculate_nsfr(bank_data)
        
        # Calculate buffers
        capital_conservation_buffer = max(0, cet1_ratio - self.min_cet1_ratio - self.capital_conservation_buffer)
        countercyclical_buffer = self.countercyclical_buffer
        
        # Check compliance
        compliance_result = self._check_compliance(
            cet1_ratio, tier1_ratio, total_capital_ratio, 
            leverage_ratio, lcr, nsfr
        )
        
        # Calculate capital surpluses/deficits
        capital_surpluses = {
            "cet1_surplus": cet1_ratio - (self.min_cet1_ratio + self.capital_conservation_buffer),
            "tier1_surplus": tier1_ratio - self.min_tier1_ratio,
            "total_capital_surplus": total_capital_ratio - self.min_total_capital_ratio,
            "leverage_surplus": leverage_ratio - self.min_leverage_ratio
        }
        
        return BaselMetrics(
            cet1_ratio=cet1_ratio,
            tier1_capital_ratio=tier1_ratio,
            total_capital_ratio=total_capital_ratio,
            leverage_ratio=leverage_ratio,
            liquidity_coverage_ratio=lcr,
            net_stable_funding_ratio=nsfr,
            total_rwa=total_rwa,
            credit_rwa=rwa_breakdown["credit"],
            market_rwa=rwa_breakdown["market"],
            operational_rwa=rwa_breakdown["operational"],
            is_compliant=compliance_result["compliant"],
            compliance_issues=compliance_result["issues"],
            capital_surpluses=capital_surpluses,
            capital_conservation_buffer=capital_conservation_buffer,
            countercyclical_buffer=countercyclical_buffer
        )
    
    def _calculate_rwa(self, bank_data: BankFinancials) -> Dict[str, float]:
        """Calculate Risk-Weighted Assets by category."""
        
        # Credit Risk RWA
        credit_rwa = (
            bank_data.cash_and_equivalents * self.risk_weights["cash"] / 100 +
            bank_data.sovereign_exposures * self.risk_weights["sovereign"] / 100 +
            bank_data.bank_exposures * self.risk_weights["bank"] / 100 +
            bank_data.corporate_exposures * self.risk_weights["corporate"] / 100 +
            bank_data.retail_exposures * self.risk_weights["retail"] / 100 +
            bank_data.real_estate_residential * self.risk_weights["residential_re"] / 100 +
            bank_data.real_estate_commercial * self.risk_weights["commercial_re"] / 100 +
            bank_data.past_due_exposures * self.risk_weights["past_due"] / 100 +
            bank_data.other_exposures * self.risk_weights["other"] / 100 +
            bank_data.off_balance_sheet_exposures * self.risk_weights["off_balance_sheet"] / 100 +
            bank_data.derivatives_exposure * self.risk_weights["derivatives"] / 100
        )
        
        # Market Risk RWA (simplified calculation)
        market_rwa = bank_data.total_assets * 0.05  # 5% of total assets as approximation
        
        # Operational Risk RWA (simplified Basic Indicator Approach)
        operational_rwa = abs(bank_data.gross_income) * 0.15  # 15% of gross income
        
        total_rwa = credit_rwa + market_rwa + operational_rwa
        
        return {
            "credit": credit_rwa,
            "market": market_rwa,
            "operational": operational_rwa,
            "total": total_rwa
        }
    
    def _calculate_total_exposure(self, bank_data: BankFinancials) -> float:
        """Calculate total exposure for leverage ratio."""
        # Simplified calculation - in practice, this includes adjustments
        return (
            bank_data.total_assets + 
            bank_data.off_balance_sheet_exposures * 0.5 +  # Credit conversion factor
            bank_data.derivatives_exposure
        )
    
    def _calculate_lcr(self, bank_data: BankFinancials) -> float:
        """Calculate Liquidity Coverage Ratio."""
        net_cash_outflows = max(
            bank_data.cash_outflows_30d - bank_data.cash_inflows_30d * 0.75,  # 75% inflow cap
            bank_data.cash_outflows_30d * 0.25  # 25% minimum outflow
        )
        
        if net_cash_outflows == 0:
            return float('inf')
        
        return (bank_data.high_quality_liquid_assets / net_cash_outflows) * 100
    
    def _calculate_nsfr(self, bank_data: BankFinancials) -> float:
        """Calculate Net Stable Funding Ratio."""
        if bank_data.required_stable_funding == 0:
            return float('inf')
        
        return (bank_data.available_stable_funding / bank_data.required_stable_funding) * 100
    
    def _check_compliance(
        self, 
        cet1_ratio: float, 
        tier1_ratio: float, 
        total_capital_ratio: float,
        leverage_ratio: float, 
        lcr: float, 
        nsfr: float
    ) -> Dict[str, Any]:
        """Check Basel III compliance status."""
        
        issues = []
        
        # Check capital ratios
        if cet1_ratio < self.min_cet1_ratio + self.capital_conservation_buffer:
            issues.append(f"CET1 ratio {cet1_ratio:.2f}% below required {self.min_cet1_ratio + self.capital_conservation_buffer:.2f}%")
        
        if tier1_ratio < self.min_tier1_ratio:
            issues.append(f"Tier 1 ratio {tier1_ratio:.2f}% below required {self.min_tier1_ratio:.2f}%")
        
        if total_capital_ratio < self.min_total_capital_ratio:
            issues.append(f"Total capital ratio {total_capital_ratio:.2f}% below required {self.min_total_capital_ratio:.2f}%")
        
        if leverage_ratio < self.min_leverage_ratio:
            issues.append(f"Leverage ratio {leverage_ratio:.2f}% below required {self.min_leverage_ratio:.2f}%")
        
        # Check liquidity ratios
        if lcr < self.min_lcr:
            issues.append(f"LCR {lcr:.1f}% below required {self.min_lcr:.1f}%")
        
        if nsfr < self.min_nsfr:
            issues.append(f"NSFR {nsfr:.1f}% below required {self.min_nsfr:.1f}%")
        
        return {
            "compliant": len(issues) == 0,
            "issues": issues
        }
    
    def stress_test_capital(
        self, 
        bank_data: BankFinancials, 
        stress_scenario: Dict[str, float]
    ) -> Dict[str, Any]:
        """Perform stress test on capital ratios."""
        
        # Apply stress scenario
        stressed_data = self._apply_stress_scenario(bank_data, stress_scenario)
        
        # Calculate metrics under stress
        baseline_metrics = self.calculate_basel_metrics(bank_data)
        stressed_metrics = self.calculate_basel_metrics(stressed_data)
        
        # Calculate impact
        impact = {
            "cet1_change": stressed_metrics.cet1_ratio - baseline_metrics.cet1_ratio,
            "tier1_change": stressed_metrics.tier1_capital_ratio - baseline_metrics.tier1_capital_ratio,
            "total_capital_change": stressed_metrics.total_capital_ratio - baseline_metrics.total_capital_ratio,
            "leverage_change": stressed_metrics.leverage_ratio - baseline_metrics.leverage_ratio,
            "lcr_change": stressed_metrics.liquidity_coverage_ratio - baseline_metrics.liquidity_coverage_ratio
        }
        
        return {
            "baseline_metrics": baseline_metrics,
            "stressed_metrics": stressed_metrics,
            "impact": impact,
            "passes_stress_test": stressed_metrics.is_compliant,
            "stress_scenario": stress_scenario
        }
    
    def _apply_stress_scenario(
        self, 
        bank_data: BankFinancials, 
        scenario: Dict[str, float]
    ) -> BankFinancials:
        """Apply stress scenario to bank data."""
        
        # Create a copy of the data
        stressed_data = bank_data.copy()
        
        # Apply capital loss
        if "capital_loss" in scenario:
            loss_rate = scenario["capital_loss"]
            stressed_data.common_equity_tier1 *= (1 - loss_rate)
            stressed_data.additional_tier1 *= (1 - loss_rate)
            stressed_data.tier2_capital *= (1 - loss_rate)
        
        # Apply RWA increases
        if "corporate_rwa_increase" in scenario:
            increase_rate = scenario["corporate_rwa_increase"]
            stressed_data.corporate_exposures *= (1 + increase_rate)
        
        if "retail_rwa_increase" in scenario:
            increase_rate = scenario["retail_rwa_increase"]
            stressed_data.retail_exposures *= (1 + increase_rate)
        
        # Apply liquidity stress
        if "hqla_haircut" in scenario:
            haircut_rate = scenario["hqla_haircut"]
            stressed_data.high_quality_liquid_assets *= (1 - haircut_rate)
        
        if "outflow_increase" in scenario:
            increase_rate = scenario["outflow_increase"]
            stressed_data.cash_outflows_30d *= (1 + increase_rate)
        
        return stressed_data
    
    def get_regulatory_minimums(self) -> Dict[str, float]:
        """Get current regulatory minimum requirements."""
        return {
            "cet1_ratio": self.min_cet1_ratio,
            "tier1_ratio": self.min_tier1_ratio,
            "total_capital_ratio": self.min_total_capital_ratio,
            "leverage_ratio": self.min_leverage_ratio,
            "lcr": self.min_lcr,
            "nsfr": self.min_nsfr,
            "capital_conservation_buffer": self.capital_conservation_buffer,
            "countercyclical_buffer": self.countercyclical_buffer
        }