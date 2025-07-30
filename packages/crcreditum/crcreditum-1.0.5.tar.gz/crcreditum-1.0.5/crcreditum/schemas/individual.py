"""Enhanced individual credit assessment schema with 28+ fields."""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator
from .enums import (
    EmploymentStatus, EducationLevel, MaritalStatus, IncomeType, 
    EmployerType, HousingStatus, LoanPurpose, BaselRiskRating,
    CreditAccess, IncomeVerificationMethod, PrimaryBankingRelationship
)
import uuid
from datetime import datetime


class IndividualCoreFields(BaseModel):
    """Core required fields for individual assessment (20 fields)."""
    
    # Personal Information
    age: int = Field(..., ge=18, le=100, description="Applicant age")
    
    # Credit Profile
    credit_score: int = Field(..., ge=300, le=850, description="FICO credit score")
    credit_utilization: float = Field(..., ge=0, le=100, description="Credit utilization percentage")
    payment_history_score: float = Field(..., ge=0, le=100, description="Payment history score")
    credit_accounts: int = Field(..., ge=0, le=50, description="Number of credit accounts")
    credit_inquiries_6m: int = Field(..., ge=0, le=20, description="Credit inquiries in last 6 months")
    
    # Income and Employment
    annual_income: float = Field(..., gt=0, description="Annual income in USD")
    employment_years: float = Field(..., ge=0, le=50, description="Years in current employment")
    employment_status: EmploymentStatus = Field(..., description="Current employment status")
    
    # Financial Position
    monthly_debt_payments: float = Field(..., ge=0, description="Total monthly debt payments")
    liquid_assets: float = Field(..., ge=0, description="Liquid assets available")
    total_assets: float = Field(..., ge=0, description="Total assets owned")
    monthly_expenses: float = Field(..., ge=0, description="Total monthly expenses")
    existing_loans: int = Field(..., ge=0, le=20, description="Number of existing loans")
    
    # Housing
    housing_status: HousingStatus = Field(..., description="Current housing situation")
    monthly_housing_cost: float = Field(..., ge=0, description="Monthly housing cost")
    
    # Loan Details
    loan_amount: float = Field(..., gt=0, description="Requested loan amount")
    loan_purpose: LoanPurpose = Field(..., description="Purpose of the loan")
    loan_term_months: int = Field(..., ge=6, le=480, description="Loan term in months")
    years_of_credit_history: float = Field(..., ge=0, le=50, description="Years of credit history")

    @validator('credit_utilization')
    def validate_credit_utilization(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Credit utilization must be between 0 and 100')
        return v

    @validator('payment_history_score')
    def validate_payment_history(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Payment history score must be between 0 and 100')
        return v


class IndividualOptionalFields(BaseModel):
    """Optional enhancement fields for individual assessment (35+ fields)."""
    
    # Extended Credit Profile
    total_payments: Optional[int] = Field(None, ge=0, description="Total payment history count")
    delinquent_payments: Optional[int] = Field(None, ge=0, description="Number of delinquent payments")
    total_balance: Optional[float] = Field(None, ge=0, description="Total credit card balance")
    total_credit_limit: Optional[float] = Field(None, ge=0, description="Total credit limit")
    months_since_first_credit: Optional[int] = Field(None, ge=0, description="Months since first credit account")
    recent_credit_inquiries: Optional[int] = Field(None, ge=0, description="Recent credit inquiries")
    
    # Basel III Risk Factors
    basel_credit_risk_rating: Optional[BaselRiskRating] = Field(None, description="Basel risk rating")
    
    # CRA Credit Access
    cra_credit_access: Optional[CreditAccess] = Field(None, description="CRA credit access rating")
    
    # Employment Details
    months_at_employer: Optional[int] = Field(None, ge=0, description="Months at current employer")
    job_title: Optional[str] = Field(None, max_length=100, description="Current job title")
    income_type: Optional[IncomeType] = Field(None, description="Primary income type")
    other_monthly_income: Optional[float] = Field(None, ge=0, description="Other monthly income")
    employer_type: Optional[EmployerType] = Field(None, description="Type of employer")
    employer_size: Optional[str] = Field(None, description="Employer size category")
    
    # Assets and Banking
    savings_balance: Optional[float] = Field(None, ge=0, description="Savings account balance")
    checking_balance: Optional[float] = Field(None, ge=0, description="Checking account balance")
    investment_accounts: Optional[float] = Field(None, ge=0, description="Investment account value")
    retirement_401k: Optional[float] = Field(None, ge=0, description="401k/retirement savings")
    home_value: Optional[float] = Field(None, ge=0, description="Primary residence value")
    vehicle_value: Optional[float] = Field(None, ge=0, description="Vehicle value")
    
    # Housing Details
    monthly_rent_mortgage: Optional[float] = Field(None, ge=0, description="Monthly rent or mortgage")
    years_at_address: Optional[float] = Field(None, ge=0, description="Years at current address")
    
    # Personal Demographics
    education_level: Optional[EducationLevel] = Field(None, description="Highest education level")
    marital_status: Optional[MaritalStatus] = Field(None, description="Marital status")
    dependents: Optional[int] = Field(None, ge=0, le=10, description="Number of dependents")
    
    # Banking Relationship
    bank_account_age_months: Optional[int] = Field(None, ge=0, description="Age of primary bank account")
    average_bank_balance: Optional[float] = Field(None, ge=0, description="Average bank balance")
    overdraft_frequency: Optional[int] = Field(None, ge=0, description="Overdrafts in last 12 months")
    nsf_incidents: Optional[int] = Field(None, ge=0, description="NSF incidents in last 12 months")
    
    # Payment History
    rent_payment_history: Optional[float] = Field(None, ge=0, le=100, description="Rent payment history %")
    utility_payment_history: Optional[float] = Field(None, ge=0, le=100, description="Utility payment history %")
    
    # Risk Factors
    bankruptcy_history: Optional[bool] = Field(None, description="Bankruptcy in credit history")
    foreclosure_history: Optional[bool] = Field(None, description="Foreclosure in credit history")
    tax_liens: Optional[bool] = Field(None, description="Tax liens on record")
    collections_12m: Optional[int] = Field(None, ge=0, description="Collections in last 12 months")
    missed_payments_6m: Optional[int] = Field(None, ge=0, description="Missed payments in last 6 months")
    
    # CRA Enhancement Fields
    zip_code: Optional[str] = Field(None, min_length=5, max_length=10, description="ZIP code")
    census_tract: Optional[str] = Field(None, max_length=20, description="Census tract identifier")
    is_minority_owned: Optional[bool] = Field(None, description="Minority-owned business indicator")
    is_women_owned: Optional[bool] = Field(None, description="Women-owned business indicator")
    serves_lmi_communities: Optional[bool] = Field(None, description="Serves low-to-moderate income communities")
    percent_lmi_customers: Optional[float] = Field(None, ge=0, le=100, description="Percentage of LMI customers")
    income_verification_method: Optional[IncomeVerificationMethod] = Field(None, description="Method of income verification")
    primary_banking_relationship: Optional[PrimaryBankingRelationship] = Field(None, description="Primary banking relationship type")
    first_time_homebuyer: Optional[bool] = Field(None, description="First-time homebuyer status")
    veteran_status: Optional[bool] = Field(None, description="Military veteran status")
    disability_income: Optional[bool] = Field(None, description="Receives disability income")
    household_size: Optional[int] = Field(None, ge=1, le=15, description="Household size")


class IndividualAssessment(BaseModel):
    """Complete individual credit assessment with enhanced features."""
    
    # Core data
    core: IndividualCoreFields
    optional: Optional[IndividualOptionalFields] = None
    
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

    def calculate_debt_to_income_ratio(self) -> float:
        """Calculate debt-to-income ratio."""
        monthly_income = self.core.annual_income / 12
        if monthly_income == 0:
            return float('inf')
        return self.core.monthly_debt_payments / monthly_income

    def calculate_payment_to_income_ratio(self) -> float:
        """Calculate payment-to-income ratio including new loan."""
        monthly_income = self.core.annual_income / 12
        if monthly_income == 0:
            return float('inf')
        
        # Estimate monthly payment (simplified calculation)
        estimated_payment = self.core.loan_amount / self.core.loan_term_months
        total_payments = self.core.monthly_debt_payments + estimated_payment
        
        return total_payments / monthly_income

    def calculate_liquid_asset_ratio(self) -> float:
        """Calculate liquid assets to loan amount ratio."""
        if self.core.loan_amount == 0:
            return float('inf')
        return self.core.liquid_assets / self.core.loan_amount

    def calculate_risk_score(self, assessment_type: str = "basic") -> Dict[str, Any]:
        """Calculate risk score based on assessment type."""
        
        # Basic risk score calculation
        base_score = 0.5  # Start at neutral
        
        # Credit score factor (30% weight)
        credit_factor = (self.core.credit_score - 300) / 550  # Normalize 300-850 to 0-1
        base_score += (credit_factor - 0.5) * 0.3
        
        # Debt-to-income factor (25% weight)
        dti = self.calculate_debt_to_income_ratio()
        dti_factor = max(0, 1 - (dti / 0.43))  # 43% is typical max DTI
        base_score += (dti_factor - 0.5) * 0.25
        
        # Employment stability (15% weight)
        employment_factor = min(1, self.core.employment_years / 5)  # Normalize to 5 years
        base_score += (employment_factor - 0.5) * 0.15
        
        # Credit utilization (15% weight)
        util_factor = max(0, 1 - (self.core.credit_utilization / 100))
        base_score += (util_factor - 0.5) * 0.15
        
        # Assets factor (15% weight)
        asset_ratio = self.calculate_liquid_asset_ratio()
        asset_factor = min(1, asset_ratio)
        base_score += (asset_factor - 0.5) * 0.15
        
        # Enhanced adjustments
        if assessment_type == "enhanced" and self.optional:
            # Payment history enhancement
            if self.optional.rent_payment_history is not None:
                payment_factor = self.optional.rent_payment_history / 100
                base_score += (payment_factor - 0.5) * 0.05
            
            # Banking relationship stability
            if self.optional.bank_account_age_months is not None:
                bank_factor = min(1, self.optional.bank_account_age_months / 60)  # 5 years
                base_score += (bank_factor - 0.5) * 0.03
            
            # Education level
            education_boost = {
                EducationLevel.DOCTORAL: 0.02,
                EducationLevel.MASTERS: 0.015,
                EducationLevel.BACHELORS: 0.01,
                EducationLevel.ASSOCIATES: 0.005
            }
            if self.optional.education_level in education_boost:
                base_score += education_boost[self.optional.education_level]
        
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
            "debt_to_income_ratio": dti,
            "liquid_asset_ratio": asset_ratio,
            "factors": {
                "credit_score_factor": credit_factor,
                "dti_factor": dti_factor,
                "employment_factor": employment_factor,
                "utilization_factor": util_factor,
                "asset_factor": asset_factor
            }
        }

    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }