import csv
import json

# Input and output file paths
import csv
import json
import unicodedata

# File paths
csv_file = "data_with_lyrics.csv"  # Replace with the actual file path
json_file = "data_with_lyrics_1.json"

# Function to remove diacritics (tones) from Vietnamese text
def remove_vietnamese_tones(text):
    tmp = ''.join(
        char for char in unicodedata.normalize('NFD', text)
        if unicodedata.category(char) != 'Mn'
    )
    tmp =tmp.replace("đ","d")
    return tmp

# Convert CSV to JSON with additional non-tonal lyrics attribute
with open(csv_file, encoding='utf-8') as csvf, open(json_file, 'w', encoding='utf-8') as jsonf:
    reader = csv.DictReader(csvf)
    data = []
    for row in reader:  # Overwrite the `name` column
        row['lyrics'] = row['lyrics'] + " " + remove_vietnamese_tones(row['lyrics'])  # Overwrite the `lyrics` column
        data.append(row)
    json.dump(data, jsonf, indent=4, ensure_ascii=False)

print(f"JSON file with non-tonal lyrics saved to {json_file}")