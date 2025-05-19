"""
ARK UI class definitions generator with unique class names.
This script generates an updated version of ark_ui_classes.py with unique class names from class.txt.
"""

def extract_classes_from_txt(txt_path):
    """Extract class names and descriptions from class.txt."""
    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    classes = []
    for line in lines:
        line = line.strip()
        if ' - ' in line:
            # Format: 'class_name - Description'
            name, desc = line.split(' - ', 1)
            classes.append((name.strip(), desc.strip()))
        elif ':' in line and '#' in line and not line.startswith('  '):
            # Format: '  id: class_name # description'
            parts = line.split('#')
            if len(parts) > 1:
                name_part = parts[0].split(':')
                if len(name_part) > 1:
                    name = name_part[1].strip()
                    desc = parts[1].strip()
                    classes.append((name, desc))
    
    return classes

def make_unique_name(name, count):
    """Append _n to make the name unique."""
    if count == 1:
        return name
    return f"{name}_{count - 1}"

def generate_python_file(classes, output_path):
    """Generate the Python file with unique class names."""
    header = '''"""
ARK UI class definitions - Single source of truth.
This file contains the comprehensive list of UI classes for ARK: Survival Ascended.
"""'''

    imports = '''
import os
import yaml
'''

    class_definition = '''
# Complete list of ARK UI classes for detection - Enhanced Super Complete Version
ARK_UI_CLASSES = [
'''

    # Track class name occurrences and make them unique
    class_count = {}
    unique_classes = []
    
    # First pass: count occurrences of each class
    for name, desc in classes:
        class_count[name] = class_count.get(name, 0) + 1
    
    # Second pass: create unique names
    name_occurrence = {}
    for name, desc in classes:
        name_occurrence[name] = name_occurrence.get(name, 0) + 1
        unique_name = make_unique_name(name, name_occurrence[name])
        unique_classes.append((unique_name, desc))

    # Generate class entries with comments
    class_entries = []
    for i, (name, desc) in enumerate(unique_classes):
        # Add comment for every 10th item
        if i % 10 == 0:
            if i > 0:
                class_entries.append('    ' + f'# {((i//10) * 10)}-{((i//10) * 10) + 9}') 
            else:
                class_entries.append('    # 0-9')
        
        # Add the class with comment
        class_entries.append(f"    '{name}',  # {desc}")


    # Add footer
    footer = ''']'''

    # Combine all parts
    content = '\n'.join([header, imports, class_definition, 
                         ',\n'.join(class_entries), 
                         footer])

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    input_file = "class.txt"
    output_file = "ark_ui_classes_unique.py"
    
    try:
        print(f"Extracting classes from {input_file}...")
        classes = extract_classes_from_txt(input_file)
        print(f"Found {len(classes)} total entries")
        
        # Count unique base names (before appending numbers)
        base_names = set(name for name, _ in classes)
        print(f"Found {len(base_names)} unique base class names")
        
        print(f"Generating {output_file} with unique class names...")
        generate_python_file(classes, output_file)
        print(f"Successfully generated {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")