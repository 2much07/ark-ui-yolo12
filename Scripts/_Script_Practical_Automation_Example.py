import time
import numpy as np
import cv2
import pyautogui
from ultralytics import YOLO
import keyboard
import random
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('ark_automation')

class ArkUIAutomation:
    def __init__(self, model_path="best.pt", confidence=0.4):
        """Initialize the ARK UI automation system."""
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.screen_width, self.screen_height = pyautogui.size()
        self.last_action_time = time.time()
        self.cooldown = 0.5  # Seconds between actions
        
        # Dictionary to track UI element locations
        self.ui_memory = {}
        
        # Load class names
        self.class_names = self.model.names
        
        logger.info(f"Initialized ArkUIAutomation with model: {model_path}")
        logger.info(f"Default confidence threshold: {confidence}")
        
    def detect_ui_elements(self, confidence=None):
        """
        Detect all UI elements in the current screen.
        
        Returns:
            Dictionary mapping class names to lists of detection results
        """
        if confidence is None:
            confidence = self.confidence
            
        # Capture screenshot
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
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
                    'height': coords[3] - coords[1]
                })
        
        # Update memory of UI elements
        for cls_name, items in detections.items():
            self.ui_memory[cls_name] = items
        
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
        if update or element_name not in self.ui_memory:
            detections = self.detect_ui_elements(confidence)
        else:
            detections = self.ui_memory
        
        if element_name in detections and detections[element_name]:
            # Get the highest confidence detection
            return max(detections[element_name], key=lambda x: x['confidence'])
        
        return None
    
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
    
    def get_element_text(self, element_name, confidence=None):
        """
        Get text from a UI element (experimental, requires OCR).
        This is just a placeholder - actual OCR would need to be implemented.
        """
        element = self.find_element(element_name, confidence)
        
        if not element:
            return None
        
        # This is where OCR would be implemented
        # For ARK Ascended, you would need to crop the text area and use an OCR library
        # such as pytesseract or EasyOCR
        
        logger.warning("OCR functionality not implemented")
        return None
    
    def get_stack_count(self, item_slot):
        """
        Get the count of items in a stack (experimental).
        Would require specialized detection or OCR for the numbers.
        """
        # This would require specific training for number recognition
        # or OCR implementation
        logger.warning("Stack count detection not implemented")
        return None
    
    def wait_for_animation(self, duration=1.0):
        """Wait for an in-game animation to complete."""
        time.sleep(duration)
    
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
    
    # Higher-level ARK Ascended specific functions
    
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
        valid_tabs = ['inventory_tab', 'crafting_tab', 'engram_tab', 'cosmetics_tab']
        
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
        
        # In a full implementation, you would detect the fill level of status bars
        # This would require more sophisticated image processing
        
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
    
    def drink_water(self):
        """
        Drink water to restore water level.
        In ARK, this usually means going to water source and pressing E.
        """
        # This would typically require navigating to water
        # For this example, we'll just assume we're at water and press E
        self.press_key('e')
        logger.info("Attempted to drink water")
        return True
    
    def approach_structure(self, structure_name):
        """
        Walk towards a specific structure.
        
        This requires broader scene understanding and navigation,
        which is beyond the scope of UI detection.
        """
        logger.warning("Physical navigation not implemented")
        return False
    
    def access_container(self, container_name):
        """
        Access a storage container.
        
        Args:
            container_name: Type of container to access
        """
        # Look for container in view
        container = self.find_element(container_name)
        
        if not container:
            logger.warning(f"Container {container_name} not found in view")
            return False
        
        # Position crosshair on container (approximate)
        center_x, center_y = container['center']
        
        # Move mouse to container and press 'E'
        pyautogui.moveTo(center_x, center_y)
        time.sleep(0.2)
        self.press_key('e')
        
        # Wait for inventory UI to appear
        if self.wait_for_element('inventory_tab'):
            logger.info(f"Accessed {container_name}")
            return True
        
        return False
    
    def sort_inventory(self):
        """Sort inventory items in ARK (usually using Sort Items button)."""
        # Open inventory if needed
        if not self.is_element_present('inventory_tab'):
            self.open_inventory()
        
        # Try to find and click a sort button if it exists
        # Note: ARK may not have a standard sort button, depends on UI mods
        if self.click_element('sort_button', confidence=0.3):
            logger.info("Sorted inventory using button")
            return True
        
        logger.warning("Sort button not found")
        return False
    
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
    
    def quick_slot_item(self, item_name, slot_number):
        """
        Place an item in a specific hotbar slot.
        
        Args:
            item_name: Item to place in hotbar
            slot_number: Hotbar slot (1-0)
        """
        # Open inventory
        if not self.open_inventory():
            return False
        
        # Find the item
        item = self.find_element(item_name)
        
        if not item:
            logger.warning(f"Item {item_name} not found")
            return False
        
        # Drag to hotbar or use keyboard shortcut
        # In ARK, you can typically drag items or press a number key while item is selected
        
        # Select the item
        self.click_element(item_name)
        
        # Press the number key for the slot
        slot_key = str(slot_number)
        if slot_number == 10:
            slot_key = '0'
        
        self.press_key(slot_key)
        
        logger.info(f"Placed {item_name} in quick slot {slot_number}")
        return True
    
    def tame_creature(self, food_item='inventory_item_berry'):
        """
        Handle the taming process for a creature.
        This is a complex process in ARK and varies by creature.
        """
        # This would be a complex sequence specific to the creature type
        # For simplicity, we'll just model feeding a knocked out creature
        
        # Check if taming bar is visible (creature is being tamed)
        if not self.is_element_present('taming_bar'):
            logger.warning("No taming in progress detected")
            return False
        
        # Open inventory (assuming we're looking at the creature)
        if not self.open_inventory():
            return False
        
        # Look for food item
        if not self.find_element(food_item):
            logger.warning(f"Food {food_item} not found")
            return False
        
        # Transfer food to creature inventory
        # In ARK, this is typically dragging to right side or using transfer button
        if not self.drag_element(food_item, 'creature_inventory'):
            logger.warning("Failed to transfer food to creature")
            return False
        
        # Close inventory
        self.close_inventory()
        
        logger.info(f"Placed {food_item} in creature inventory for taming")
        return True

# Example usage script
def main():
    # Initialize the automation system
    ark = ArkUIAutomation("runs/ark_ui_detector/weights/best.pt")
    
    # Main automation loop
    try:
        logger.info("Starting ARK UI automation")
        
        # Example: Basic inventory management and crafting workflow
        
        # Step 1: Open inventory
        if ark.open_inventory():
            logger.info("Successfully opened inventory")
            
            # Step 2: Check player status
            status = ark.check_player_status()
            if 'starvation' in status['warnings']:
                logger.info("Player is starving, attempting to eat food")
                ark.eat_food()
            
            # Step 3: Switch to crafting tab
            if ark.switch_to_tab('crafting_tab'):
                logger.info("Switched to crafting tab")
                
                # Step 4: Craft a stone pick (common early game item)
                if ark.craft_item('inventory_item_stone_pick'):
                    logger.info("Crafting stone pick")
                    
                    # Wait for crafting to finish
                    ark.wait_for_animation(2.0)
                    
                    # Step 5: Equip the newly crafted item
                    if ark.equip_item('inventory_item_stone_pick'):
                        logger.info("Equipped stone pick")
                
                # Step 6: Craft more items as needed
                ark.craft_item('inventory_item_stone_hatchet')
                ark.wait_for_animation(2.0)
            
            # Step 7: Close inventory to return to game
            ark.close_inventory()
        
        # Wait a moment before performing field actions
        time.sleep(2)
        
        # Step 8: Demonstrate gathering resources
        # In a real implementation, this would involve looking around for resources
        # For this example, we'll just simulate the key presses
        
        logger.info("Simulating resource gathering")
        
        # Look around for resources (simulated)
        for _ in range(3):
            # Random movement
            direction = random.choice(['w', 'a', 's', 'd'])
            ark.press_and_hold(direction, 1.0)
            
            # Look around
            pyautogui.move(random.randint(-200, 200), random.randint(-100, 100), duration=0.5)
            
            # Attempt to gather with left click
            pyautogui.click()
            time.sleep(1)
        
        # Step 9: Check if we found a storage container
        if ark.find_element('structure_name', confidence=0.3):
            logger.info("Found a storage structure")
            
            # Approach and access it
            ark.access_container('storage_structure')
            
            # Transfer items if inventory opened
            if ark.is_element_present('inventory_tab'):
                ark.transfer_all_items('to_container')
                ark.close_inventory()
        
        # Step 10: Check for level up
        ark.check_level_up()
        
        logger.info("Automation sequence completed")
    
    except KeyboardInterrupt:
        logger.info("Automation stopped by user")
    except Exception as e:
        logger.error(f"Error in automation: {str(e)}")
    
    logger.info("Automation complete")

if __name__ == "__main__":
    main()