from PIL import Image, ImageChops, ImageEnhance


def perform_ela(image_path, output_path, quality=90):
    # Original image open karo
    original = Image.open(image_path).convert("RGB")

    # Temporary JPEG save karo
    temp_path = "temp.jpg"
    original.save(temp_path, "JPEG", quality=quality)

    # Compressed image open karo
    compressed = Image.open(temp_path).convert("RGB")

    # Original aur compressed image ka difference
    difference = ImageChops.difference(original, compressed)

    # Difference ko bright karo
    enhanced = ImageEnhance.Brightness(difference).enhance(10)

    # ELA result save karo
    enhanced.save(output_path)

    print("ELA completed:", output_path)


# Genuine image
perform_ela(
    "sample_images/genuine.jpg",
    "genuine_ela.jpg"
)

# Edited image
perform_ela(
    "sample_images/edited.jpg",
    "edited_ela.jpg"
)
