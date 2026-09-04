from fastapi import FastAPI, UploadFile, File
from app.api.routes import health, upload, extraction, validation, tampering, face, risk, report, screening

app = FastAPI(
    title="Authenova API",
    description="AI-powered identity and document verification platform",
    version="0.1.0"
)

# Include all API routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(extraction.router, prefix="/api/v1", tags=["extraction"])
app.include_router(validation.router, prefix="/api/v1", tags=["validation"])
app.include_router(tampering.router, prefix="/api/v1", tags=["tampering"])
app.include_router(face.router, prefix="/api/v1", tags=["face"])
app.include_router(risk.router, prefix="/api/v1", tags=["risk"])
app.include_router(report.router, prefix="/api/v1", tags=["report"])
app.include_router(screening.router, prefix="/api/v1", tags=["screening"])


@app.get("/")
def root():
    return {
        "message": "Authenova API is running",
        "version": "0.1.0"
    }


