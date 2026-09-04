from PIL import Image, ImageDraw, ImageFont


def make_doc(lines, filename):
    image = Image.new("RGB", (600, 300), color="white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 24)

    y = 20
    for line in lines:
        draw.text((20, y), line, fill="black", font=font)
        y += 40

    image.save(filename)
    print(f"Saved {filename}")


# Variant A: different label wording (DOB instead of DATE OF BIRTH)
make_doc([
    "REPUBLIC OF INDIA PASSPORT",
    "NAME: PRIYA SHARMA",
    "NATIONALITY: INDIAN",
    "PASSPORT NO A9876543",
    "DOB: 15/03/1998",
    "DATE OF ISSUE 01/06/2021",
    "DATE OF EXPIRY 31/05/2031",
], "../data/samples/documents/variant_a_different_labels.png")

# Variant B: different field order
make_doc([
    "REPUBLIC OF INDIA PASSPORT",
    "PASSPORT NO B1112223",
    "DATE OF EXPIRY 20/09/2029",
    "NAME: ROHAN MEHTA",
    "DATE OF BIRTH 12/12/1995",
    "NATIONALITY: INDIAN",
    "DATE OF ISSUE 20/09/2019",
], "../data/samples/documents/variant_b_reordered.png")

# Variant C: missing a field (no nationality line at all)
make_doc([
    "REPUBLIC OF INDIA PASSPORT",
    "NAME: ANITA RAO",
    "PASSPORT NO C4445556",
    "DATE OF BIRTH 05/07/2001",
    "DATE OF EXPIRY 04/07/2031",
], "../data/samples/documents/variant_c_missing_field.png")