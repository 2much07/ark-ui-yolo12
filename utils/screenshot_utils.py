"""
Screenshot utilities for ARK UI detection.
This module provides functions for capturing and processing screenshots.
"""
import os
import time
import datetime
import mss
import mss.tools
import numpy as np
from PIL import Image
import cv2
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('screenshot_utils')

def capture_screenshot(sct=None, monitor=None):
    """
    Capture a screenshot using MSS.
    
    Args:
        sct: MSS instance (optional, creates a new one if not provided)
        monitor: Monitor to capture (optional, uses primary monitor if not provided)
        
    Returns:
        Screenshot as numpy array
    """
    close_sct = False
    if sct is None:
        sct = mss.mss()
        close_sct = True
    
    if monitor is None:
        monitor = sct.monitors[1]  # Primary monitor
    
    # Capture screenshot
    img = sct.grab(monitor)
    img_np = np.array(img)
    
    # Convert to RGB format
    img_rgb = cv2.cvtColor(img_np, cv2.COLOR_BGRA2RGB)
    
    if close_sct:
        sct.close()
    
    return img_rgb

def save_screenshot(img, filepath, format='auto'):
    """
    Save a screenshot to file.
    
    Args:
        img: Screenshot as numpy array
        filepath: Path to save the screenshot
        format: Image format (auto, png, jpg)
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    
    # Determine format from filepath if set to auto
    if format == 'auto':
        _, ext = os.path.splitext(filepath)
        if ext.lower() in ['.jpg', '.jpeg']:
            format = 'jpg'
        else:
            format = 'png'
    
    # Convert to PIL Image
    if isinstance(img, np.ndarray):
        img_pil = Image.fromarray(img)
    else:
        img_pil = img
    
    # Save image
    if format.lower() == 'jpg':
        img_pil.save(filepath, 'JPEG', quality=95)
    else:
        img_pil.save(filepath, 'PNG')
    
    return filepath

def crop_screenshot(img, x, y, width, height):
    """
    Crop a screenshot to a specific region.
    
    Args:
        img: Screenshot as numpy array
        x: X coordinate of top-left corner
        y: Y coordinate of top-left corner
        width: Width of region
        height: Height of region
        
    Returns:
        Cropped screenshot as numpy array
    """
    if isinstance(img, np.ndarray):
        return img[y:y+height, x:x+width]
    else:
        # Convert PIL Image to numpy array
        img_np = np.array(img)
        cropped = img_np[y:y+height, x:x+width]
        return Image.fromarray(cropped)

def resize_screenshot(img, width, height, keep_aspect_ratio=True):
    """
    Resize a screenshot.
    
    Args:
        img: Screenshot as numpy array
        width: Target width
        height: Target height
        keep_aspect_ratio: Whether to maintain aspect ratio
        
    Returns:
        Resized screenshot as numpy array
    """
    if isinstance(img, np.ndarray):
        if keep_aspect_ratio:
            # Calculate the target dimensions while preserving aspect ratio
            h, w = img.shape[:2]
            aspect = w / h
            
            if width / height > aspect:
                # Width is the limiting factor
                new_width = int(height * aspect)
                new_height = height
            else:
                # Height is the limiting factor
                new_width = width
                new_height = int(width / aspect)
            
            return cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        else:
            return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    else:
        # Handle PIL Image
        img_np = np.array(img)
        resized = resize_screenshot(img_np, width, height, keep_aspect_ratio)
        return Image.fromarray(resized)

def enhance_screenshot(img, brightness=1.0, contrast=1.0, saturation=1.0):
    """
    Enhance a screenshot for better visibility.
    
    Args:
        img: Screenshot as numpy array
        brightness: Brightness adjustment factor
        contrast: Contrast adjustment factor
        saturation: Saturation adjustment factor
        
    Returns:
        Enhanced screenshot as numpy array
    """
    if isinstance(img, np.ndarray):
        # Convert to float for processing
        img_float = img.astype(np.float32) / 255.0
        
        # Apply brightness adjustment
        img_float = img_float * brightness
        
        # Apply contrast adjustment
        img_float = (img_float - 0.5) * contrast + 0.5
        
        # Apply saturation adjustment
        if saturation != 1.0:
            # Convert to HSV
            img_hsv = cv2.cvtColor(img_float, cv2.COLOR_RGB2HSV)
            img_hsv[:, :, 1] = img_hsv[:, :, 1] * saturation
            img_float = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)
        
        # Clip values to valid range
        img_float = np.clip(img_float, 0, 1)
        
        # Convert back to uint8
        return (img_float * 255).astype(np.uint8)
    else:
        # Handle PIL Image
        img_np = np.array(img)
        enhanced = enhance_screenshot(img_np, brightness, contrast, saturation)
        return Image.fromarray(enhanced)

def capture_screen_region(x, y, width, height, sct=None):
    """
    Capture a specific region of the screen.
    
    Args:
        x: X coordinate of top-left corner
        y: Y coordinate of top-left corner
        width: Width of region
        height: Height of region
        sct: MSS instance (optional)
        
    Returns:
        Screenshot of region as numpy array
    """
    close_sct = False
    if sct is None:
        sct = mss.mss()
        close_sct = True
    
    # Define region to capture
    monitor = {"top": y, "left": x, "width": width, "height": height}
    
    # Capture screenshot
    img = sct.grab(monitor)
    img_np = np.array(img)
    
    # Convert to RGB format
    img_rgb = cv2.cvtColor(img_np, cv2.COLOR_BGRA2RGB)
    
    if close_sct:
        sct.close()
    
    return img_rgb

def capture_game_window(window_title="ARK: Survival Ascended", sct=None):
    """
    Capture the ARK game window.
    
    Args:
        window_title: Title of the game window
        sct: MSS instance (optional)
        
    Returns:
        Screenshot of game window as numpy array or None if window not found
    """
    try:
        # Try to import pygetwindow
        import pygetwindow as gw
        
        # Find the game window
        window = gw.getWindowsWithTitle(window_title)
        
        if not window:
            logger.warning(f"Window with title '{window_title}' not found")
            return None
        
        # Get the first matching window
        window = window[0]
        
        # Get window position and size
        x, y = window.left, window.top
        width, height = window.width, window.height
        
        # Capture the window
        return capture_screen_region(x, y, width, height, sct)
    
    except ImportError:
        logger.warning("pygetwindow not installed. Install with: pip install pygetwindow")
        logger.info("Falling back to full screen capture")
        return capture_screenshot(sct)

def save_screenshot_sequence(prefix="ark_screenshot", directory="screenshots", interval=2.0, limit=None):
    """
    Save a sequence of screenshots.
    
    Args:
        prefix: Filename prefix
        directory: Directory to save screenshots
        interval: Time between screenshots in seconds
        limit: Maximum number of screenshots to capture (None for unlimited)
        
    Returns:
        List of saved screenshot paths
    """
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    saved_paths = []
    count = 0
    
    try:
        with mss.mss() as sct:
            while True:
                if limit is not None and count >= limit:
                    break
                
                # Capture screenshot
                img = capture_screenshot(sct)
                
                # Generate filename with timestamp
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = os.path.join(directory, f"{prefix}_{timestamp}.png")
                
                # Save screenshot
                save_screenshot(img, filepath)
                saved_paths.append(filepath)
                
                count += 1
                logger.info(f"Saved screenshot {count}: {filepath}")
                
                # Wait for next interval
                time.sleep(interval)
    
    except KeyboardInterrupt:
        logger.info("Screenshot sequence interrupted by user")
    
    return saved_paths

def detect_ui_change(previous_img, current_img, threshold=0.95):
    """
    Detect if there's a significant change in the UI.
    
    Args:
        previous_img: Previous screenshot as numpy array
        current_img: Current screenshot as numpy array
        threshold: Similarity threshold (0-1)
        
    Returns:
        True if significant change detected, False otherwise
    """
    # Ensure same dimensions
    if previous_img.shape != current_img.shape:
        current_img = cv2.resize(current_img, (previous_img.shape[1], previous_img.shape[0]))
    
    # Convert to grayscale
    prev_gray = cv2.cvtColor(previous_img, cv2.COLOR_RGB2GRAY)
    curr_gray = cv2.cvtColor(current_img, cv2.COLOR_RGB2GRAY)
    
    # Calculate structural similarity index
    try:
        from skimage.metrics import structural_similarity as ssim
        similarity = ssim(prev_gray, curr_gray)
    except ImportError:
        # Fallback to mean squared error
        mse = np.mean((prev_gray - curr_gray) ** 2)
        similarity = 1 - mse / 255
    
    return similarity < threshold

def wait_for_ui_change(initial_img=None, timeout=10, check_interval=0.2, threshold=0.95, sct=None):
    """
    Wait for a change in the UI.
    
    Args:
        initial_img: Initial screenshot as numpy array (optional)
        timeout: Maximum time to wait in seconds
        check_interval: Time between checks in seconds
        threshold: Similarity threshold (0-1)
        sct: MSS instance (optional)
        
    Returns:
        New screenshot after change or None if timeout
    """
    close_sct = False
    if sct is None:
        sct = mss.mss()
        close_sct = True
    
    # Capture initial screenshot if not provided
    if initial_img is None:
        initial_img = capture_screenshot(sct)
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        # Capture current screenshot
        current_img = capture_screenshot(sct)
        
        # Check for significant change
        if detect_ui_change(initial_img, current_img, threshold):
            if close_sct:
                sct.close()
            return current_img
        
        # Wait for next check
        time.sleep(check_interval)
    
    if close_sct:
        sct.close()
    
    logger.warning(f"Timeout waiting for UI change after {timeout} seconds")
    return None

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Screenshot Utilities for ARK UI Detection")
    parser.add_argument("--save", "-s", action="store_true", help="Save a screenshot")
    parser.add_argument("--sequence", "-q", action="store_true", help="Capture a sequence of screenshots")
    parser.add_argument("--interval", "-i", type=float, default=2.0, help="Interval between screenshots")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Number of screenshots to capture")
    parser.add_argument("--output", "-o", default="screenshots", help="Output directory")
    
    args = parser.parse_args()
    
    if args.save:
        # Capture and save a single screenshot
        img = capture_screenshot()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(args.output, f"ark_screenshot_{timestamp}.png")
        save_screenshot(img, filepath)
        print(f"Screenshot saved to {filepath}")
    
    elif args.sequence:
        # Capture a sequence of screenshots
        print(f"Capturing {args.limit} screenshots with {args.interval} second interval")
        print(f"Press Ctrl+C to stop")
        save_screenshot_sequence(
            prefix="ark_screenshot",
            directory=args.output,
            interval=args.interval,
            limit=args.limit
        )
    
    else:
        # Just capture and display a screenshot
        img = capture_screenshot()
        cv2.imshow("Screenshot", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        cv2.waitKey(0)
        cv2.destroyAllWindows()