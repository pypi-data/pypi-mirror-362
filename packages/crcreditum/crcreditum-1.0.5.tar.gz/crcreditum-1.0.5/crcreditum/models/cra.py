"""Community Reinvestment Act (CRA) compliance analysis module."""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from enum import Enum
import math


class CRATestScores(BaseModel):
    """CRA three-test framework scores."""
    
    lending_test: float = Field(..., ge=0, le=100, description="Lending test score")
    investment_test: float = Field(..., ge=0, le=100, description="Investment test score") 
    service_test: float = Field(..., ge=0, le=100, description="Service test score")
    overall_score: float = Field(..., ge=0, le=100, description="Overall CRA score")
    rating: str = Field(..., description="CRA rating (Outstanding, Satisfactory, etc.)")


class CRAAnalysisResult(BaseModel):
    """Complete CRA analysis result."""
    
    applicant_type: str = Field(..., description="Type of applicant (individual/corporate)")
    qualifies_for_cra_credit: bool = Field(..., description="Qualifies for CRA credit")
    test_scores: CRATestScores = Field(..., description="CRA test scores")
    risk_adjustment_multiplier: float = Field(..., ge=0.5, le=1.5, description="Risk adjustment multiplier")
    cra_factors: Dict[str, Any] = Field(..., description="CRA qualifying factors")
    recommendations: List[str] = Field(default_factory=list, description="CRA recommendations")


class CRAAnalyzer:
    """Community Reinvestment Act compliance analyzer."""
    
    def __init__(self):
        """Initialize CRA analyzer with standard thresholds."""
        
        # CRA qualifying income thresholds (% of Area Median Income)
        self.lmi_income_threshold = 0.8  # 80% of AMI
        self.moderate_income_threshold = 0.5  # 50% of AMI
        
        # Small business revenue threshold
        self.small_business_threshold = 1000000  # $1M annual revenue
        
        # Geographic factors (simplified - would use actual census data)
        self.lmi_zip_codes = {
            "10001", "10002", "10003", "10009", "10025", "10026", "10027", "10030",
            "11201", "11205", "11206", "11207", "11208", "11212", "11213", "11216"
        }
        
        # CRA test weights
        self.test_weights = {
            "lending": 0.5,     # 50% weight
            "investment": 0.25, # 25% weight  
            "service": 0.25     # 25% weight
        }
        
    def analyze_cra_compliance(
        self, 
        applicant_data: Dict[str, Any], 
        applicant_type: str
    ) -> CRAAnalysisResult:
        """
        Analyze CRA compliance for a loan application.
        
        Args:
            applicant_data: Application data
            applicant_type: "individual" or "corporate"
            
        Returns:
            CRA analysis result
        """
        
        if applicant_type == "individual":
            return self._analyze_individual_cra(applicant_data)
        elif applicant_type == "corporate":
            return self._analyze_corporate_cra(applicant_data)
        else:
            raise ValueError(f"Invalid applicant type: {applicant_type}")
    
    def _analyze_individual_cra(self, data: Dict[str, Any]) -> CRAAnalysisResult:
        """Analyze CRA compliance for individual applicant."""
        
        # Extract key fields
        annual_income = data.get("annual_income", 0)
        zip_code = data.get("zip_code", "")
        loan_purpose = data.get("loan_purpose", "")
        is_minority_owned = data.get("is_minority_owned", False)
        serves_lmi_communities = data.get("serves_lmi_communities", False)
        first_time_homebuyer = data.get("first_time_homebuyer", False)
        
        # Initialize CRA factors
        cra_factors = {}
        qualifies = False
        
        # Check LMI income qualification
        # Using simplified national median income (would use local AMI in production)
        national_median_income = 70000
        income_ratio = annual_income / national_median_income
        
        if income_ratio <= self.lmi_income_threshold:
            cra_factors["lmi_income"] = True
            qualifies = True
        else:
            cra_factors["lmi_income"] = False
        
        # Check geographic qualification
        if zip_code in self.lmi_zip_codes:
            cra_factors["lmi_geography"] = True
            qualifies = True
        else:
            cra_factors["lmi_geography"] = False
        
        # Check loan purpose qualification
        cra_qualifying_purposes = {
            "home_purchase", "home_refinance", "home_improvement",
            "small_business", "education", "community_development"
        }
        if loan_purpose in cra_qualifying_purposes:
            cra_factors["qualifying_purpose"] = True
            if loan_purpose in ["home_purchase", "home_improvement"]:
                qualifies = True
        else:
            cra_factors["qualifying_purpose"] = False
        
        # Check special populations
        if is_minority_owned or first_time_homebuyer:
            cra_factors["special_population"] = True
            qualifies = True
        else:
            cra_factors["special_population"] = False
        
        # Calculate test scores
        test_scores = self._calculate_individual_test_scores(data, cra_factors)
        
        # Calculate risk adjustment
        risk_adjustment = self._calculate_risk_adjustment(cra_factors, qualifies)
        
        # Generate recommendations
        recommendations = self._generate_individual_recommendations(cra_factors, test_scores)
        
        return CRAAnalysisResult(
            applicant_type="individual",
            qualifies_for_cra_credit=qualifies,
            test_scores=test_scores,
            risk_adjustment_multiplier=risk_adjustment,
            cra_factors=cra_factors,
            recommendations=recommendations
        )
    
    def _analyze_corporate_cra(self, data: Dict[str, Any]) -> CRAAnalysisResult:
        """Analyze CRA compliance for corporate applicant."""
        
        # Extract key fields
        annual_revenue = data.get("annual_revenue", 0)
        industry = data.get("industry", "")
        zip_code = data.get("zip_code", "")
        loan_purpose = data.get("loan_purpose", "")
        is_small_business = data.get("is_small_business", False)
        is_minority_owned = data.get("is_minority_owned", False)
        is_women_owned = data.get("is_women_owned", False)
        serves_lmi_communities = data.get("serves_lmi_communities", False)
        
        # Initialize CRA factors
        cra_factors = {}
        qualifies = False
        
        # Check small business qualification
        if annual_revenue <= self.small_business_threshold or is_small_business:
            cra_factors["small_business"] = True
            qualifies = True
        else:
            cra_factors["small_business"] = False
        
        # Check geographic qualification
        if zip_code in self.lmi_zip_codes:
            cra_factors["lmi_geography"] = True
            qualifies = True
        else:
            cra_factors["lmi_geography"] = False
        
        # Check minority/women-owned business
        if is_minority_owned or is_women_owned:
            cra_factors["minority_women_owned"] = True
            qualifies = True
        else:
            cra_factors["minority_women_owned"] = False
        
        # Check community service
        if serves_lmi_communities:
            cra_factors["community_service"] = True
            qualifies = True
        else:
            cra_factors["community_service"] = False
        
        # Check loan purpose
        cra_business_purposes = {
            "working_capital", "equipment", "expansion", 
            "inventory", "real_estate", "community_development"
        }
        if loan_purpose in cra_business_purposes:
            cra_factors["qualifying_purpose"] = True
        else:
            cra_factors["qualifying_purpose"] = False
        
        # Check industry
        community_benefit_industries = {
            "healthcare", "education", "non_profit", 
            "affordable_housing", "community_services"
        }
        if industry in community_benefit_industries:
            cra_factors["community_benefit_industry"] = True
            qualifies = True
        else:
            cra_factors["community_benefit_industry"] = False
        
        # Calculate test scores
        test_scores = self._calculate_corporate_test_scores(data, cra_factors)
        
        # Calculate risk adjustment
        risk_adjustment = self._calculate_risk_adjustment(cra_factors, qualifies)
        
        # Generate recommendations
        recommendations = self._generate_corporate_recommendations(cra_factors, test_scores)
        
        return CRAAnalysisResult(
            applicant_type="corporate",
            qualifies_for_cra_credit=qualifies,
            test_scores=test_scores,
            risk_adjustment_multiplier=risk_adjustment,
            cra_factors=cra_factors,
            recommendations=recommendations
        )
    
    def _calculate_individual_test_scores(
        self, 
        data: Dict[str, Any], 
        cra_factors: Dict[str, bool]
    ) -> CRATestScores:
        """Calculate CRA test scores for individual."""
        
        # Lending Test (50% weight)
        lending_score = 60  # Base score
        if cra_factors.get("lmi_income"):
            lending_score += 15
        if cra_factors.get("lmi_geography"):
            lending_score += 10
        if cra_factors.get("qualifying_purpose"):
            lending_score += 10
        if cra_factors.get("special_population"):
            lending_score += 5
        
        # Investment Test (25% weight)
        investment_score = 65  # Base score
        if cra_factors.get("lmi_geography"):
            investment_score += 15
        if data.get("loan_purpose") == "home_purchase":
            investment_score += 10
        if cra_factors.get("special_population"):
            investment_score += 10
        
        # Service Test (25% weight)
        service_score = 70  # Base score
        if cra_factors.get("lmi_geography"):
            service_score += 15
        if data.get("first_time_homebuyer"):
            service_score += 10
        if data.get("serves_lmi_communities"):
            service_score += 5
        
        # Ensure scores don't exceed 100
        lending_score = min(100, lending_score)
        investment_score = min(100, investment_score)
        service_score = min(100, service_score)
        
        # Calculate overall score
        overall_score = (
            lending_score * self.test_weights["lending"] +
            investment_score * self.test_weights["investment"] +
            service_score * self.test_weights["service"]
        )
        
        # Determine rating
        rating = self._get_cra_rating(overall_score)
        
        return CRATestScores(
            lending_test=lending_score,
            investment_test=investment_score,
            service_test=service_score,
            overall_score=overall_score,
            rating=rating
        )
    
    def _calculate_corporate_test_scores(
        self, 
        data: Dict[str, Any], 
        cra_factors: Dict[str, bool]
    ) -> CRATestScores:
        """Calculate CRA test scores for corporate."""
        
        # Lending Test (50% weight)
        lending_score = 65  # Base score for businesses
        if cra_factors.get("small_business"):
            lending_score += 20
        if cra_factors.get("lmi_geography"):
            lending_score += 10
        if cra_factors.get("minority_women_owned"):
            lending_score += 5
        
        # Investment Test (25% weight)
        investment_score = 60  # Base score
        if cra_factors.get("community_service"):
            investment_score += 20
        if cra_factors.get("community_benefit_industry"):
            investment_score += 15
        if cra_factors.get("lmi_geography"):
            investment_score += 5
        
        # Service Test (25% weight)
        service_score = 70  # Base score
        if cra_factors.get("community_service"):
            service_score += 15
        if cra_factors.get("minority_women_owned"):
            service_score += 10
        if data.get("employee_count", 0) >= 10:  # Job creation
            service_score += 5
        
        # Ensure scores don't exceed 100
        lending_score = min(100, lending_score)
        investment_score = min(100, investment_score)
        service_score = min(100, service_score)
        
        # Calculate overall score
        overall_score = (
            lending_score * self.test_weights["lending"] +
            investment_score * self.test_weights["investment"] +
            service_score * self.test_weights["service"]
        )
        
        # Determine rating
        rating = self._get_cra_rating(overall_score)
        
        return CRATestScores(
            lending_test=lending_score,
            investment_test=investment_score,
            service_test=service_score,
            overall_score=overall_score,
            rating=rating
        )
    
    def _get_cra_rating(self, score: float) -> str:
        """Convert numerical score to CRA rating."""
        if score >= 90:
            return "Outstanding"
        elif score >= 80:
            return "Satisfactory"
        elif score >= 70:
            return "Needs to Improve"
        else:
            return "Substantial Noncompliance"
    
    def _calculate_risk_adjustment(
        self, 
        cra_factors: Dict[str, bool], 
        qualifies: bool
    ) -> float:
        """Calculate risk adjustment multiplier based on CRA factors."""
        
        base_multiplier = 1.0
        
        if qualifies:
            # Positive adjustments for CRA qualifying factors
            qualifying_factors = sum(cra_factors.values())
            adjustment = min(0.1, qualifying_factors * 0.02)  # Max 10% reduction
            base_multiplier -= adjustment
        else:
            # No penalty for non-qualifying, just no benefit
            pass
        
        # Ensure multiplier stays within reasonable bounds
        return max(0.8, min(1.2, base_multiplier))
    
    def _generate_individual_recommendations(
        self, 
        cra_factors: Dict[str, bool], 
        test_scores: CRATestScores
    ) -> List[str]:
        """Generate CRA recommendations for individual applicant."""
        
        recommendations = []
        
        if not cra_factors.get("lmi_income") and not cra_factors.get("lmi_geography"):
            recommendations.append(
                "Consider targeting LMI borrowers or LMI geographies to improve CRA performance"
            )
        
        if test_scores.lending_test < 80:
            recommendations.append(
                "Increase lending in CRA assessment areas to improve lending test score"
            )
        
        if test_scores.investment_test < 80:
            recommendations.append(
                "Consider qualified investments in community development to improve investment test"
            )
        
        if test_scores.service_test < 80:
            recommendations.append(
                "Enhance retail services in LMI areas to improve service test performance"
            )
        
        if cra_factors.get("special_population"):
            recommendations.append(
                "Document special population benefits for CRA credit"
            )
        
        return recommendations
    
    def _generate_corporate_recommendations(
        self, 
        cra_factors: Dict[str, bool], 
        test_scores: CRATestScores
    ) -> List[str]:
        """Generate CRA recommendations for corporate applicant."""
        
        recommendations = []
        
        if not cra_factors.get("small_business"):
            recommendations.append(
                "Focus on small business lending to improve CRA small business metrics"
            )
        
        if not cra_factors.get("community_service"):
            recommendations.append(
                "Develop programs to serve LMI communities for CRA credit"
            )
        
        if test_scores.lending_test < 80:
            recommendations.append(
                "Increase small business lending in assessment areas"
            )
        
        if test_scores.investment_test < 80:
            recommendations.append(
                "Consider community development investments and affordable housing"
            )
        
        if cra_factors.get("minority_women_owned"):
            recommendations.append(
                "Highlight minority/women-owned business benefits in CRA reporting"
            )
        
        return recommendations