import datetime
import re


# ============================================================
# FIELD-LEVEL VALIDATION CHECKS
# ============================================================

def check_expiry(expiry_text):
    expiry_date = datetime.datetime.strptime(expiry_text, "%Y-%m-%d").date()
    today = datetime.date.today()

    if today < expiry_date:
        return {"status": "PASS", "reason": f"Document is valid upto {expiry_date}."}
    else:
        return {"status": "FAIL", "reason": f"Document is expired on {expiry_date}."}


def check_passport_format(passport_number):
    pattern = r"^[A-Z]\d{7}$"

    if re.fullmatch(pattern, passport_number):
        return {"status": "PASS", "reason": "passport format number is valid"}
    else:
        return {"status": "FAIL", "reason": "passport format number is invalid"}


def check_aadhaar_format(aadhaar_number):
    pattern = r"^\d{12}$"

    if re.fullmatch(pattern, aadhaar_number):
        return {"status": "PASS", "reason": "Aadhaar number is valid"}
    else:
        return {"status": "FAIL", "reason": "Aadhaar number is invalid"}


def check_visa_format(visa_number):
    # NOTE: placeholder format (2 letters + 7 digits) — visa number formats vary
    # by issuing country. Replace with actual required format if the project
    # targets a specific visa type.
    pattern = r"^\d{6}$|^\d{8}$"

    if re.fullmatch(pattern, visa_number):
        return {"status": "PASS", "reason": "Visa number format is valid."}
    else:
        return {"status": "FAIL", "reason": f"'{visa_number}' does not match expected format (2 letters + 7 digits)."}


def check_permit_format(permit_number):
    # NOTE: placeholder format (6 to 10 digits) — permit formats vary widely
    # by type and issuing authority. Replace with actual required format if
    # the project targets a specific permit type.
    pattern = r"^\d{6,10}$"

    if re.fullmatch(pattern, permit_number):
        return {"status": "PASS", "reason": "Permit number format is valid."}
    else:
        return {"status": "FAIL", "reason": f"'{permit_number}' does not match expected format (6 to 10 digits)."}


def check_document_type(document_type):
    allowed_types = ["passport", "visa", "aadhaar", "permit"]
    normalized_type = document_type.lower()

    if normalized_type in allowed_types:
        return {"status": "PASS", "reason": f"'{document_type}' is a recognized document type."}
    else:
        return {"status": "FAIL", "reason": f"'{document_type}' is not a recognized document type."}


def check_name(name):
    if name.strip() == "":
        return {"status": "FAIL", "reason": "Name field is empty or unreadable."}
    else:
        return {"status": "PASS", "reason": f"Name '{name}' extracted successfully."}


def check_dob(dob_text):
    dob = datetime.datetime.strptime(dob_text, "%Y-%m-%d").date()
    today = datetime.date.today()

    if dob >= today:
        return {"status": "FAIL", "reason": f"Date of birth {dob} is not in the past."}
    else:
        return {"status": "PASS", "reason": f"Date of birth {dob} is valid."}


def check_nationality(nationality):
    if nationality.strip() == "":
        return {"status": "FAIL", "reason": "Nationality field is empty or unreadable."}
    else:
        return {"status": "PASS", "reason": f"Nationality '{nationality}' extracted successfully."}


# ============================================================
# COMBINED VALIDATOR (deliverable 1)
# ============================================================

def validate_document(document):
    report = {}

    if "document_type" in document:
        report["document_type"] = check_document_type(document["document_type"])
    else:
        report["document_type"] = {"status": "FAIL", "reason": "Document type is missing."}

    if "name" in document:
        report["name"] = check_name(document["name"])
    else:
        report["name"] = {"status": "FAIL", "reason": "Name is missing."}

    if "nationality" in document:
        report["nationality"] = check_nationality(document["nationality"])
    else:
        report["nationality"] = {"status": "FAIL", "reason": "Nationality is missing."}

    if "date_of_birth" in document:
        report["date_of_birth"] = check_dob(document["date_of_birth"])
    else:
        report["date_of_birth"] = {"status": "FAIL", "reason": "Date of birth is missing."}

    if "expiry_date" in document:
        report["expiry_date"] = check_expiry(document["expiry_date"])
    else:
        report["expiry_date"] = {"status": "FAIL", "reason": "Expiry date is missing."}

    # ID number check depends on document type
    doc_type = document.get("document_type", "").lower()

    if doc_type == "passport":
        if "passport_number" in document:
            report["id_number"] = check_passport_format(document["passport_number"])
        else:
            report["id_number"] = {"status": "FAIL", "reason": "Passport number is missing."}

    elif doc_type == "aadhaar":
        if "aadhaar_number" in document:
            report["id_number"] = check_aadhaar_format(document["aadhaar_number"])
        else:
            report["id_number"] = {"status": "FAIL", "reason": "Aadhaar number is missing."}

    elif doc_type == "visa":
        if "visa_number" in document:
            report["id_number"] = check_visa_format(document["visa_number"])
        else:
            report["id_number"] = {"status": "FAIL", "reason": "Visa number is missing."}

    elif doc_type == "permit":
        if "permit_number" in document:
            report["id_number"] = check_permit_format(document["permit_number"])
        else:
            report["id_number"] = {"status": "FAIL", "reason": "Permit number is missing."}

    else:
        report["id_number"] = {"status": "FAIL", "reason": f"No ID format check available for document type '{doc_type}'."}

    return report


def get_failed_validation_reasons(validation_report):
    failed_reasons = []

    for field_name in validation_report:
        field_result = validation_report[field_name]
        if field_result["status"] == "FAIL":
            failed_reasons.append(field_result["reason"])

    return failed_reasons


# ============================================================
# RISK CONVERSION FUNCTIONS
# ============================================================

def calculate_validation_risk(validation_report):
    total_fields = len(validation_report)
    failed_fields = 0

    for field_name in validation_report:
        if validation_report[field_name]["status"] == "FAIL":
            failed_fields = failed_fields + 1

    risk_score = round((failed_fields / total_fields) * 100, 2)
    return risk_score


def calculate_tampering_risk(tampering_score):
    # Guard: tampering module may fail to produce a score (e.g. corrupted image).
    # If so, don't crash — fall back to a neutral score and say so honestly.
    if tampering_score is None or not isinstance(tampering_score, (int, float)):
        return {
            "risk_score": 50.0,
            "reason": "Tampering score unavailable — using neutral estimate.",
            "unavailable": True
        }

    risk_score = round(tampering_score * 100, 2)

    if risk_score <= 30:
        reason = f"Low tampering risk ({risk_score:.0f}% probability of digital editing)."
    elif risk_score <= 70:
        reason = f"Moderate tampering risk ({risk_score:.0f}% probability of digital editing)."
    else:
        reason = f"High tampering risk ({risk_score:.0f}% probability of digital editing)."

    return {"risk_score": risk_score, "reason": reason, "unavailable": False}


def calculate_face_risk(similarity_score):
    # Guard: face verification may have no photo to compare, or fail to run.
    # If so, don't crash — fall back to a neutral score and say so honestly.
    if similarity_score is None or not isinstance(similarity_score, (int, float)):
        return {
            "risk_score": 50.0,
            "reason": "Face similarity score unavailable — using neutral estimate.",
            "unavailable": True
        }

    risk_score = round(100 - (similarity_score * 100), 2)

    if risk_score <= 30:
        reason = f"Low face-mismatch risk ({risk_score:.0f}% risk, faces closely match)."
    elif risk_score <= 70:
        reason = f"Moderate face-mismatch risk ({risk_score:.0f}% risk, partial match)."
    else:
        reason = f"High face-mismatch risk ({risk_score:.0f}% risk, faces do not match well)."

    return {"risk_score": risk_score, "reason": reason, "unavailable": False}


def calculate_completeness_risk(document):
    required_fields = ["document_type", "name", "nationality", "date_of_birth", "expiry_date"]
    total_required = len(required_fields)
    missing_count = 0

    for field_name in required_fields:
        if field_name not in document:
            missing_count = missing_count + 1

    missing_risk = (missing_count / total_required) * 100

    # OCR confidence risk: only factor this in if OCR actually provided a confidence score.
    if "ocr_confidence" in document:
        ocr_confidence = document["ocr_confidence"]
        ocr_risk = 100 - (ocr_confidence * 100)
    else:
        ocr_risk = 0  # no confidence score provided, so it doesn't add extra risk

    # Combine both signals with equal weight (50/50) into one completeness score.
    risk_score = round((missing_risk * 0.5) + (ocr_risk * 0.5), 2)

    reasons = []

    if missing_count == 0:
        reasons.append("All required fields are present.")
    else:
        reasons.append(f"{missing_count} out of {total_required} required fields are missing.")

    if "ocr_confidence" in document:
        reasons.append(f"OCR confidence was {ocr_confidence * 100:.0f}%.")
    else:
        reasons.append("No OCR confidence score was provided.")

    reason = " ".join(reasons)

    return {"risk_score": risk_score, "reason": reason}


# ============================================================
# FINAL WEIGHTED RISK ENGINE (deliverable 2)
# Weights: validation 20%, tampering 40%, face verification 30%, completeness 10%
# ============================================================

def calculate_final_risk(document, tampering_score, similarity_score):
    validation_report = validate_document(document)
    validation_risk_score = calculate_validation_risk(validation_report)
    failed_reasons = get_failed_validation_reasons(validation_report)

    if len(failed_reasons) == 0:
        validation_reason = "All validation checks passed."
    else:
        validation_reason = "Validation issues: " + "; ".join(failed_reasons)

    tampering_result = calculate_tampering_risk(tampering_score)
    face_result = calculate_face_risk(similarity_score)
    completeness_result = calculate_completeness_risk(document)

    final_score = (
        (validation_risk_score * 0.20) +
        (tampering_result["risk_score"] * 0.40) +
        (face_result["risk_score"] * 0.30) +
        (completeness_result["risk_score"] * 0.10)
    )
    final_score = round(final_score, 2)

    if final_score <= 30:
        risk_level = "LOW"
    elif final_score <= 70:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    reasons = [
        validation_reason,
        tampering_result["reason"],
        face_result["reason"],
        completeness_result["reason"]
    ]

    # If any module's score was estimated (not real), flag this clearly so the
    # officer knows the risk score is partly a guess, not fully backed by data.
    if tampering_result.get("unavailable") or face_result.get("unavailable"):
        reasons.append("Note: one or more scores were unavailable and estimated — treat this result with caution.")

    return {
        "risk_score": final_score,
        "risk_level": risk_level,
        "reasons": reasons
    }


# ============================================================
# TEST CALLS
# ============================================================

if __name__ == "__main__":
    sample_document = {
        "document_type": "aadhaar",
        "name": "TEST USER",
        "nationality": "Indian",
        "date_of_birth": "2000-01-15",
        "aadhaar_number": "123456789012",
        "expiry_date": "2030-05-10"
    }

    bad_document = {
        "document_type": "aadhaar",
        "name": "TEST USER",
        "nationality": "Indian",
        "date_of_birth": "2000-01-15",
        "aadhaar_number": "123456789012",
        "expiry_date": "2024-01-01"
    }

    print(calculate_final_risk(sample_document, tampering_score=0.15, similarity_score=0.95))
    print(calculate_final_risk(bad_document, tampering_score=0.15, similarity_score=0.95))