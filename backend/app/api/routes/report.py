from fastapi import APIRouter
from app.schemas.report import ScreeningReportResponse, ScreeningReportData

router = APIRouter()


@router.get("/screening-report/{document_id}", response_model=ScreeningReportResponse)
async def get_screening_report(document_id: str):
    """
    Get the complete screening report for a document.
    Aggregates results from all verification modules into a single report.
    """
    # Mock implementation - will be replaced with actual report aggregation
    return ScreeningReportResponse(
        success=True,
        data=ScreeningReportData(
            document_id=document_id,
            document_type="passport",
            extracted_fields={
                "name": "TEST USER",
                "passport_number": "P1234567",
                "date_of_birth": "2007-10-02",
                "expiry_date": "2030-05-10"
            },
            ocr_confidence=0.94,
            validation={
                "is_valid_format": True,
                "warnings": []
            },
            tampering={
                "tampering_score": 0.18,
                "indicators": ["stamp_irregularity"]
            },
            face_verification={
                "similarity_score": 0.91,
                "verification_status": "high_similarity"
            },
            risk_assessment={
                "risk_score": 18.0,
                "risk_level": "low"
            },
            decision_note="Human officer review required"
        ),
        errors=[]
    )
