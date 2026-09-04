import re

sample_text = "passport P1234567 issued"

match = re.search(r"[A-Z]\d+", sample_text)
print(match.group())