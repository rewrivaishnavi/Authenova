import cv2
import json
import numpy as np
# Input image
image_path = "sample_images/edited.jpg"
# Output image
output_path = "copy_move_result.jpg"

# Image read karo
image = cv2.imread(image_path)

# Image ko grayscale mein convert karo
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ORB detector create karo
orb = cv2.ORB_create(nfeatures=2000)

# Image ke important points aur unke descriptors find karo
keypoints, descriptors = orb.detectAndCompute(gray, None)

print("Total keypoints found:", len(keypoints))

# Agar features nahi mile
if descriptors is None:
    print("No features found!")
    exit()

# ORB descriptors ke liye Hamming distance use hota hai
bf = cv2.BFMatcher(cv2.NORM_HAMMING)

# Har feature ko doosre features se compare karo
matches = bf.knnMatch(descriptors, descriptors, k=3)

suspicious_matches = []

for match_group in matches:

    # Self-match ko ignore karo
    valid_matches = [
        m for m in match_group
        if m.queryIdx != m.trainIdx
    ]

    if len(valid_matches) < 2:
        continue

    m = valid_matches[0]
    n = valid_matches[1]

    # Good match check
    if m.distance < 0.75 * n.distance:

        point1 = np.array(keypoints[m.queryIdx].pt)
        point2 = np.array(keypoints[m.trainIdx].pt)

        # Dono points ke beech distance
        distance = np.linalg.norm(point1 - point2)

        # Bahut paas ke points ko ignore karo
        if distance > 50:
            suspicious_matches.append(m)

print("Suspicious matches found:", len(suspicious_matches))

# Suspicious points collect karo
suspicious_points = []

for match in suspicious_matches:
    point = keypoints[match.queryIdx].pt
    suspicious_points.append(
        (int(point[0]), int(point[1]))
    )

# Suspicious region ka bounding box
if suspicious_points:
    points = np.array(suspicious_points)

    x, y, w, h = cv2.boundingRect(points)

    cv2.rectangle(
        image,
        (x, y),
        (x + w, y + h),
        (0, 0, 255),
        3
    )
# Suspicious matching points ko image par draw karo
result = image.copy()

for match in suspicious_matches:
    point = tuple(map(int, keypoints[match.queryIdx].pt))

    cv2.circle(
        result,
        point,
        8,
        (0, 0, 255),
        2
    )

# Result save karo
cv2.imwrite(output_path, result)

print("Copy-Move Detection completed!")
print("Result saved as:", output_path)

# JSON report
report = {
    "method": "ORB Copy-Move Detection",
    "total_keypoints": len(keypoints),
    "suspicious_matches": len(suspicious_matches),
    "tampering_detected": len(suspicious_matches) > 0,
    "suspicious_region": {
        "x": int(x) if suspicious_points else None,
        "y": int(y) if suspicious_points else None,
        "width": int(w) if suspicious_points else None,
        "height": int(h) if suspicious_points else None
    }
}

with open("copy_move_result.json", "w") as file:
    json.dump(report, file, indent=4)

print("JSON report saved as: copy_move_result.json")