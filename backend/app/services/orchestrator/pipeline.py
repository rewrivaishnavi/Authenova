"""
Orchestrator Service
Chains all verification modules into a single screening pipeline.
Uses document_id as the connecting identifier throughout all stages.
"""
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

# Import schemas
from app.schemas.upload import UploadData
from app.schemas.extraction import ExtractionData, ExtractedFields
from app.schemas.validation import ValidationData, ValidationChecks
from app.schemas.tampering import TamperingData, TamperingIndicators
from app.schemas.face import FaceData
from app.schemas.risk import RiskData, RiskFactor
from app.schemas.report import ScreeningReportData


class ScreeningPipeline:
    """
    Manages the complete document screening workflow.
    Chains: Upload → OCR → Validation → Tampering → Face → Risk → Report
    """

    def __init__(self):
        self.screenings: Dict[str, Dict[str, Any]] = {}

    def generate_document_id(self) -> str:
        """Generate a unique document identifier."""
        return f"DOC-{uuid.uuid4().hex[:8].upper()}"

    async def run_screening(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
        document_type: str = "passport",
        verification_image_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run the complete screening pipeline for a document.
        Returns the full screening report with all module results.
        """
        document_id = self.generate_document_id()

        # Stage 1: Upload
        upload_result = self._process_upload(document_id, filename, content_type)

        # Stage 2: OCR Extraction
        extraction_result = await self._process_extraction(document_id, document_type)

        # Stage 3: Document Validation
        validation_result = await self._process_validation(
            document_id,
            document_type,
            extraction_result.extracted_fields.__dict__
        )

        # Stage 4: Tampering Detection
        tampering_result = await self._process_tampering(document_id, f"uploads/{document_id}.jpg")

        # Stage 5: Face Verification
        face_result = None
        if verification_image_path:
            face_result = await self._process_face_verification(
                document_id,
                f"uploads/{document_id}.jpg",
                verification_image_path
            )

        # Stage 6: Risk Calculation
        risk_result = await self._process_risk_calculation(
            document_id,
            extraction_result.ocr_confidence,
            {
                "is_valid_format": validation_result.is_valid_format,
                "warnings_count": len(validation_result.validation_warnings)
            },
            {"tampering_score": tampering_result.tampering_score},
            {"similarity_score": face_result.similarity_score if face_result else 0.0}
        )

        # Stage 7: Generate Report
        report = self._generate_report(
            document_id,
            document_type,
            extraction_result,
            validation_result,
            tampering_result,
            face_result,
            risk_result
        )

        # Store the screening result
        self.screenings[document_id] = {
            "upload": upload_result,
            "extraction": extraction_result,
            "validation": validation_result,
            "tampering": tampering_result,
            "face_verification": face_result,
            "risk": risk_result,
            "report": report,
            "timestamp": datetime.now().isoformat()
        }

        return {
            "document_id": document_id,
            "status": "completed",
            "report": report
        }

    def _process_upload(self, document_id: str, filename: str, content_type: str) -> UploadData:
        """Process document upload."""
        return UploadData(
            document_id=document_id,
            filename=filename,
            content_type=content_type
        )

    async def _process_extraction(self, document_id: str, document_type: str) -> ExtractionData:
        """Process OCR extraction."""
        # Mock implementation - will be replaced with actual OCR service
        return ExtractionData(
            document_id=document_id,
            document_type=document_type,
            extracted_fields=ExtractedFields(
                name="TEST USER",
                passport_number="P1234567",
                date_of_birth="2007-10-02",
                expiry_date="2030-05-10",
                nationality="IND"
            ),
            ocr_confidence=0.94
        )

    async def _process_validation(
        self,
        document_id: str,
        document_type: str,
        extracted_fields: Dict
    ) -> ValidationData:
        """Process document validation."""
        # Mock implementation - will be replaced with actual validation service
        return ValidationData(
            document_id=document_id,
            is_valid_format=True,
            checks=ValidationChecks(
                required_fields_present=True,
                passport_number_format=True,
                date_format_valid=True,
                expiry_date_valid=True
            ),
            validation_warnings=[]
        )

    async def _process_tampering(self, document_id: str, image_path: str) -> TamperingData:
        """Process tampering detection."""
        # Mock implementation - will be replaced with actual tampering service
        return TamperingData(
            document_id=document_id,
            tampering_score=0.18,
            indicators=TamperingIndicators(
                photo_region_anomaly=False,
                text_region_anomaly=False,
                stamp_irregularity=True,
                metadata_anomaly=False
            ),
            evidence=["Possible irregularity detected in stamp region"]
        )

    async def _process_face_verification(
        self,
        document_id: str,
        document_image_path: str,
        verification_image_path: str
    ) -> Optional[FaceData]:
        """Process face verification."""
        # Mock implementation - will be replaced with actual face verification service
        return FaceData(
            document_id=document_id,
            face_detected_document=True,
            face_detected_verification=True,
            similarity_score=0.91,
            verification_status="high_similarity"
        )

    async def _process_risk_calculation(
        self,
        document_id: str,
        ocr_confidence: float,
        validation_result: Dict,
        tampering_result: Dict,
        face_result: Dict
    ) -> RiskData:
        """Calculate risk score based on all module results."""
        # Mock implementation - will be replaced with actual risk scoring engine
        return RiskData(
            document_id=document_id,
            risk_score=18.0,
            risk_level="low",
            factors=[
                RiskFactor(
                    factor="OCR confidence",
                    contribution=2.0,
                    explanation="High OCR confidence"
                ),
                RiskFactor(
                    factor="Document validation",
                    contribution=0.0,
                    explanation="No validation issues detected"
                ),
                RiskFactor(
                    factor="Tampering analysis",
                    contribution=8.0,
                    explanation="Minor stamp-region irregularity detected"
                ),
                RiskFactor(
                    factor="Face verification",
                    contribution=8.0,
                    explanation="High facial similarity"
                )
            ]
        )

    def _generate_report(
        self,
        document_id: str,
        document_type: str,
        extraction_result: ExtractionData,
        validation_result: ValidationData,
        tampering_result: TamperingData,
        face_result: Optional[FaceData],
        risk_result: RiskData
    ) -> ScreeningReportData:
        """Generate the complete screening report."""
        return ScreeningReportData(
            document_id=document_id,
            document_type=document_type,
            extracted_fields=extraction_result.extracted_fields.__dict__,
            ocr_confidence=extraction_result.ocr_confidence,
            validation={
                "is_valid_format": validation_result.is_valid_format,
                "warnings": validation_result.validation_warnings
            },
            tampering={
                "tampering_score": tampering_result.tampering_score,
                "indicators": [
                    k for k, v in tampering_result.indicators.__dict__.items() if v
                ]
            },
            face_verification={
                "similarity_score": face_result.similarity_score if face_result else 0.0,
                "verification_status": face_result.verification_status if face_result else "not_available"
            },
            risk_assessment={
                "risk_score": risk_result.risk_score,
                "risk_level": risk_result.risk_level
            },
            decision_note="Human officer review required"
        )

    def get_screening(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a screening result by document_id."""
        return self.screenings.get(document_id)


# Global pipeline instance
pipeline = ScreeningPipeline()
