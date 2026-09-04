"""
Integration tests for the Authenova API endpoints.
Tests all mock endpoints and the complete screening pipeline.
"""
import io
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestHealthEndpoints:
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Authenova API is running"
        assert data["version"] == "0.1.0"

    def test_health(self):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestUploadEndpoint:
    def test_upload_document(self):
        files = {"file": ("passport.jpg", io.BytesIO(b"fake-image-data"), "image/jpeg")}
        response = client.post("/api/v1/upload-document", files=files)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["document_id"] == "DOC-001"
        assert data["data"]["filename"] == "passport.jpg"
        assert data["data"]["content_type"] == "image/jpeg"
        assert data["errors"] == []


class TestExtractionEndpoint:
    def test_extract_data(self):
        payload = {"document_id": "DOC-001", "document_type": "passport"}
        response = client.post("/api/v1/extract-data", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["document_id"] == "DOC-001"
        assert data["data"]["document_type"] == "passport"
        fields = data["data"]["extracted_fields"]
        assert fields["name"] == "TEST USER"
        assert fields["passport_number"] == "P1234567"
        assert data["data"]["ocr_confidence"] == 0.94


class TestValidationEndpoint:
    def test_validate_document(self):
        payload = {
            "document_id": "DOC-001",
            "document_type": "passport",
            "extracted_fields": {
                "name": "TEST USER",
                "passport_number": "P1234567",
                "date_of_birth": "2007-10-02",
                "expiry_date": "2030-05-10",
                "nationality": "IND"
            }
        }
        response = client.post("/api/v1/validate-document", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["is_valid_format"] is True
        assert data["data"]["checks"]["required_fields_present"] is True
        assert data["data"]["checks"]["passport_number_format"] is True
        assert data["data"]["checks"]["date_format_valid"] is True
        assert data["data"]["checks"]["expiry_date_valid"] is True


class TestTamperingEndpoint:
    def test_detect_tampering(self):
        payload = {"document_id": "DOC-001", "image_path": "uploads/DOC-001.jpg"}
        response = client.post("/api/v1/detect-tampering", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["tampering_score"] == 0.18
        assert data["data"]["indicators"]["stamp_irregularity"] is True
        assert len(data["data"]["evidence"]) > 0


class TestFaceVerificationEndpoint:
    def test_verify_face(self):
        payload = {
            "document_id": "DOC-001",
            "document_image_path": "uploads/DOC-001.jpg",
            "verification_image_path": "verification/DOC-001-face.jpg"
        }
        response = client.post("/api/v1/verify-face", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["face_detected_document"] is True
        assert data["data"]["face_detected_verification"] is True
        assert data["data"]["similarity_score"] == 0.91
        assert data["data"]["verification_status"] == "high_similarity"


class TestRiskEndpoint:
    def test_calculate_risk(self):
        payload = {
            "document_id": "DOC-001",
            "ocr_confidence": 0.94,
            "validation_result": {"is_valid_format": True, "warnings_count": 0},
            "tampering_result": {"tampering_score": 0.18},
            "face_result": {"similarity_score": 0.91}
        }
        response = client.post("/api/v1/calculate-risk", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["risk_score"] == 18.0
        assert data["data"]["risk_level"] == "low"
        assert len(data["data"]["factors"]) == 4


class TestReportEndpoint:
    def test_screening_report(self):
        response = client.get("/api/v1/screening-report/DOC-001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["document_id"] == "DOC-001"
        assert data["data"]["document_type"] == "passport"
        assert data["data"]["decision_note"] == "Human officer review required"


class TestScreeningPipeline:
    def test_screening_end_to_end(self):
        files = {"file": ("passport.jpg", io.BytesIO(b"fake-image-data"), "image/jpeg")}
        response = client.post("/api/v1/screen", files=files, data={"document_type": "passport"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["status"] == "completed"
        document_id = data["document_id"]

        # Verify results are available
        results = client.get(f"/api/v1/results/{document_id}")
        assert results.status_code == 200
        result_data = results.json()
        assert result_data["success"] is True
        assert result_data["data"]["document_id"] == document_id
        assert result_data["data"]["document_type"] == "passport"
        assert "risk_assessment" in result_data["data"]
        assert result_data["data"]["decision_note"] == "Human officer review required"