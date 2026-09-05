from PIL import Image, ImageChops
import numpy as np
import json
import os


def calculate_ela_score(image_path, quality=90):

    original = Image.open(image_path).convert("RGB")

    temp_path = "temp_ela.jpg"

    original.save(temp_path, "JPEG", quality=quality)

    compressed = Image.open(temp_path).convert("RGB")

    difference = ImageChops.difference(original, compressed)

    difference_array = np.array(difference, dtype=np.float32)

    score = float(np.mean(difference_array))

    os.remove(temp_path)

    return score


genuine_score = calculate_ela_score("sample_images/genuine.jpg")

edited_score = calculate_ela_score("sample_images/edited.jpg")


report = {
    "method": "Error Level Analysis",
    "genuine_score": round(genuine_score, 4),
    "edited_score": round(edited_score, 4)
}


with open("ela_result.json", "w") as file:
    json.dump(report, file, indent=4)


print("ELA Score Calculation Completed!")
print("Genuine Score:", round(genuine_score, 4))
print("Edited Score:", round(edited_score, 4))
print("Result saved as: ela_result.json")