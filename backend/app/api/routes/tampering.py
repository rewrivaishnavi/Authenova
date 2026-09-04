from fastapi import APIRouter
from pydantic import BaseModel
from app.schemas.tampering import TamperingResponse, TamperingData, TamperingIndicators

router = APIRouter()


class TamperingRequest(BaseModel):
    document_id: str
    image_path: str


@router.post("/detect-tampering", response_model=TamperingResponse)
async def detect_tampering(request: TamperingRequest):
    """
    Analyze the document image for signs of digital tampering or manipulation.
    Returns tampering indicators and a risk score.
    """
    # Mock implementation - will be replaced with actual tampering detection service
    return TamperingResponse(
        success=True,
        data=TamperingData(
            document_id=request.document_id,
            tampering_score=0.18,
            indicators=TamperingIndicators(
                photo_region_anomaly=False,
                text_region_anomaly=False,
                stamp_irregularity=True,
                metadata_anomaly=False
            ),
            evidence=["Possible irregularity detected in stamp region"]
        ),
        errors=[]
    )
