from ultralytics import YOLO
import pyautogui
import numpy as np
import time
import cv2

# Load your trained model
model = YOLO("runs/ark_ui_detector_best/weights/best.pt")

def find_and_click(element_name, confidence=0.5, max_attempts=3):
    """Find and click on a UI element by name."""
    for attempt in range(max_attempts):
        # Capture screen
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        
        # Run detection
        results = model.predict(source=frame, conf=confidence)
        
        # Process results
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]
                conf = box.conf[0]
                
                if cls_name == element_name:
                    # Get coordinates
                    x1, y1, x2, y2 = box.xyxy[0].astype(int)
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    
                    # Click on element
                    pyautogui.click(center_x, center_y)
                    print(f"Clicked on {element_name} (confidence: {conf:.2f})")
                    return True
        
        print(f"Attempt {attempt+1}: {element_name} not found, retrying...")
        time.sleep(0.5)
    
    print(f"Failed to find {element_name} after {max_attempts} attempts")
    return False

# Example usage
def open_inventory():
    """Open inventory if not already open."""
    if not find_and_click("nav_tab", confidence=0.7):
        # Try pressing inventory hotkey instead
        pyautogui.press('i')
        time.sleep(0.5)

def craft_item(item_name):
    """Craft an item."""
    # Open inventory
    open_inventory()
    
    # Click on crafting tab
    if find_and_click("nav_tab", confidence=0.7):
        time.sleep(0.5)
        
        # Find and click on item to craft
        if find_and_click(item_name, confidence=0.6):
            # Find and click craft button
            return find_and_click("button", confidence=0.7)
    
    return False

# Demo: Craft a simple item
craft_item("item_spear")