from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')


# ============================================================
# KNOWLEDGE BASE
# Placeholder reference rules, matching the checks already
# implemented in validation_risk_engine.py. Not real cited
# ICAO standards — refine with real citations if time allows.
# ============================================================

knowledge_base = [
    {"id": "kb_001", "text": "A document is considered expired if its expiry date is earlier than or equal to the current date. Expired documents should be flagged as high risk, as they are no longer legally valid for identity verification."},
    {"id": "kb_002", "text": "Indian passport numbers follow the format of one uppercase letter followed by seven digits (e.g. M1234567). A passport number that does not match this pattern indicates a possible OCR error or a forged document."},
    {"id": "kb_003", "text": "Aadhaar numbers are exactly 12 digits with no letters. Any deviation from this format, such as extra characters or incorrect length, should be treated as invalid."},
    {"id": "kb_004", "text": "Visa numbers are typically issued as a combination of letters followed by digits, varying by issuing country. Exact format should be verified against the specific country's visa numbering standard."},
    {"id": "kb_005", "text": "A missing required field, such as name, date of birth, or document type, significantly reduces confidence in the document's completeness and should raise the associated risk score."},
    {"id": "kb_006", "text": "Low OCR confidence on a critical field, such as an ID number or expiry date, suggests the extracted text may be inaccurate and downstream validation results should be treated with caution."},
    {"id": "kb_007", "text": "A high tampering detection score, typically above 70 percent, indicates strong evidence of digital editing such as photo replacement, text alteration, or recompression artifacts, and warrants close manual review."},
    {"id": "kb_008", "text": "A low face similarity score between the document photo and the presented photo suggests the person presenting the document may not match the identity shown on it, which is a strong indicator of impersonation."},
    {"id": "kb_009", "text": "Date of birth must always be a date in the past. A date of birth that is today or in the future is logically invalid and indicates either a data entry error or a fraudulent document."},
    {"id": "kb_010", "text": "Document types are limited to a known, recognized set (passport, visa, aadhaar, permit). An unrecognized document type may indicate an unsupported document, a scanning error, or an attempt to bypass validation."}
]

for entry in knowledge_base:
    entry["embedding"] = model.encode(entry["text"])


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve_best_match(query_text, knowledge_base):
    query_embedding = model.encode(query_text)

    best_entry = None
    best_score = -1

    for entry in knowledge_base:
        score = util.cos_sim(query_embedding, entry["embedding"]).item()
        if score > best_score:
            best_score = score
            best_entry = entry

    return best_entry, best_score


# ============================================================
# GROUNDED EXPLANATION
# Always uses the actually-retrieved text — nothing invented.
# ============================================================

def generate_grounded_explanation(query_text, retrieved_entry):
    return f'Regarding the flagged issue "{query_text}" - {retrieved_entry["text"]}'


# ============================================================
# COMBINED FUNCTION — this is what Member 1 (backend) would call
# ============================================================

def explain_flagged_issue(query_text):
    """
    Takes one flagged issue (e.g. a FAIL reason from validate_document,
    or a high-risk reason from calculate_final_risk) and returns a
    grounded explanation, retrieved from the knowledge base.
    """
    retrieved_entry, score = retrieve_best_match(query_text, knowledge_base)
    explanation = generate_grounded_explanation(query_text, retrieved_entry)

    return {
        "explanation": explanation,
        "source_id": retrieved_entry["id"],
        "similarity_score": round(score, 4)
    }


# ============================================================
# TEST CALLS
# ============================================================

if __name__ == "__main__":
    test_queries = [
        "Document is expired on 2024-01-01.",
        "Aadhaar number is invalid",
        "High tampering risk (90% probability of digital editing).",
        "Low face-mismatch risk... faces do not match well",
    ]

    for q in test_queries:
        result = explain_flagged_issue(q)
        print(f"Query: {q}")
        print(f"  -> Source: {result['source_id']} (score: {result['similarity_score']})")
        print(f"  -> {result['explanation']}")
        print()