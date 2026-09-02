from pydantic import BaseModel


class RiskFactor(BaseModel):
    factor: str
    contribution: float
    explanation: str


class RiskData(BaseModel):
    document_id: str
    risk_score: float
    risk_level: str
    factors: list[RiskFactor]


class RiskResponse(BaseModel):
    success: bool
    data: RiskData
    errors: list