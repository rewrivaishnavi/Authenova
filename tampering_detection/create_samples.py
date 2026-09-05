from PIL import Image, ImageDraw, ImageFont


# -----------------------------
# 1. Create genuine image
# -----------------------------

width = 1000
height = 600

image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# Border
draw.rectangle(
    (30, 30, 970, 570),
    outline="black",
    width=5
)

# Title
draw.text(
    (350, 70),
    "TEST DOCUMENT",
    fill="black"
)

# Document information
draw.text(
    (100, 180),
    "Name: TEST USER",
    fill="black"
)

draw.text(
    (100, 240),
    "Document No: TEST123456",
    fill="black"
)

draw.text(
    (100, 300),
    "Date: 01-09-2026",
    fill="black"
)

draw.text(
    (100, 360),
    "Status: VALID",
    fill="black"
)

# Stamp
draw.rectangle(
    (700, 400, 900, 500),
    outline="black",
    width=4
)

draw.text(
    (735, 435),
    "STAMP",
    fill="black"
)

# Save genuine image
image.save("sample_images/genuine.jpg", quality=95)


# -----------------------------
# 2. Create edited image
# -----------------------------

edited = image.copy()
edited_draw = ImageDraw.Draw(edited)

# Change one field
edited_draw.rectangle(
    (90, 230, 500, 270),
    fill="white"
)

edited_draw.text(
    (100, 240),
    "Document No: FAKE987654",
    fill="black"
)

# Copy the stamp and paste it somewhere else
stamp = image.crop((700, 400, 900, 500))

edited.paste(
    stamp,
    (700, 280)
)

# Save edited image
edited.save("sample_images/edited.jpg", quality=95)

print("Genuine image created successfully!")
print("Edited image created successfully!")