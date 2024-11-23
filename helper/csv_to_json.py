import csv
import json
import re

# Token abbreviations mapping
ABBREVIATIONS = {
    'R': 'red',
    'G': 'green',
    'B': 'blue',
    'K': 'black',
    'P': 'purple',
    'W': 'white',
    '*': 'gold'
}

def parse_colors(color_string):
    """
    Converts a color string like '2W2G1P' into a dictionary like:
    {'white': 2, 'green': 2, 'purple': 1}
    """
    pattern = r"(\d+)([RGBKPW*])"
    matches = re.findall(pattern, color_string)
    return {ABBREVIATIONS[color]: int(quantity) for quantity, color in matches}

def convert_csv_to_json(csv_file):
    """
    Reads a CSV file and converts it into the desired JSON format.
    """
    result = []

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)

        print("Column Names:", reader.fieldnames)
        for row in reader:
            # Parse Requirements and Output
            requirements = parse_colors(row['Requirements'])
            output = parse_colors(row['Output'])

            # Construct JSON object
            item = {
                "level": int(row['Level']),
                "points": int(row['Points']),
                "feature": row['Feature'],
                "requirements": requirements,
                "output": output,
                "crowns": int(row['Crowns'])
            }
            result.append(item)

    return result

# Input CSV file
csv_file = "../resources/deck/deck.csv"

# Convert CSV to JSON
json_data = convert_csv_to_json(csv_file)

# Save JSON to a file
output_file = "../resources/deck/deck.json"
with open(output_file, 'w') as file:
    json.dump(json_data, file, indent=4)

print(f"Conversion complete. JSON saved to {output_file}.")