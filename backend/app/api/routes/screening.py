"""
Screening API Routes
Endpoints for running the complete document screening pipeline.
"""
from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional

from app.services.orchestrator.pipeline import pipeline
from app.schemas.report import ScreeningReportResponse, ScreeningReportData

router = APIRouter()


class ScreeningStatusResponse(BaseModel):
    success: bool
    document_id: str
    status: str
    message: str


@router.post("/screen", response_model=ScreeningStatusResponse)
async def start_screening(
    file: UploadFile = File(...),
    document_type: str = Form("passport"),
    verification_image: Optional[UploadFile] = File(None)
):
    """
    Start a complete document screening process.
    This will run all verification modules and return a screening report.
    """
    # Read file content
    file_content = await file.read()
    verification_content = None
    verification_path = None

    if verification_image:
        verification_content = await verification_image.read()
        verification_path = f"verification/{file.filename}"

    # Run the complete screening pipeline
    result = await pipeline.run_screening(
        file_content=file_content,
        filename=file.filename,
        content_type=file.content_type,
        document_type=document_type,
        verification_image_path=verification_path
    )

    return ScreeningStatusResponse(
        success=True,
        document_id=result["document_id"],
        status="completed",
        message="Screening completed successfully"
    )


@router.get("/results/{document_id}", response_model=ScreeningReportResponse)
async def get_screening_results(document_id: str):
    """
    Get the results of a completed screening.
    Returns the full screening report with all module results.
    """
    screening = pipeline.get_screening(document_id)

    if not screening:
        return ScreeningReportResponse(
            success=False,
            data=ScreeningReportData(
                document_id=document_id,
                document_type="unknown",
                extracted_fields={},
                ocr_confidence=0.0,
                validation={},
                tampering={},
                face_verification={},
                risk_assessment={},
                decision_note="Screening not found"
            ),
            errors=[f"Screening with document_id {document_id} not found"]
        )

    report = screening["report"]
    return ScreeningReportResponse(
        success=True,
        data=report,
        errors=[]
    )
