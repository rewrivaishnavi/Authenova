import json

# Copy-Move result
with open("copy_move_result.json", "r") as file:
    copy_move = json.load(file)

# Metadata result
with open("metadata_result.json", "r") as file:
    metadata = json.load(file)

# ELA result
with open("ela_result.json", "r") as file:
    ela = json.load(file)


# Get values
copy_move_detected = copy_move["tampering_detected"]
metadata_found = metadata["metadata_found"]

genuine_ela_score = ela["genuine_score"]
edited_ela_score = ela["edited_score"]


# Simple combined score
copy_move_score = 1 if copy_move_detected else 0
metadata_score = 1 if metadata_found else 0

ela_score = min(edited_ela_score / 0.1, 1)


combined_score = (
    (ela_score * 0.4) +
    (copy_move_score * 0.5) +
    (metadata_score * 0.1)
)


tampering_detected = combined_score >= 0.5


# Final report
final_result = {
    "ela_analysis": ela,
    "copy_move_detection": copy_move,
    "metadata_analysis": metadata,
    "combined_tampering_score": round(combined_score, 4),
    "tampering_detected": tampering_detected
}


# Save JSON
with open("final_result.json", "w") as file:
    json.dump(final_result, file, indent=4)


print("Final combined result created!")
print("Combined Tampering Score:", round(combined_score, 4))
print("Tampering Detected:", tampering_detected)
print("Result saved as: final_result.json")