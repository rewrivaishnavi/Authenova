from fastapi import APIRouter
from pydantic import BaseModel
from app.schemas.face import FaceResponse, FaceData

router = APIRouter()


class FaceVerificationRequest(BaseModel):
    document_id: str
    document_image_path: str
    verification_image_path: str


@router.post("/verify-face", response_model=FaceResponse)
async def verify_face(request: FaceVerificationRequest):
    """
    Compare the face photo in the document with a presented/live verification photo.
    Returns similarity score and verification status.
    """
    # Mock implementation - will be replaced with actual face verification service
    return FaceResponse(
        success=True,
        data=FaceData(
            document_id=request.document_id,
            face_detected_document=True,
            face_detected_verification=True,
            similarity_score=0.91,
            verification_status="high_similarity"
        ),
        errors=[]
    )
