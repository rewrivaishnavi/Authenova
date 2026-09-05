from PIL import Image
from PIL.ExifTags import TAGS
import json

# Image path
image_path = "sample_images/edited.jpg"

# Image open karo
image = Image.open(image_path)

# EXIF metadata nikalo
exif_data = image.getexif()

metadata = {}

for tag_id, value in exif_data.items():
    tag = TAGS.get(tag_id, tag_id)
    metadata[tag] = str(value)

# Terminal par metadata print karo
print("Metadata found:", len(metadata))

for key, value in metadata.items():
    print(key, ":", value)

# JSON file mein save karo
report = {
    "metadata_found": len(metadata) > 0,
    "metadata_count": len(metadata),
    "metadata": metadata
}

with open("metadata_result.json", "w") as file:
    json.dump(report, file, indent=4)

print("Metadata result saved as: metadata_result.json")

