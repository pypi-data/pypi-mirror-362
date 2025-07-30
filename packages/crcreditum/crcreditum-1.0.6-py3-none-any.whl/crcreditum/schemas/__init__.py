"""Schema definitions for CRCreditum credit assessment."""

from .assessment import CreditAssessment
from .individual import (
    IndividualCoreFields,
    IndividualOptionalFields, 
    IndividualAssessment
)
from .corporate import (
    CorporateCoreFields,
    CorporateOptionalFields,
    CorporateAssessment
)
from .enums import (
    EmploymentStatus,
    BusinessIndustry,
    LoanPurpose,
    BusinessStructure,
    EducationLevel,
    MaritalStatus,
    IncomeType,
    EmployerType,
    HousingStatus,
    CRAInvestment,
    BaselRiskRating,
    AuditOpinion
)
from .legacy import CreditApplication, CreditConfig

__all__ = [
    # Main assessment classes
    "CreditAssessment",
    "IndividualAssessment",
    "CorporateAssessment",
    
    # Field definitions
    "IndividualCoreFields",
    "IndividualOptionalFields",
    "CorporateCoreFields", 
    "CorporateOptionalFields",
    
    # Enums
    "EmploymentStatus",
    "BusinessIndustry",
    "LoanPurpose",
    "BusinessStructure",
    "EducationLevel",
    "MaritalStatus",
    "IncomeType",
    "EmployerType",
    "HousingStatus",
    "CRAInvestment",
    "BaselRiskRating",
    "AuditOpinion",
    
    # Legacy compatibility
    "CreditApplication",
    "CreditConfig",
]