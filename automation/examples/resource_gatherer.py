"""
ARK Resource Gathering Example
This script demonstrates how to use the ArkUIAutomation class to assist with resource gathering in ARK: Survival Ascended.
"""
import os
import sys
import time
import logging
import argparse
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from automation.ark_ui_automation import ArkUIAutomation

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('resource_gatherer')

# Define resource types and their associated tools
RESOURCE_TOOLS = {
    "wood": ["stone_hatchet", "metal_hatchet", "chainsaw"],
    "stone": ["stone_pick", "metal_pick", "ankylosaurus"],
    "metal": ["metal_pick", "ankylosaurus"],
    "flint": ["stone_pick", "metal_pick"],
    "thatch": ["stone_hatchet", "metal_hatchet"],
    "fiber": ["sickle"],
    "berries": ["hands", "stone_pick"]
}

def equip_best_tool(ark, resource_type):
    """
    Equip the best available tool for gathering a specific resource.
    
    Args:
        ark: ArkUIAutomation instance
        resource_type: Type of resource to gather
    
    Returns:
        bool: True if a tool was equipped
    """
    logger.info(f"Finding best tool for gathering {resource_type}...")
    
    # Get list of tools for this resource
    if resource_type not in RESOURCE_TOOLS:
        logger.warning(f"Unknown resource type: {resource_type}")
        return False
    
    tools = RESOURCE_TOOLS[resource_type]
    
    # Open inventory
    if not ark.is_element_present('inventory_tab'):
        ark.open_inventory()
    
    # Try to find and equip each tool in order (best tools first)
    for tool in tools:
        tool_class = f"inventory_item_{tool}"
        
        # Check if tool exists in inventory
        if ark.find_element(tool_class):
            # Double-click to equip
            if ark.double_click_element(tool_class):
                logger.info(f"Equipped {tool} for gathering {resource_type}")
                
                # Close inventory
                ark.close_inventory()
                return True
    
    logger.warning(f"No suitable tools found for gathering {resource_type}")
    
    # Close inventory
    ark.close_inventory()
    return False

def detect_resources(ark, resource_type):
    """
    Look for resources of a specific type in the environment.
    Note: This is a simplified simulation as resource detection
    would require visual recognition of the 3D game world.
    
    Args:
        ark: ArkUIAutomation instance
        resource_type: Type of resource to look for
        
    Returns:
        bool: True if resources were found (simulated)
    """
    logger.info(f"Looking for {resource_type} resources...")
    
    # This is a simulation - in a real implementation, you would use
    # computer vision to detect resources in the 3D environment
    
    # Simulate resource detection
    found = random.random() > 0.3  # 70% chance of "finding" resources
    
    if found:
        logger.info(f"Found {resource_type} resources")
    else:
        logger.info(f"No {resource_type} resources found nearby")
    
    return found

def gather_resources(ark, resource_type, duration=30):
    """
    Gather resources of a specific type.
    
    Args:
        ark: ArkUIAutomation instance
        resource_type: Type of resource to gather
        duration: How long to gather in seconds
        
    Returns:
        dict: Gathering results
    """
    logger.info(f"Starting to gather {resource_type} for {duration} seconds...")
    
    # Equip the best tool
    if not equip_best_tool(ark, resource_type):
        return {"success": False, "error": "No suitable tool found"}
    
    # Look for resources
    if not detect_resources(ark, resource_type):
        return {"success": False, "error": "No resources found"}
    
    # Simulate gathering
    start_time = time.time()
    gather_actions = 0
    
    try:
        while time.time() - start_time < duration:
            # Simulate looking around
            move_direction = random.choice(['w', 'a', 's', 'd'])
            ark.press_and_hold(move_direction, random.uniform(0.3, 1.0))
            
            # Simulate mouse movement to look around
            pyautogui_available = 'pyautogui' in sys.modules
            if pyautogui_available:
                import pyautogui
                pyautogui.move(
                    random.randint(-100, 100), 
                    random.randint(-50, 50), 
                    duration=0.3
                )
            
            # Simulate gathering action (left click)
            pyautogui_available = 'pyautogui' in sys.modules
            if pyautogui_available:
                import pyautogui
                pyautogui.click()
            
            gather_actions += 1
            
            # Small delay between gathering actions
            time.sleep(random.uniform(0.5, 1.5))
            
            # Check if inventory is full (simulated)
            if random.random() > 0.9:  # 10% chance of inventory "full"
                logger.info("Inventory full notification detected")
                break
    
    except KeyboardInterrupt:
        logger.info("Gathering interrupted by user")
    
    # Calculate gathering time
    gather_time = time.time() - start_time
    
    # Simulate gathered amount
    gathered_amount = int(gather_actions * random.uniform(2, 5))
    
    logger.info(f"Gathered approximately {gathered_amount} {resource_type} in {gather_time:.1f} seconds")
    
    return {
        "success": True,
        "resource": resource_type,
        "amount": gathered_amount,
        "actions": gather_actions,
        "time": gather_time
    }

def check_inventory_space(ark):
    """
    Check if inventory has space.
    
    Args:
        ark: ArkUIAutomation instance
        
    Returns:
        bool: True if inventory has space
    """
    logger.info("Checking inventory space...")
    
    # Open inventory
    if not ark.is_element_present('inventory_tab'):
        ark.open_inventory()
    
    # Check for overweight message
    if ark.is_element_present('overweight_alert'):
        logger.warning("Inventory is overweight")
        ark.close_inventory()
        return False
    
    # Check weight indicator (simulated)
    weight_indicator = ark.find_element('weight_indicator')
    if weight_indicator:
        # In a real implementation, you would read the weight values
        # Here we'll just simulate it
        has_space = random.random() > 0.2  # 80% chance of having space
        
        if has_space:
            logger.info("Inventory has space")
        else:
            logger.info("Inventory is full")
        
        ark.close_inventory()
        return has_space
    
    # Default to assuming we have space
    logger.info("Couldn't determine inventory space, assuming it's available")
    ark.close_inventory()
    return True

def deposit_resources(ark, storage_name="structure_storage"):
    """
    Deposit resources into a storage container.
    
    Args:
        ark: ArkUIAutomation instance
        storage_name: Class name of the storage structure
        
    Returns:
        bool: True if resources were deposited
    """
    logger.info(f"Attempting to deposit resources in {storage_name}...")
    
    # Look for storage in view (simplified)
    if not ark.find_element(storage_name):
        logger.warning(f"No {storage_name} found in view")
        return False
    
    # Interact with storage
    if not ark.is_element_present('inventory_tab'):
        # Simulate pressing 'E' to interact
        ark.press_key('e')
        time.sleep(1)
    
    # Check if inventory opened
    if not ark.is_element_present('inventory_tab'):
        logger.warning("Failed to open storage inventory")
        return False
    
    # Transfer all items
    if not ark.click_element('transfer_all'):
        logger.warning("Failed to transfer items")
        ark.close_inventory()
        return False
    
    logger.info("Successfully deposited resources")
    
    # Close inventory
    ark.close_inventory()
    return True

def gather_multiple_resources(ark, resource_types, duration_each=30):
    """
    Gather multiple types of resources.
    
    Args:
        ark: ArkUIAutomation instance
        resource_types: List of resource types to gather
        duration_each: Duration to spend on each resource type
        
    Returns:
        dict: Results for each resource type
    """
    logger.info(f"Starting multi-resource gathering: {', '.join(resource_types)}")
    
    results = {}
    
    for resource_type in resource_types:
        # Check inventory space
        if not check_inventory_space(ark):
            logger.warning("Inventory full, attempting to deposit resources")
            if not deposit_resources(ark):
                logger.warning("Failed to deposit resources, skipping further gathering")
                break
        
        # Gather this resource type
        result = gather_resources(ark, resource_type, duration_each)
        results[resource_type] = result
    
    return results

def main():
    parser = argparse.ArgumentParser(description="ARK Resource Gathering Example")
    parser.add_argument("--weights", "-w", required=True, help="Path to trained model weights")
    parser.add_argument("--resource", "-r", default="wood", help="Resource type to gather")
    parser.add_argument("--duration", "-d", type=int, default=30, 
                      help="Duration to gather in seconds")
    parser.add_argument("--multi", "-m", action="store_true", 
                      help="Gather multiple resource types")
    
    args = parser.parse_args()
    
    # Initialize the ARK UI automation
    with ArkUIAutomation(args.weights, confidence=0.4) as ark:
        logger.info("ARK Resource Gatherer started")
        
        if args.multi:
            # Gather multiple resource types
            resource_types = ["wood", "stone", "fiber", "berries"]
            results = gather_multiple_resources(ark, resource_types, args.duration)
            
            # Log results
            logger.info("Multi-resource gathering results:")
            for resource, result in results.items():
                if result["success"]:
                    logger.info(f"- {resource}: {result['amount']} gathered in {result['time']:.1f} seconds")
                else:
                    logger.info(f"- {resource}: Failed - {result.get('error', 'Unknown error')}")
        else:
            # Gather single resource type
            result = gather_resources(ark, args.resource, args.duration)
            
            if result["success"]:
                logger.info(f"Successfully gathered {result['amount']} {args.resource}")
            else:
                logger.warning(f"Failed to gather {args.resource}: {result.get('error', 'Unknown error')}")
        
        logger.info("ARK Resource Gatherer completed")

if __name__ == "__main__":
    main()