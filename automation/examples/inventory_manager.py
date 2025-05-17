"""
Example automation script for inventory management in ARK: Survival Ascended.
This script demonstrates how to use the ArkUIAutomation class to manage your inventory.
"""
import os
import sys
import time
import logging
import argparse

# Add parent directory to path if necessary
# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
automation_dir = os.path.dirname(script_dir)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from ark_ui_automation import ArkUIAutomation

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('inventory_manager')

def sort_inventory(ark):
    """Sort inventory items (simulation - ARK has no built-in sort)."""
    logger.info("Sorting inventory...")
    
    # In ARK, there's no built-in sort button, so we'll simulate by moving items
    # First, we need to detect all inventory slots with items
    
    # Open inventory if not already open
    if not ark.is_element_present('inventory_tab'):
        ark.open_inventory()
    
    # Find all inventory items
    items = ark.find_all_elements('inventory_item')
    logger.info(f"Found {len(items)} items in inventory")
    
    # In a real implementation, you would organize items by dragging them
    # For this example, we'll just log what we found
    for i, item in enumerate(items):
        logger.info(f"Item {i+1}: Position {item['center']}, Size {item['width']}x{item['height']}")
    
    logger.info("Inventory sorting simulation complete")
    return True

def transfer_all_to_container(ark):
    """Transfer all items to a container."""
    logger.info("Transferring all items to container...")
    
    # Open inventory if not already open
    if not ark.is_element_present('inventory_tab'):
        ark.open_inventory()
    
    # Make sure we're looking at a container
    container_check = any([
        ark.is_element_present('structure_name'),
        ark.is_element_present('storage_label')
    ])
    
    if not container_check:
        logger.warning("No container detected. Make sure you're looking at a storage container.")
        return False
    
    # Find and click the Transfer All button (right-pointing arrow)
    if ark.click_element('transfer_all'):
        logger.info("Clicked Transfer All button")
        return True
    
    # Try right arrow key as fallback
    logger.info("Transfer All button not found, trying keyboard shortcut")
    ark.press_key('right')
    
    return True

def equip_items_from_inventory(ark, item_names):
    """
    Equip specific items from inventory.
    
    Args:
        ark: ArkUIAutomation instance
        item_names: List of item class names to equip
    """
    logger.info(f"Equipping items: {', '.join(item_names)}")
    
    # Open inventory if not already open
    if not ark.is_element_present('inventory_tab'):
        ark.open_inventory()
    
    # Try to equip each item
    equipped_items = []
    for item_name in item_names:
        if ark.double_click_element(item_name):
            logger.info(f"Equipped {item_name}")
            equipped_items.append(item_name)
            time.sleep(0.5)  # Wait for equip animation
    
    logger.info(f"Equipped {len(equipped_items)}/{len(item_names)} items")
    return equipped_items

def drop_unwanted_items(ark, unwanted_items):
    """
    Drop unwanted items from inventory.
    
    Args:
        ark: ArkUIAutomation instance
        unwanted_items: List of item class names to drop
    """
    logger.info(f"Dropping unwanted items: {', '.join(unwanted_items)}")
    
    # Open inventory if not already open
    if not ark.is_element_present('inventory_tab'):
        ark.open_inventory()
    
    # Try to drop each item
    dropped_items = []
    for item_name in unwanted_items:
        # Find the item
        item = ark.find_element(item_name)
        if not item:
            logger.info(f"Item {item_name} not found")
            continue
        
        # Click to select
        ark.click_element(item_name)
        time.sleep(0.2)
        
        # Try to find drop button
        if ark.click_element('drop_item'):
            logger.info(f"Dropped {item_name} using button")
            dropped_items.append(item_name)
        else:
            # Fallback to keyboard shortcut
            ark.press_key('o')
            logger.info(f"Dropped {item_name} using keyboard shortcut")
            dropped_items.append(item_name)
        
        time.sleep(0.5)  # Wait for drop animation
    
    logger.info(f"Dropped {len(dropped_items)}/{len(unwanted_items)} items")
    return dropped_items

def quick_transfer_items(ark, source_container, target_container):
    """
    Transfer items between containers.
    
    Args:
        ark: ArkUIAutomation instance
        source_container: Source container type
        target_container: Target container type
    """
    logger.info(f"Transferring items from {source_container} to {target_container}")
    
    # This function would typically access one container, take items,
    # then access another container and deposit them.
    # For simplicity, we'll just simulate the process.
    
    logger.info("Simulating container transfer")
    time.sleep(1)
    
    return True

def main():
    parser = argparse.ArgumentParser(description="ARK Inventory Management Example")
    parser.add_argument("--weights", "-w", required=True, help="Path to trained model weights")
    parser.add_argument("--action", "-a", choices=["sort", "transfer", "equip", "drop"], 
                      default="sort", help="Action to perform")
    parser.add_argument("--confidence", "-c", type=float, default=0.4, help="Detection confidence threshold")
    
    args = parser.parse_args()
    
    # Initialize the ARK UI automation
    with ArkUIAutomation(args.weights, confidence=args.confidence) as ark:
        logger.info("ARK Inventory Manager started")
        
        # Perform the selected action
        if args.action == "sort":
            sort_inventory(ark)
        elif args.action == "transfer":
            transfer_all_to_container(ark)
        elif args.action == "equip":
            # Example items to equip - adjust these to match your model's classes
            items_to_equip = ['inventory_item_pike', 'inventory_item_sword']
            equip_items_from_inventory(ark, items_to_equip)
        elif args.action == "drop":
            # Example items to drop - adjust these to match your model's classes
            items_to_drop = ['inventory_item_stone', 'inventory_item_thatch']
            drop_unwanted_items(ark, items_to_drop)
        
        # Close inventory when done
        ark.close_inventory()
        
        logger.info("ARK Inventory Manager completed")

if __name__ == "__main__":
    main()
