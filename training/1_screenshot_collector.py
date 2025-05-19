#!/usr/bin/env python
"""
Screenshot collector script for ARK: Survival Ascended UI detection.
This script organizes screenshots into subfolders based on UI states
defined in ark_ui_classes.py for CVAT annotation.
"""

import os
import time
import json
import argparse
import keyboard
import mss
import numpy as np
import cv2
from datetime import datetime
from pathlib import Path
import sys
import importlib.util
import yaml

# Add parent directory to path to allow importing ark_ui_classes.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

def load_ui_classes_from_module(class_collection=None):
    """
    Load UI classes from the ark_ui_classes.py module.
    Returns a list of UI element dictionaries in CVAT-compatible format.
    
    Args:
        class_collection: Which class collection to use ('ark', 'common', 'all', or None for auto-detect)
    """
    try:
        # Try to import the module directly
        module_loaded = False
        ui_classes = None
        
        try:
            # Try to access directly first
            if class_collection == 'common':
                from utils.ark_ui_classes import COMMON_ITEMS
                ui_classes = COMMON_ITEMS
                module_loaded = True
                print("Successfully loaded COMMON_ITEMS from utils.ark_ui_classes")
            elif class_collection == 'all':
                from utils.ark_ui_classes import ALL_ARK_UI_CLASSES
                ui_classes = ALL_ARK_UI_CLASSES
                module_loaded = True
                print("Successfully loaded ALL_ARK_UI_CLASSES from utils.ark_ui_classes")
            else:  # default to ARK_UI_CLASSES
                from utils.ark_ui_classes import ARK_UI_CLASSES
                ui_classes = ARK_UI_CLASSES
                module_loaded = True
                print("Successfully loaded ARK_UI_CLASSES from utils.ark_ui_classes")
        except (ImportError, NameError, AttributeError) as e:
            print(f"Couldn't directly import classes: {e}")
            
            # Try to locate the file
            module_path = None
            for path in [
                os.path.join(parent_dir, 'utils', 'ark_ui_classes.py'),
                os.path.join(parent_dir, 'ark_ui_classes.py'),
                os.path.join(current_dir, 'utils', 'ark_ui_classes.py'),
                os.path.join(current_dir, 'ark_ui_classes.py')
            ]:
                if os.path.exists(path):
                    module_path = path
                    break
            
            if module_path:
                print(f"Found module at {module_path}")
                
                # Try to extract classes directly from file
                ui_classes = extract_classes_from_file(module_path, class_collection)
                if ui_classes:
                    module_loaded = True
                    print(f"Successfully extracted {len(ui_classes)} UI classes from file")
            
        # If we couldn't load from the module, try YAML
        if not module_loaded or ui_classes is None:
            print("Falling back to YAML loading...")
            try:
                ui_classes = load_ui_classes_from_yaml()
                print("Successfully loaded classes from YAML")
            except Exception as yaml_error:
                print(f"Error loading from YAML: {yaml_error}")
                ui_classes = create_default_ui_classes()
                print("Using default UI classes")
        
        # Convert to CVAT-compatible format
        return convert_to_cvat_format(ui_classes)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return create_default_ui_classes()

def convert_to_cvat_format(classes):
    """
    Convert UI classes to CVAT-compatible format.
    
    CVAT expects a format like:
    [
        {"name": "class_name", "color": "#hex_color", "type": "rectangle", "attributes": []},
        ...
    ]
    """
    cvat_classes = []
    colors = [
        "#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff", "#00ffff", 
        "#ff8000", "#8000ff", "#00ff80", "#ff0080", "#80ff00", "#0080ff",
        "#800000", "#008000", "#000080", "#808000", "#800080", "#008080",
        "#ff8080", "#80ff80", "#8080ff", "#c00000", "#00c000", "#0000c0"
    ]
    
    # Check if classes are already in CVAT format
    if isinstance(classes, list) and all(isinstance(cls, dict) and "name" in cls and "color" in cls and "type" in cls for cls in classes):
        # Ensure all required fields are present
        for cls in classes:
            if "attributes" not in cls:
                cls["attributes"] = []
        return classes
    
    # If it's a list of strings (class names)
    if isinstance(classes, list) and all(isinstance(cls, str) for cls in classes):
        for i, class_name in enumerate(classes):
            color_idx = i % len(colors)
            cvat_classes.append({
                "name": class_name,
                "color": colors[color_idx],
                "type": "rectangle",
                "attributes": []
            })
    # If it's a dictionary with id -> name mapping
    elif isinstance(classes, dict):
        for i, (class_id, class_name) in enumerate(classes.items()):
            if isinstance(class_name, str):
                color_idx = i % len(colors)
                cvat_classes.append({
                    "name": class_name,
                    "color": colors[color_idx],
                    "type": "rectangle",
                    "attributes": []
                })
            elif isinstance(class_name, dict) and "name" in class_name:
                # Handle more complex formats
                cvat_class = {
                    "name": class_name["name"],
                    "color": class_name.get("color", colors[i % len(colors)]),
                    "type": class_name.get("type", "rectangle"),
                    "attributes": class_name.get("attributes", [])
                }
                cvat_classes.append(cvat_class)
    
    return cvat_classes

def load_ui_classes_from_yaml():
    """
    Load UI classes from the ark_ui_data.yaml file.
    Returns a list of UI element dictionaries.
    """
    yaml_paths = [
        os.path.join(parent_dir, 'config', 'ark_ui_data.yaml'),
        os.path.join(current_dir, 'config', 'ark_ui_data.yaml'),
        os.path.join(parent_dir, 'ark_ui_data.yaml')
    ]
    
    for yaml_path in yaml_paths:
        if os.path.exists(yaml_path):
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)
                # Extract class information from YAML
                if 'names' in data:
                    # Convert the names list to our UI class format
                    ui_classes = []
                    for i, name in enumerate(data['names']):
                        ui_classes.append({
                            "name": name,
                            "color": f"#{i:06x}",  # Generate a color based on index
                            "type": "rectangle",
                            "attributes": []
                        })
                    return ui_classes
    
    raise FileNotFoundError("Could not find ark_ui_data.yaml")

def create_default_ui_classes():
    """Create default UI classes if all else fails."""
    print("WARNING: Using default UI classes. This might not match your project's requirements.")
    return [
        {"name": "hud_healthbar", "color": "#c80000", "type": "rectangle", "attributes": []},
        {"name": "hud_healthbar_full", "color": "#f004ac8", "type": "rectangle", "attributes": []},
        {"name": "hud_healthbar_medium", "color": "#94c800", "type": "rectangle", "attributes": []},
        {"name": "inventory_slot", "color": "#0000c8", "type": "rectangle", "attributes": []},
        {"name": "inventory_item", "color": "#00c800", "type": "rectangle", "attributes": []},
        {"name": "craft_button", "color": "#c8c800", "type": "rectangle", "attributes": []},
        {"name": "close_button", "color": "#c80076", "type": "rectangle", "attributes": []}
    ]

def extract_classes_from_file(file_path, class_collection=None):
    """
    Extract UI classes directly from the file by parsing it.
    This is a last resort if module importing fails.
    
    Args:
        file_path: Path to the ark_ui_classes.py file
        class_collection: Which class collection to extract ('ark', 'common', 'all', or None for auto-detect)
    """
    try:
        print(f"Attempting to extract classes from {file_path} by parsing...")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        collections = {}
        
        # Extract ARK_UI_CLASSES
        if "ARK_UI_CLASSES = [" in content:
            start_index = content.find("ARK_UI_CLASSES = [")
            if start_index != -1:
                # Find the matching closing bracket
                open_brackets = 0
                closing_index = -1
                for i in range(start_index + 16, len(content)):
                    if content[i] == '[':
                        open_brackets += 1
                    elif content[i] == ']':
                        if open_brackets == 0:
                            closing_index = i
                            break
                        open_brackets -= 1
                
                if closing_index != -1:
                    classes_str = content[start_index+16:closing_index+1]
                    try:
                        # Try to parse as JSON
                        import re
                        json_str = re.sub(r"'([^']*)':", r'"\1":', classes_str)
                        json_str = json_str.replace("'", '"')
                        collections['ark'] = json.loads(json_str)
                        print(f"Successfully extracted {len(collections['ark'])} classes from ARK_UI_CLASSES")
                    except json.JSONDecodeError:
                        # Simple string parsing for class names
                        classes = []
                        name_matches = re.findall(r"['\"]name['\"]: ['\"]([^'\"]+)['\"]", classes_str)
                        colors = ["#c80000", "#00c800", "#0000c8", "#c8c800", "#c800c8", "#00c8c8"]
                        for i, name in enumerate(name_matches):
                            classes.append({
                                "name": name,
                                "color": colors[i % len(colors)],
                                "type": "rectangle",
                                "attributes": []
                            })
                        collections['ark'] = classes
                        print(f"Successfully extracted {len(collections['ark'])} classes from ARK_UI_CLASSES via pattern matching")
        
        # Extract COMMON_ITEMS
        if "COMMON_ITEMS = [" in content:
            start_index = content.find("COMMON_ITEMS = [")
            if start_index != -1:
                # Find the matching closing bracket
                open_brackets = 0
                closing_index = -1
                for i in range(start_index + 15, len(content)):
                    if content[i] == '[':
                        open_brackets += 1
                    elif content[i] == ']':
                        if open_brackets == 0:
                            closing_index = i
                            break
                        open_brackets -= 1
                
                if closing_index != -1:
                    classes_str = content[start_index+15:closing_index+1]
                    try:
                        # Try to parse as JSON
                        import re
                        json_str = re.sub(r"'([^']*)':", r'"\1":', classes_str)
                        json_str = json_str.replace("'", '"')
                        collections['common'] = json.loads(json_str)
                        print(f"Successfully extracted {len(collections['common'])} classes from COMMON_ITEMS")
                    except json.JSONDecodeError:
                        # Simple string parsing for class names
                        classes = []
                        name_matches = re.findall(r"['\"]name['\"]: ['\"]([^'\"]+)['\"]", classes_str)
                        colors = ["#c80000", "#00c800", "#0000c8", "#c8c800", "#c800c8", "#00c8c8"]
                        for i, name in enumerate(name_matches):
                            classes.append({
                                "name": name,
                                "color": colors[i % len(colors)],
                                "type": "rectangle",
                                "attributes": []
                            })
                        collections['common'] = classes
                        print(f"Successfully extracted {len(collections['common'])} classes from COMMON_ITEMS via pattern matching")
        
        # If we couldn't find either collection specifically, use regex to extract any class definitions
        if not collections:
            import re
            class_regex = r'{\s*["\']name["\']: ["\'](.*?)["\'],["\']color["\']: ["\'](.*?)["\']'
            matches = re.findall(class_regex, content)
            if matches:
                classes = []
                for name, color in matches:
                    classes.append({
                        "name": name,
                        "color": color,
                        "type": "rectangle",
                        "attributes": []
                    })
                collections['all'] = classes
                print(f"Successfully extracted {len(collections['all'])} classes using regex pattern matching")
        
        # If we still couldn't find anything, look for any string that might be a class name
        if not collections:
            potential_classes = re.findall(r'["\'](hud_[^"\']*)["\']', content)
            potential_classes.extend(re.findall(r'["\'](inventory_[^"\']*)["\']', content))
            potential_classes.extend(re.findall(r'["\'](button_[^"\']*)["\']', content))
            potential_classes.extend(re.findall(r'["\'](status_[^"\']*)["\']', content))
            
            if potential_classes:
                # Remove duplicates
                potential_classes = list(set(potential_classes))
                classes = []
                colors = ["#c80000", "#00c800", "#0000c8", "#c8c800", "#c800c8", "#00c8c8"]
                for i, name in enumerate(potential_classes):
                    classes.append({
                        "name": name,
                        "color": colors[i % len(colors)],
                        "type": "rectangle",
                        "attributes": []
                    })
                collections['names'] = classes
                print(f"Successfully extracted {len(collections['names'])} classes from potential class names")
        
        # Return the requested collection, or choose the best available one
        if class_collection == 'ark' and 'ark' in collections:
            return collections['ark']
        elif class_collection == 'common' and 'common' in collections:
            return collections['common']
        elif class_collection == 'all' and ('ark' in collections or 'common' in collections):
            # Combine ARK_UI_CLASSES and COMMON_ITEMS
            combined = []
            if 'ark' in collections:
                combined.extend(collections['ark'])
            if 'common' in collections:
                combined.extend(collections['common'])
            print(f"Returning combined collection with {len(combined)} classes")
            return combined
        elif 'ark' in collections:
            return collections['ark']
        elif 'all' in collections:
            return collections['all']
        elif 'common' in collections:
            return collections['common']
        elif 'names' in collections:
            return collections['names']
        
        # If we still couldn't find anything, return default classes
        return create_default_ui_classes()
    except Exception as e:
        print(f"Error extracting classes from file: {e}")
        return create_default_ui_classes()

def export_to_cvat_format(ui_classes, output_path):
    """
    Export UI classes to CVAT-compatible format.
    """
    cvat_classes = convert_to_cvat_format(ui_classes)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    # Write to file
    with open(output_path, 'w') as f:
        json.dump(cvat_classes, f, indent=2)
    
    print(f"Exported {len(cvat_classes)} classes in CVAT format to {output_path}")
    return cvat_classes

def group_ui_classes_by_state(ui_classes):
    """
    Group UI classes into logical states for screenshot collection.
    Returns a dictionary mapping state names to lists of UI elements.
    """
    # Create UI state groups based on element names
    states = {}
    
    # Create prefixes map to group elements based on their names
    prefix_to_state = {
        'hud_': 'hud',
        'health': 'status_bars',
        'stamina': 'status_bars',
        'food': 'status_bars',
        'water': 'status_bars',
        'inventory': 'inventory',
        'craft': 'crafting',
        'map': 'map',
        'button': 'controls',
        'slot': 'inventory',
        'item': 'inventory',
        'tab': 'tabs',
        'menu': 'menus',
        'taming': 'taming',
        'creature': 'creatures',
        'dino': 'creatures',
        'weapon': 'combat',
        'ammo': 'combat',
        'armor': 'equipment',
        'tool': 'equipment',
        'resource': 'resources',
        'structure': 'building',
        'tribe': 'tribe',
        'chat': 'communication',
        'notification': 'communication',
        'close': 'controls',
    }
    
    # Initialize state groups
    for state in set(prefix_to_state.values()):
        states[state] = []
    
    # Add a 'misc' state for elements that don't match any known prefix
    states['misc'] = []
    
    # Assign UI elements to states based on their names
    for elem in ui_classes:
        assigned = False
        element_name = elem['name'].lower()
        
        for prefix, state in prefix_to_state.items():
            if prefix in element_name:
                states[state].append(elem)
                assigned = True
                break
        
        # If not assigned to any state, put it in 'misc'
        if not assigned:
            states['misc'].append(elem)
    
    # Remove empty states
    states = {k: v for k, v in states.items() if v}
    
    return states

def take_screenshot(output_dir, state_name, counter):
    """Take a screenshot and save it to the specified directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{state_name}_{timestamp}_{counter:04d}.png"
    filepath = os.path.join(output_dir, filename)
    
    with mss.mss() as sct:
        monitor = sct.monitors[0]  # Capture the main monitor
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        cv2.imwrite(filepath, img)
    
    print(f"Screenshot saved: {filepath}")
    return filepath

def create_state_subfolders(base_dir, states):
    """Create subfolders for each UI state."""
    for state_name in states.keys():
        state_dir = os.path.join(base_dir, state_name)
        os.makedirs(state_dir, exist_ok=True)
    return {state: os.path.join(base_dir, state) for state in states.keys()}

def get_state_instructions(state_name):
    """Get specific instructions for capturing each UI state."""
    instructions = {
        'hud': [
            "Ensure your HUD is visible (press Backspace if hidden)",
            "Stand in different environments for variety",
            "Try different lighting conditions"
        ],
        'status_bars': [
            "Capture with different health/stamina/food/water levels",
            "Try running to deplete stamina",
            "Try taking damage to show health bar changes",
            "Try eating/drinking to show food/water changes"
        ],
        'inventory': [
            "Open your inventory (press 'I')",
            "Move items around for different inventory states",
            "Include empty and filled slots",
            "Try different sorting options"
        ],
        'crafting': [
            "Open the crafting menu",
            "Navigate through different crafting categories",
            "Select items that can be crafted",
            "Show crafting in progress if possible"
        ],
        'map': [
            "Open the map (press 'M')",
            "Zoom in/out and pan around",
            "Place markers if possible",
            "Try different map modes if available"
        ],
        'controls': [
            "Show UI with buttons visible",
            "Hover over buttons to show any highlight effects",
            "Click buttons to show pressed states"
        ],
        'equipment': [
            "Open inventory to show equipped items",
            "Show armor/equipment slots with and without items"
        ],
        'tabs': [
            "Capture UI showing different tabs",
            "Show both selected and unselected tab states"
        ],
        'creatures': [
            "Stand near tameable creatures",
            "Show taming UI elements",
            "Capture mounted creature UI"
        ],
        'combat': [
            "Hold weapons to show weapon UI",
            "Show targeting UI if applicable",
            "Capture during combat scenarios"
        ],
        'tribe': [
            "Show tribe menu if applicable",
            "Capture tribe member UI elements"
        ],
        'communication': [
            "Open chat window",
            "Show notifications when they appear"
        ],
        'resources': [
            "Show resource gathering UI elements",
            "Capture resource count displays"
        ],
        'building': [
            "Enter building mode",
            "Show structure placement UI"
        ],
        'menus': [
            "Capture various game menus",
            "Show settings, options, etc."
        ],
        'misc': [
            "Capture any UI elements not covered by other categories",
            "Try to get clear shots of each element"
        ]
    }
    
    # Return default instructions if state not found
    return instructions.get(state_name, [
        f"Capture UI showing {state_name} elements",
        "Try to get clear shots of all UI elements in this category"
    ])

def interactive_sequence_mode(output_dir, states, interval=2, limit=None, hotkey='f10'):
    """
    Guide the user through capturing screenshots for each UI state.
    
    Args:
        output_dir: Base output directory
        states: Dictionary mapping state names to UI elements
        interval: Time between screenshots in seconds
        limit: Maximum number of screenshots per state
        hotkey: Key to press to stop capturing
    """
    state_dirs = create_state_subfolders(output_dir, states)
    
    print("\n=== ARK UI Screenshot Collection Sequence ===")
    print(f"Press '{hotkey}' at any time to stop capturing.")
    print("Screenshots will be organized in subfolders for CVAT annotation.\n")
    
    for state_name, elements in states.items():
        element_names = [elem['name'] for elem in elements]
        print(f"\n=== Capturing {state_name.upper()} UI state ===")
        print(f"UI elements to focus on: {', '.join(element_names)}")
        print(f"Instructions for {state_name}:")
        
        # Get specific instructions for this state
        instructions = get_state_instructions(state_name)
        for instruction in instructions:
            print(f"  - {instruction}")
        
        print(f"\nReady to capture {state_name} screenshots? Press Enter to begin...")
        input()
        
        counter = 0
        try:
            while limit is None or counter < limit:
                if keyboard.is_pressed(hotkey):
                    print(f"Hotkey '{hotkey}' pressed. Stopping capture of {state_name}.")
                    break
                
                screenshot_path = take_screenshot(state_dirs[state_name], state_name, counter)
                counter += 1
                
                print(f"Waiting {interval} seconds for next screenshot... (Press '{hotkey}' to stop)")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("Interrupted by user. Moving to next UI state...")
        
        print(f"Captured {counter} screenshots for {state_name}.")
        
        if state_name != list(states.keys())[-1]:
            print("\nPrepare for next UI state or press Ctrl+C to exit...")
            try:
                time.sleep(2)
            except KeyboardInterrupt:
                print("Exiting sequence mode.")
                break
    
    print("\n=== Screenshot collection complete! ===")
    print(f"Captured screenshots are organized in {output_dir}")
    print("You can now use these for annotation in CVAT.")

def main():
    parser = argparse.ArgumentParser(description="ARK UI Screenshot Collector")
    parser.add_argument('--output', '-o', type=str, default='dataset/raw',
                      help='Directory to save screenshots (default: "dataset/raw")')
    parser.add_argument('--interval', '-i', type=float, default=2,
                      help='Time in seconds between screenshots (default: 2)')
    parser.add_argument('--limit', '-l', type=int, default=None,
                      help='Maximum number of screenshots per UI state (default: none)')
    parser.add_argument('--hotkey', type=str, default='f10',
                      help='Key to press to stop the collector (default: "f10")')
    parser.add_argument('--state', '-s', type=str, default=None,
                      help='UI state tag to add to filenames (e.g., "inventory", "map")')
    parser.add_argument('--sequence', action='store_true',
                      help='Guide through capturing a sequence of important UI states')
    parser.add_argument('--save-classes', action='store_true',
                      help='Save the loaded UI classes to converted_ui_classes.json')
    parser.add_argument('--cvat-export', type=str, default='converted_ui_classes.json',
                      help='Export UI classes in CVAT-compatible format (default: "converted_ui_classes.json")')
    parser.add_argument('--class-collection', type=str, choices=['ark', 'common', 'all'], default=None,
                      help='Which class collection to use: ARK_UI_CLASSES, COMMON_ITEMS, or both (default: auto-detect)')
    parser.add_argument('--list-collections', action='store_true',
                      help='List available class collections in the ark_ui_classes.py file')
    
    args = parser.parse_args()
    
    # List collections if requested
    if args.list_collections:
        module_path = None
        for path in [
            os.path.join(parent_dir, 'utils', 'ark_ui_classes.py'),
            os.path.join(parent_dir, 'ark_ui_classes.py'),
            os.path.join(current_dir, 'utils', 'ark_ui_classes.py'),
            os.path.join(current_dir, 'ark_ui_classes.py')
        ]:
            if os.path.exists(path):
                module_path = path
                break
        
        if module_path:
            print(f"Found ark_ui_classes.py at {module_path}")
            with open(module_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            collections = []
            if "ARK_UI_CLASSES = [" in content:
                collections.append('ark')
            if "COMMON_ITEMS = [" in content:
                collections.append('common')
            if "ALL_ARK_UI_CLASSES = " in content:
                collections.append('all')
            
            if collections:
                print("Available class collections:")
                for collection in collections:
                    print(f"  - {collection}")
                print("\nUse --class-collection to specify which collection to use")
            else:
                print("No specific class collections found in the file")
            
            return
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Load UI classes from ark_ui_classes.py with specified collection
    ui_classes = load_ui_classes_from_module(args.class_collection)
    
    # Print info about loaded UI classes
    print(f"Loaded {len(ui_classes)} UI element classes")
    
    # Export to CVAT format
    if args.save_classes or args.cvat_export:
        cvat_classes = export_to_cvat_format(ui_classes, args.cvat_export)
        print(f"Exported CVAT-compatible class definitions to {args.cvat_export}")
        print("These can be imported directly into CVAT when creating a new annotation project.")
    
    if args.sequence:
        # Group UI classes by state
        ui_states = group_ui_classes_by_state(ui_classes)
        print(f"Organized UI elements into {len(ui_states)} states for screenshot collection")
        
        # Run interactive sequence mode
        interactive_sequence_mode(args.output, ui_states, args.interval, args.limit, args.hotkey)
    else:
        # Single state mode
        state_name = args.state or "general"
        state_dir = os.path.join(args.output, state_name)
        os.makedirs(state_dir, exist_ok=True)
        
        print(f"Press any key to start capturing {state_name} screenshots...")
        keyboard.read_event()
        
        counter = 0
        print(f"Starting screenshot capture. Press '{args.hotkey}' to stop...")
        try:
            while args.limit is None or counter < args.limit:
                if keyboard.is_pressed(args.hotkey):
                    print(f"Hotkey '{args.hotkey}' pressed. Stopping capture.")
                    break
                
                take_screenshot(state_dir, state_name, counter)
                counter += 1
                
                print(f"Waiting {args.interval} seconds for next screenshot...")
                time.sleep(args.interval)
                
        except KeyboardInterrupt:
            print("Interrupted by user.")
        
        print(f"Captured {counter} screenshots in {state_dir}.")

if __name__ == "__main__":
    main()