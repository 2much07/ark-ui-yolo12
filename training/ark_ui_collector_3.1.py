#!/usr/bin/env python
"""
ARK UI Screenshot Collector 3.0
- Fully integrated with ark_ui_class_hierarchy.py
- Captures only the ARK: Survival Ascended game window
- Allows navigation through categories, subcategories, and UI elements
- Hierarchical folder structure for organized dataset
- Gives full control over when screenshots are taken
- Exports to CVAT format (manual or automatic)
"""

import os
import sys
import time
import json
from pynput import keyboard as pynput_keyboard
import argparse
import traceback
from datetime import datetime
import numpy as np
import cv2
import mss
import mss.tools
import tkinter as tk
from tkinter import messagebox
import threading
import re
from pathlib import Path

# Try to import Windows-specific modules
try:
    import win32gui
    import win32con
    import win32process
    import win32api
    import psutil
    HAS_WIN32GUI = True
except ImportError:
    HAS_WIN32GUI = False
    print("Warning: win32gui or psutil not available. Automatic window detection will be limited.")

# Add parent directory to path to allow importing ark_ui_class_hierarchy.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Try to import ark_ui_class_hierarchy.py
try:
    from ark_ui_class_hierarchy import (
        UIElement, HUDElements, InventoryElements, TabElements, 
        CraftingElements, EngramElements, DinoElements, StructureElements,
        MapElements, AlertElements, PlayerStatsElements, TribeElements,
        StructurePlacementElements, ElectricalSystemElements, TransferInterfaceElements,
        SettingsMenuElements, HolidayEventElements, TekElements, BossArenaElements,
        EventInterfaceElements, DeathScreenElements, BreedingInterfaceElements,
        PaintingInterfaceElements, CaveElements, CreatureRidingElements, LootCrateElements,
        get_ui_element_class, create_ui_element, UI_ELEMENTS
    )
    HIERARCHY_IMPORTED = True
    print("Successfully imported ark_ui_class_hierarchy.py")
except ImportError:
    print("Warning: ark_ui_class_hierarchy.py not found. Using fallback categories.")
    HIERARCHY_IMPORTED = False

# Colors for UI display
COLORS = {
    'primary': '#1E88E5',   # Blue
    'secondary': '#FFC107', # Amber
    'success': '#4CAF50',   # Green
    'warning': '#FF9800',   # Orange
    'danger': '#F44336',    # Red
    'dark': '#212121',      # Almost black
    'light': '#FAFAFA',     # Almost white
    'tooltip': '#424242',   # Dark gray
    'overlay': '#000000',   # Black (for overlay)
}

class GameWindowSelector:
    """Window selection tool to find the ARK game window."""
    def __init__(self):
        self.rect_coords = None
        self.selection_confirmed = False
        
        # Just look for ArkAscended - nothing else, no complicated code
        try:
            # Try direct window title matches in order of preference
            window_titles = ["ArkAscended", "ARK: Survival Ascended", "ShooterGame"]
            
            for title in window_titles:
                try:
                    hwnd = win32gui.FindWindow(None, title)
                    if hwnd != 0:
                        rect = win32gui.GetWindowRect(hwnd)
                        self.rect_coords = rect
                        self.selection_confirmed = True
                        print(f"ARK window found: '{title}'")
                        print(f"Window coordinates: {rect}")
                        return
                except:
                    continue
        except Exception as e:
            print(f"Error finding ARK window: {str(e)}")
        
        # Fallback to full screen if we can't find the window
        print("Could not find ARK window, using full screen")
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            self.rect_coords = (0, 0, monitor["width"], monitor["height"])
            self.selection_confirmed = True    
    

    def show_error_message(self, title, message):
        """Show an error message dialog."""
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
    
    def find_game_window_automatically(self):
        """Find the ARK game window with error handling."""
        if not HAS_WIN32GUI:
            return None
            
        try:
            # Try direct window title match first (simplest approach)
            for title in ["ARK: Survival Ascended", "ARK", "ArkAscended", "ShooterGame"]:
                try:
                    hwnd = win32gui.FindWindow(None, title)
                    if hwnd != 0 and win32gui.IsWindowVisible(hwnd):
                        # Basic check to make sure it's a reasonably sized window
                        rect = win32gui.GetWindowRect(hwnd)
                        width = rect[2] - rect[0]
                        height = rect[3] - rect[1]
                        if width > 640 and height > 480:
                            return (hwnd, title, win32gui.GetClassName(hwnd))
                except:
                    continue
                    
            # If direct match fails, try partial match
            windows = []
            
            def enum_windows_callback(hwnd, results):
                if not win32gui.IsWindowVisible(hwnd):
                    return True
                    
                try:
                    window_text = win32gui.GetWindowText(hwnd)
                    if 'ark' in window_text.lower():
                        rect = win32gui.GetWindowRect(hwnd)
                        width = rect[2] - rect[0]
                        height = rect[3] - rect[1]
                        if width > 640 and height > 480:
                            results.append((hwnd, window_text, win32gui.GetClassName(hwnd)))
                except:
                    pass
                return True
                
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                return windows[0]
                
        except Exception as e:
            print(f"Error in window detection: {str(e)}")
        
        return None
    


class ARKUICollector:
    """
    ARK UI Screenshot Collector with interactive controls.
    Fully integrated with ark_ui_class_hierarchy.py
    """
    def __init__(self, output_dir="dataset/raw", cvat_export_path="cvat_ui_classes.json"):
        self.output_dir = output_dir
        self.cvat_export_path = cvat_export_path
        
        # Hierarchy storage
        self.category_structure = {}  # Will store the full category hierarchy
        self.ui_elements = []  # All UI elements flattened
        
        # Navigation 
        self.current_category_idx = 0
        self.current_subcategory_idx = 0
        self.current_element_idx = 0
        
        # Category and element lists for navigation
        self.category_names = []
        self.subcategory_names = {}
        self.element_lists = {}
        
        # Operation state
        self.monitor = None
        self.screenshot_count = {}
        self.is_running = False
        self.focus_mode = False
        self.overlay_window = None
        self.last_key_time = 0
        self.key_cooldown = 0.2  # seconds
        
        # Key bindings
        self.key_bindings = {
            'prev_category': 'f1',
            'next_category': 'f2',
            'prev_subcategory': 'f3',
            'next_subcategory': 'f4',
            'prev_element': 'f5',
            'next_element': 'f6',
            'take_screenshot': 'f7',
            'toggle_focus': 'f8',
            'export_cvat': 'f9',
            'select_window': 'f10',
            'exit': 'f11',
            'export_yolo': 'f12',
        }
        
        # Make sure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Load hierarchy
        self.build_hierarchy_structure()

    def build_hierarchy_structure(self):
        """Build hierarchy structure from ark_ui_class_hierarchy.py"""
        if not HIERARCHY_IMPORTED:
            self.use_fallback_categories()
            return
        
        print("Building hierarchy structure from ark_ui_class_hierarchy.py...")
        
        # Extract main categories (direct subclasses of UIElement)
        for name in dir(sys.modules["ark_ui_class_hierarchy"]):
            obj = getattr(sys.modules["ark_ui_class_hierarchy"], name)
            
            # Check if it's a class and inherits from UIElement
            if isinstance(obj, type) and issubclass(obj, UIElement) and obj != UIElement:
                # Check if it's a main category class (direct child of UIElement)
                if obj.__bases__[0] == UIElement:
                    category_name = name.replace("Elements", "")
                    self.category_structure[category_name] = {
                        "class": obj,
                        "subcategories": {}
                    }
        
        # Find all subcategories for each category
        for name in dir(sys.modules["ark_ui_class_hierarchy"]):
            obj = getattr(sys.modules["ark_ui_class_hierarchy"], name)
            
            # Check if it's a class and inherits from UIElement but not a direct child
            if isinstance(obj, type) and issubclass(obj, UIElement) and obj != UIElement:
                # Skip if it's a direct child of UIElement (main category)
                if obj.__bases__[0] == UIElement:
                    continue
                    
                # Get the parent class (category)
                parent_class = obj.__bases__[0]
                parent_name = parent_class.__name__.replace("Elements", "")
                
                # Skip if parent not in our structure (shouldn't happen)
                if parent_name not in self.category_structure:
                    continue
                
                # Extract subcategory name
                subcategory_name = name
                if parent_name in subcategory_name:
                    subcategory_name = subcategory_name.replace(parent_name, "")
                
                # Initialize the subcategory
                self.category_structure[parent_name]["subcategories"][subcategory_name] = {
                    "class": obj,
                    "elements": []
                }
                
                # Find all UI elements in this subcategory class
                for attr_name in dir(obj):
                    # Skip special attributes and methods
                    if attr_name.startswith("__") or callable(getattr(obj, attr_name)):
                        continue
                    
                    # Check if it looks like an element name
                    attr_value = getattr(obj, attr_name)
                    if isinstance(attr_value, str) and '_' in attr_value:
                        self.category_structure[parent_name]["subcategories"][subcategory_name]["elements"].append(attr_value)
                        self.ui_elements.append(attr_value)
        
        # Prepare navigation references
        self.category_names = list(self.category_structure.keys())
        self.subcategory_names = {}
        
        for category in self.category_structure:
            subcats = list(self.category_structure[category]["subcategories"].keys())
            self.subcategory_names[category] = subcats
            
            self.element_lists[category] = {}
            for subcat in subcats:
                self.element_lists[category][subcat] = self.category_structure[category]["subcategories"][subcat]["elements"]
        
        # Print some statistics
        total_categories = len(self.category_names)
        total_subcategories = sum(len(subcats) for subcats in self.subcategory_names.values())
        total_elements = len(self.ui_elements)
        
        print(f"Loaded {total_categories} categories, {total_subcategories} subcategories, and {total_elements} UI elements")
        
        # Create folder structure
        self.create_folder_structure()
    
    def use_fallback_categories(self):
        """Use fallback categories when ark_ui_class_hierarchy.py is not available"""
        print("Using fallback category structure...")
        
        # Define fallback category mapping
        category_mapping = {
            'HUD Elements': ['hud_', 'status_'],
            'Player Stats': ['status_', 'player_stat_'],
            'Inventory': ['inventory_', 'player_inventory_', 'entity_inventory_'],
            'Items': ['inventory_item_', 'item_'],
            'Crafting': ['crafting_', 'craft_'],
            'Engrams': ['engram_'],
            'Structures': ['structure_'],
            'Creature UI': ['creature_', 'dino_'],
            'Map Elements': ['map_'],
            'Buttons & Controls': ['button_', '_button'],
            'Tabs & Panels': ['tab_', 'panel_', '_tab'],
            'Tooltips': ['tooltip_', '_tooltip'],
            'Tek Elements': ['tek_'],
            'Cosmetics': ['cosmetic_', 'painting_'],
            'Miscellaneous': []  # Fallback category
        }
        
        # Define some elements for each category
        fallback_elements = {
            'HUD Elements': ['hud_healthbar', 'hud_staminabar', 'hud_foodbar', 'hud_waterbar'],
            'Player Stats': ['player_stat_health', 'player_stat_stamina', 'player_stat_food'],
            'Inventory': ['inventory_slot', 'inventory_item', 'inventory_container'],
            'Items': ['item_resource', 'item_tool', 'item_weapon'],
            'Crafting': ['crafting_slot', 'crafting_button', 'crafting_progress'],
            'Engrams': ['engram_icon', 'engram_button', 'engram_list'],
            'Structures': ['structure_foundation', 'structure_wall', 'structure_door'],
            'Creature UI': ['creature_health', 'creature_stamina', 'creature_inventory'],
            'Map Elements': ['map_background', 'map_marker', 'map_button'],
            'Buttons & Controls': ['button_action', 'button_craft', 'button_close'],
            'Tabs & Panels': ['tab_inventory', 'tab_crafting', 'tab_stats'],
            'Tooltips': ['tooltip_item', 'tooltip_engram', 'tooltip_status'],
            'Tek Elements': ['tek_element', 'tek_structure', 'tek_item'],
            'Cosmetics': ['cosmetic_skin', 'cosmetic_armor', 'cosmetic_weapon'],
            'Miscellaneous': ['misc_notification', 'misc_warning', 'misc_indicator']
        }
        
        # Build simplified structure
        for category, prefixes in category_mapping.items():
            self.category_structure[category] = {
                "class": None,
                "subcategories": {
                    "Default": {
                        "class": None,
                        "elements": fallback_elements.get(category, [])
                    }
                }
            }
            
            # Add elements to the flattened list
            self.ui_elements.extend(fallback_elements.get(category, []))
        
        # Prepare navigation references
        self.category_names = list(self.category_structure.keys())
        self.subcategory_names = {}
        
        for category in self.category_structure:
            subcats = list(self.category_structure[category]["subcategories"].keys())
            self.subcategory_names[category] = subcats
            
            self.element_lists[category] = {}
            for subcat in subcats:
                self.element_lists[category][subcat] = self.category_structure[category]["subcategories"][subcat]["elements"]
        
        # Create folder structure
        self.create_folder_structure()

    def create_folder_structure(self):
        """Create hierarchical folder structure based on the category structure"""
        print("Creating folder structure...")
        
        # Create the main output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize screenshot counter
        self.screenshot_count = {}
        
        # Create folders for each category, subcategory, and element
        for category_name, category_data in self.category_structure.items():
            # Create category folder
            category_folder = os.path.join(self.output_dir, self.sanitize_folder_name(category_name))
            os.makedirs(category_folder, exist_ok=True)
            
            # Create subcategory folders
            for subcategory_name, subcategory_data in category_data["subcategories"].items():
                subcategory_folder = os.path.join(category_folder, self.sanitize_folder_name(subcategory_name))
                os.makedirs(subcategory_folder, exist_ok=True)
                
                # Create element folders
                for element_name in subcategory_data["elements"]:
                    element_folder = os.path.join(subcategory_folder, self.sanitize_folder_name(element_name))
                    os.makedirs(element_folder, exist_ok=True)
                    
                    # Count existing screenshots
                    self.screenshot_count[element_name] = len([
                        f for f in os.listdir(element_folder) 
                        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
                    ])
        
        print(f"Folder structure created in {self.output_dir}")
        
    def sanitize_folder_name(self, name):
        """Sanitize folder name to be valid on all operating systems."""
        # First, clean up any whitespace and newlines
        name = name.strip()
        
        # Replace newlines, tabs, and multiple spaces with a single space
        name = re.sub(r'\s+', ' ', name)
        
        # Replace invalid characters with underscores
        # Windows disallows: \ / : * ? " < > |
        # Some Unix systems have issues with: & $ ; ` ' ! ( ) [ ] { } ^ ~ # , %
        name = re.sub(r'[\\/*?:"<>|&$;`\'!()[\]{}^~#,%]', '_', name)
        
        # Limit length (Windows has a 255 character path limit, but folder names should be shorter)
        if len(name) > 64:
            name = name[:61] + "..."
            
        # Ensure the name is not empty
        if not name or name.isspace():
            name = "unnamed_element"
            
        # Remove any leading/trailing dots or spaces (not allowed in Windows)
        name = name.strip('. ')
        
        # Replace any remaining problematic characters to be safe
        name = ''.join(c if c.isalnum() or c in '-_ ' else '_' for c in name)
        
        return name
    
    def take_screenshot(self):
        """Take a screenshot of the game window."""
        if not self.monitor:
            print("Error: No game window selected")
            return
        
        if not self.category_names:
            print("Error: No UI elements loaded")
            return
        
        # Get current category, subcategory, and element
        current_category = self.category_names[self.current_category_idx]
        current_subcategory = self.subcategory_names[current_category][self.current_subcategory_idx]
        
        elements = self.element_lists[current_category][current_subcategory]
        if not elements:
            print(f"No elements in {current_category}/{current_subcategory}")
            return
        
        current_element = elements[self.current_element_idx]
        
        # Create folder path
        category_folder = os.path.join(self.output_dir, self.sanitize_folder_name(current_category))
        subcategory_folder = os.path.join(category_folder, self.sanitize_folder_name(current_subcategory))
        element_folder = os.path.join(subcategory_folder, self.sanitize_folder_name(current_element))
        
        # Ensure the folder exists
        os.makedirs(element_folder, exist_ok=True)
        
        # Take screenshot
        with mss.mss() as sct:
            screenshot = sct.grab(self.monitor)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            count = self.screenshot_count.get(current_element, 0)
            filename = f"{current_element}_{timestamp}_{count:04d}.png"
            filepath = os.path.join(element_folder, filename)
            
            # Save screenshot
            cv2.imwrite(filepath, img)
            
            # Update counter
            count += 1
            self.screenshot_count[current_element] = count
            self.update_overlay()
            
            print(f"Screenshot saved: {filepath}")    

    def select_game_window(self):
        """Automatically select the ARK game window."""
        print("Searching for ARK game window...")
        selector = GameWindowSelector()
        self.monitor = selector.get_coordinates()
        
        if not self.monitor:
            print("Error: No ARK game window found")
            return False
        
        print(f"Selected game window: {self.monitor}")
        return True
    
    def create_overlay_window(self):
        """Create an overlay window to show current state."""
        self.overlay_window = tk.Tk()
        self.overlay_window.title("ARK UI Collector 3.0")
        self.overlay_window.attributes('-topmost', True)
        self.overlay_window.attributes('-alpha', 0.8)
        self.overlay_window.geometry("450x400+10+10")  # Position in top-left
        
        # Configure the main frame
        self.main_frame = tk.Frame(self.overlay_window, bg=COLORS['dark'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title label
        self.title_label = tk.Label(self.main_frame, text="ARK UI Collector 3.0", 
                                  font=("Arial", 16, "bold"), bg=COLORS['dark'], fg=COLORS['light'])
        self.title_label.pack(pady=(5, 15))
        
        # Current category
        self.category_frame = tk.Frame(self.main_frame, bg=COLORS['dark'])
        self.category_frame.pack(fill=tk.X, pady=5)
        
        self.category_label = tk.Label(self.category_frame, text="Category:", 
                                     font=("Arial", 12), bg=COLORS['dark'], fg=COLORS['secondary'])
        self.category_label.pack(side=tk.LEFT)
        
        self.category_value = tk.Label(self.category_frame, text="None", 
                                    font=("Arial", 12, "bold"), bg=COLORS['dark'], fg=COLORS['light'])
        self.category_value.pack(side=tk.LEFT, padx=(5, 0))
        
        # Current subcategory
        self.subcategory_frame = tk.Frame(self.main_frame, bg=COLORS['dark'])
        self.subcategory_frame.pack(fill=tk.X, pady=5)
        
        self.subcategory_label = tk.Label(self.subcategory_frame, text="Subcategory:", 
                                        font=("Arial", 12), bg=COLORS['dark'], fg=COLORS['secondary'])
        self.subcategory_label.pack(side=tk.LEFT)
        
        self.subcategory_value = tk.Label(self.subcategory_frame, text="None", 
                                       font=("Arial", 12, "bold"), bg=COLORS['dark'], fg=COLORS['light'])
        self.subcategory_value.pack(side=tk.LEFT, padx=(5, 0))
        
        # Current element
        self.element_frame = tk.Frame(self.main_frame, bg=COLORS['dark'])
        self.element_frame.pack(fill=tk.X, pady=5)
        
        self.element_label = tk.Label(self.element_frame, text="Element:", 
                                    font=("Arial", 12), bg=COLORS['dark'], fg=COLORS['secondary'])
        self.element_label.pack(side=tk.LEFT)
        
        self.element_value = tk.Label(self.element_frame, text="None", 
                                   font=("Arial", 12, "bold"), bg=COLORS['dark'], fg=COLORS['light'])
        self.element_value.pack(side=tk.LEFT, padx=(5, 0))
        
        # Screenshot count
        self.count_frame = tk.Frame(self.main_frame, bg=COLORS['dark'])
        self.count_frame.pack(fill=tk.X, pady=5)
        
        self.count_label = tk.Label(self.count_frame, text="Screenshots:", 
                                  font=("Arial", 12), bg=COLORS['dark'], fg=COLORS['secondary'])
        self.count_label.pack(side=tk.LEFT)
        
        self.count_value = tk.Label(self.count_frame, text="0", 
                                  font=("Arial", 12, "bold"), bg=COLORS['dark'], fg=COLORS['light'])
        self.count_value.pack(side=tk.LEFT, padx=(5, 0))
        
        # Status
        self.status_frame = tk.Frame(self.main_frame, bg=COLORS['dark'])
        self.status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = tk.Label(self.status_frame, text="Status:", 
                                   font=("Arial", 12), bg=COLORS['dark'], fg=COLORS['secondary'])
        self.status_label.pack(side=tk.LEFT)
        
        self.status_value = tk.Label(self.status_frame, text="Ready", 
                                  font=("Arial", 12, "bold"), bg=COLORS['dark'], fg=COLORS['success'])
        self.status_value.pack(side=tk.LEFT, padx=(5, 0))
        
        # Controls frame
        self.controls_frame = tk.Frame(self.main_frame, bg=COLORS['dark'])
        self.controls_frame.pack(fill=tk.X, pady=(15, 5))
        
        self.controls_title = tk.Label(self.controls_frame, text="Controls:", 
                                     font=("Arial", 12, "bold"), bg=COLORS['dark'], fg=COLORS['secondary'])
        self.controls_title.pack(anchor=tk.W)
        
        # Controls text
        controls_text = (
            f"F1/F2: Change category\n"
            f"F3/F4: Change subcategory\n"
            f"F5/F6: Change element\n"
            f"F7: Take screenshot\n"
            f"F8: Toggle focus mode\n"
            f"F9: Export to CVAT\n"
            f"F10: Reselect game window\n"
            f"F12: Export to YOLO\n" 
            f"F11: Exit"
        )
        
        self.controls_info = tk.Label(self.controls_frame, text=controls_text, 
                                    font=("Arial", 10), bg=COLORS['dark'], fg=COLORS['light'],
                                    justify=tk.LEFT)
        self.controls_info.pack(anchor=tk.W, padx=(10, 0))
        
        # Update overlay with initial values
        self.update_overlay()

    def update_overlay(self):
        """Update overlay window with current state."""
        if not self.overlay_window:
            return
        
        if not self.category_names:
            return
            
        # Update category
        current_category = self.category_names[self.current_category_idx]
        self.category_value.config(text=current_category)
        
        # Update subcategory if available
        if current_category in self.subcategory_names and self.subcategory_names[current_category]:
            current_subcategory = self.subcategory_names[current_category][self.current_subcategory_idx]
            self.subcategory_value.config(text=current_subcategory)
            
            # Update element if available
            if current_subcategory in self.element_lists[current_category] and self.element_lists[current_category][current_subcategory]:
                elements = self.element_lists[current_category][current_subcategory]
                if elements:
                    current_element = elements[self.current_element_idx]
                    self.element_value.config(text=current_element)
                    
                    # Update screenshot count
                    if current_element in self.screenshot_count:
                        self.count_value.config(text=str(self.screenshot_count[current_element]))
                    else:
                        self.count_value.config(text="0")
                else:
                    self.element_value.config(text="No elements")
                    self.count_value.config(text="0")
            else:
                self.element_value.config(text="No elements")
                self.count_value.config(text="0")
        else:
            self.subcategory_value.config(text="No subcategories")
            self.element_value.config(text="No elements")
            self.count_value.config(text="0")
        
        # Adjust transparency in focus mode
        if self.focus_mode:
            self.overlay_window.attributes('-alpha', 0.3)
        else:
            self.overlay_window.attributes('-alpha', 0.8)
        
        # Update the window to ensure changes are visible
        self.overlay_window.update()
    
    def handle_key(self, key):
        """Handle a key press."""
        # Ignore if cooldown not passed
        current_time = time.time()
        if current_time - self.last_key_time < self.key_cooldown:
            return
        self.last_key_time = current_time
            
        if key == self.key_bindings['select_window']:
            # Reselect game window
            self.status_value.config(text="Selecting window...", fg=COLORS['warning'])
            self.overlay_window.update()
            self.select_game_window()
            self.status_value.config(text="Ready", fg=COLORS['success'])
        
        elif key == self.key_bindings['prev_category']:
            # Previous category
            if self.category_names:
                self.current_category_idx = (self.current_category_idx - 1) % len(self.category_names)
                self.current_subcategory_idx = 0
                self.current_element_idx = 0
                self.update_overlay()
        
        elif key == self.key_bindings['next_category']:
            # Next category
            if self.category_names:
                self.current_category_idx = (self.current_category_idx + 1) % len(self.category_names)
                self.current_subcategory_idx = 0
                self.current_element_idx = 0
                self.update_overlay()
        
        elif key == self.key_bindings['prev_subcategory']:
            # Previous subcategory
            if self.category_names:
                current_category = self.category_names[self.current_category_idx]
                if current_category in self.subcategory_names and self.subcategory_names[current_category]:
                    subcategories = self.subcategory_names[current_category]
                    self.current_subcategory_idx = (self.current_subcategory_idx - 1) % len(subcategories)
                    self.current_element_idx = 0
                    self.update_overlay()
        
        elif key == self.key_bindings['next_subcategory']:
            # Next subcategory
            if self.category_names:
                current_category = self.category_names[self.current_category_idx]
                if current_category in self.subcategory_names and self.subcategory_names[current_category]:
                    subcategories = self.subcategory_names[current_category]
                    self.current_subcategory_idx = (self.current_subcategory_idx + 1) % len(subcategories)
                    self.current_element_idx = 0
                    self.update_overlay()
        
        elif key == self.key_bindings['prev_element']:
            # Previous element
            if self.category_names:
                current_category = self.category_names[self.current_category_idx]
                if current_category in self.subcategory_names and self.subcategory_names[current_category]:
                    current_subcategory = self.subcategory_names[current_category][self.current_subcategory_idx]
                    if current_subcategory in self.element_lists[current_category]:
                        elements = self.element_lists[current_category][current_subcategory]
                        if elements:
                            self.current_element_idx = (self.current_element_idx - 1) % len(elements)
                            self.update_overlay()
        
        elif key == self.key_bindings['next_element']:
            # Next element
            if self.category_names:
                current_category = self.category_names[self.current_category_idx]
                if current_category in self.subcategory_names and self.subcategory_names[current_category]:
                    current_subcategory = self.subcategory_names[current_category][self.current_subcategory_idx]
                    if current_subcategory in self.element_lists[current_category]:
                        elements = self.element_lists[current_category][current_subcategory]
                        if elements:
                            self.current_element_idx = (self.current_element_idx + 1) % len(elements)
                            self.update_overlay()
        
        elif key == self.key_bindings['take_screenshot']:
            # Take screenshot
            self.status_value.config(text="Taking screenshot...", fg=COLORS['warning'])
            self.overlay_window.update()
            self.take_screenshot()
            self.status_value.config(text="Ready", fg=COLORS['success'])
        
        elif key == self.key_bindings['toggle_focus']:
            # Toggle focus mode
            self.focus_mode = not self.focus_mode
            self.update_overlay()
        
        elif key == self.key_bindings['export_cvat']:
            # Export to CVAT
            self.status_value.config(text="Exporting to CVAT...", fg=COLORS['warning'])
            self.overlay_window.update()
            self.export_to_cvat()
            self.status_value.config(text="Export complete", fg=COLORS['success'])
 
        elif key == self.key_bindings['export_yolo']:
            # Export to YOLO format
            self.status_value.config(text="Exporting to YOLO...", fg=COLORS['warning'])
            self.overlay_window.update()
            self.export_to_yolo_yaml()
            self.status_value.config(text="Export complete", fg=COLORS['success'])
 
        elif key == self.key_bindings['exit']:
            # Exit
            self.stop()

    def export_to_cvat(self):
        """Export UI elements to CVAT format in a single-line format."""
        if not self.ui_elements:
            print("Error: No UI elements loaded")
            return
        
        # Create CVAT-compatible format
        cvat_classes = []
        existing_names = set()  # To track duplicates
        
        if HIERARCHY_IMPORTED:
            # Extract elements with their actual colors from the hierarchy
            for element_name in self.ui_elements:
                # Skip duplicates
                if element_name in existing_names:
                    print(f"Warning: Skipping duplicate element: {element_name}")
                    continue
                    
                existing_names.add(element_name)
                
                # Try to get the element's color from the hierarchy
                element_color = "#ffffff"  # Default color
                
                try:
                    # Use the create_ui_element function to get proper color
                    element = create_ui_element(element_name)
                    if hasattr(element, 'color'):
                        element_color = element.color
                except:
                    # If error, use default color
                    pass
                
                cvat_classes.append({
                    "name": element_name,
                    "color": element_color,
                    "type": "rectangle", 
                    "attributes": []
                })
        else:
            # Fallback with standard colors
            colors = ["#c80000", "#004ac8", "#00c800", "#c8c800", "#c800c8", "#00c8c8"]
            for i, element_name in enumerate(self.ui_elements):
                # Skip duplicates
                if element_name in existing_names:
                    continue
                    
                existing_names.add(element_name)
                
                color_idx = i % len(colors)
                cvat_classes.append({
                    "name": element_name,
                    "color": colors[color_idx],
                    "type": "rectangle",
                    "attributes": []
                })
        
        # Save to file in a single line format with absolutely minimal whitespace
        with open(self.cvat_export_path, 'w') as f:
            # Use separators without any spaces for maximum compression
            json_str = json.dumps(cvat_classes, separators=(',',':'))
            f.write(json_str)
        
        print(f"Exported {len(cvat_classes)} elements to {self.cvat_export_path}")
        
        # Show confirmation in GUI
        if self.overlay_window:
            messagebox.showinfo("Export Complete", 
                             f"Exported {len(cvat_classes)} elements to {self.cvat_export_path}")
    
    
    def export_to_yolo_yaml(self, output_path='ark_ui_data.yaml'):
        """Export UI elements in YOLO training format."""
        if not self.ui_elements:
            print("Error: No UI elements loaded")
            return
        
        # Create YOLO dataset configuration
        data = {
            'path': './dataset_yolo',  # Dataset root directory
            'train': 'train/images',   # Train images relative to 'path'
            'val': 'val/images',       # Val images relative to 'path'
            'names': {}                # Class names with numeric IDs
        }
        
        # Add class names with IDs
        for i, element_name in enumerate(self.ui_elements):
            data['names'][i] = element_name
        
        # Add comments for categories
        yaml_str = "# ARK Ascended UI Detection Dataset Configuration\n"
        yaml_str += f"path: {data['path']}  # Dataset root directory\n"
        yaml_str += f"train: {data['train']}  # Train images (relative to 'path')\n"
        yaml_str += f"val: {data['val']}  # Val images (relative to 'path')\n\n"
        yaml_str += "# Class names\n"
        yaml_str += "names:\n"
        
        # Group elements by category for better organization in the YAML
        category_counts = {}
        for category in self.category_structure:
            category_counts[category] = 0
            for subcategory in self.category_structure[category]["subcategories"]:
                category_counts[category] += len(
                    self.category_structure[category]["subcategories"][subcategory]["elements"]
                )
        
        # Add element entries with category comments
        current_id = 0
        for category, count in category_counts.items():
            if count > 0:
                yaml_str += f"  # {category} ({current_id}-{current_id + count - 1})\n"
                
                # Add all elements from this category
                for subcategory in self.category_structure[category]["subcategories"]:
                    elements = self.category_structure[category]["subcategories"][subcategory]["elements"]
                    for element in elements:
                        yaml_str += f"  {current_id}: {element}  # {subcategory}\n"
                        current_id += 1
        
        # Write to file
        with open(output_path, 'w') as f:
            f.write(yaml_str)
        
        print(f"Exported YOLO configuration to {output_path}")
        
        # Show confirmation in GUI
        if self.overlay_window:
            messagebox.showinfo("Export Complete", 
                             f"Exported YOLO configuration to {output_path}")
    
    def setup_keyboard_hooks(self):
        """Setup truly global keyboard hooks using both pynput and win32 hooks."""
        print("Setting up redundant global keyboard hooks for maximum reliability...")
        
        # Method 1: pynput hooks
        # Create a mapping from key codes to our function keys
        key_mapping = {
            pynput_keyboard.Key.f1: self.key_bindings['prev_category'],
            pynput_keyboard.Key.f2: self.key_bindings['next_category'],
            pynput_keyboard.Key.f3: self.key_bindings['prev_subcategory'],
            pynput_keyboard.Key.f4: self.key_bindings['next_subcategory'],
            pynput_keyboard.Key.f5: self.key_bindings['prev_element'],
            pynput_keyboard.Key.f6: self.key_bindings['next_element'],
            pynput_keyboard.Key.f7: self.key_bindings['take_screenshot'],
            pynput_keyboard.Key.f8: self.key_bindings['toggle_focus'],
            pynput_keyboard.Key.f9: self.key_bindings['export_cvat'],
            pynput_keyboard.Key.f10: self.key_bindings['select_window'],
            pynput_keyboard.Key.f11: self.key_bindings['exit'],
            pynput_keyboard.Key.f12: self.key_bindings['export_yolo'],
        }
        
        def on_key_press(key):
            # Check if the pressed key is in our mapping
            if key in key_mapping:
                action_key = key_mapping[key]
                # Use threading to avoid blocking the keyboard listener
                threading.Thread(target=self.handle_key, args=(action_key,), daemon=True).start()
                
        # Start keyboard listener in a non-blocking thread
        self.listener = pynput_keyboard.Listener(on_press=on_key_press)
        self.listener.start()
        
        # Method 2: Direct key polling using a background thread
        # This is a backup in case the pynput hooks don't catch everything
        def key_polling_thread():
            # Map windows virtual key codes to our function keys
            vk_mapping = {
                0x70: self.key_bindings['prev_category'],    # F1
                0x71: self.key_bindings['next_category'],    # F2
                0x72: self.key_bindings['prev_subcategory'], # F3
                0x73: self.key_bindings['next_subcategory'], # F4
                0x74: self.key_bindings['prev_element'],     # F5
                0x75: self.key_bindings['next_element'],     # F6
                0x76: self.key_bindings['take_screenshot'],  # F7
                0x77: self.key_bindings['toggle_focus'],     # F8
                0x78: self.key_bindings['export_cvat'],      # F9
                0x79: self.key_bindings['select_window'],    # F10
                0x7A: self.key_bindings['exit'],             # F11
                0x7B: self.key_bindings['export_yolo'],      # F12
            }
            
            # Track the state of each key
            key_state = {vk: False for vk in vk_mapping}
            
            while self.is_running:
                for vk, action_key in vk_mapping.items():
                    # Check if key is pressed using GetAsyncKeyState
                    try:
                        if win32api.GetAsyncKeyState(vk) & 0x8000:
                            # Only trigger once per press
                            if not key_state[vk]:
                                key_state[vk] = True
                                threading.Thread(target=self.handle_key, args=(action_key,), daemon=True).start()
                        else:
                            key_state[vk] = False
                    except:
                        pass
                time.sleep(0.01)  # Small sleep to reduce CPU usage
        
        # Start the key polling thread if win32api is available
        try:
            self.polling_thread = threading.Thread(target=key_polling_thread, daemon=True)
            self.polling_thread.start()
            print("Started redundant key polling thread")
        except Exception as e:
            print(f"Could not start polling thread: {str(e)}")
            print("Using only pynput hooks")

    def start(self):
        """Start the screenshot collector."""
        if not self.category_names:
            print("Error: No UI hierarchy loaded")
            return False
        
        if not self.select_game_window():
            return False
        
        # Create overlay window
        self.create_overlay_window()
        
        # Setup global keyboard hooks
        self.is_running = True
        self.setup_keyboard_hooks()
        
        print("ARK UI Collector 3.0 started. Press F11 to exit.")
        print("Keys will work globally - no need to click on the overlay window.")
        
        # Keep running until stopped - use the TK main loop
        try:
            self.overlay_window.mainloop()
        except KeyboardInterrupt:
            self.stop()
        
        return True
    
    def stop(self):
        """Stop the screenshot collector."""
        self.is_running = False
        
        # Stop keyboard listener if exists
        if hasattr(self, 'listener') and self.listener:
            self.listener.stop()
        
        # Polling thread will stop automatically when is_running becomes False
        
        # Export to CVAT if configured
        if self.cvat_export_path:
            self.export_to_cvat()
        
        # Close overlay window
        if self.overlay_window:
            self.overlay_window.destroy()
        
        print("ARK UI Collector 3.0 stopped.")


def main():
    parser = argparse.ArgumentParser(description="ARK UI Screenshot Collector 3.0")
    parser.add_argument('--output', '-o', type=str, default='dataset/raw',
                      help='Directory to save screenshots (default: "dataset/raw")')
    parser.add_argument('--cvat-export', type=str, default='cvat_ui_classes.json',
                      help='Export UI elements in CVAT-compatible format (default: "cvat_ui_classes.json")')
    
    args = parser.parse_args()
    
    collector = ARKUICollector(args.output, args.cvat_export)
    collector.start()

if __name__ == "__main__":
    main()