from fastapi import APIRouter, UploadFile, File
from app.schemas.upload import UploadResponse, UploadData

router = APIRouter()


@router.post("/upload-document", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document image for verification.
    Returns a document_id that will be used throughout the verification pipeline.
    """
    # Mock implementation - will be replaced with actual file storage
    return UploadResponse(
        success=True,
        data=UploadData(
            document_id="DOC-001",
            filename=file.filename,
            content_type=file.content_type
        ),
        errors=[]
    )
