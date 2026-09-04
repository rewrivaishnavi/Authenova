from fastapi import APIRouter
from pydantic import BaseModel
from app.schemas.risk import RiskResponse, RiskData, RiskFactor

router = APIRouter()


class RiskRequest(BaseModel):
    document_id: str
    ocr_confidence: float
    validation_result: dict
    tampering_result: dict
    face_result: dict


@router.post("/calculate-risk", response_model=RiskResponse)
async def calculate_risk(request: RiskRequest):
    """
    Calculate an explainable risk score by combining signals from all verification modules.
    Returns risk level, score, and contributing factors with explanations.
    """
    # Mock implementation - will be replaced with actual risk scoring engine
    return RiskResponse(
        success=True,
        data=RiskData(
            document_id=request.document_id,
            risk_score=18.0,
            risk_level="low",
            factors=[
                RiskFactor(
                    factor="OCR confidence",
                    contribution=2.0,
                    explanation="High OCR confidence"
                ),
                RiskFactor(
                    factor="Document validation",
                    contribution=0.0,
                    explanation="No validation issues detected"
                ),
                RiskFactor(
                    factor="Tampering analysis",
                    contribution=8.0,
                    explanation="Minor stamp-region irregularity detected"
                ),
                RiskFactor(
                    factor="Face verification",
                    contribution=8.0,
                    explanation="High facial similarity"
                )
            ]
        ),
        errors=[]
    )
