"""Enumeration definitions for CRCreditum schemas."""

from enum import Enum


class EmploymentStatus(str, Enum):
    """Employment status options."""
    EMPLOYED = "employed"
    SELF_EMPLOYED = "self_employed"
    UNEMPLOYED = "unemployed"
    RETIRED = "retired"
    STUDENT = "student"
    DISABLED = "disabled"
    OTHER = "other"


class BusinessIndustry(str, Enum):
    """Business industry classifications."""
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    RETAIL = "retail"
    MANUFACTURING = "manufacturing"
    CONSTRUCTION = "construction"
    REAL_ESTATE = "real_estate"
    EDUCATION = "education"
    HOSPITALITY = "hospitality"
    TRANSPORTATION = "transportation"
    AGRICULTURE = "agriculture"
    ENERGY = "energy"
    TELECOMMUNICATIONS = "telecommunications"
    MEDIA = "media"
    PROFESSIONAL_SERVICES = "professional_services"
    NON_PROFIT = "non_profit"
    GOVERNMENT = "government"
    OTHER = "other"


class LoanPurpose(str, Enum):
    """Loan purpose classifications."""
    HOME_PURCHASE = "home_purchase"
    HOME_REFINANCE = "home_refinance"
    HOME_IMPROVEMENT = "home_improvement"
    AUTO = "auto"
    PERSONAL = "personal"
    DEBT_CONSOLIDATION = "debt_consolidation"
    EDUCATION = "education"
    BUSINESS = "business"
    EQUIPMENT = "equipment"
    WORKING_CAPITAL = "working_capital"
    EXPANSION = "expansion"
    REAL_ESTATE_INVESTMENT = "real_estate_investment"
    INVENTORY = "inventory"
    OTHER = "other"


class BusinessStructure(str, Enum):
    """Business structure types."""
    SOLE_PROPRIETORSHIP = "sole_proprietorship"
    PARTNERSHIP = "partnership"
    LLC = "llc"
    CORPORATION = "corporation"
    S_CORPORATION = "s_corporation"
    NON_PROFIT = "non_profit"
    COOPERATIVE = "cooperative"
    OTHER = "other"


class EducationLevel(str, Enum):
    """Education level classifications."""
    NO_HIGH_SCHOOL = "no_high_school"
    HIGH_SCHOOL = "high_school"
    SOME_COLLEGE = "some_college"
    ASSOCIATES = "associates"
    BACHELORS = "bachelors"
    MASTERS = "masters"
    DOCTORAL = "doctoral"
    PROFESSIONAL = "professional"
    TRADE_SCHOOL = "trade_school"
    OTHER = "other"


class MaritalStatus(str, Enum):
    """Marital status options."""
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    SEPARATED = "separated"
    WIDOWED = "widowed"
    DOMESTIC_PARTNERSHIP = "domestic_partnership"
    OTHER = "other"


class IncomeType(str, Enum):
    """Income type classifications."""
    W2 = "W2"
    SELF_EMPLOYED = "self_employed"
    INVESTMENT = "investment"
    RETIREMENT = "retirement"
    SOCIAL_SECURITY = "social_security"
    DISABILITY = "disability"
    UNEMPLOYMENT = "unemployment"
    OTHER = "other"


class EmployerType(str, Enum):
    """Employer type classifications."""
    GOVERNMENT = "government"
    NON_PROFIT = "non_profit"
    SMALL_BUSINESS = "small_business"
    LARGE_CORPORATION = "large_corporation"
    STARTUP = "startup"
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    FINANCE = "finance"
    OTHER = "other"


class HousingStatus(str, Enum):
    """Housing status options."""
    OWN = "own"
    RENT = "rent"
    LIVE_WITH_FAMILY = "live_with_family"
    OTHER = "other"


class CRAInvestment(str, Enum):
    """CRA community investment ratings."""
    OUTSTANDING = "outstanding"
    SATISFACTORY = "satisfactory"
    NEEDS_TO_IMPROVE = "needs_to_improve"
    SUBSTANTIAL_NONCOMPLIANCE = "substantial_noncompliance"


class BaselRiskRating(str, Enum):
    """Basel risk rating classifications."""
    INVESTMENT_GRADE = "investment_grade"
    NON_INVESTMENT_GRADE = "non_investment_grade"
    HIGH_RISK = "high_risk"
    DEFAULT = "default"


class AuditOpinion(str, Enum):
    """Audit opinion types."""
    UNQUALIFIED = "unqualified"
    QUALIFIED = "qualified"
    ADVERSE = "adverse"
    DISCLAIMER = "disclaimer"


class CreditAccess(str, Enum):
    """CRA credit access ratings."""
    OUTSTANDING = "outstanding"
    SATISFACTORY = "satisfactory"
    NEEDS_TO_IMPROVE = "needs_to_improve"
    SUBSTANTIAL_NONCOMPLIANCE = "substantial_noncompliance"


class BusinessContinuityPlan(str, Enum):
    """Business continuity plan ratings."""
    COMPREHENSIVE = "comprehensive"
    ADEQUATE = "adequate"
    BASIC = "basic"
    NONE = "none"


class CyberSecurityRating(str, Enum):
    """Cyber security rating classifications."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class IncomeVerificationMethod(str, Enum):
    """Income verification method types."""
    W2_PAYSTUBS = "W2_paystubs"
    TAX_RETURNS = "tax_returns"
    BANK_STATEMENTS = "bank_statements"
    EMPLOYMENT_VERIFICATION = "employment_verification"
    ASSET_VERIFICATION = "asset_verification"
    OTHER = "other"


class PrimaryBankingRelationship(str, Enum):
    """Primary banking relationship types."""
    CHECKING_SAVINGS = "checking_savings"
    CREDIT_CARDS = "credit_cards"
    LOANS = "loans"
    INVESTMENTS = "investments"
    BUSINESS_BANKING = "business_banking"
    OTHER = "other"