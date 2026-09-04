
import numpy as np
import json
import re
import cv2
import pytesseract
from pytesseract import Output

def deskew_image(image):
    """
    Detect and correct rotation in a document photo.

    How it works: threshold the image to find where the TEXT pixels are
    (not the background), then find the smallest rectangle that contains
    all of them (cv2.minAreaRect). That rectangle's angle tells us how
    tilted the text is. We rotate the whole image back by that angle.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    # minAreaRect returns angles in a slightly unintuitive range;
    # this correction maps it to the actual rotation needed.
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    deskewed = cv2.warpAffine(
        image, rotation_matrix, (w, h),
        flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255)
    )
    return deskewed


def preprocess_image(image_path):
    """
    Full preprocessing pipeline: load -> deskew -> grayscale ->
    denoise -> threshold. Returns a cleaned-up image ready for Tesseract.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not read image at: {image_path}")

    deskewed = deskew_image(image)

    gray = cv2.cvtColor(deskewed, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    _, thresholded = cv2.threshold(
        denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresholded


def extract_text_and_confidence(image_path):
    image = preprocess_image(image_path)

    extracted_text = pytesseract.image_to_string(image)

    data = pytesseract.image_to_data(
        image,
        output_type=Output.DICT
    )

    confidences = []

    for i in range(len(data["text"])):
        word = data["text"][i].strip()
        confidence = float(data["conf"][i])

        if word and confidence >= 0:
            confidences.append(confidence)

    if confidences:
        average_confidence = round(
            sum(confidences) / len(confidences) / 100,
            2
        )
    else:
        average_confidence = 0.0

    return extracted_text, average_confidence

def extract_passport_number(text):
    match = re.search(r"\b[A-Z]\d{7}\b", text)

    if match:
        return match.group()
    else:
        return None

def extract_name(text):
    match = re.search(r"NAME:\s*(.+)", text)

    if match:
        return match.group(1).strip()
    return None

def extract_dob(text):
    match = re.search(r"DATE OF BIRTH\s+(\d{2}/\d{2}/\d{4})", text)

    if match:
        return match.group(1)
    return None


def extract_expiry(text):
    match = re.search(r"DATE OF EXPIRY\s+(\d{2}/\d{2}/\d{4})", text)

    if match:
        return match.group(1)
    return None

def extract_nationality(text):
    match = re.search(r"NATIONALITY[:\s]+([A-Z]+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def extract_issue_date(text):
    match = re.search(r"DATE OF ISSUE\s+(\d{2}/\d{2}/\d{4})", text)
    if match:
        return match.group(1)
    return None

def extract_document_type(text):
    if re.search(r"\bPASSPORT\b", text, re.IGNORECASE):
        return "PASSPORT"
    return "UNKNOWN"

def extract_document(image_path):
    text, confidence = extract_text_and_confidence(image_path)

    result = {
        "document_type": extract_document_type(text),
        "name": extract_name(text),
        "passport_number": extract_passport_number(text),
        "nationality": extract_nationality(text),
        "date_of_birth": extract_dob(text),
        "date_of_issue": extract_issue_date(text),
        "expiry_date": extract_expiry(text),   # <-- renamed from "date_of_expiry"
        "ocr_confidence": confidence
    }

    return result
    

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = "../../../../data/samples/documents/test_document.png"

    result = extract_document(image_path)
    print(json.dumps(result, indent=4))

    

    