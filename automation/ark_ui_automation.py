"""
ARK UI Automation System for ARK: Survival Ascended.
This class provides methods to interact with the game UI using YOLOv8 object detection.
"""
import time
import numpy as np
import cv2
import pyautogui
import mss
import mss.tools
from ultralytics import YOLO
import keyboard
import random
import logging
import os
import yaml
import sys
import threading


# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("ark_automation.log")
    ]
)
logger = logging.getLogger('ark_automation')

class ArkUIAutomation:
    def __init__(self, model_path, config_path=None, confidence=0.4):
        """
        Initialize the ARK UI automation system.
        
        Args:
            model_path: Path to trained YOLOv8 model
            config_path: Path to automation configuration file (optional)
            confidence: Default confidence threshold for detections
        """
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.screen_width, self.screen_height = pyautogui.size()
        self.last_action_time = time.time()
        self.cooldown = 0.5  # Seconds between actions
        
        # Dictionary to track UI element locations
        self.ui_memory = {}
        self.memory_timeout = 1.0  # Seconds before memory is considered stale
        self.last_detection_time = 0
        
        # Load class names
        self.class_names = self.model.names
        
        # Load configuration if provided
        self.config = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            
            # Apply configuration
            if 'confidence' in self.config:
                self.confidence = self.config['confidence']
            
            if 'cooldown' in self.config:
                self.cooldown = self.config['cooldown']
            
            if 'memory_timeout' in self.config:
                self.memory_timeout = self.config['memory_timeout']
        
        # Setup screenshot capture
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]  # Primary monitor
        
        # Detection thread
        self.detection_thread = None
        self.stop_thread = False
        self.detection_lock = threading.Lock()
        
        logger.info(f"Initialized ArkUIAutomation with model: {model_path}")
        logger.info(f"Default confidence threshold: {confidence}")
    
    def start_background_detection(self, interval=0.2):
        """Start background detection thread."""
        if self.detection_thread is not None and self.detection_thread.is_alive():
            logger.warning("Background detection is already running")
            return
        
        self.stop_thread = False
        self.detection_thread = threading.Thread(target=self._background_detection_loop, args=(interval,))
        self.detection_thread.daemon = True
        self.detection_thread.start()
        logger.info(f"Started background detection with interval {interval} seconds")
    
    def stop_background_detection(self):
        """Stop background detection thread."""
        if self.detection_thread is None or not self.detection_thread.is_alive():
            logger.warning("No background detection running")
            return
        
        self.stop_thread = True
        self.detection_thread.join(timeout=2.0)
        logger.info("Stopped background detection")
    
    def _background_detection_loop(self, interval):
        """Background detection loop."""
        while not self.stop_thread:
            with self.detection_lock:
                self.detect_ui_elements()
            time.sleep(interval)
    
    def detect_ui_elements(self, confidence=None):
        """
        Detect all UI elements in the current screen.
        
        Args:
            confidence: Confidence threshold (optional, uses default if not specified)
            
        Returns:
            Dictionary mapping class names to lists of detection results
        """
        if confidence is None:
            confidence = self.confidence
        
        # Capture screenshot
        img = self.sct.grab(self.monitor)
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGRA2RGB)
        
        # Run detection
        results = self.model.predict(source=frame, conf=confidence)
        
        # Organize results by class
        detections = {}
        
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                cls_id = int(box.cls[0])
                cls_name = self.class_names[cls_id]
                conf = box.conf[0]
                coords = box.xyxy[0].astype(int)  # [x1, y1, x2, y2]
                
                # Store detection
                if cls_name not in detections:
                    detections[cls_name] = []
                
                detections[cls_name].append({
                    'coords': coords,
                    'confidence': conf,
                    'center': ((coords[0] + coords[2]) // 2, (coords[1] + coords[3]) // 2),
                    'width': coords[2] - coords[0],
                    'height': coords[3] - coords[1],
                    'area': (coords[2] - coords[0]) * (coords[3] - coords[1])
                })
        
        # Update memory of UI elements
        with self.detection_lock:
            self.ui_memory = detections
            self.last_detection_time = time.time()
        
        return detections
    
    def find_element(self, element_name, confidence=None, update=True):
        """
        Find a specific UI element by name.
        
        Args:
            element_name: Name of the element to find
            confidence: Confidence threshold (optional)
            update: Whether to update the UI memory
            
        Returns:
            Best match detection or None if not found
        """
        current_time = time.time()
        memory_stale = current_time - self.last_detection_time > self.memory_timeout
        
        if update or memory_stale or element_name not in self.ui_memory:
            detections = self.detect_ui_elements(confidence)
        else:
            with self.detection_lock:
                detections = self.ui_memory
        
        if element_name in detections and detections[element_name]:
            # Get the highest confidence detection
            return max(detections[element_name], key=lambda x: x['confidence'])
        
        return None
    
    def find_all_elements(self, element_name, confidence=None, update=True):
        """
        Find all instances of a specific UI element.
        
        Args:
            element_name: Name of elements to find
            confidence: Confidence threshold (optional)
            update: Whether to update the UI memory
            
        Returns:
            List of detections or empty list if none found
        """
        current_time = time.time()
        memory_stale = current_time - self.last_detection_time > self.memory_timeout
        
        if update or memory_stale or element_name not in self.ui_memory:
            detections = self.detect_ui_elements(confidence)
        else:
            with self.detection_lock:
                detections = self.ui_memory
        
        if element_name in detections:
            # Sort by confidence
            return sorted(detections[element_name], key=lambda x: x['confidence'], reverse=True)
        
        return []
    
    def wait_for_element(self, element_name, timeout=10, confidence=None, check_interval=0.5):
        """
        Wait for a UI element to appear.
        
        Args:
            element_name: Name of element to wait for
            timeout: Maximum time to wait in seconds
            confidence: Confidence threshold (optional)
            check_interval: Time between checks in seconds
            
        Returns:
            Element detection if found within timeout, None otherwise
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            element = self.find_element(element_name, confidence, update=True)
            
            if element:
                logger.info(f"Element {element_name} appeared after {time.time() - start_time:.1f} seconds")
                return element
            
            time.sleep(check_interval)
        
        logger.warning(f"Timeout waiting for element: {element_name}")
        return None
    
    def is_element_present(self, element_name, confidence=None):
        """Check if a UI element is currently on screen."""
        element = self.find_element(element_name, confidence)
        return element is not None
    
    def click_element(self, element_name, confidence=None, offset_x=0, offset_y=0):
        """
        Click on a specific UI element.
        
        Args:
            element_name: Name of element to click
            confidence: Confidence threshold (optional)
            offset_x: X offset from center (optional)
            offset_y: Y offset from center (optional)
            
        Returns:
            True if element was found and clicked, False otherwise
        """
        # Respect cooldown
        current_time = time.time()
        if current_time - self.last_action_time < self.cooldown:
            time.sleep(self.cooldown - (current_time - self.last_action_time))
        
        # Find the element
        element = self.find_element(element_name, confidence)
        
        if element:
            center_x, center_y = element['center']
            
            # Apply offset
            center_x += offset_x
            center_y += offset_y
            
            # Click the element
            pyautogui.click(center_x, center_y)
            self.last_action_time = time.time()
            
            logger.info(f"Clicked on {element_name} at ({center_x}, {center_y})")
            return True
        
        logger.warning(f"Element not found: {element_name}")
        return False
    
    def double_click_element(self, element_name, confidence=None):
        """Double-click on a UI element (useful for equipping items)."""
        element = self.find_element(element_name, confidence)
        
        if element:
            center_x, center_y = element['center']
            pyautogui.doubleClick(center_x, center_y)
            self.last_action_time = time.time()
            
            logger.info(f"Double-clicked on {element_name} at ({center_x}, {center_y})")
            return True
        
        logger.warning(f"Element not found for double-click: {element_name}")
        return False
    
    def right_click_element(self, element_name, confidence=None):
        """Right-click on a UI element."""
        element = self.find_element(element_name, confidence)
        
        if element:
            center_x, center_y = element['center']
            pyautogui.rightClick(center_x, center_y)
            self.last_action_time = time.time()
            
            logger.info(f"Right-clicked on {element_name} at ({center_x}, {center_y})")
            return True
        
        logger.warning(f"Element not found for right-click: {element_name}")
        return False
    
    def drag_element(self, source_element, target_element, source_conf=None, target_conf=None):
        """
        Drag one UI element to another (for moving items).
        
        Args:
            source_element: Name of source element
            target_element: Name of target element
            source_conf: Source confidence threshold (optional)
            target_conf: Target confidence threshold (optional)
            
        Returns:
            True if drag operation was successful, False otherwise
        """
        # Find source and target
        source = self.find_element(source_element, source_conf)
        target = self.find_element(target_element, target_conf)
        
        if source and target:
            source_x, source_y = source['center']
            target_x, target_y = target['center']
            
            # Perform drag operation
            pyautogui.moveTo(source_x, source_y)
            pyautogui.mouseDown()
            time.sleep(0.2)  # Small delay for game to register
            pyautogui.moveTo(target_x, target_y, duration=0.3)  # Smooth movement
            time.sleep(0.1)
            pyautogui.mouseUp()
            
            self.last_action_time = time.time()
            
            logger.info(f"Dragged {source_element} to {target_element}")
            return True
        
        if not source:
            logger.warning(f"Source element not found: {source_element}")
        if not target:
            logger.warning(f"Target element not found: {target_element}")
        
        return False
    
    def press_key(self, key):
        """Press a keyboard key."""
        pyautogui.press(key)
        self.last_action_time = time.time()
        logger.info(f"Pressed key: {key}")
    
    def press_and_hold(self, key, duration=1.0):
        """Press and hold a key for a specific duration."""
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)
        self.last_action_time = time.time()
        logger.info(f"Held key {key} for {duration} seconds")
    
    def wait_for_animation(self, duration=1.0):
        """Wait for an in-game animation to complete."""
        time.sleep(duration)
    
    # ARK: Survival Ascended specific methods
    
    def open_inventory(self):
        """Open character inventory if not already open."""
        # Check if inventory is already open
        if self.is_element_present('inventory_tab'):
            logger.info("Inventory is already open")
            return True
        
        # Press inventory key
        self.press_key('i')
        
        # Wait for inventory to appear
        return self.wait_for_element('inventory_tab', timeout=3) is not None
    
    def close_inventory(self):
        """Close inventory if open."""
        if self.is_element_present('inventory_tab'):
            # Find and click close button
            if self.click_element('close_button'):
                return True
            
            # Fallback to ESC key
            self.press_key('esc')
            time.sleep(0.5)
            
            # Verify inventory is closed
            return not self.is_element_present('inventory_tab')
        
        return True  # Already closed
    
    def switch_to_tab(self, tab_name):
        """Switch to a specific inventory tab."""
        valid_tabs = ['inventory_tab', 'crafting_tab', 'engram_tab', 'cosmetics_tab', 'tribe_tab', 'structure_tab']
        
        if tab_name not in valid_tabs:
            logger.warning(f"Invalid tab name: {tab_name}")
            return False
        
        return self.click_element(tab_name)
    
    def transfer_all_items(self, direction='to_container'):
        """Transfer all items to or from a container."""
        # Make sure inventory is open with a container
        if not self.is_element_present('inventory_tab'):
            logger.warning("Inventory not open")
            return False
        
        if direction == 'to_container':
            # Find and click the transfer all button (arrow pointing right)
            for button in ['transfer_all', 'transfer_button']:
                if self.click_element(button):
                    return True
        else:  # from_container
            # Need to find the left-pointing transfer button
            # This might require specific training to differentiate directions
            logger.warning("Transfer from container not specifically implemented")
            return False
        
        return False
    
    def equip_item(self, item_name):
        """
        Equip a specific item from inventory.
        
        Args:
            item_name: Specific item class to equip (e.g., 'inventory_item_pike')
        """
        # Open inventory if needed
        if not self.is_element_present('inventory_tab'):
            self.open_inventory()
        
        # Double-click the item to equip it
        return self.double_click_element(item_name)
    
    def craft_item(self, item_name, engram_name=None):
        """
        Craft a specific item.
        
        Args:
            item_name: Name of the item to craft (UI element name)
            engram_name: Name of engram if not learned yet (optional)
        """
        # Open inventory
        if not self.open_inventory():
            return False
        
        # Switch to crafting tab
        if not self.switch_to_tab('crafting_tab'):
            return False
        
        # If engram is provided and item not found, try to learn it first
        if engram_name and not self.find_element(item_name):
            logger.info(f"Item {item_name} not found, trying to learn engram")
            
            # Switch to engram tab
            if not self.switch_to_tab('engram_tab'):
                return False
            
            # Find and click the engram
            if not self.click_element(engram_name):
                logger.warning(f"Engram {engram_name} not found")
                return False
            
            # Click the learn button
            if not self.click_element('learn_button'):
                logger.warning("Learn button not found")
                return False
            
            # Switch back to crafting tab
            if not self.switch_to_tab('crafting_tab'):
                return False
        
        # Find and click the item to select it
        if not self.click_element(item_name):
            logger.warning(f"Item {item_name} not found in crafting menu")
            return False
        
        # Click the craft button
        if not self.click_element('craft_button'):
            logger.warning("Craft button not found")
            return False
        
        logger.info(f"Started crafting {item_name}")
        return True
    
    def drop_item(self, item_name):
        """Drop a specific item from inventory."""
        # Open inventory if needed
        if not self.is_element_present('inventory_tab'):
            self.open_inventory()
        
        # Click on the item first to select it
        if not self.click_element(item_name):
            logger.warning(f"Item {item_name} not found")
            return False
        
        # Click the drop button or press 'O' key
        if self.click_element('drop_item'):
            logger.info(f"Dropped {item_name} using drop button")
            return True
        
        # Fallback to keyboard shortcut
        self.press_key('o')
        logger.info(f"Dropped {item_name} using keyboard shortcut")
        return True
    
    def check_player_status(self):
        """
        Check player status bars and return warnings.
        Returns dictionary with status values and warnings.
        """
        status = {
            'health': None,
            'stamina': None,
            'food': None,
            'water': None,
            'weight': None,
            'warnings': []
        }
        
        # Check for explicit warning messages
        if self.is_element_present('starvation_alert'):
            status['warnings'].append('starvation')
        
        if self.is_element_present('dehydration_alert'):
            status['warnings'].append('dehydration')
        
        if self.is_element_present('overweight_alert'):
            status['warnings'].append('overweight')
        
        # Try to detect status bars
        bars = ['health_bar', 'stamina_bar', 'food_bar', 'water_bar', 'weight_bar']
        for bar_name in bars:
            bar = self.find_element(bar_name)
            if bar:
                # In a full implementation, you would detect the fill level
                # This would require image processing or specialized detection
                bar_type = bar_name.replace('_bar', '')
                status[bar_type] = 'detected'
        
        return status
    
    def eat_food(self, food_item='inventory_item_berry'):
        """Eat food from inventory to restore food level."""
        # Open inventory if needed
        if not self.is_element_present('inventory_tab'):
            self.open_inventory()
        
        # Find and consume food item
        food_consumed = False
        
        # Try to find and click the food item
        if self.double_click_element(food_item):
            logger.info(f"Consumed {food_item}")
            food_consumed = True
        
        # Close inventory
        self.close_inventory()
        
        return food_consumed
    
    def check_level_up(self):
        """Check if level up is available and apply it."""
        # Look for level up notification
        if self.is_element_present('level_alert') or self.is_element_present('level_icon'):
            logger.info("Level up available")
            
            # Access inventory/character screen
            self.open_inventory()
            
            # Wait for and click the level up button
            if self.wait_for_element('level_button'):
                self.click_element('level_button')
                
                # You would add logic here to select which stat to increase
                # For example:
                time.sleep(1)
                self.click_element('health_stat')  # Increase health
                
                logger.info("Applied level up to health")
                return True
        
        return False
    
    def clean_up(self):
        """Clean up resources when done."""
        try:
            self.stop_background_detection()
            
            # Close any open game interfaces
            self.press_key('esc')
            
            # Release the screenshot grabber
            self.sct.close()
            
            logger.info("Successfully cleaned up resources")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
    
    def __enter__(self):
        """Support for 'with' statement."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up when exiting 'with' block."""
        self.clean_up()

# Example usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ARK UI Automation Test")
    parser.add_argument("--weights", "-w", required=True, help="Path to trained model weights")
    parser.add_argument("--confidence", "-c", type=float, default=0.4, help="Confidence threshold")
    parser.add_argument("--test", "-t", choices=["detect", "inventory", "craft"], 
                      default="detect", help="Test to run")
    
    args = parser.parse_args()
    
    # Create the automation instance
    with ArkUIAutomation(args.weights, confidence=args.confidence) as ark:
        logger.info("ARK UI Automation Test")
        
        if args.test == "detect":
            # Basic detection test
            logger.info("Running detection test")
            elements = ark.detect_ui_elements()
            for cls_name, detections in elements.items():
                logger.info(f"Detected {len(detections)} instances of {cls_name}")
        
        elif args.test == "inventory":
            # Inventory test
            logger.info("Running inventory test")
            if ark.open_inventory():
                logger.info("Inventory opened successfully")
                time.sleep(2)
                ark.close_inventory()
                logger.info("Inventory closed")
            else:
                logger.warning("Failed to open inventory")
        
        elif args.test == "craft":
            # Crafting test
            logger.info("Running crafting test")
            if ark.open_inventory():
                logger.info("Inventory opened successfully")
                if ark.switch_to_tab('crafting_tab'):
                    logger.info("Switched to crafting tab")
                    # Find and click first craftable item
                    time.sleep(1)
                    ark.close_inventory()
                else:
                    logger.warning("Failed to switch to crafting tab")
                    ark.close_inventory()
            else:
                logger.warning("Failed to open inventory")
        
        logger.info("Test completed")
