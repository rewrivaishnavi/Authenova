from fastapi import APIRouter
from pydantic import BaseModel
from app.schemas.extraction import ExtractionResponse, ExtractionData, ExtractedFields

router = APIRouter()


class ExtractionRequest(BaseModel):
    document_id: str
    document_type: str


@router.post("/extract-data", response_model=ExtractionResponse)
async def extract_data(request: ExtractionRequest):
    """
    Extract text data from the uploaded document using OCR.
    Returns structured fields like name, passport number, dates, etc.
    """
    # Mock implementation - will be replaced with actual OCR service
    return ExtractionResponse(
        success=True,
        data=ExtractionData(
            document_id=request.document_id,
            document_type=request.document_type,
            extracted_fields=ExtractedFields(
                name="TEST USER",
                passport_number="P1234567",
                date_of_birth="2007-10-02",
                expiry_date="2030-05-10",
                nationality="IND"
            ),
            ocr_confidence=0.94
        ),
        errors=[]
    )
