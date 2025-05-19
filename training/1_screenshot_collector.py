"""
Enhanced Screenshot Collector for ARK: Survival Ascended UI Detection.
This script automatically captures screenshots of the game at defined intervals,
with specific support for capturing different UI states and inventory types.
Optimized for collecting training data for YOLOv12 UI detection models.
"""
import os
import time
import datetime
import argparse
import keyboard
import mss
import mss.tools
import numpy as np
from PIL import Image
import cv2
import yaml
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.screenshot_utils import capture_screenshot, save_screenshot

# Define UI state categories for better organization
UI_STATES = {
    "general": "General gameplay UI",
    "inventory": "Character inventory screen",
    "split_inventory": "Split-screen inventory (player + container/dino)",
    "map": "Map screen",
    "taming": "Taming interface",
    "crafting": "Crafting interface",
    "engrams": "Engram learning screen",
    "tribe": "Tribe management interface",
    "character": "Character stats screen",
    "status_low": "Status bars in low state (health/food/water low)",
    "status_full": "Status bars in full state (health/food/water full)",
    "creature_ui": "Creature stats and management UI",
    "tek_interface": "Tek tier interfaces",
    "building": "Building placement UI",
    "obelisk": "Obelisk/terminal interface",
    "mission": "Mission interface",
    "event_ui": "Special event UI elements",
    "death_screen": "Death/respawn interface",
    "level_up": "Level up notification and stat allocation",
    "tooltip": "Item tooltip and description popups",
    "alert": "Alert messages (starvation, overweight, etc.)",
    "structure": "Structure inventory and options",
    "dino_inventory": "Dinosaur inventory screen",
    "cryopod": "Cryopod interface",
    "cooking": "Cooking pot/industrial cooker interface",
    "smithy": "Smithy crafting interface",
    "fabricator": "Fabricator crafting interface",
    "replicator": "Tek replicator interface",
    "transmitter": "Transmitter interface",
    "hotbar": "Hotbar UI elements",
    "button_states": "Buttons in different states (active/inactive)",
    "stamina_states": "Stamina bar in different states",
    "torpor_states": "Torpidity bar in different states",
    "custom": "Custom UI elements"
}

def create_directory(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def capture_screenshots(output_dir, interval=2, limit=None, hotkey='f10', state=None, session_name=None, burst=False, burst_count=5, burst_delay=0.2, auto_organize=True, display_overlay=True):
    """
    Capture screenshots at regular intervals with enhanced UI state tracking.
    
    Args:
        output_dir: Directory to save screenshots
        interval: Time between screenshots in seconds
        limit: Maximum number of screenshots to capture (None for unlimited)
        hotkey: Key to press to stop capturing
        state: UI state category to tag screenshots with
        session_name: Optional name for this screenshot session
        burst: Capture a quick burst of screenshots (for animation/transition)
        burst_count: Number of screenshots to take in burst mode
        burst_delay: Delay between screenshots in burst mode
        auto_organize: Automatically organize screenshots into state folders
        display_overlay: Show on-screen information during capture
    """
    # Create parent directory
    create_directory(output_dir)
    
    # Create state-specific directory if auto-organize is enabled
    screenshot_dir = output_dir
    if auto_organize and state and state in UI_STATES:
        screenshot_dir = os.path.join(output_dir, state)
        create_directory(screenshot_dir)
    
    # Screenshot metadata
    metadata = {
        'capture_date': datetime.datetime.now().strftime("%Y-%m-%d"),
        'game': 'ARK: Survival Ascended',
        'ui_state': state if state else 'general',
        'session_name': session_name,
        'screenshot_count': 0,
        'screenshot_files': [],
        'burst_mode': burst,
        'capture_interval': interval if not burst else burst_delay
    }
    
    # Print session information
    print(f"\n=== ARK UI Enhanced Screenshot Collector ===")
    print(f"Saving screenshots to: {screenshot_dir}")
    print(f"Interval: {interval if not burst else burst_delay} seconds")
    print(f"Limit: {limit if limit else ('Unlimited' if not burst else burst_count)}")
    print(f"Stop key: '{hotkey}'")
    print(f"UI State: {state if state else 'general'}")
    
    if state in UI_STATES:
        print(f"State description: {UI_STATES[state]}")
    
    if burst:
        print(f"BURST MODE ENABLED: Will capture {burst_count} screenshots rapidly")
    
    print("\nPress any key to start capturing...")
    print("(Position the ARK: Survival Ascended window as desired)")
    keyboard.read_key()
    
    # Setup screen capture
    print("\nStarting capture. Press '{hotkey}' to stop.")
    
    with mss.mss() as sct:
        # Get primary monitor
        monitor = sct.monitors[1]
        
        try:
            count = 0
            
            # Set maximum screenshot count for burst mode
            max_count = burst_count if burst else (limit if limit else float('inf'))
            
            while count < max_count:
                # Get timestamp for filename
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                state_tag = f"_{state}" if state else ""
                session_tag = f"_{session_name}" if session_name else ""
                filename = f"ark_ui{state_tag}{session_tag}_{timestamp}.png"
                filepath = os.path.join(screenshot_dir, filename)
                
                # Capture screenshot
                img = capture_screenshot(sct, monitor)
                
                # Add overlay information if enabled
                if display_overlay:
                    # Create a copy of the image for overlay
                    img_with_overlay = img.copy()
                    
                    # Add UI state and timestamp overlay
                    overlay_text = f"State: {state if state else 'general'} | {timestamp}"
                    cv2.putText(img_with_overlay, overlay_text, (10, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # Display counter
                    counter_text = f"#{count+1}/{max_count if max_count != float('inf') else 'unlimited'}"
                    cv2.putText(img_with_overlay, counter_text, (10, 70), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # Display the image with overlay
                    cv2.imshow("ARK Screenshot Collector", cv2.cvtColor(img_with_overlay, cv2.COLOR_RGB2BGR))
                    cv2.waitKey(1)
                
                # Save the original screenshot without the overlay
                save_screenshot(img, filepath)
                
                count += 1
                metadata['screenshot_count'] = count
                metadata['screenshot_files'].append(filename)
                
                print(f"Captured #{count}: {filename}")
                
                # Check if stop key pressed
                if keyboard.is_pressed(hotkey):
                    print(f"\n'{hotkey}' key pressed. Stopping capture.")
                    break
                
                # Wait for next interval
                delay = burst_delay if burst else interval
                time.sleep(delay)
            
            if count >= max_count and burst:
                print(f"\nBurst capture complete. Captured {count} screenshots.")
            elif count >= max_count:
                print(f"\nReached limit of {limit} screenshots. Stopping.")
                
        except KeyboardInterrupt:
            print("\nCapture interrupted by user.")
        
        finally:
            # Close any open windows
            cv2.destroyAllWindows()
            
            # Save metadata
            metadata_file = os.path.join(screenshot_dir, "capture_metadata.yaml")
            with open(metadata_file, 'w') as f:
                yaml.dump(metadata, f)
            
            print(f"\nCapture complete. {count} screenshots saved to {screenshot_dir}")
            print(f"Metadata saved to {metadata_file}")

def capture_state_sequence(output_dir, states, wait_time=5, hotkey='f10'):
    """
    Guide the user through capturing a sequence of specific UI states.
    
    Args:
        output_dir: Directory to save screenshots
        states: List of UI states to capture
        wait_time: Time to wait for user to set up each state
        hotkey: Key to press to stop capturing
    """
    print("\n=== ARK UI State Sequence Capture ===")
    print(f"This will guide you through capturing {len(states)} different UI states")
    print("For each state, you'll have time to set up the game UI before capture")
    print(f"Press '{hotkey}' at any time to abort the sequence")
    print("\nPress any key to begin the sequence...")
    keyboard.read_key()
    
    for i, state in enumerate(states):
        if state not in UI_STATES:
            print(f"\nSkipping unknown state: {state}")
            continue
        
        print(f"\n[{i+1}/{len(states)}] Preparing to capture: {state}")
        print(f"Description: {UI_STATES[state]}")
        print(f"Please set up the game to show this UI state...")
        
        # Countdown
        for j in range(wait_time, 0, -1):
            print(f"Capturing in {j} seconds... (Press '{hotkey}' to skip)", end='\r')
            
            if keyboard.is_pressed(hotkey):
                print(f"\nSkipped state: {state}")
                break
                
            time.sleep(1)
        
        if keyboard.is_pressed(hotkey):
            continue
        
        print(f"\nCapturing {state} UI state now!")
        
        # Capture screenshots for this state
        capture_screenshots(
            output_dir=output_dir,
            interval=1,
            limit=3,  # Take 3 screenshots of each state
            hotkey=hotkey,
            state=state,
            session_name=f"sequence_{i+1}of{len(states)}",
            burst=True,
            burst_count=3,
            burst_delay=0.3,
            auto_organize=True
        )
    
    print("\nState sequence capture complete!")

def show_ui_state_reference():
    """Display a reference guide for different UI states to capture."""
    print("\n=== ARK UI States Reference Guide ===")
    print("Here are the UI states you should try to capture for best model training:")
    
    # Group states by category
    categories = {
        "Inventory & Items": ["inventory", "split_inventory", "dino_inventory", "structure", "cryopod"],
        "Character Status": ["status_low", "status_full", "stamina_states", "torpor_states"],
        "Crafting & Building": ["crafting", "engrams", "building", "smithy", "fabricator", "replicator"],
        "Creature Management": ["taming", "creature_ui"],
        "Map & Navigation": ["map"],
        "Tribe & Multiplayer": ["tribe"],
        "Special Interfaces": ["tek_interface", "obelisk", "mission", "transmitter"],
        "UI Elements": ["tooltip", "alert", "button_states", "hotbar", "death_screen", "level_up"]
    }
    
    for category, states in categories.items():
        print(f"\n{category}:")
        for state in states:
            if state in UI_STATES:
                print(f"  - {state}: {UI_STATES[state]}")
    
    print("\nCapturing a diverse set of these UI states will improve model training!")
    print("Use the --state parameter to specify which state you're capturing.")

def get_important_states():
    """Get a list of the most important UI states to capture."""
    return [
        "inventory",
        "split_inventory", 
        "status_low",
        "status_full",
        "crafting",
        "taming",
        "dino_inventory",
        "structure",
        "button_states",
        "tooltip",
        "alert"
    ]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhanced ARK UI Screenshot Collector")
    parser.add_argument("--output", "-o", default="dataset", help="Output directory for screenshots")
    parser.add_argument("--interval", "-i", type=float, default=2, help="Time between screenshots in seconds")
    parser.add_argument("--limit", "-l", type=int, default=None, help="Maximum number of screenshots to capture")
    parser.add_argument("--hotkey", default="f10", help="Hotkey to stop capturing")
    parser.add_argument("--state", "-s", default=None, choices=list(UI_STATES.keys()), 
                      help="UI state to tag screenshots with")
    parser.add_argument("--session", "-n", default=None, help="Optional session name")
    parser.add_argument("--burst", "-b", action="store_true", help="Capture a quick burst of screenshots")
    parser.add_argument("--burst-count", type=int, default=5, help="Number of screenshots in burst mode")
    parser.add_argument("--burst-delay", type=float, default=0.2, help="Delay between burst screenshots")
    parser.add_argument("--no-organize", action="store_true", help="Don't organize into state folders")
    parser.add_argument("--no-overlay", action="store_true", help="Don't show capture overlay")
    parser.add_argument("--guide", "-g", action="store_true", help="Show UI state reference guide")
    parser.add_argument("--sequence", action="store_true", 
                      help="Guide through capturing a sequence of important UI states")
    parser.add_argument("--states", nargs='+', help="Custom list of states for sequence capture")
    
    args = parser.parse_args()
    
    # Show guide if requested
    if args.guide:
        show_ui_state_reference()
        sys.exit(0)
    
    # Handle sequence capture
    if args.sequence:
        if args.states:
            # Use custom state list
            states_to_capture = args.states
        else:
            # Use default important states
            states_to_capture = get_important_states()
            
        capture_state_sequence(args.output, states_to_capture, 10, args.hotkey)
    else:
        # Regular screenshot capture
        capture_screenshots(
            args.output, 
            args.interval, 
            args.limit, 
            args.hotkey, 
            args.state,
            args.session,
            args.burst,
            args.burst_count,
            args.burst_delay,
            not args.no_organize,
            not args.no_overlay
        )