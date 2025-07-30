"""Main credit assessment interface for CRCreditum."""

from typing import Dict, Any, Optional, Union
import uuid
from datetime import datetime
from .individual import IndividualAssessment, IndividualCoreFields, IndividualOptionalFields
from .corporate import CorporateAssessment, CorporateCoreFields, CorporateOptionalFields


class CreditAssessment:
    """Main credit assessment interface compatible with test scripts."""
    
    def __init__(self):
        """Initialize the credit assessment engine."""
        self.version = "1.0.0"
        self.total_assessments = 0
        self.supported_types = ["individual", "business", "enhanced"]
        
    def assess_individual(
        self, 
        core_data: Dict[str, Any], 
        optional_data: Optional[Dict[str, Any]] = None,
        assessment_type: str = "basic"
    ) -> Dict[str, Any]:
        """
        Assess individual credit application.
        
        Args:
            core_data: Core required fields
            optional_data: Optional enhancement fields
            assessment_type: Type of assessment ("basic" or "enhanced")
            
        Returns:
            Assessment result dictionary
        """
        try:
            # Validate and create core fields
            core = IndividualCoreFields(**core_data)
            
            # Create optional fields if provided
            optional = None
            if optional_data:
                optional = IndividualOptionalFields(**optional_data)
            
            # Create assessment
            assessment = IndividualAssessment(core=core, optional=optional)
            
            # Calculate risk score
            result = assessment.calculate_risk_score(assessment_type)
            
            # Update counter
            self.total_assessments += 1
            
            # Return result in expected format
            return {
                "assessment_id": assessment.assessment_id,
                "decision": result["decision"],
                "risk_score": result["risk_score"],
                "risk_category": result["risk_category"],
                "assessment_type": assessment_type,
                "debt_to_income_ratio": result.get("debt_to_income_ratio"),
                "factors": result.get("factors", {}),
                "timestamp": assessment.assessment_date.isoformat(),
                "enhancement_factors": assessment.enhancement_factors or {}
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "assessment_id": str(uuid.uuid4()),
                "decision": "error",
                "risk_score": 0.0,
                "timestamp": datetime.now().isoformat()
            }
    
    def assess_business(
        self, 
        core_data: Dict[str, Any], 
        optional_data: Optional[Dict[str, Any]] = None,
        assessment_type: str = "basic"
    ) -> Dict[str, Any]:
        """
        Assess business credit application.
        
        Args:
            core_data: Core required fields
            optional_data: Optional enhancement fields
            assessment_type: Type of assessment ("basic" or "enhanced")
            
        Returns:
            Assessment result dictionary
        """
        try:
            # Validate and create core fields
            core = CorporateCoreFields(**core_data)
            
            # Create optional fields if provided
            optional = None
            if optional_data:
                optional = CorporateOptionalFields(**optional_data)
            
            # Create assessment
            assessment = CorporateAssessment(core=core, optional=optional)
            
            # Calculate risk score
            result = assessment.calculate_risk_score(assessment_type)
            
            # Update counter
            self.total_assessments += 1
            
            # Return result in expected format
            return {
                "assessment_id": assessment.assessment_id,
                "decision": result["decision"],
                "risk_score": result["risk_score"],
                "risk_category": result["risk_category"],
                "assessment_type": assessment_type,
                "debt_service_coverage": result.get("debt_service_coverage"),
                "current_ratio": result.get("current_ratio"),
                "factors": result.get("factors", {}),
                "timestamp": assessment.assessment_date.isoformat(),
                "enhancement_factors": assessment.enhancement_factors or {}
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "assessment_id": str(uuid.uuid4()),
                "decision": "error", 
                "risk_score": 0.0,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_assessment_summary(self) -> Dict[str, Any]:
        """Get assessment engine summary."""
        return {
            "version": self.version,
            "supported_types": self.supported_types,
            "total_assessments": self.total_assessments,
            "features": [
                "Enhanced schemas with 28+ individual and 32+ corporate fields",
                "CRA compliance analysis",
                "Basel III integration",
                "Explainable AI support",
                "Stress testing capabilities"
            ]
        }
    
    def validate_individual_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate individual assessment data."""
        try:
            core = IndividualCoreFields(**data)
            return {"valid": True, "message": "Data validation successful"}
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def validate_business_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate business assessment data."""
        try:
            core = CorporateCoreFields(**data)
            return {"valid": True, "message": "Data validation successful"}
        except Exception as e:
            return {"valid": False, "error": str(e)}