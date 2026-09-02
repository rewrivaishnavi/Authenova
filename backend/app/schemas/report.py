from pydantic import BaseModel


class ScreeningReportData(BaseModel):
    document_id: str
    document_type: str
    extracted_fields: dict
    ocr_confidence: float
    validation: dict
    tampering: dict
    face_verification: dict
    risk_assessment: dict
    decision_note: str


class ScreeningReportResponse(BaseModel):
    success: bool
    data: ScreeningReportData
    errors: list