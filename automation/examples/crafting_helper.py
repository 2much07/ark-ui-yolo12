"""
Example automation script for crafting in ARK: Survival Ascended.
This script demonstrates how to use the ArkUIAutomation class to craft items.
"""
import os
import sys
import time
import logging
import argparse
import json

# Add parent directory to path if necessary
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from ark_ui_automation import ArkUIAutomation

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('crafting_helper')

# Define crafting recipes (simplified)
CRAFTING_RECIPES = {
    "stone_pick": {
        "materials": {
            "wood": 1,
            "stone": 1,
            "thatch": 10
        },
        "engram_required": True,
        "item_class": "inventory_item_stone_pick",
        "engram_class": "engram_stone_pick"
    },
    "stone_hatchet": {
        "materials": {
            "wood": 1,
            "stone": 1,
            "thatch": 10
        },
        "engram_required": True,
        "item_class": "inventory_item_stone_hatchet",
        "engram_class": "engram_stone_hatchet"
    },
    "spear": {
        "materials": {
            "wood": 5,
            "flint": 2
        },
        "engram_required": True,
        "item_class": "inventory_item_spear",
        "engram_class": "engram_spear"
    },
    "campfire": {
        "materials": {
            "wood": 2,
            "stone": 16,
            "thatch": 12
        },
        "engram_required": True,
        "item_class": "inventory_item_campfire",
        "engram_class": "engram_campfire"
    }
}

def check_materials(ark, recipe):
    """
    Check if player has materials for a recipe.
    
    Args:
        ark: ArkUIAutomation instance
        recipe: Recipe dictionary
        
    Returns:
        dict: Materials status
    """
    logger.info(f"Checking materials for {recipe}")
    
    # This would normally check inventory for materials
    # For this example, we'll just simulate it
    
    # Open inventory if not already open
    if not ark.is_element_present('inventory_tab'):
        ark.open_inventory()
    
    # In a real implementation, you would search for each material item
    # and check its stack count
    material_status = {}
    for material, required_amount in CRAFTING_RECIPES[recipe]["materials"].items():
        # Look for material in inventory (simulated)
        material_class = f"inventory_item_{material}"
        material_exists = ark.find_element(material_class)
        
        if material_exists:
            # In a real implementation, you would read the stack count
            # For now, we'll just assume enough
            material_status[material] = {
                "required": required_amount,
                "available": required_amount,  # Simulated
                "sufficient": True
            }
        else:
            material_status[material] = {
                "required": required_amount,
                "available": 0,
                "sufficient": False
            }
    
    return material_status

def learn_engram(ark, engram_name):
    """
    Learn an engram if not already learned.
    
    Args:
        ark: ArkUIAutomation instance
        engram_name: Class name of the engram
        
    Returns:
        bool: True if successful
    """
    logger.info(f"Attempting to learn engram: {engram_name}")
    
    # Open inventory
    if not ark.is_element_present('inventory_tab'):
        ark.open_inventory()
    
    # Switch to engram tab
    if not ark.switch_to_tab('engram_tab'):
        logger.warning("Failed to switch to engram tab")
        return False
    
    # Find the engram
    if not ark.find_element(engram_name):
        logger.warning(f"Engram {engram_name} not found")
        return False
    
    # Click the engram
    if not ark.click_element(engram_name):
        logger.warning(f"Failed to click engram {engram_name}")
        return False
    
    # Click the learn button
    if not ark.click_element('learn_button'):
        logger.warning("Learn button not found")
        return False
    
    logger.info(f"Successfully learned engram: {engram_name}")
    return True

def craft_single_item(ark, recipe):
    """
    Craft a single item based on its recipe.
    
    Args:
        ark: ArkUIAutomation instance
        recipe: Name of the recipe to craft
        
    Returns:
        bool: True if crafting was successful
    """
    if recipe not in CRAFTING_RECIPES:
        logger.warning(f"Unknown recipe: {recipe}")
        return False
    
    recipe_data = CRAFTING_RECIPES[recipe]
    logger.info(f"Crafting {recipe}...")
    
    # Open inventory
    if not ark.is_element_present('inventory_tab'):
        ark.open_inventory()
    
    # Check if we have the engram if required
    if recipe_data["engram_required"]:
        # Switch to crafting tab
        if not ark.switch_to_tab('crafting_tab'):
            logger.warning("Failed to switch to crafting tab")
            return False
        
        # Check if we can see the item in crafting menu
        if not ark.find_element(recipe_data["item_class"]):
            logger.info(f"Item {recipe} not found in crafting menu, trying to learn engram")
            
            # Try to learn the engram
            if not learn_engram(ark, recipe_data["engram_class"]):
                logger.warning(f"Failed to learn engram for {recipe}")
                return False
            
            # Switch back to crafting tab
            if not ark.switch_to_tab('crafting_tab'):
                logger.warning("Failed to switch back to crafting tab")
                return False
    
    # Check if we have materials
    materials = check_materials(ark, recipe)
    all_materials_available = all(status["sufficient"] for status in materials.values())
    
    if not all_materials_available:
        logger.warning(f"Insufficient materials for {recipe}")
        for material, status in materials.items():
            if not status["sufficient"]:
                logger.warning(f"  {material}: {status['available']}/{status['required']}")
        return False
    
    # Click the item in the crafting menu
    if not ark.click_element(recipe_data["item_class"]):
        logger.warning(f"Failed to find {recipe} in crafting menu")
        return False
    
    # Click the craft button
    if not ark.click_element('craft_button'):
        logger.warning("Craft button not found")
        return False
    
    logger.info(f"Successfully started crafting {recipe}")
    
    # Wait for crafting to complete
    # In a real implementation, you would wait for the crafting animation or progress bar
    time.sleep(2)
    
    return True

def craft_multiple_items(ark, recipe, quantity):
    """
    Craft multiple items of the same type.
    
    Args:
        ark: ArkUIAutomation instance
        recipe: Name of the recipe to craft
        quantity: Number of items to craft
        
    Returns:
        int: Number of items successfully crafted
    """
    logger.info(f"Crafting {quantity}x {recipe}...")
    
    # In ARK, you can craft multiple items by clicking craft button multiple times
    # or by using the slider/input to set quantity
    
    crafted = 0
    for i in range(quantity):
        if craft_single_item(ark, recipe):
            crafted += 1
        else:
            logger.warning(f"Failed to craft item {i+1}/{quantity}")
            break
    
    logger.info(f"Crafted {crafted}/{quantity} {recipe}")
    return crafted

def batch_craft_items(ark, crafting_list):
    """
    Craft multiple items from a list.
    
    Args:
        ark: ArkUIAutomation instance
        crafting_list: Dictionary mapping recipe names to quantities
        
    Returns:
        dict: Results of crafting operations
    """
    logger.info(f"Batch crafting items: {crafting_list}")
    
    results = {}
    
    # Open inventory
    if not ark.is_element_present('inventory_tab'):
        ark.open_inventory()
    
    # Switch to crafting tab
    if not ark.switch_to_tab('crafting_tab'):
        logger.warning("Failed to switch to crafting tab")
        return results
    
    # Craft each item in the list
    for recipe, quantity in crafting_list.items():
        if recipe in CRAFTING_RECIPES:
            crafted = craft_multiple_items(ark, recipe, quantity)
            results[recipe] = {
                "requested": quantity,
                "crafted": crafted,
                "success": crafted == quantity
            }
        else:
            logger.warning(f"Unknown recipe: {recipe}")
            results[recipe] = {
                "requested": quantity,
                "crafted": 0,
                "success": False,
                "error": "Unknown recipe"
            }
    
    # Close inventory when done
    ark.close_inventory()
    
    return results

def main():
    parser = argparse.ArgumentParser(description="ARK Crafting Helper Example")
    parser.add_argument("--weights", "-w", required=True, help="Path to trained model weights")
    parser.add_argument("--recipe", "-r", default="stone_pick", help="Recipe to craft")
    parser.add_argument("--quantity", "-q", type=int, default=1, help="Quantity to craft")
    parser.add_argument("--batch", "-b", action="store_true", help="Use batch crafting")
    parser.add_argument("--confidence", "-c", type=float, default=0.4, help="Detection confidence threshold")
    
    args = parser.parse_args()
    
    # Initialize the ARK UI automation
    with ArkUIAutomation(args.weights, confidence=args.confidence) as ark:
        logger.info("ARK Crafting Helper started")
        
        if args.batch:
            # Example batch crafting
            crafting_list = {
                "stone_pick": 1,
                "stone_hatchet": 1,
                "spear": 1
            }
            results = batch_craft_items(ark, crafting_list)
            logger.info(f"Batch crafting results: {json.dumps(results, indent=2)}")
        else:
            # Craft single recipe
            craft_multiple_items(ark, args.recipe, args.quantity)
        
        logger.info("ARK Crafting Helper completed")

if __name__ == "__main__":
    main()
