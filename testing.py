import chardet

with open("csv_database.csv", "rb") as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)

print("Detected Encoding:", result["encoding"])
