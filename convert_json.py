import csv
import json

# Input and output file paths
csv_file = "data_with_lyrics.csv"  # Replace with the actual file path
json_file = "data_with_lyrics.json"

# Convert CSV to JSON
with open(csv_file, encoding='utf-8') as csvf, open(json_file, 'w', encoding='utf-8') as jsonf:
    reader = csv.DictReader(csvf)
    json.dump([row for row in reader], jsonf, indent=4, ensure_ascii=False)

print(f"JSON file saved to {json_file}")
