"""
Clean duplicate entries from ark_ui_classes_updated.py
Keeps entries with the same name but different descriptions.
"""

def clean_duplicates(input_file, output_file):
    """Remove duplicate entries where both name and description match."""
    entries = set()  # To track unique (name, description) pairs
    lines_to_keep = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#') or line.startswith('"""'):
            lines_to_keep.append(lines[i])
            i += 1
            continue
            
        # Check if this is a class definition line
        if line.startswith("'"):
            try:
                # Extract the class name and description
                name = line.split("'")[1]
                desc = line.split('#', 1)[1].strip() if '#' in line else ''
                
                # Check if we've seen this exact (name, desc) before
                entry_key = (name, desc)
                if entry_key not in entries:
                    entries.add(entry_key)
                    lines_to_keep.append(lines[i])
                else:
                    print(f"Removing duplicate: {name} - {desc}")
            except Exception as e:
                print(f"Error processing line: {line}")
                print(f"Error: {e}")
                lines_to_keep.append(lines[i])  # Keep the line if we can't parse it
        else:
            lines_to_keep.append(lines[i])
            
        i += 1
    
    # Write the cleaned content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(lines_to_keep)
    
    print(f"\nOriginal entries: {len(lines)}")
    print(f"Unique entries: {len(entries)}")
    print(f"Removed {len(lines) - len(lines_to_keep)} duplicate entries")
    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    input_file = "ark_ui_classes_updated.py"
    output_file = "ark_ui_classes_cleaned.py"
    clean_duplicates(input_file, output_file)
