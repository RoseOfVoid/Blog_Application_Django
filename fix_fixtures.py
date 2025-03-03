import chardet

# First detect encoding
with open("database_config/fixtures.json", "rb") as f:
    raw_data = f.read()
    detected = chardet.detect(raw_data)
    encoding = detected['encoding']
    print(f"Detected encoding: {encoding}")

# If not UTF-8 then we fix it
if encoding.lower() != "utf-8":
    with open("database_config/fixtures.json", "r", encoding=encoding) as f:
        data = f.read()

    with open("database_config/fixtures_fixed.json", "w", encoding="utf-8") as f:
        f.write(data)

    print("Fixtures transfered to UTF-8!")
    print("New fixtures saved to database_config/fixtures_fixed.json")