from pydantic import BaseModel


class FaceData(BaseModel):
    document_id: str
    face_detected_document: bool
    face_detected_verification: bool
    similarity_score: float
    verification_status: str


class FaceResponse(BaseModel):
    success: bool
    data: FaceData
    errors: list