from pydantic import BaseModel


class ExtractedFields(BaseModel):
    name: str
    passport_number: str
    date_of_birth: str
    expiry_date: str
    nationality: str


class ExtractionData(BaseModel):
    document_id: str
    document_type: str
    extracted_fields: ExtractedFields
    ocr_confidence: float


class ExtractionResponse(BaseModel):
    success: bool
    data: ExtractionData
    errors: list