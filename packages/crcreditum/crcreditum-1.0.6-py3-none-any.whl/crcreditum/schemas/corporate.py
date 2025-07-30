"""Enhanced corporate credit assessment schema with 32+ fields."""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator
from .enums import (
    BusinessIndustry, BusinessStructure, LoanPurpose, AuditOpinion,
    CRAInvestment, BusinessContinuityPlan, CyberSecurityRating
)
import uuid
from datetime import datetime


class CorporateCoreFields(BaseModel):
    """Core required fields for corporate assessment (32 fields)."""
    
    # Company Information
    company_name: str = Field(..., min_length=1, max_length=200, description="Legal company name")
    industry: BusinessIndustry = Field(..., description="Primary business industry")
    years_in_business: float = Field(..., ge=0, le=200, description="Years in business")
    employee_count: int = Field(..., ge=1, le=1000000, description="Number of employees")
    
    # Financial Performance
    annual_revenue: float = Field(..., gt=0, description="Annual revenue in USD")
    net_income: float = Field(..., description="Net income (can be negative)")
    total_assets: float = Field(..., gt=0, description="Total assets value")
    total_liabilities: float = Field(..., ge=0, description="Total liabilities")
    current_assets: float = Field(..., ge=0, description="Current assets")
    current_liabilities: float = Field(..., ge=0, description="Current liabilities")
    cash_and_equivalents: float = Field(..., ge=0, description="Cash and cash equivalents")
    total_debt: float = Field(..., ge=0, description="Total debt outstanding")
    
    # Loan Information
    loan_amount: float = Field(..., gt=0, description="Requested loan amount")
    loan_purpose: LoanPurpose = Field(..., description="Purpose of the loan")
    loan_term_months: int = Field(..., ge=6, le=360, description="Loan term in months")
    
    # Key Financial Ratios
    cash_flow: float = Field(..., description="Operating cash flow")
    ebitda: float = Field(..., description="EBITDA")
    debt_service_coverage: float = Field(..., ge=0, description="Debt service coverage ratio")
    working_capital: float = Field(..., description="Working capital")
    asset_turnover: float = Field(..., ge=0, description="Asset turnover ratio")
    interest_expense: float = Field(..., ge=0, description="Annual interest expense")
    debt_to_equity: float = Field(..., ge=0, description="Debt-to-equity ratio")
    current_ratio: float = Field(..., ge=0, description="Current ratio")
    quick_ratio: float = Field(..., ge=0, description="Quick ratio")
    roa: float = Field(..., description="Return on assets percentage")
    roe: float = Field(..., description="Return on equity percentage")
    profit_margin: float = Field(..., description="Profit margin percentage")
    revenue_growth_rate: float = Field(..., description="Revenue growth rate percentage")
    
    # Management and Operations
    management_experience: float = Field(..., ge=0, le=50, description="Average management experience years")
    audit_opinion: AuditOpinion = Field(..., description="Most recent audit opinion")
    regulatory_issues: bool = Field(..., description="Any regulatory issues or violations")
    
    # Market Position
    market_share: float = Field(..., ge=0, le=100, description="Market share percentage")
    customer_concentration: float = Field(..., ge=0, le=100, description="Top customer concentration %")
    geographic_diversification: float = Field(..., ge=0, le=100, description="Geographic diversification %")
    collateral_value: float = Field(..., ge=0, description="Available collateral value")
    
    # Business Structure
    business_structure: BusinessStructure = Field(..., description="Legal business structure")
    
    # Legacy compatibility fields
    monthly_revenue: float = Field(..., gt=0, description="Average monthly revenue")
    monthly_expenses: float = Field(..., ge=0, description="Average monthly expenses")
    current_business_debt: float = Field(..., ge=0, description="Current business debt")

    @validator('current_ratio')
    def validate_current_ratio(cls, v):
        if v < 0:
            raise ValueError('Current ratio cannot be negative')
        return v

    @validator('debt_service_coverage')
    def validate_dscr(cls, v):
        if v < 0:
            raise ValueError('Debt service coverage ratio cannot be negative')
        return v


class CorporateOptionalFields(BaseModel):
    """Optional enhancement fields for corporate assessment (40+ fields)."""
    
    # Advanced Financial Metrics
    financial_leverage: Optional[float] = Field(None, ge=0, description="Financial leverage ratio")
    times_interest_earned: Optional[float] = Field(None, ge=0, description="Times interest earned ratio")
    inventory_turnover: Optional[float] = Field(None, ge=0, description="Inventory turnover ratio")
    receivables_turnover: Optional[float] = Field(None, ge=0, description="Receivables turnover ratio")
    gross_margin: Optional[float] = Field(None, description="Gross margin percentage")
    operating_margin: Optional[float] = Field(None, description="Operating margin percentage")
    operating_cash_flow: Optional[float] = Field(None, description="Operating cash flow")
    capital_expenditure: Optional[float] = Field(None, ge=0, description="Capital expenditure")
    
    # Management and Governance
    ceo_tenure: Optional[float] = Field(None, ge=0, description="CEO tenure in years")
    management_team_experience: Optional[float] = Field(None, ge=0, description="Management team avg experience")
    board_independence: Optional[float] = Field(None, ge=0, le=100, description="Board independence percentage")
    employee_turnover: Optional[float] = Field(None, ge=0, le=100, description="Employee turnover rate")
    operational_efficiency: Optional[float] = Field(None, ge=0, le=100, description="Operational efficiency score")
    cyber_security_rating: Optional[CyberSecurityRating] = Field(None, description="Cyber security rating")
    quality_certifications: Optional[bool] = Field(None, description="Has quality certifications")
    business_continuity_plan: Optional[BusinessContinuityPlan] = Field(None, description="Business continuity plan quality")
    
    # Basel III Compliance Fields
    basel_capital_ratio: Optional[float] = Field(None, ge=0, le=100, description="Basel capital adequacy ratio")
    basel_leverage_ratio: Optional[float] = Field(None, ge=0, le=100, description="Basel leverage ratio")
    basel_liquidity_ratio: Optional[float] = Field(None, ge=0, description="Basel liquidity coverage ratio")
    basel_risk_weighted_assets: Optional[float] = Field(None, ge=0, description="Basel risk-weighted assets")
    tier1_capital_ratio: Optional[float] = Field(None, ge=0, le=100, description="Tier 1 capital ratio")
    leverage_ratio: Optional[float] = Field(None, ge=0, description="Leverage ratio")
    liquidity_coverage_ratio: Optional[float] = Field(None, ge=0, description="Liquidity coverage ratio")
    net_stable_funding_ratio: Optional[float] = Field(None, ge=0, description="Net stable funding ratio")
    risk_weighted_assets: Optional[float] = Field(None, ge=0, description="Risk weighted assets")
    capital_buffer: Optional[float] = Field(None, ge=0, description="Capital conservation buffer")
    stress_test_score: Optional[float] = Field(None, ge=0, le=100, description="Stress test score")
    basel_compliance: Optional[bool] = Field(None, description="Basel III compliance status")
    
    # CRA Community Investment Fields
    cra_community_investment: Optional[CRAInvestment] = Field(None, description="CRA community investment rating")
    cra_small_business_lending: Optional[CRAInvestment] = Field(None, description="CRA small business lending rating")
    small_business_lending: Optional[float] = Field(None, ge=0, description="Small business lending amount")
    community_development_investments: Optional[float] = Field(None, ge=0, description="Community development investments")
    cra_rating: Optional[CRAInvestment] = Field(None, description="Overall CRA rating")
    minority_lending_percentage: Optional[float] = Field(None, ge=0, le=100, description="Minority lending percentage")
    affordable_housing_financing: Optional[float] = Field(None, ge=0, description="Affordable housing financing amount")
    branch_presence_lmi: Optional[float] = Field(None, ge=0, le=100, description="Branch presence in LMI areas %")
    volunteer_hours: Optional[int] = Field(None, ge=0, description="Employee volunteer hours annually")
    community_partnerships: Optional[bool] = Field(None, description="Has community partnerships")
    cra_affordable_housing: Optional[CRAInvestment] = Field(None, description="CRA affordable housing rating")
    cra_economic_development: Optional[CRAInvestment] = Field(None, description="CRA economic development rating")
    
    # CRA Enhancement Fields
    is_small_business: Optional[bool] = Field(None, description="Qualifies as small business")
    zip_code: Optional[str] = Field(None, min_length=5, max_length=10, description="Business ZIP code")
    census_tract: Optional[str] = Field(None, max_length=20, description="Census tract identifier")
    is_minority_owned: Optional[bool] = Field(None, description="Minority-owned business")
    is_women_owned: Optional[bool] = Field(None, description="Women-owned business")
    serves_lmi_communities: Optional[bool] = Field(None, description="Serves low-to-moderate income communities")
    percent_lmi_customers: Optional[float] = Field(None, ge=0, le=100, description="Percentage of LMI customers")
    
    # Legacy Compatibility Fields
    gross_profit: Optional[float] = Field(None, description="Gross profit")
    net_profit: Optional[float] = Field(None, description="Net profit")
    accounts_receivable: Optional[float] = Field(None, ge=0, description="Accounts receivable")
    accounts_payable: Optional[float] = Field(None, ge=0, description="Accounts payable")
    inventory_value: Optional[float] = Field(None, ge=0, description="Inventory value")
    fixed_assets: Optional[float] = Field(None, ge=0, description="Fixed assets value")
    owner_equity: Optional[float] = Field(None, description="Owner equity")


class CorporateAssessment(BaseModel):
    """Complete corporate credit assessment with enhanced features."""
    
    # Core data
    core: CorporateCoreFields
    optional: Optional[CorporateOptionalFields] = None
    
    # Assessment metadata
    assessment_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique assessment ID")
    assessment_date: datetime = Field(default_factory=datetime.now, description="Assessment timestamp")
    assessment_type: str = Field(default="enhanced", description="Type of assessment performed")
    
    # Results (populated after assessment)
    risk_score: Optional[float] = Field(None, ge=0, le=1, description="Calculated risk score")
    risk_category: Optional[str] = Field(None, description="Risk category classification")
    decision: Optional[str] = Field(None, description="Approval decision")
    decision_factors: Optional[List[Dict[str, Any]]] = Field(None, description="Key decision factors")
    
    # Enhancement results
    cra_eligible: Optional[bool] = Field(None, description="CRA credit eligibility")
    basel_risk_weight: Optional[float] = Field(None, description="Basel risk weight")
    enhancement_factors: Optional[Dict[str, Any]] = Field(None, description="Risk enhancement factors")

    def calculate_debt_to_equity_ratio(self) -> float:
        """Calculate debt-to-equity ratio."""
        equity = self.core.total_assets - self.core.total_liabilities
        if equity <= 0:
            return float('inf')
        return self.core.total_debt / equity

    def calculate_interest_coverage_ratio(self) -> float:
        """Calculate interest coverage ratio."""
        if self.core.interest_expense == 0:
            return float('inf')
        return self.core.ebitda / self.core.interest_expense

    def calculate_revenue_to_debt_ratio(self) -> float:
        """Calculate revenue to debt ratio."""
        if self.core.total_debt == 0:
            return float('inf')
        return self.core.annual_revenue / self.core.total_debt

    def calculate_loan_to_revenue_ratio(self) -> float:
        """Calculate loan amount to revenue ratio."""
        if self.core.annual_revenue == 0:
            return float('inf')
        return self.core.loan_amount / self.core.annual_revenue

    def calculate_risk_score(self, assessment_type: str = "basic") -> Dict[str, Any]:
        """Calculate risk score based on assessment type."""
        
        # Basic risk score calculation
        base_score = 0.5  # Start at neutral
        
        # Debt service coverage ratio (25% weight)
        dscr_factor = min(1, self.core.debt_service_coverage / 1.25)  # 1.25 is good DSCR
        base_score += (dscr_factor - 0.5) * 0.25
        
        # Current ratio (20% weight)
        current_factor = min(1, self.core.current_ratio / 2.0)  # 2.0 is good current ratio
        base_score += (current_factor - 0.5) * 0.20
        
        # Profitability (20% weight)
        if self.core.annual_revenue > 0:
            profit_margin = self.core.net_income / self.core.annual_revenue
            profit_factor = max(0, min(1, (profit_margin + 0.1) / 0.2))  # -10% to +10% normalized
        else:
            profit_factor = 0
        base_score += (profit_factor - 0.5) * 0.20
        
        # Business stability (15% weight)
        stability_factor = min(1, self.core.years_in_business / 10)  # 10 years is stable
        base_score += (stability_factor - 0.5) * 0.15
        
        # Industry risk (10% weight) - simplified
        industry_risk = {
            BusinessIndustry.TECHNOLOGY: 0.1,
            BusinessIndustry.HEALTHCARE: 0.05,
            BusinessIndustry.FINANCE: 0.0,
            BusinessIndustry.RETAIL: -0.05,
            BusinessIndustry.CONSTRUCTION: -0.1,
            BusinessIndustry.ENERGY: -0.05
        }
        industry_adjustment = industry_risk.get(self.core.industry, 0)
        base_score += industry_adjustment
        
        # Management experience (10% weight)
        mgmt_factor = min(1, self.core.management_experience / 15)  # 15 years is experienced
        base_score += (mgmt_factor - 0.5) * 0.10
        
        # Enhanced adjustments
        if assessment_type == "enhanced" and self.optional:
            # Basel III compliance
            if self.optional.basel_compliance is True:
                base_score += 0.05
            
            # CRA community investment
            cra_boost = {
                CRAInvestment.OUTSTANDING: 0.03,
                CRAInvestment.SATISFACTORY: 0.01,
                CRAInvestment.NEEDS_TO_IMPROVE: -0.01,
                CRAInvestment.SUBSTANTIAL_NONCOMPLIANCE: -0.05
            }
            if self.optional.cra_community_investment in cra_boost:
                base_score += cra_boost[self.optional.cra_community_investment]
            
            # Operational efficiency
            if self.optional.operational_efficiency is not None:
                efficiency_factor = self.optional.operational_efficiency / 100
                base_score += (efficiency_factor - 0.5) * 0.03
            
            # Cyber security rating
            cyber_boost = {
                CyberSecurityRating.EXCELLENT: 0.02,
                CyberSecurityRating.GOOD: 0.01,
                CyberSecurityRating.FAIR: 0,
                CyberSecurityRating.POOR: -0.02
            }
            if self.optional.cyber_security_rating in cyber_boost:
                base_score += cyber_boost[self.optional.cyber_security_rating]
        
        # Ensure score is between 0 and 1
        final_score = max(0, min(1, base_score))
        
        # Determine risk category
        if final_score >= 0.7:
            risk_category = "Low Risk"
            decision = "approved"
        elif final_score >= 0.5:
            risk_category = "Medium Risk"
            decision = "conditional"
        else:
            risk_category = "High Risk"
            decision = "rejected"
        
        # Update instance fields
        self.risk_score = final_score
        self.risk_category = risk_category
        self.decision = decision
        self.assessment_type = assessment_type
        
        return {
            "risk_score": final_score,
            "risk_category": risk_category,
            "decision": decision,
            "assessment_type": assessment_type,
            "debt_service_coverage": self.core.debt_service_coverage,
            "current_ratio": self.core.current_ratio,
            "profit_margin": profit_margin if 'profit_margin' in locals() else None,
            "factors": {
                "dscr_factor": dscr_factor,
                "current_factor": current_factor,
                "profit_factor": profit_factor,
                "stability_factor": stability_factor,
                "mgmt_factor": mgmt_factor
            }
        }

    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }