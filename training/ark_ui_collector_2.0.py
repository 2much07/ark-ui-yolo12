#!/usr/bin/env python
"""
ARK UI Screenshot Collector 2.0
- Captures only the ARK: Survival Ascended game window
- Allows manual navigation through categories and UI elements
- Gives full control over when screenshots are taken
- Exports to CVAT format (manual or automatic)
"""

import os
import sys
import time
import json
import yaml
import keyboard
import argparse
import importlib.util
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

# Try to import win32gui for Windows systems
try:
    import win32gui
    import win32con
    HAS_WIN32GUI = True
except ImportError:
    HAS_WIN32GUI = False
    print("Warning: win32gui not available. Automatic window detection will be disabled.")


# Add parent directory to path to allow importing ark_ui_classes.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

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
    """Window selection tool to select just the ARK game window."""
    def __init__(self, window_name=None):
        self.rect_coords = None
        self.selection_confirmed = False
        
        # First try to find the window automatically
        if HAS_WIN32GUI:
            window_info = self.find_game_window_automatically(window_name)
            if window_info:
                # Window found automatically - no need for manual selection
                hwnd, title, class_name = window_info
                rect = win32gui.GetWindowRect(hwnd)
                self.rect_coords = rect
                self.selection_confirmed = True
                print(f"ARK window found automatically: '{title}' (Class: {class_name})")
                print(f"Window coordinates: {rect}")
                return
        
        # If automatic detection failed, use manual selection
        print("Automatic detection failed, opening manual selection interface...")
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-topmost', True)
        self.root.config(cursor="crosshair")
        
        self.canvas = tk.Canvas(self.root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.rectangle = None
        self.start_x = None
        self.start_y = None
        
        # Create label
        self.label = tk.Label(self.root, text="Click and drag to select the ARK game window\nPress ESC to cancel",
                             font=("Arial", 20), bg='black', fg='white')
        self.label.place(relx=0.5, rely=0.1, anchor='center')
        
        # Create confirm button
        self.confirm_button = tk.Button(self.root, text="Confirm Selection", 
                                     font=("Arial", 14), bg=COLORS['primary'], fg='white',
                                     command=self.confirm_selection)
        self.confirm_button.place(relx=0.5, rely=0.9, anchor='center')
        self.confirm_button.config(state=tk.DISABLED)  # Disabled until selection is made
        
        # Bind events
        self.canvas.bind('<ButtonPress-1>', self.on_button_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)
        
        # Handle escape key to cancel
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        # Handle Enter key to confirm
        self.root.bind('<Return>', self.on_enter)
        
        self.root.mainloop()
        
    def find_game_window_automatically(self, window_name=None):
        """Find the ARK game window automatically without user interaction."""
        # List of possible window names/class names to look for
        if isinstance(window_name, list):
            possible_names = window_name
        elif window_name is not None:
            possible_names = [window_name]
        else:
            # Default window names to look for
            possible_names = [
                "ARK: Survival Ascended",
                "ArkAscended.exe", 
                "ArkAscended",
                "ARK: SA",
                "ARK",
                "UnrealWindow"
            ]
        
        # Get a list of all windows
        def enum_windows_callback(hwnd, results):
            window_text = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            
            # Look for exact matches or partial matches
            for name in possible_names:
                if (name.lower() in window_text.lower() or 
                    name.lower() in class_name.lower() or
                    window_text.lower() in name.lower() or
                    class_name.lower() in name.lower()):
                    
                    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowRect(hwnd)[2] - win32gui.GetWindowRect(hwnd)[0] > 200:
                        # Window is visible and reasonably sized
                        results.append((hwnd, window_text, class_name))
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        print(f"Found {len(windows)} potential ARK windows")
        for hwnd, title, class_name in windows:
            print(f"Window: {title} (Class: {class_name})")
            
            # Return the first matching window
            return (hwnd, title, class_name)
        
        # If no window found
        return None
    
    def confirm_selection(self):
        """Confirm the selection and close the window."""
        if self.rect_coords:
            self.selection_confirmed = True
            self.root.quit()
            self.root.destroy()
    
    def on_enter(self, event=None):
        """Handle Enter key to accept selection."""
        self.confirm_selection()
    
    
    def auto_find_game_window(self, window_name=None):
        """Attempt to automatically find the ARK game window."""
        if not HAS_WIN32GUI:
            # Auto-detection not available without win32gui
            self.label.config(text="Automatic window detection not available.\nClick and drag to select the game window manually.")
            return
        
        # List of possible window names/class names to look for
        if isinstance(window_name, list):
            possible_names = window_name
        elif window_name is not None:
            possible_names = [window_name]
        else:
            # Default window names to look for
            possible_names = [
                "ARK: Survival Ascended",
                "ArkAscended.exe", 
                "ArkAscended",
                "ARK: SA",
                "ARK"
            ]
        
        # Get a list of all windows
        def enum_windows_callback(hwnd, results):
            window_text = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            
            # Look for exact matches
            for name in possible_names:
                if name.lower() in window_text.lower() or name.lower() in class_name.lower():
                    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowRect(hwnd)[2] - win32gui.GetWindowRect(hwnd)[0] > 200:
                        # Window is visible and reasonably sized
                        results.append((hwnd, window_text, class_name))
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        print(f"Found {len(windows)} potential ARK windows")
        for hwnd, title, class_name in windows:
            print(f"Window: {title} (Class: {class_name})")
            
            # Get window position and size
            rect = win32gui.GetWindowRect(hwnd)
            x1, y1, x2, y2 = rect
            
            # Try to bring window to foreground
            try:
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.5)  # Give time for window to come to foreground
            except:
                pass
            
            # Draw rectangle around found window
            if self.rectangle:
                self.canvas.delete(self.rectangle)
            
            self.rectangle = self.canvas.create_rectangle(
                x1, y1, x2, y2, 
                outline=COLORS['success'], 
                width=3
            )
            
            # Store coordinates
            self.rect_coords = (x1, y1, x2, y2)
            
            # Update label
            self.label.config(text=f"Game window found: '{title}'\nPress Enter to confirm or select manually")
            
            # Enable confirm button
            if hasattr(self, 'confirm_button'):
                self.confirm_button.config(state=tk.NORMAL)
            
            return
        
        # If no window found, show message
        self.label.config(text="ARK game window not found automatically.\nClick and drag to select it manually.")

    def on_enter(self, event):
        """Handle Enter key to accept auto-detected window."""
        self.root.quit()
        self.root.destroy()
    
    def on_button_press(self, event):
        """Handle mouse button press to start rectangle."""
        self.start_x = event.x
        self.start_y = event.y
        
        if self.rectangle:
            self.canvas.delete(self.rectangle)
            
        self.rectangle = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline=COLORS['primary'], width=3
        )
    
    def on_mouse_drag(self, event):
        """Handle mouse drag to resize rectangle."""
        if self.rectangle:
            cur_x, cur_y = event.x, event.y
            self.canvas.coords(self.rectangle, self.start_x, self.start_y, cur_x, cur_y)
            self.rect_coords = (self.start_x, self.start_y, cur_x, cur_y)
    
    def on_button_release(self, event):
        """Handle mouse button release to finalize rectangle."""
        # Make sure we have valid coordinates
        if self.start_x is not None and self.start_y is not None:
            cur_x, cur_y = event.x, event.y
            
            # Ensure we have a minimal selection area (at least 100x100 pixels)
            if abs(cur_x - self.start_x) < 100 or abs(cur_y - self.start_y) < 100:
                # Selection too small, show error
                self.label.config(text="Selection too small! Try again with a larger area.")
                # Clear the current rectangle
                if self.rectangle:
                    self.canvas.delete(self.rectangle)
                self.rectangle = None
                self.start_x = None
                self.start_y = None
                self.rect_coords = None
                return
                
            # Store coordinates before quitting
            self.rect_coords = (self.start_x, self.start_y, cur_x, cur_y)
            self.label.config(text="Selection confirmed! Press Enter to continue.")
            
            # Handle Enter key to accept the selection
            self.root.bind('<Return>', self.on_enter)
            
            # Don't close the window yet - wait for Enter key
    
    def get_coordinates(self):
        """Return the selected coordinates."""
        if self.rect_coords and hasattr(self, 'selection_confirmed') and self.selection_confirmed:
            x1, y1, x2, y2 = self.rect_coords
            # Ensure coordinates are in the right order
            left = min(x1, x2)
            top = min(y1, y2)
            right = max(x1, x2)
            bottom = max(y1, y2)
            return {"top": top, "left": left, "width": right - left, "height": bottom - top}
        return None

class ARKUICollector:
    """
    ARK UI Screenshot Collector with interactive controls.
    """
    def __init__(self, output_dir="dataset/raw", cvat_export_path="converted_ui_classes.json"):
        self.output_dir = output_dir
        self.cvat_export_path = cvat_export_path
        self.ui_classes = None
        self.class_categories = {}
        self.current_category_idx = 0
        self.current_element_idx = 0
        self.current_folder = None
        self.monitor = None
        self.screenshot_count = {}
        self.is_running = False
        self.focus_mode = False
        self.overlay_window = None
        self.last_key_time = 0
        self.key_cooldown = 0.2  # seconds
        
        # Key bindings
        self.key_bindings = {
            'select_window': 'f8',
            'prev_category': 'f1',
            'next_category': 'f2',
            'prev_element': 'f3',
            'next_element': 'f4',
            'take_screenshot': 'f5',
            'toggle_focus': 'f6',
            'export_cvat': 'f7',
            'exit': 'f10',
        }
        
        # Make sure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Setup hook for key events
        for key in self.key_bindings.values():
            keyboard.hook_key(key, self.on_key_event, suppress=True)
    
    def load_ui_classes(self, class_collection=None):
        """Load UI classes from module or file."""
        try:
            # First try to locate the module
            module_path = self.find_module_path()
            if not module_path:
                print("Error: Could not find ark_ui_classes.py")
                return False
            
            print(f"Loading UI classes from {module_path}")
            classes = self.extract_classes_from_file(module_path, class_collection)
            if not classes:
                print("Error: Could not extract UI classes from module")
                return False
            
            # Filter out problematic class names
            classes = [cls for cls in classes if cls and isinstance(cls, str) and len(cls) < 100]
            
            self.ui_classes = classes
            self.organize_classes_into_categories()
            return True
        except Exception as e:
            print(f"Error loading UI classes: {e}")
            traceback.print_exc()  # Print full traceback for debugging
            return False
    
    def find_module_path(self):
        """Find the ark_ui_classes.py module."""
        potential_paths = [
            os.path.join(parent_dir, 'utils', 'ark_ui_classes.py'),
            os.path.join(parent_dir, 'ark_ui_classes.py'),
            os.path.join(current_dir, 'utils', 'ark_ui_classes.py'),
            os.path.join(current_dir, 'ark_ui_classes.py')
        ]
        
        for path in potential_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def extract_classes_from_file(self, file_path, class_collection=None):
        """Extract UI classes from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            collections = {}
            
            # Extract ARK_UI_CLASSES
            if "ARK_UI_CLASSES = [" in content:
                ark_match = re.search(r'ARK_UI_CLASSES\s*=\s*\[(.*?)\]', content, re.DOTALL)
                if ark_match:
                    ark_content = ark_match.group(1)
                    # Extract string values using regex
                    ark_classes = re.findall(r'[\'\"]([^\'\"]+)[\'\"]', ark_content)
                    if ark_classes:
                        # Clean up the class names
                        ark_classes = [cls.strip() for cls in ark_classes if cls.strip()]
                        collections['ark'] = ark_classes
                        print(f"Found {len(ark_classes)} classes in ARK_UI_CLASSES")
            
            # Extract COMMON_ITEMS
            if "COMMON_ITEMS = [" in content:
                common_match = re.search(r'COMMON_ITEMS\s*=\s*\[(.*?)\]', content, re.DOTALL)
                if common_match:
                    common_content = common_match.group(1)
                    # Extract string values using regex
                    common_classes = re.findall(r'[\'\"]([^\'\"]+)[\'\"]', common_content)
                    if common_classes:
                        # Clean up the class names
                        common_classes = [cls.strip() for cls in common_classes if cls.strip()]
                        collections['common'] = common_classes
                        print(f"Found {len(common_classes)} classes in COMMON_ITEMS")
            
            # Determine which collection to use
            if class_collection == 'ark' and 'ark' in collections:
                result = collections['ark']
                print(f"Using {len(result)} classes from ARK_UI_CLASSES")
            elif class_collection == 'common' and 'common' in collections:
                result = collections['common']
                print(f"Using {len(result)} classes from COMMON_ITEMS")
            elif class_collection == 'all' and ('ark' in collections or 'common' in collections):
                # Combine ARK_UI_CLASSES and COMMON_ITEMS
                result = []
                if 'ark' in collections:
                    result.extend(collections['ark'])
                if 'common' in collections:
                    result.extend(collections['common'])
                # Remove duplicates
                result = list(dict.fromkeys(result))
                print(f"Using {len(result)} classes from combined collections")
            elif 'ark' in collections:
                result = collections['ark']
                print(f"Defaulting to {len(result)} classes from ARK_UI_CLASSES")
            elif 'common' in collections:
                result = collections['common']
                print(f"Defaulting to {len(result)} classes from COMMON_ITEMS")
            else:
                # Fallback: Extract all class-like strings from the file
                result = re.findall(r'[\'\"]([\w_]+)[\'\"]', content)
                result = list(set(result))  # Remove duplicates
                print(f"Extracted {len(result)} potential class names from file")
            
            return result
        except Exception as e:
            print(f"Error extracting classes from file: {e}")
            return []
    
    def organize_classes_into_categories(self):
        """Organize UI classes into logical categories for easier navigation."""
        self.class_categories = {}
        
        # Define category prefixes/keywords
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
        
        # Initialize categories with empty lists
        for category in category_mapping.keys():
            self.class_categories[category] = []
        
        # Assign classes to categories
        for ui_class in self.ui_classes:
            assigned = False
            
            # Check each category's prefixes
            for category, prefixes in category_mapping.items():
                if not assigned and any(prefix in ui_class.lower() for prefix in prefixes):
                    self.class_categories[category].append(ui_class)
                    assigned = True
                    break
            
            # If not assigned to any category, put in Miscellaneous
            if not assigned:
                self.class_categories['Miscellaneous'].append(ui_class)
        
        # Remove empty categories
        self.class_categories = {k: v for k, v in self.class_categories.items() if v}
        
        # Sort classes within categories
        for category in self.class_categories:
            self.class_categories[category].sort()
        
        # Print category stats
        print("\nUI classes organized into categories:")
        for category, classes in self.class_categories.items():
            print(f"  - {category}: {len(classes)} classes")
        
        # Initialize category indices
        self.category_names = list(self.class_categories.keys())
        if self.category_names:
            self.current_category_idx = 0
            self.current_element_idx = 0
            
            # Create folders for each UI class
            self.create_class_folders()
    
    def create_class_folders(self):
        """Create folders for each UI class."""
        # Create main output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create folders for each category and its classes
        for category, classes in self.class_categories.items():
            try:
                # Create category folder
                category_folder = os.path.join(self.output_dir, self.sanitize_folder_name(category))
                os.makedirs(category_folder, exist_ok=True)
                
                # Create class folders inside category folder
                for ui_class in classes:
                    try:
                        class_folder = os.path.join(category_folder, self.sanitize_folder_name(ui_class))
                        os.makedirs(class_folder, exist_ok=True)
                        
                        # Initialize screenshot counter for this class
                        self.screenshot_count[ui_class] = len([f for f in os.listdir(class_folder) if f.endswith(('.png', '.jpg'))])
                    except Exception as e:
                        print(f"Warning: Could not create folder for class '{ui_class}': {e}")
                        # Don't let a single class folder failure stop the whole process
                        continue
            except Exception as e:
                print(f"Warning: Could not create folder for category '{category}': {e}")
                continue
    
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
    
    def select_game_window(self):
        """Let the user select the ARK game window."""
        print("Select the ARK game window...")
        selector = GameWindowSelector(["ARK: Survival Ascended", "ArkAscended.exe", "ArkAscended"])
        self.monitor = selector.get_coordinates()
        
        if not self.monitor:
            print("Error: No game window selected")
            return False
        
        print(f"Selected game window: {self.monitor}")
        return True
    
    def create_overlay_window(self):
        """Create an overlay window to show current state."""
        self.overlay_window = tk.Tk()
        self.overlay_window.title("ARK UI Collector")
        self.overlay_window.attributes('-topmost', True)
        self.overlay_window.attributes('-alpha', 0.8)
        self.overlay_window.geometry("400x300+10+10")  # Position in top-left
        
        # Make window draggable
        self.overlay_window.bind("<ButtonPress-1>", self.start_move)
        self.overlay_window.bind("<ButtonRelease-1>", self.stop_move)
        self.overlay_window.bind("<B1-Motion>", self.on_motion)
        
        # Configure the main frame
        self.main_frame = tk.Frame(self.overlay_window, bg=COLORS['dark'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title label
        self.title_label = tk.Label(self.main_frame, text="ARK UI Collector", 
                                  font=("Arial", 16, "bold"), bg=COLORS['dark'], fg=COLORS['light'])
        self.title_label.pack(pady=(5, 10))
        
        # Current category
        self.category_frame = tk.Frame(self.main_frame, bg=COLORS['dark'])
        self.category_frame.pack(fill=tk.X, pady=5)
        
        self.category_label = tk.Label(self.category_frame, text="Category:", 
                                     font=("Arial", 12), bg=COLORS['dark'], fg=COLORS['secondary'])
        self.category_label.pack(side=tk.LEFT)
        
        self.category_value = tk.Label(self.category_frame, text="None", 
                                    font=("Arial", 12, "bold"), bg=COLORS['dark'], fg=COLORS['light'])
        self.category_value.pack(side=tk.LEFT, padx=(5, 0))
        
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
        
        # Controls frame
        self.controls_frame = tk.Frame(self.main_frame, bg=COLORS['dark'])
        self.controls_frame.pack(fill=tk.X, pady=(15, 5))
        
        self.controls_title = tk.Label(self.controls_frame, text="Controls:", 
                                     font=("Arial", 12, "bold"), bg=COLORS['dark'], fg=COLORS['secondary'])
        self.controls_title.pack(anchor=tk.W)
        
        # Controls text
        controls_text = (
            f"F1/F2: Change category\n"
            f"F3/F4: Change element\n"
            f"F5: Take screenshot\n"
            f"F6: Toggle focus mode\n"
            f"F7: Export to CVAT\n"
            f"F8: Reselect game window\n"
            f"F10: Exit"
        )
        
        self.controls_info = tk.Label(self.controls_frame, text=controls_text, 
                                    font=("Arial", 10), bg=COLORS['dark'], fg=COLORS['light'],
                                    justify=tk.LEFT)
        self.controls_info.pack(anchor=tk.W, padx=(10, 0))
        
        # Update overlay with initial values
        self.update_overlay()
    
    def start_move(self, event):
        """Start window drag."""
        self.x = event.x
        self.y = event.y
    
    def stop_move(self, event):
        """Stop window drag."""
        self.x = None
        self.y = None
    
    def on_motion(self, event):
        """Handle window drag motion."""
        if self.x is not None and self.y is not None:
            dx = event.x - self.x
            dy = event.y - self.y
            x = self.overlay_window.winfo_x() + dx
            y = self.overlay_window.winfo_y() + dy
            self.overlay_window.geometry(f"+{x}+{y}")
    
    def update_overlay(self):
        """Update overlay window with current state."""
        if not self.overlay_window:
            return
        
        if self.category_names:
            current_category = self.category_names[self.current_category_idx]
            self.category_value.config(text=current_category)
            
            if self.class_categories[current_category]:
                current_element = self.class_categories[current_category][self.current_element_idx]
                self.element_value.config(text=current_element)
                
                if current_element in self.screenshot_count:
                    self.count_value.config(text=str(self.screenshot_count[current_element]))
                else:
                    self.count_value.config(text="0")
        
        # Adjust transparency in focus mode
        if self.focus_mode:
            self.overlay_window.attributes('-alpha', 0.3)
        else:
            self.overlay_window.attributes('-alpha', 0.8)
    
    def on_key_event(self, event):
        """Handle key events."""
        # Ignore if cooldown not passed
        current_time = time.time()
        if current_time - self.last_key_time < self.key_cooldown:
            return
        self.last_key_time = current_time
        
        if not self.is_running:
            return
        
        key = event.name
        
        if key == self.key_bindings['select_window']:
            # Reselect game window
            self.select_game_window()
        
        elif key == self.key_bindings['prev_category']:
            # Previous category
            if self.category_names:
                self.current_category_idx = (self.current_category_idx - 1) % len(self.category_names)
                self.current_element_idx = 0
                self.update_overlay()
        
        elif key == self.key_bindings['next_category']:
            # Next category
            if self.category_names:
                self.current_category_idx = (self.current_category_idx + 1) % len(self.category_names)
                self.current_element_idx = 0
                self.update_overlay()
        
        elif key == self.key_bindings['prev_element']:
            # Previous element
            if self.category_names:
                current_category = self.category_names[self.current_category_idx]
                if self.class_categories[current_category]:
                    elements = self.class_categories[current_category]
                    self.current_element_idx = (self.current_element_idx - 1) % len(elements)
                    self.update_overlay()
        
        elif key == self.key_bindings['next_element']:
            # Next element
            if self.category_names:
                current_category = self.category_names[self.current_category_idx]
                if self.class_categories[current_category]:
                    elements = self.class_categories[current_category]
                    self.current_element_idx = (self.current_element_idx + 1) % len(elements)
                    self.update_overlay()
        
        elif key == self.key_bindings['take_screenshot']:
            # Take screenshot
            self.take_screenshot()
        
        elif key == self.key_bindings['toggle_focus']:
            # Toggle focus mode
            self.focus_mode = not self.focus_mode
            self.update_overlay()
        
        elif key == self.key_bindings['export_cvat']:
            # Export to CVAT
            self.export_to_cvat()
        
        elif key == self.key_bindings['exit']:
            # Exit
            self.stop()
    
    def take_screenshot(self):
        """Take a screenshot of the game window."""
        if not self.monitor:
            print("Error: No game window selected")
            return
        
        if not self.category_names:
            print("Error: No UI classes loaded")
            return
        
        # Get current category and element
        current_category = self.category_names[self.current_category_idx]
        current_element = self.class_categories[current_category][self.current_element_idx]
        
        # Create folder path
        category_folder = os.path.join(self.output_dir, self.sanitize_folder_name(current_category))
        element_folder = os.path.join(category_folder, self.sanitize_folder_name(current_element))
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
    
    def export_to_cvat(self):
        """Export UI classes to CVAT format."""
        if not self.ui_classes:
            print("Error: No UI classes loaded")
            return
        
        # Create CVAT-compatible format
        cvat_classes = []
        colors = [
            "#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff", "#00ffff", 
            "#ff8000", "#8000ff", "#00ff80", "#ff0080", "#80ff00", "#0080ff",
            "#800000", "#008000", "#000080", "#808000", "#800080", "#008080",
            "#ff8080", "#80ff80", "#8080ff", "#c00000", "#00c000", "#0000c0"
        ]
        
        for i, class_name in enumerate(self.ui_classes):
            color_idx = i % len(colors)
            cvat_classes.append({
                "name": class_name,
                "color": colors[color_idx],
                "type": "rectangle",
                "attributes": []
            })
        
        # Save to file
        with open(self.cvat_export_path, 'w') as f:
            json.dump(cvat_classes, f, indent=2)
        
        print(f"Exported {len(cvat_classes)} classes to {self.cvat_export_path}")
        
        # Show confirmation in GUI
        if self.overlay_window:
            messagebox.showinfo("Export Complete", 
                             f"Exported {len(cvat_classes)} classes to {self.cvat_export_path}")
    
    def start(self):
        """Start the screenshot collector."""
        if not self.ui_classes:
            print("Error: No UI classes loaded")
            return False
        
        if not self.select_game_window():
            return False
        
        # Create overlay window
        self.create_overlay_window()
        
        self.is_running = True
        print("ARK UI Collector started. Press F10 to exit.")
        
        # Start checking for game window focus
        self.check_window_thread = threading.Thread(target=self.check_game_window_focus)
        self.check_window_thread.daemon = True
        self.check_window_thread.start()
        
        # Update overlay regularly
        self.update_overlay()
        
        # Keep running until stopped
        try:
            self.overlay_window.mainloop()
        except KeyboardInterrupt:
            self.stop()
        
        return True
    
    def check_game_window_focus(self):
        """Periodically check if the ARK game window is still in focus."""
        while self.is_running:
            # Check if ARK window is still active
            # This is a placeholder - you'd need to implement actual window focus check
            time.sleep(1)
    
    def stop(self):
        """Stop the screenshot collector."""
        self.is_running = False
        
        # Export to CVAT if configured
        if self.cvat_export_path:
            self.export_to_cvat()
        
        # Close overlay window
        if self.overlay_window:
            self.overlay_window.destroy()
        
        print("ARK UI Collector stopped.")

def main():
    parser = argparse.ArgumentParser(description="ARK UI Screenshot Collector 2.0")
    parser.add_argument('--output', '-o', type=str, default='dataset/raw',
                      help='Directory to save screenshots (default: "dataset/raw")')
    parser.add_argument('--cvat-export', type=str, default='converted_ui_classes.json',
                      help='Export UI classes in CVAT-compatible format (default: "converted_ui_classes.json")')
    parser.add_argument('--class-collection', type=str, choices=['ark', 'common', 'all'], default='all',
                      help='Which class collection to use (default: all)')
    parser.add_argument('--list-collections', action='store_true',
                      help='List available class collections and exit')
    
    args = parser.parse_args()
    
    collector = ARKUICollector(args.output, args.cvat_export)
    
    # Load UI classes
    success = collector.load_ui_classes(args.class_collection)
    if not success:
        print("Failed to load UI classes. Exiting.")
        return
    
    # If list-collections flag is set, exit after listing
    if args.list_collections:
        return
    
    # Start collector
    collector.start()

if __name__ == "__main__":
    main()