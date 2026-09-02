from fastapi import FastAPI, UploadFile, File
from app.api.routes import health

app = FastAPI(
    title="Authenova API",
    description="AI-powered identity and document verification platform",
    version="0.1.0"
)

app.include_router(health.router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Authenova API is running",
        "version": "0.1.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    return {
        "success": True,
        "data": {
            "document_id": "DOC-001",
            "filename": file.filename,
            "content_type": file.content_type
        },
        "errors": []
    }