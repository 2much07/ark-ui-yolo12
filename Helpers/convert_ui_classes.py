import json
import random

def generate_color(index):
    """Generate a unique color based on the index."""
    # Use golden ratio to generate visually distinct colors
    golden_ratio = 0.618033988749895
    h = (index * golden_ratio) % 1.0
    
    # Convert HSV to RGB
    h_i = int(h * 6)
    f = h * 6 - h_i
    p = 0
    q = int(255 * (1 - f))
    t = int(255 * f)
    v = 200  # Keep value high for better visibility
    
    if h_i == 0:
        r, g, b = v, t, p
    elif h_i == 1:
        r, g, b = q, v, p
    elif h_i == 2:
        r, g, b = p, v, t
    elif h_i == 3:
        r, g, b = p, q, v
    elif h_i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q
    
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def convert_ui_classes(input_file, output_file):
    """Convert the UI classes file to the desired format."""
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Process each line to extract class names
    classes = []
    name_count = {}
    
    for line in lines:
        # Handle lines with format: "name - description" or "id: name # description"
        if ' - ' in line:
            name = line.split(' - ')[0].strip()
        elif ':' in line and '#' in line:
            name = line.split('#')[0].split(':')[1].strip()
        else:
            continue
            
        # Skip empty names
        if not name:
            continue
        
        # Make name lowercase and replace spaces with underscores
        name = name.lower().replace(' ', '_')
        
        # Handle duplicate names by appending a number
        if name in name_count:
            name_count[name] += 1
            unique_name = f"{name}_{name_count[name]}"
        else:
            name_count[name] = 0
            unique_name = name
        
        # Add to classes list with unique color and name
        color = generate_color(len(classes))
        classes.append(
            '{{"name": "{}", "color": "{}", "type": "rectangle", "attributes": []}}'.format(unique_name, color)
        )
    
    # Save to output file with exact formatting
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('[' + ',\n'.join(classes) + ']')
    
    return len(classes)

if __name__ == "__main__":
    input_file = "este.json"
    output_file = "converted_ui_classes.json"
    
    try:
        count = convert_ui_classes(input_file, output_file)
        print(f"Successfully converted {count} UI classes to {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")
