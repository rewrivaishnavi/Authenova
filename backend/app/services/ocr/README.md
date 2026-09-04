# OCR Extraction Module

Owner: Khushi (Member 2)

Reads a document image (passport, ID, visa, permit) and returns structured
JSON with extracted fields and a confidence score. This module never makes
any "real/fake" judgment about the document — that decision lives in the
Risk Engine (Member 3) and stays with the human officer, per the project spec.

Pure computer vision / regex — no LLM, no external API calls, no API key
required.

## How to use it

```python
from engine import extract_document

result = extract_document("path/to/document/image.jpg")
```

Returns a dict:
```json
{
    "document_type": "PASSPORT",
    "name": "TEST USER",
    "passport_number": "P1234567",
    "nationality": "INDIAN",
    "date_of_birth": "02/10/2007",
    "date_of_issue": "15/01/2020",
    "date_of_expiry": "10/05/2030",
    "ocr_confidence": 0.95
}
```

Any field that couldn't be extracted returns `null` (Python `None`) rather
than a guessed or default value — check for `null` before relying on a
field downstream. `ocr_confidence` is a float from 0.0 to 1.0.

## Pipeline (what happens inside `extract_document`)

1. `preprocess_image()` — deskews (auto-corrects rotation), converts to
   grayscale, denoises, and thresholds the image for better OCR accuracy.
2. `pytesseract.image_to_string()` — extracts raw text.
3. `pytesseract.image_to_data()` — extracts per-word confidence scores,
   averaged into the final `ocr_confidence`.
4. A set of `extract_*` regex functions each independently search the raw
   text for one field (name, passport number, dates, etc.).

Each `extract_*` function is independent — one field failing to match does
not affect the others, and does not crash the pipeline.

## Tested against

- Clean synthetic passport image — all fields extract correctly (0.95 confidence)
- 12°-rotated image — fails completely (empty string) WITHOUT preprocessing;
  extracts all fields correctly WITH preprocessing (proves deskewing matters)
- Different field label wording (e.g. "DOB:" instead of "DATE OF BIRTH") —
  that specific field returns `null`, all other fields unaffected
- Reordered fields — extraction is order-independent, all fields still correct
- Missing field in source document — returns `null` for that field, no crash
- Non-document image (a photo unrelated to any ID) — `document_type: "UNKNOWN"`,
  all fields `null`, `ocr_confidence: 0.0`, no crash

## Known limitations

- Regex patterns are tuned to the label wording used in our synthetic test
  documents (e.g. "NAME:", "DATE OF BIRTH"). Real government documents may
  use different label text or bilingual layouts — patterns will need
  adjustment once tested against real (consented) samples.
- Only tested on passport-style layouts so far. Visa/permit formats may
  need their own field patterns.

## For integration (Member 1 / FastAPI)

Call `extract_document(image_path)` with the path to a saved image file.
It's synchronous (blocking) — for a production API route, consider running
it in a thread pool or background task if request volume matters, since
OCR + preprocessing takes a noticeable moment per image.