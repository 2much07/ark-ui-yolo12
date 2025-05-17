"""
Screenshot collector for ARK: Survival Ascended UI Detection.
This script automatically captures screenshots of the game at defined intervals.
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

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.screenshot_utils import capture_screenshot, save_screenshot

def create_directory(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def capture_screenshots(output_dir, interval=2, limit=None, hotkey='f10', game_mode=None):
    """
    Capture screenshots at regular intervals.
    
    Args:
        output_dir: Directory to save screenshots
        interval: Time between screenshots in seconds
        limit: Maximum number of screenshots to capture (None for unlimited)
        hotkey: Key to press to stop capturing
        game_mode: Game mode to tag screenshots with ('inventory', 'map', 'all', etc.)
    """
    # Create directories
    create_directory(output_dir)
    
    # Screenshot metadata
    metadata = {
        'capture_date': datetime.datetime.now().strftime("%Y-%m-%d"),
        'game': 'ARK: Survival Ascended',
        'game_mode': game_mode if game_mode else 'general',
        'screenshot_count': 0,
        'screenshot_files': []
    }
    
    count = 0
    print(f"\n=== ARK UI Screenshot Collector ===")
    print(f"Saving screenshots to: {output_dir}")
    print(f"Interval: {interval} seconds")
    print(f"Limit: {limit if limit else 'Unlimited'}")
    print(f"Stop key: '{hotkey}'")
    print(f"Game mode tag: {game_mode if game_mode else 'general'}")
    print("\nPress any key to start capturing...")
    print("(Position the ARK: Survival Ascended window as desired)")
    keyboard.read_key()
    
    # Setup screen capture
    print("\nStarting capture. Press '{hotkey}' to stop.")
    
    with mss.mss() as sct:
        # Get primary monitor
        monitor = sct.monitors[1]
        
        try:
            while True:
                if limit and count >= limit:
                    print(f"\nReached limit of {limit} screenshots. Stopping.")
                    break
                
                # Get timestamp for filename
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                mode_tag = f"_{game_mode}" if game_mode else ""
                filename = f"ark_ui{mode_tag}_{timestamp}.png"
                filepath = os.path.join(output_dir, filename)
                
                # Capture screenshot
                img = capture_screenshot(sct, monitor)
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
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nCapture interrupted by user.")
        
        # Save metadata
        metadata_file = os.path.join(output_dir, "capture_metadata.yaml")
        with open(metadata_file, 'w') as f:
            yaml.dump(metadata, f)
        
        print(f"\nCapture complete. {count} screenshots saved to {output_dir}")
        print(f"Metadata saved to {metadata_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARK UI Screenshot Collector")
    parser.add_argument("--output", "-o", default="dataset", help="Output directory for screenshots")
    parser.add_argument("--interval", "-i", type=float, default=2, help="Time between screenshots in seconds")
    parser.add_argument("--limit", "-l", type=int, default=None, help="Maximum number of screenshots to capture")
    parser.add_argument("--hotkey", default="f10", help="Hotkey to stop capturing")
    parser.add_argument("--mode", "-m", default=None, help="Game mode tag (inventory, map, taming, etc.)")
    
    args = parser.parse_args()
    capture_screenshots(args.output, args.interval, args.limit, args.hotkey, args.mode)