import json
import csv

# Read the JSON file
with open('converted_ui_classes.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Write to CSV
with open('converted_ui_classes.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['name', 'color', 'type', 'attributes'])
    
    for item in data:
        attributes = ','.join(item.get('attributes', []))
        writer.writerow([
            item.get('name', ''),
            item.get('color', ''),
            item.get('type', ''),
            attributes
        ])

print(f"Successfully converted {len(data)} entries to CSV format.")