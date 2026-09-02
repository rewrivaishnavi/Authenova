from pydantic import BaseModel


class UploadData(BaseModel):
    document_id: str
    filename: str
    content_type: str


class UploadResponse(BaseModel):
    success: bool
    data: UploadData
    errors: list