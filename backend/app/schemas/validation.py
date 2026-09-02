from pydantic import BaseModel


class ValidationChecks(BaseModel):
    required_fields_present: bool
    passport_number_format: bool
    date_format_valid: bool
    expiry_date_valid: bool


class ValidationData(BaseModel):
    document_id: str
    is_valid_format: bool
    checks: ValidationChecks
    validation_warnings: list[str]


class ValidationResponse(BaseModel):
    success: bool
    data: ValidationData
    errors: list