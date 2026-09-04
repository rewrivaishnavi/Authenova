import numpy as np
import cv2

from PIL import Image, ImageDraw, ImageFont

image = Image.new("RGB", (600, 300), color="white")
draw = ImageDraw.Draw(image)

# Load an actual font at a readable size, instead of the tiny default one.
# "arial.ttf" ships with Windows, so this should work directly for you.
font = ImageFont.truetype("arial.ttf", 24)

lines = [
    "REPUBLIC OF INDIA PASSPORT",
    "NAME: TEST USER",
    "NATIONALITY: INDIAN",
    "PASSPORT NO P1234567",
    "DATE OF BIRTH 02/10/2007",
    "DATE OF ISSUE 15/01/2020",
    "DATE OF EXPIRY 10/05/2030",
]

y_position = 20
for line in lines:
    draw.text((20, y_position), line, fill="black", font=font)
    y_position += 40

image.save("../data/samples/documents/test_document.png")
print("Saved test_document.png")

# --- Generate a rotated version to test deskewing ---
cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
h, w = cv_image.shape[:2]

# Rotate onto a bigger white canvas so corners don't get cut off during rotation
canvas = np.full((h + 100, w + 100, 3), 255, dtype=np.uint8)
canvas[50:50 + h, 50:50 + w] = cv_image

center = (canvas.shape[1] // 2, canvas.shape[0] // 2)
rotation_matrix = cv2.getRotationMatrix2D(center, angle=12, scale=1.0)
rotated = cv2.warpAffine(
    canvas, rotation_matrix, (canvas.shape[1], canvas.shape[0]),
    borderValue=(255, 255, 255)
)

cv2.imwrite("../data/samples/documents/test_document_rotated.png", rotated)
print("Saved test_document_rotated.png (12-degree rotated, for testing deskew)")