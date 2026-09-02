from pydantic import BaseModel


class TamperingIndicators(BaseModel):
    photo_region_anomaly: bool
    text_region_anomaly: bool
    stamp_irregularity: bool
    metadata_anomaly: bool


class TamperingData(BaseModel):
    document_id: str
    tampering_score: float
    indicators: TamperingIndicators
    evidence: list[str]


class TamperingResponse(BaseModel):
    success: bool
    data: TamperingData
    errors: list