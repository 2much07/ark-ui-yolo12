#!/usr/bin/env python
"""
ARK UI Manual Screenshot Collector

A keyboard-driven tool for MANUALLY collecting and categorizing screenshots of 
ARK: Survival Ascended UI elements. Gives you complete control over the process
with clear visual feedback.

Key Features:
- Navigate categories with F1/F2
- Take screenshots with F5 
- Quick screenshot with F4
- Captures ONLY the game window
- Creates CVAT-compatible exports
- Visual guidance and feedback

Controls:
- F1: Previous category
- F2: Next category
- F3: Previous class within category
- F4: Quick screenshot to 'misc' folder
- F5: Take screenshot of current selected class
- F6: Toggle focus mode
- F7: Export to CVAT format
- F8: Set game window region
- ESC: Exit

Author: Claude & You
"""

import os
import sys
import time
import json
import yaml
import argparse
import keyboard
import mss
import numpy as np
import cv2
import threading
import importlib.util
import signal
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageGrab
import tkinter as tk
from tkinter import simpledialog, messagebox

# Add parent directory to path to allow importing ark_ui_classes.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Define ARK-specific categories
ARK_CATEGORIES = {
    "hud": {
        "name": "HUD Elements",
        "description": "Main gameplay HUD elements (health, stamina, etc.)",
        "keywords": ["hud_", "status_", "quickbar_", "crosshair", "compass"]
    },
    "inventory": {
        "name": "Inventory Interface",
        "description": "Player and container inventory elements",
        "keywords": ["inventory_", "player_", "item_", "slot"]
    },
    "crafting": {
        "name": "Crafting & Engrams",
        "description": "Crafting interfaces and engram elements",
        "keywords": ["craft", "engram", "blueprint", "recipe"]
    },
    "creature": {
        "name": "Creature & Taming",
        "description": "Dinosaur and creature related UI",
        "keywords": ["creature", "dino", "taming", "breeding"]
    },
    "map": {
        "name": "Map & Navigation",
        "description": "Map interface and navigation elements",
        "keywords": ["map_", "gps", "coordinate", "beacon", "obelisk"]
    },
    "structures": {
        "name": "Building & Structures",
        "description": "Building interface and structure elements",
        "keywords": ["structure", "building", "foundation", "wall"]
    },
    "tribe": {
        "name": "Tribe Management",
        "description": "Tribe and multiplayer interface elements",
        "keywords": ["tribe_", "alliance", "member", "permission"]
    },
    "boss": {
        "name": "Boss Fights & Events",
        "description": "Boss fight and special event UI elements",
        "keywords": ["boss_", "arena", "tribute", "artifact"]
    },
    "special": {
        "name": "Special UI Elements",
        "description": "Specialized or unique UI elements",
        "keywords": ["tek_", "genesis", "aberration", "scorched"]
    },
    "buttons": {
        "name": "Buttons & Controls",
        "description": "Interactive controls and buttons",
        "keywords": ["button", "_active", "_inactive", "_pressed"]
    },
    "misc": {
        "name": "Miscellaneous UI",
        "description": "Other UI elements that don't fit elsewhere",
        "keywords": []
    }
}

# Global variables
CURRENT_CATEGORY = 0
CURRENT_CLASS = 0
RUNNING = True
FOCUS_MODE = False
CATEGORIES = list(ARK_CATEGORIES.keys())
ALL_CLASSES = []
CATEGORY_CLASSES = {}
GAME_REGION = None
CONFIG_FILE = "ark_collector_config.json"
STATUS_MESSAGE = ""
CVAT_EXPORT_PATH = "converted_ui_classes.json"
DISPLAY_INFO = None
SCREENSHOT_COUNT = {}

# Main display thread
def display_overlay():
    """Display an overlay with current category and class information"""
    global CURRENT_CATEGORY, CURRENT_CLASS, RUNNING, FOCUS_MODE
    global CATEGORIES, ALL_CLASSES, CATEGORY_CLASSES, STATUS_MESSAGE
    
    # Create a transparent overlay window
    root = tk.Tk()
    root.title("ARK UI Collector")
    
    # Position and size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    overlay_width = 400
    overlay_height = 200
    overlay_x = 20
    overlay_y = 60
    
    # Set window properties
    root.geometry(f"{overlay_width}x{overlay_height}+{overlay_x}+{overlay_y}")
    root.attributes("-topmost", True)
    root.configure(bg='black')
    root.attributes("-alpha", 0.8)
    root.overrideredirect(True)  # Remove window decorations
    
    # Create display labels
    title_label = tk.Label(root, text="ARK UI Screenshot Collector", 
                           font=("Arial", 14, "bold"), fg="white", bg="black")
    title_label.pack(pady=(10, 5))
    
    category_label = tk.Label(root, text="", font=("Arial", 12), fg="yellow", bg="black")
    category_label.pack(pady=(0, 5))
    
    class_label = tk.Label(root, text="", font=("Arial", 12), fg="cyan", bg="black")
    class_label.pack(pady=(0, 5))
    
    count_label = tk.Label(root, text="", font=("Arial", 10), fg="green", bg="black")
    count_label.pack(pady=(0, 5))
    
    status_label = tk.Label(root, text="", font=("Arial", 10), fg="orange", bg="black")
    status_label.pack(pady=(5, 0))
    
    help_label = tk.Label(root, text="F1/F2: Change Category | F3/F4: Change Class | F5: Capture | ESC: Exit", 
                         font=("Arial", 8), fg="gray", bg="black")
    help_label.pack(pady=(10, 0))
    
    # Function to update display
    def update_display():
        if not RUNNING:
            root.destroy()
            return
        
        if FOCUS_MODE:
            root.attributes("-alpha", 0.2)
        else:
            root.attributes("-alpha", 0.8)
        
        # Get current category and class info
        if CATEGORIES and CURRENT_CATEGORY < len(CATEGORIES):
            category_key = CATEGORIES[CURRENT_CATEGORY]
            category_name = ARK_CATEGORIES[category_key]["name"]
            category_label.config(text=f"Category: {category_name} ({CURRENT_CATEGORY+1}/{len(CATEGORIES)})")
            
            if category_key in CATEGORY_CLASSES and CATEGORY_CLASSES[category_key]:
                class_list = CATEGORY_CLASSES[category_key]
                if CURRENT_CLASS < len(class_list):
                    class_name = class_list[CURRENT_CLASS]
                    class_label.config(text=f"Class: {class_name} ({CURRENT_CLASS+1}/{len(class_list)})")
                    
                    # Show count of screenshots for this class
                    class_key = f"{category_key}/{class_name}"
                    count = SCREENSHOT_COUNT.get(class_key, 0)
                    count_label.config(text=f"Screenshots: {count}")
                else:
                    class_label.config(text="No classes in this category")
                    count_label.config(text="")
            else:
                class_label.config(text="No classes in this category")
                count_label.config(text="")
        else:
            category_label.config(text="No categories available")
            class_label.config(text="")
            count_label.config(text="")
        
        status_label.config(text=STATUS_MESSAGE)
        root.after(100, update_display)
    
    # Start update loop
    update_display()
    
    try:
        root.mainloop()
    except:
        pass

def extract_list_from_content(content, start_marker, end_marker):
    """Extract a Python list from file content between markers"""
    if start_marker not in content:
        return None
    
    start_idx = content.find(start_marker) + len(start_marker)
    
    # Simplified method to extract items from Python list
    in_quote = False
    quote_char = None
    items = []
    current_item = ''
    
    code_section = content[start_idx:].strip()
    
    # First check if this is a simple assignment (ALL_ARK_UI_CLASSES = ARK_UI_CLASSES + COMMON_ITEMS)
    if code_section.startswith('ARK_UI_CLASSES + COMMON_ITEMS'):
        return None  # We'll handle this case separately by combining the lists
    
    # Process multi-line list format with items on separate lines
    reading = False
    for line in code_section.split('\n'):
        line = line.strip()
        
        # Skip comments and empty lines
        if line.startswith('#') or not line:
            continue
        
        # Handle list ending
        if line == ']' and not reading:
            break
        
        # Extract item string
        if "'" in line or '"' in line:
            # Extract the part between quotes
            reading = True
            if "'" in line:
                parts = line.split("'")
                if len(parts) >= 3:  # 'item', or 'item',  # comment
                    item = parts[1].strip()
                    items.append(item)
            elif '"' in line:
                parts = line.split('"')
                if len(parts) >= 3:  # "item", or "item",  # comment
                    item = parts[1].strip()
                    items.append(item)
    
    return items

def load_ui_classes(class_collection=None):
    """
    Load UI classes from ark_ui_classes.py module or yaml file.
    
    Args:
        class_collection: Which collection to use ('ark', 'common', 'all' or None for auto-detect)
    
    Returns:
        list: List of UI class names
    """
    global STATUS_MESSAGE
    STATUS_MESSAGE = "Loading UI classes..."
    
    # Try multiple methods to get the classes
    classes = None
    
    # Method 1: Try direct module import
    try:
        if class_collection == 'common':
            from utils.ark_ui_classes import COMMON_ITEMS
            classes = COMMON_ITEMS
            print(f"Successfully loaded {len(classes)} classes from COMMON_ITEMS")
        elif class_collection == 'all':
            from utils.ark_ui_classes import ALL_ARK_UI_CLASSES
            classes = ALL_ARK_UI_CLASSES
            print(f"Successfully loaded {len(classes)} classes from ALL_ARK_UI_CLASSES")
        else:  # Default to ARK_UI_CLASSES
            from utils.ark_ui_classes import ARK_UI_CLASSES
            classes = ARK_UI_CLASSES
            print(f"Successfully loaded {len(classes)} classes from ARK_UI_CLASSES")
    except Exception as e:
        print(f"Direct import failed: {e}")
    
    # Method 2: Look for the file and extract manually if direct import failed
    if classes is None:
        module_paths = [
            os.path.join(parent_dir, 'utils', 'ark_ui_classes.py'),
            os.path.join(parent_dir, 'ark_ui_classes.py'),
            os.path.join(current_dir, '..', 'utils', 'ark_ui_classes.py')
        ]
        
        for module_path in module_paths:
            if os.path.exists(module_path):
                print(f"Found module at {module_path}")
                
                # Read the file content
                with open(module_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract the appropriate class collection
                if class_collection == 'common' and 'COMMON_ITEMS = [' in content:
                    start_marker = 'COMMON_ITEMS = ['
                    end_marker = ']'
                    print("Extracting COMMON_ITEMS list")
                    classes = extract_list_from_content(content, start_marker, end_marker)
                    if classes:
                        print(f"Extracted {len(classes)} classes from COMMON_ITEMS")
                
                elif class_collection == 'all' and 'ALL_ARK_UI_CLASSES = ' in content:
                    # Try to extract ALL_ARK_UI_CLASSES directly
                    if 'ALL_ARK_UI_CLASSES = [' in content:
                        start_marker = 'ALL_ARK_UI_CLASSES = ['
                        end_marker = ']'
                        print("Extracting ALL_ARK_UI_CLASSES list")
                        classes = extract_list_from_content(content, start_marker, end_marker)
                    
                    # If that doesn't work or the list is empty, try to combine ARK_UI_CLASSES and COMMON_ITEMS
                    if not classes and 'ARK_UI_CLASSES = [' in content and 'COMMON_ITEMS = [' in content:
                        print("Extracting and combining ARK_UI_CLASSES and COMMON_ITEMS")
                        ark_classes = extract_list_from_content(content, 'ARK_UI_CLASSES = [', ']')
                        common_classes = extract_list_from_content(content, 'COMMON_ITEMS = [', ']')
                        
                        if ark_classes and common_classes:
                            classes = ark_classes + common_classes
                            print(f"Combined {len(ark_classes)} ARK classes with {len(common_classes)} common classes")
                
                # Default to ARK_UI_CLASSES
                if not classes and 'ARK_UI_CLASSES = [' in content:
                    start_marker = 'ARK_UI_CLASSES = ['
                    end_marker = ']'
                    print("Extracting ARK_UI_CLASSES list")
                    classes = extract_list_from_content(content, start_marker, end_marker)
                    if classes:
                        print(f"Extracted {len(classes)} classes from ARK_UI_CLASSES")
                
                if classes:
                    break
    
    # Method 3: Try to load from YAML if available
    if classes is None:
        yaml_paths = [
            os.path.join(parent_dir, 'config', 'ark_ui_data.yaml'),
            os.path.join(current_dir, 'config', 'ark_ui_data.yaml'),
            os.path.join(parent_dir, 'ark_ui_data.yaml')
        ]
        
        for yaml_path in yaml_paths:
            if os.path.exists(yaml_path):
                with open(yaml_path, 'r') as f:
                    data = yaml.safe_load(f)
                
                if 'names' in data:
                    # Could be a list or a dict
                    if isinstance(data['names'], list):
                        classes = data['names']
                    elif isinstance(data['names'], dict):
                        classes = list(data['names'].values())
                    
                    print(f"Loaded {len(classes)} classes from {yaml_path}")
                    break
    
    # Method 4: Create default classes as a last resort
    if classes is None:
        print("No classes found, creating default set")
        # Basic default set for ARK UI
        classes = [
            "hud_healthbar", "hud_staminabar", "hud_foodbar", "hud_waterbar", "hud_oxygenbar",
            "hud_weightbar", "hud_xp_bar", "hud_compass", "hud_crosshair", "inventory_slot",
            "inventory_item", "craft_button", "engram_icon", "map_player_marker", "dino_health_bar"
        ]
    
    # Ensure class names are strings (not nested lists/dicts)
    if isinstance(classes, list):
        classes = [c for c in classes if isinstance(c, str)]
    
    STATUS_MESSAGE = f"Loaded {len(classes)} UI classes"
    return classes

def categorize_ui_classes(ui_classes):
    """
    Categorize UI classes into ARK-specific categories.
    
    Args:
        ui_classes: List of UI class names
    
    Returns:
        dict: Categories with their UI classes
    """
    global STATUS_MESSAGE
    STATUS_MESSAGE = "Categorizing UI classes..."
    
    category_classes = {}
    
    # Initialize categories
    for cat_key in ARK_CATEGORIES.keys():
        category_classes[cat_key] = []
    
    # Categorize each class
    for ui_class in ui_classes:
        assigned = False
        
        # Try to find matching category
        for cat_key, cat_info in ARK_CATEGORIES.items():
            for keyword in cat_info["keywords"]:
                if keyword in ui_class.lower():
                    category_classes[cat_key].append(ui_class)
                    assigned = True
                    break
            if assigned:
                break
        
        # If not assigned, put in misc
        if not assigned:
            category_classes["misc"].append(ui_class)
    
    # Remove empty categories
    category_classes = {k: v for k, v in category_classes.items() if v}
    
    # Log the categorization
    for cat_key, classes in category_classes.items():
        print(f"Category {ARK_CATEGORIES[cat_key]['name']}: {len(classes)} elements")
    
    STATUS_MESSAGE = "UI classes categorized"
    return category_classes

def export_to_cvat_format(ui_classes, output_path):
    """
    Export UI classes to CVAT-compatible format.
    
    Args:
        ui_classes: List of UI class names
        output_path: Output file path
    
    Returns:
        list: CVAT-formatted class definitions
    """
    global STATUS_MESSAGE
    STATUS_MESSAGE = f"Exporting to CVAT format: {output_path}"
    
    # Generate colors based on class name hash to ensure consistency
    def generate_color(class_name):
        import hashlib
        hash_value = int(hashlib.md5(class_name.encode()).hexdigest(), 16) % 0xFFFFFF
        return f"#{hash_value:06x}"
    
    # Create CVAT format
    cvat_classes = []
    for i, class_name in enumerate(ui_classes):
        color = generate_color(class_name)
        cvat_classes.append({
            "name": class_name,
            "color": color,
            "type": "rectangle",
            "attributes": []
        })
    
    # Write to file
    os.makedirs(os.path.dirname(os.path.abspath(output_path)) if os.path.dirname(output_path) else '.', exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(cvat_classes, f, indent=2)
    
    print(f"Exported {len(cvat_classes)} classes to {output_path}")
    STATUS_MESSAGE = f"Exported {len(cvat_classes)} classes to CVAT format"
    return cvat_classes

def create_category_folders(base_dir, category_classes):
    """
    Create folders for each category.
    
    Args:
        base_dir: Base output directory
        category_classes: Dict of categories with their classes
    """
    global STATUS_MESSAGE
    STATUS_MESSAGE = "Creating category folders..."
    
    for cat_key, classes in category_classes.items():
        # Create a main category folder
        cat_dir = os.path.join(base_dir, cat_key)
        os.makedirs(cat_dir, exist_ok=True)
        
        # Create folder for each class within this category
        for class_name in classes:
            # Clean class_name to be a valid folder name
            safe_class_name = class_name.replace('/', '_').replace('\\', '_')
            class_dir = os.path.join(cat_dir, safe_class_name)
            os.makedirs(class_dir, exist_ok=True)
    
    STATUS_MESSAGE = "Category folders created"

def get_screenshot_counts(base_dir, category_classes):
    """
    Count existing screenshots for each class.
    
    Args:
        base_dir: Base output directory
        category_classes: Dict of categories with their classes
    
    Returns:
        dict: Counts of screenshots for each class
    """
    counts = {}
    
    for cat_key, classes in category_classes.items():
        for class_name in classes:
            # Clean class_name to be a valid folder name
            safe_class_name = class_name.replace('/', '_').replace('\\', '_')
            class_dir = os.path.join(base_dir, cat_key, safe_class_name)
            
            # Count PNG, JPG and JPEG files
            count = 0
            if os.path.exists(class_dir):
                for file in os.listdir(class_dir):
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        count += 1
            
            counts[f"{cat_key}/{class_name}"] = count
    
    return counts

def save_screenshot(img, category, class_name, base_dir):
    """
    Save screenshot to the appropriate folder.
    
    Args:
        img: Screenshot image
        category: Category key
        class_name: Class name
        base_dir: Base output directory
    
    Returns:
        str: Path to saved screenshot
    """
    global SCREENSHOT_COUNT
    
    # Clean class_name to be a valid folder name
    safe_class_name = class_name.replace('/', '_').replace('\\', '_')
    class_dir = os.path.join(base_dir, category, safe_class_name)
    os.makedirs(class_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    count = SCREENSHOT_COUNT.get(f"{category}/{class_name}", 0)
    filename = f"{safe_class_name}_{timestamp}_{count+1:04d}.png"
    filepath = os.path.join(class_dir, filename)
    
    # Save the image
    cv2.imwrite(filepath, img)
    
    # Update count
    SCREENSHOT_COUNT[f"{category}/{class_name}"] = count + 1
    
    return filepath

def set_game_region():
    """
    Let user select the game window region.
    
    Returns:
        tuple: (x, y, width, height) region
    """
    global GAME_REGION, STATUS_MESSAGE
    
    # Create instruction window
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Set Game Region", 
                       "You'll now select the game window region.\n\n"
                       "1. Resize this dialog and move it aside\n"
                       "2. Switch to your ARK game window\n"
                       "3. Press F8 when ready to select region\n"
                       "4. Click and drag to select the game area")
    
    STATUS_MESSAGE = "Press F8 to select game window region..."
    
    # Wait for F8 key
    while True:
        if keyboard.is_pressed('f8'):
            break
        time.sleep(0.1)
        if not RUNNING:
            return None
    
    # Let user select region
    try:
        import pyautogui
        STATUS_MESSAGE = "Click and drag to select game region..."
        region = pyautogui.screenshot()
        
        # Convert to OpenCV format for processing
        region = np.array(region)
        region = cv2.cvtColor(region, cv2.COLOR_RGB2BGR)
        
        # Now let's have the user select a region on this screenshot
        selection = cv2.selectROI("Select Game Region", region, False, False)
        cv2.destroyAllWindows()
        
        if selection[2] > 0 and selection[3] > 0:
            GAME_REGION = selection
            
            # Save configuration
            config = {'game_region': list(GAME_REGION)}
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f)
            
            STATUS_MESSAGE = f"Game region set to {GAME_REGION}"
            return GAME_REGION
        else:
            STATUS_MESSAGE = "Game region selection cancelled"
            return None
    
    except Exception as e:
        print(f"Error setting game region: {e}")
        STATUS_MESSAGE = f"Error setting game region: {e}"
        return None

def capture_game_screenshot():
    """
    Capture screenshot of just the game window.
    
    Returns:
        numpy.ndarray: Screenshot image
    """
    global GAME_REGION
    
    if GAME_REGION is None:
        # If no region is set, capture full screen and let the user know
        with mss.mss() as sct:
            monitor = sct.monitors[0]  # Capture the main monitor
            sct_img = sct.grab(monitor)
            img = np.array(sct_img)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            STATUS_MESSAGE = "Warning: Captured full screen (no game region set)"
    else:
        # Capture just the defined game region
        x, y, width, height = GAME_REGION
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": width, "height": height}
            sct_img = sct.grab(monitor)
            img = np.array(sct_img)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    
    return img

def load_config():
    """Load configuration from file"""
    global GAME_REGION, CVAT_EXPORT_PATH
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
            
            if 'game_region' in config:
                GAME_REGION = tuple(config['game_region'])
                print(f"Loaded game region: {GAME_REGION}")
            
            if 'cvat_export_path' in config:
                CVAT_EXPORT_PATH = config['cvat_export_path']
                print(f"Loaded CVAT export path: {CVAT_EXPORT_PATH}")
            
            return True
        except Exception as e:
            print(f"Error loading config: {e}")
            return False
    
    return False

def save_config():
    """Save configuration to file"""
    global GAME_REGION, CVAT_EXPORT_PATH
    
    config = {
        'game_region': list(GAME_REGION) if GAME_REGION else None,
        'cvat_export_path': CVAT_EXPORT_PATH
    }
    
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def find_ark_window():
    """
    Automatically find the ARK: Survival Ascended window.
    
    Returns:
        tuple: (x, y, width, height) of the ARK window or None if not found
    """
    try:
        # Try to use different window detection methods based on platform
        import platform
        
        if platform.system() == "Windows":
            # Windows-specific window detection
            import win32gui
            
            def callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    # Check for ARK window (using partial matches to catch different versions)
                    if any(title in window_title for title in ["ARK:", "ARK -", "ARK Survival", "Survival Ascended"]):
                        try:
                            rect = win32gui.GetWindowRect(hwnd)
                            x, y, x2, y2 = rect
                            width = x2 - x
                            height = y2 - y
                            
                            # Skip if too small (probably not the game window)
                            if width < 640 or height < 480:
                                return
                                
                            windows.append((hwnd, x, y, width, height, window_title))
                        except:
                            pass
                            
            windows = []
            win32gui.EnumWindows(callback, windows)
            
            # If we found ark windows, use the largest one
            if windows:
                # Sort by size (width * height), largest first
                windows.sort(key=lambda w: w[3] * w[4], reverse=True)
                hwnd, x, y, width, height, title = windows[0]
                
                print(f"Found ARK window: {title} at {x},{y} ({width}x{height})")
                STATUS_MESSAGE = f"Found ARK window: {width}x{height}"
                
                # Account for window borders by adding small offset
                # This depends on the exact window style, so it's an approximation
                return (x + 8, y + 31, width - 16, height - 39)
        
        elif platform.system() == "Linux":
            # Linux-specific window detection using xdotool
            import subprocess
            
            try:
                # Find windows with ARK in the title
                output = subprocess.check_output(["xdotool", "search", "--name", "ARK"]).decode().strip()
                window_ids = output.split("\n")
                
                for window_id in window_ids:
                    # Get window geometry
                    geometry = subprocess.check_output(["xdotool", "getwindowgeometry", window_id]).decode()
                    
                    # Parse position and size
                    position_line = [line for line in geometry.split("\n") if "Position" in line][0]
                    size_line = [line for line in geometry.split("\n") if "Geometry" in line][0]
                    
                    position = position_line.split(":")[1].strip()
                    size = size_line.split(":")[1].strip()
                    
                    x, y = map(int, position.split(","))
                    width, height = map(int, size.split("x"))
                    
                    window_title = subprocess.check_output(["xdotool", "getwindowname", window_id]).decode().strip()
                    
                    # Skip if too small (probably not the game window)
                    if width < 640 or height < 480:
                        continue
                    
                    print(f"Found ARK window: {window_title} at {x},{y} ({width}x{height})")
                    STATUS_MESSAGE = f"Found ARK window: {width}x{height}"
                    
                    # Account for window borders
                    return (x, y, width, height)
            except:
                pass
        
        # If we get here, we couldn't find the window using platform-specific methods
        # Fall back to a generic screenshot and user selection
        return None
    
    except Exception as e:
        print(f"Error finding ARK window: {e}")
        return None

def key_monitor():
    """Monitor keystrokes and handle commands"""
    global CURRENT_CATEGORY, CURRENT_CLASS, RUNNING, FOCUS_MODE, GAME_REGION
    global CATEGORIES, CATEGORY_CLASSES, STATUS_MESSAGE
    
    print("Key monitor started. Press F12 to exit.")
    print("F1/F2: Navigate categories, F3/F4: Navigate classes, F5: Take screenshot")
    
    # Try to find Ark window automatically
    if GAME_REGION is None:
        ark_region = find_ark_window()
        if ark_region:
            GAME_REGION = ark_region
            # Save configuration
            config = {'game_region': list(GAME_REGION)}
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f)
            STATUS_MESSAGE = f"ARK window detected: {GAME_REGION}"
    
    while RUNNING:
        # Category navigation
        if keyboard.is_pressed('f1'):
            CURRENT_CATEGORY = (CURRENT_CATEGORY - 1) % len(CATEGORIES)
            CURRENT_CLASS = 0
            time.sleep(0.2)  # Debounce
        
        elif keyboard.is_pressed('f2'):
            CURRENT_CATEGORY = (CURRENT_CATEGORY + 1) % len(CATEGORIES)
            CURRENT_CLASS = 0
            time.sleep(0.2)  # Debounce
        
        # Class navigation
        elif keyboard.is_pressed('f3'):
            cat_key = CATEGORIES[CURRENT_CATEGORY]
            if cat_key in CATEGORY_CLASSES and CATEGORY_CLASSES[cat_key]:
                class_list = CATEGORY_CLASSES[cat_key]
                CURRENT_CLASS = (CURRENT_CLASS - 1) % len(class_list)
            time.sleep(0.2)  # Debounce
        
        elif keyboard.is_pressed('f4'):
            cat_key = CATEGORIES[CURRENT_CATEGORY]
            if cat_key in CATEGORY_CLASSES and CATEGORY_CLASSES[cat_key]:
                class_list = CATEGORY_CLASSES[cat_key]
                CURRENT_CLASS = (CURRENT_CLASS + 1) % len(class_list)
            time.sleep(0.2)  # Debounce
        
        # Toggle focus mode
        elif keyboard.is_pressed('f6'):
            FOCUS_MODE = not FOCUS_MODE
            STATUS_MESSAGE = f"Focus mode: {'ON' if FOCUS_MODE else 'OFF'}"
            time.sleep(0.2)  # Debounce
        
        # Export to CVAT
        elif keyboard.is_pressed('f7'):
            export_to_cvat_format(ALL_CLASSES, CVAT_EXPORT_PATH)
            time.sleep(0.2)  # Debounce
        
        # Set game region
        elif keyboard.is_pressed('f8'):
            set_game_region()
            time.sleep(0.2)  # Debounce
        
        # Quick screenshot to misc category (F9)
        elif keyboard.is_pressed('f9'):
            try:
                # Capture screenshot to misc category
                img = capture_game_screenshot()
                if img is not None:
                    # Save to misc folder
                    filepath = save_screenshot(img, "misc", "misc_quick_capture", "dataset/raw")
                    STATUS_MESSAGE = f"Quick save: {os.path.basename(filepath)}"
                    print(f"Quick screenshot saved: {filepath}")
                else:
                    STATUS_MESSAGE = "Failed to capture screenshot"
            except Exception as e:
                STATUS_MESSAGE = f"Error: {str(e)}"
                print(f"Error taking screenshot: {e}")
            
            time.sleep(0.2)  # Debounce
        
        # Take screenshot for current class
        elif keyboard.is_pressed('f5'):
            try:
                # Get current category and class
                cat_key = CATEGORIES[CURRENT_CATEGORY]
                class_list = CATEGORY_CLASSES[cat_key]
                class_name = class_list[CURRENT_CLASS]
                
                # Capture screenshot
                img = capture_game_screenshot()
                if img is not None:
                    filepath = save_screenshot(img, cat_key, class_name, "dataset/raw")
                    STATUS_MESSAGE = f"Saved: {os.path.basename(filepath)}"
                    print(f"Screenshot saved: {filepath}")
                else:
                    STATUS_MESSAGE = "Failed to capture screenshot"
            except Exception as e:
                STATUS_MESSAGE = f"Error: {str(e)}"
                print(f"Error taking screenshot: {e}")
            
            time.sleep(0.2)  # Debounce
        
        # Exit program (F12 instead of ESC)
        elif keyboard.is_pressed('f12'):
            RUNNING = False
            STATUS_MESSAGE = "Exiting..."
            break
        
        time.sleep(0.05)  # Reduce CPU usage

def main():
    global CURRENT_CATEGORY, CURRENT_CLASS, RUNNING, FOCUS_MODE
    global CATEGORIES, ALL_CLASSES, CATEGORY_CLASSES, STATUS_MESSAGE
    global SCREENSHOT_COUNT, GAME_REGION
    
    parser = argparse.ArgumentParser(description="ARK UI Manual Screenshot Collector")
    
    parser.add_argument('--output', '-o', type=str, default='dataset/raw',
                      help='Directory to save screenshots (default: "dataset/raw")')
    parser.add_argument('--class-collection', type=str, choices=['ark', 'common', 'all'], default='all',
                      help='Which class collection to use (default: all)')
    parser.add_argument('--cvat-export', type=str, default='converted_ui_classes.json',
                      help='Export UI classes in CVAT-compatible format (default: "converted_ui_classes.json")')
    parser.add_argument('--auto-detect', '-a', action='store_true',
                      help='Automatically detect ARK: Survival Ascended window')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Load configuration
    load_config()
    
    # Update CVAT export path if specified
    if args.cvat_export:
        CVAT_EXPORT_PATH = args.cvat_export
    
    # Auto-detect game window if requested or if no region is set
    if args.auto_detect or GAME_REGION is None:
        STATUS_MESSAGE = "Searching for ARK: Survival Ascended window..."
        ark_region = find_ark_window()
        if ark_region:
            GAME_REGION = ark_region
            # Save configuration
            config = {'game_region': list(GAME_REGION), 'cvat_export_path': CVAT_EXPORT_PATH}
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f)
            print(f"ARK window detected: {GAME_REGION}")
        else:
            print("ARK window not found. You'll need to set it manually with F8.")
    
    # Load UI classes
    ALL_CLASSES = load_ui_classes(args.class_collection)
    
    # Categorize UI classes
    CATEGORY_CLASSES = categorize_ui_classes(ALL_CLASSES)
    
    # Set up categories list
    CATEGORIES = list(CATEGORY_CLASSES.keys())
    
    # Create category folders
    create_category_folders(args.output, CATEGORY_CLASSES)
    
    # Count existing screenshots
    SCREENSHOT_COUNT = get_screenshot_counts(args.output, CATEGORY_CLASSES)
    
    # Show help message
    print("\n=== ARK UI Manual Screenshot Collector ===")
    print("F1/F2: Navigate categories")
    print("F3/F4: Navigate UI elements within category")
    print("F5: Take screenshot of current UI element")
    print("F6: Toggle focus mode (makes overlay more transparent)")
    print("F7: Export to CVAT format")
    print("F8: Manually set game window region")
    print("F9: Quick screenshot to misc folder")
    print("F12: Exit program")
    print("\nA small overlay will show your current category and UI element.")
    print("Screenshots are automatically saved to category/class folders.")
    
    # Start display overlay thread
    display_thread = threading.Thread(target=display_overlay)
    display_thread.daemon = True
    display_thread.start()
    
    # Main key monitoring loop
    try:
        key_monitor()
    except Exception as e:
        print(f"Error in main loop: {e}")
    finally:
        RUNNING = False
        print("Exiting...")
        
        # Save configuration
        save_config()
        
        # Export to CVAT format on exit
        try:
            export_to_cvat_format(ALL_CLASSES, CVAT_EXPORT_PATH)
        except Exception as e:
            print(f"Error exporting to CVAT format: {e}")
        
        # Wait for threads to finish
        time.sleep(1)

if __name__ == "__main__":
    main()
