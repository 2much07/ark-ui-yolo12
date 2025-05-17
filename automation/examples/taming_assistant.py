```python
"""
ARK Taming Assistant Example
This script demonstrates how to use the ArkUIAutomation class to assist with taming creatures in ARK: Survival Ascended.
"""
import os
import sys
import time
import logging
import argparse
import threading

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from automation.ark_ui_automation import ArkUIAutomation

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('taming_assistant')

# Define taming foods for different creatures
TAMING_FOODS = {
    "parasaur": ["berry_mejoberry", "berry_amarberry"],
    "raptor": ["raw_meat", "cooked_meat"],
    "triceratops": ["berry_mejoberry", "vegetable"],
    "pteranodon": ["raw_meat", "cooked_meat"],
    "dodo": ["berry", "seed"],
    "rex": ["raw_prime_meat", "raw_meat"],
    "argentavis": ["raw_meat", "raw_prime_meat"],
    "ankylosaurus": ["berry_mejoberry", "vegetable"]
}

# Define narcotic requirements (number of narcotics needed per hour)
NARCOTIC_REQUIREMENTS = {
    "parasaur": 5,
    "raptor": 10,
    "triceratops": 15,
    "pteranodon": 8,
    "dodo": 2,
    "rex": 40,
    "argentavis": 25,
    "ankylosaurus": 20
}

class TamingMonitor:
    """Class to monitor taming progress."""
    
    def __init__(self, ark, creature_type):
        """Initialize taming monitor."""
        self.ark = ark
        self.creature_type = creature_type
        self.running = False
        self.thread = None
        self.taming_start_time = None
        self.last_narcotic_time = None
        self.food_added_count = 0
        self.narcotic_added_count = 0
    
    def start_monitoring(self, interval=5.0):
        """Start monitoring taming progress."""
        if self.thread is not None and self.thread.is_alive():
            logger.warning("Monitoring already active")
            return False
        
        self.running = True
        self.taming_start_time = time.time()
        self.last_narcotic_time = self.taming_start_time
        self.thread = threading.Thread(target=self._monitoring_loop, args=(interval,))
        self.thread.daemon = True
        self.thread.start()
        
        logger.info(f"Started taming monitor for {self.creature_type}")
        return True
    
    def stop_monitoring(self):
        """Stop monitoring taming progress."""
        if self.thread is None or not self.thread.is_alive():
            logger.warning("No monitoring active")
            return False
        
        self.running = False
        self.thread.join(timeout=2.0)
        
        # Log taming session summary
        elapsed_time = time.time() - self.taming_start_time
        hours = elapsed_time / 3600
        
        logger.info(f"Taming session summary for {self.creature_type}:")
        logger.info(f"- Duration: {elapsed_time:.1f} seconds ({hours:.2f} hours)")
        logger.info(f"- Food added: {self.food_added_count} items")
        logger.info(f"- Narcotics used: {self.narcotic_added_count}")
        
        return True
    
    def _monitoring_loop(self, interval):
        """Main monitoring loop."""
        while self.running:
            try:
                # Check if taming UI is visible
                taming_visible = self.ark.is_element_present('taming_bar')
                
                if not taming_visible:
                    logger.warning("Taming UI not visible")
                    time.sleep(interval)
                    continue
                
                # Check torpidity
                self._check_torpidity()
                
                # Check food
                self._check_food()
                
                # Sleep until next check
                time.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error in taming monitor: {str(e)}")
                time.sleep(interval)
    
    def _check_torpidity(self):
        """Check and manage creature torpidity."""
        # In a real implementation, you would check the torpidity bar level
        # Here we'll use a simple time-based approach
        
        # Calculate time since last narcotic
        elapsed = time.time() - self.last_narcotic_time
        hours_elapsed = elapsed / 3600
        
        # Calculate required narcotics based on time
        required_narcotics = NARCOTIC_REQUIREMENTS.get(self.creature_type, 10)
        
        # Check if we need to add narcotics (every 10 minutes in this simulation)
        if elapsed > 600:  # 10 minutes
            logger.info("Torpidity getting low, adding narcotics...")
            
            # Open inventory if needed
            if not self.ark.is_element_present('inventory_tab'):
                self.ark.open_inventory()
            
            # Look for narcotic in inventory
            narcotic_found = self.ark.find_element('inventory_item_narcotic')
            
            if narcotic_found:
                # Transfer narcotic to creature
                if self._transfer_item_to_creature('inventory_item_narcotic'):
                    self.last_narcotic_time = time.time()
                    self.narcotic_added_count += 1
                    logger.info("Added narcotic to creature")
                else:
                    logger.warning("Failed to add narcotic")
            else:
                logger.warning("No narcotics found in inventory")
        
        # Log torpidity status
        remaining = 600 - (elapsed % 600)
        logger.info(f"Torpidity OK. Next narcotic in {remaining:.1f} seconds")
    
    def _check_food(self):
        """Check and manage creature food."""
        # In a real implementation, you would check if the creature has food
        # Here we'll add food every 5 minutes as a simulation
        
        # Check if 5 minutes have passed since last food addition
        if not hasattr(self, 'last_food_time'):
            self.last_food_time = time.time()
        
        elapsed = time.time() - self.last_food_time
        
        # Add food every 5 minutes
        if elapsed > 300:  # 5 minutes
            logger.info("Adding food to creature...")
            
            # Open inventory if needed
            if not self.ark.is_element_present('inventory_tab'):
                self.ark.open_inventory()
            
            # Get preferred foods for this creature
            preferred_foods = TAMING_FOODS.get(self.creature_type, ["raw_meat", "berry"])
            
            # Try each food type
            for food in preferred_foods:
                food_item = f"inventory_item_{food}"
                food_found = self.ark.find_element(food_item)
                
                if food_found:
                    # Transfer food to creature
                    if self._transfer_item_to_creature(food_item):
                        self.last_food_time = time.time()
                        self.food_added_count += 1
                        logger.info(f"Added {food} to creature")
                        break
                    else:
                        logger.warning(f"Failed to add {food}")
                else:
                    logger.warning(f"No {food} found in inventory")
            else:
                logger.warning("No suitable food found in inventory")
    
    def _transfer_item_to_creature(self, item_name):
        """Transfer an item to the creature inventory."""
        # Find the item
        item = self.ark.find_element(item_name)
        
        if not item:
            return False
        
        # Find creature inventory (right side of screen)
        creature_inventory = self.ark.find_element('creature_inventory')
        
        if not creature_inventory:
            return False
        
        # Drag item to creature inventory
        return self.ark.drag_element(item_name, 'creature_inventory')

def feed_creature(ark, creature_type):
    """Feed a creature being tamed."""
    logger.info(f"Feeding {creature_type}...")
    
    # Get preferred foods for this creature
    preferred_foods = TAMING_FOODS.get(creature_type, ["raw_meat", "berry"])
    
    # Open inventory
    if not ark.is_element_present('inventory_tab'):
        ark.open_inventory()
    
    # Check if we're looking at a creature
    if not ark.is_element_present('taming_bar'):
        logger.warning("No creature being tamed detected")
        return False
    
    # Try to feed each preferred food
    for food in preferred_foods:
        food_item = f"inventory_item_{food}"
        food_found = ark.find_element(food_item)
        
        if food_found:
            # Drag food to creature inventory
            if ark.drag_element(food_item, 'creature_inventory'):
                logger.info(f"Fed {food} to {creature_type}")
                return True
    
    logger.warning(f"No suitable food found for {creature_type}")
    return False

def apply_narcotic(ark):
    """Apply narcotic to a creature."""
    logger.info("Applying narcotic...")
    
    # Open inventory
    if not ark.is_element_present('inventory_tab'):
        ark.open_inventory()
    
    # Check if we're looking at a creature
    if not ark.is_element_present('taming_bar'):
        logger.warning("No creature being tamed detected")
        return False
    
    # Look for narcotic in inventory
    narcotic_found = ark.find_element('inventory_item_narcotic')
    
    if narcotic_found:
        # Drag narcotic to creature inventory
        if ark.drag_element('inventory_item_narcotic', 'creature_inventory'):
            logger.info("Applied narcotic to creature")
            return True
        else:
            logger.warning("Failed to apply narcotic")
    else:
        logger.warning("No narcotics found in inventory")
    
    return False

def main():
    parser = argparse.ArgumentParser(description="ARK Taming Assistant Example")
    parser.add_argument("--weights", "-w", required=True, help="Path to trained model weights")
    parser.add_argument("--creature", "-c", default="raptor", help="Creature type to tame")
    parser.add_argument("--monitor", "-m", action="store_true", help="Start taming monitor")
    parser.add_argument("--duration", "-d", type=int, default=60, 
                       help="Duration to monitor in seconds (with --monitor)")
    
    args = parser.parse_args()
    
    # Initialize the ARK UI automation
    with ArkUIAutomation(args.weights, confidence=0.4) as ark:
        logger.info("ARK Taming Assistant started")
        
        if args.monitor:
            # Start taming monitor
            monitor = TamingMonitor(ark, args.creature)
            monitor.start_monitoring()
            
            logger.info(f"Monitoring {args.creature} taming for {args.duration} seconds")
            try:
                time.sleep(args.duration)
            except KeyboardInterrupt:
                logger.info("Monitoring interrupted by user")
            
            monitor.stop_monitoring()
        else:
            # One-time actions
            feed_creature(ark, args.creature)
            apply_narcotic(ark)
        
        logger.info("ARK Taming Assistant completed")

if __name__ == "__main__":
    main()