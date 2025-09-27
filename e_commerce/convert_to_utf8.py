import chardet

# Step 1: Detect encoding
with open("data.json", "rb") as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    print("Detected encoding:", result['encoding'])

# Step 2: Decode with detected encoding and save as UTF-8
with open("data.json", "r", encoding=result['encoding']) as f:
    data = f.read()

with open("data_utf8.json", "w", encoding="utf-8") as f:
    f.write(data)

print("Conversion complete!")
