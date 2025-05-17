"""
OCR utilities for reading text from ARK UI elements.
This module provides functions to extract text from UI elements using OCR.
Note: This requires either pytesseract or easyocr to be installed.
"""
import cv2
import numpy as np
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('ocr_utils')

# Try to import OCR libraries
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    logger.warning("pytesseract not installed. Install with: pip install pytesseract")
    logger.warning("You also need to install Tesseract OCR: https://github.com/tesseract-ocr/tesseract")
    TESSERACT_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
    # Initialize reader lazily when needed
    READER = None
except ImportError:
    logger.warning("easyocr not installed. Install with: pip install easyocr")
    EASYOCR_AVAILABLE = False

def preprocess_image(image, preprocess_type='default'):
    """
    Preprocess image for better OCR results.
    
    Args:
        image: Input image (numpy array)
        preprocess_type: Type of preprocessing to apply
        
    Returns:
        Preprocessed image
    """
    # Convert to grayscale if it's a color image
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    if preprocess_type == 'default':
        # Apply thresholding to get black text on white background
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        # Apply slight blur to reduce noise
        processed = cv2.GaussianBlur(thresh, (3, 3), 0)
    
    elif preprocess_type == 'adaptive':
        # Use adaptive thresholding for varying lighting
        processed = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
    
    elif preprocess_type == 'ark_ui':
        # Special processing for ARK UI text (often blue/cyan on dark background)
        # Invert colors for better recognition
        gray = cv2.bitwise_not(gray)
        
        # Increase contrast
        alpha = 1.5  # Contrast control
        beta = 0     # Brightness control
        processed = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
        
        # Apply thresholding
        _, processed = cv2.threshold(processed, 150, 255, cv2.THRESH_BINARY)
    
    else:
        processed = gray
    
    return processed

def read_text_tesseract(image, preprocess_type='default', config='--psm 6'):
    """
    Extract text from image using Tesseract OCR.
    
    Args:
        image: Input image (numpy array)
        preprocess_type: Type of preprocessing to apply
        config: Tesseract configuration string
        
    Returns:
        Extracted text
    """
    if not TESSERACT_AVAILABLE:
        logger.error("Tesseract OCR not available. Please install pytesseract and Tesseract OCR.")
        return None
    
    try:
        # Preprocess image
        processed_img = preprocess_image(image, preprocess_type)
        
        # Extract text
        text = pytesseract.image_to_string(processed_img, config=config)
        
        return text.strip()
    except Exception as e:
        logger.error(f"Error in Tesseract OCR: {str(e)}")
        return None

def read_text_easyocr(image, preprocess_type='default'):
    """
    Extract text from image using EasyOCR.
    
    Args:
        image: Input image (numpy array)
        preprocess_type: Type of preprocessing to apply
        
    Returns:
        Extracted text
    """
    global READER
    
    if not EASYOCR_AVAILABLE:
        logger.error("EasyOCR not available. Please install easyocr.")
        return None
    
    try:
        # Initialize reader if not already done
        if READER is None:
            READER = easyocr.Reader(['en'])
        
        # Preprocess image
        processed_img = preprocess_image(image, preprocess_type)
        
        # Extract text
        results = READER.readtext(processed_img)
        
        # Combine all detected text
        text = ' '.join([result[1] for result in results])
        
        return text.strip()
    except Exception as e:
        logger.error(f"Error in EasyOCR: {str(e)}")
        return None

def read_text(image, preprocess_type='default', engine='auto'):
    """
    Extract text from image using available OCR engine.
    
    Args:
        image: Input image (numpy array)
        preprocess_type: Type of preprocessing to apply
        engine: OCR engine to use ('tesseract', 'easyocr', or 'auto')
        
    Returns:
        Extracted text
    """
    if engine == 'auto':
        # Try tesseract first, then easyocr
        if TESSERACT_AVAILABLE:
            text = read_text_tesseract(image, preprocess_type)
        elif EASYOCR_AVAILABLE:
            text = read_text_easyocr(image, preprocess_type)
        else:
            logger.error("No OCR engine available. Please install pytesseract or easyocr.")
            return None
    elif engine == 'tesseract':
        if not TESSERACT_AVAILABLE:
            logger.error("Tesseract OCR not available. Please install pytesseract.")
            return None
        text = read_text_tesseract(image, preprocess_type)
    elif engine == 'easyocr':
        if not EASYOCR_AVAILABLE:
            logger.error("EasyOCR not available. Please install easyocr.")
            return None
        text = read_text_easyocr(image, preprocess_type)
    else:
        logger.error(f"Unknown OCR engine: {engine}")
        return None
    
    return text

def read_number(image, preprocess_type='default'):
    """
    Extract a number from an image.
    
    Args:
        image: Input image (numpy array)
        preprocess_type: Type of preprocessing to apply
        
    Returns:
        Extracted number or None if not found
    """
    # Read text
    text = read_text(image, preprocess_type)
    
    if text:
        # Try to extract number
        match = re.search(r'\d+', text)
        if match:
            try:
                return int(match.group())
            except ValueError:
                pass
    
    return None

def read_item_count(ark, item_element):
    """
    Read the stack count from an inventory item.
    
    Args:
        ark: ArkUIAutomation instance
        item_element: Detected UI element for the item
        
    Returns:
        Item count (int) or None if not found
    """
    if not item_element:
        return None
    
    # Get item coordinates
    x1, y1, x2, y2 = item_element['coords']
    
    # Get screenshot
    img = ark.sct.grab(ark.monitor)
    img_np = np.array(img)
    screen = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
    
    # Extract the bottom-right corner of the item (where count is typically shown)
    width = x2 - x1
    height = y2 - y1
    
    # Stack count is usually in the bottom right corner
    count_region_x1 = max(0, x2 - width // 3)
    count_region_y1 = max(0, y2 - height // 3)
    count_region = screen[count_region_y1:y2, count_region_x1:x2]
    
    # If the region is too small, return None
    if count_region.size == 0 or count_region.shape[0] < 10 or count_region.shape[1] < 10:
        return None
    
    # Try to read the number
    count = read_number(count_region, preprocess_type='ark_ui')
    
    return count

def read_durability(ark, item_element):
    """
    Read the durability percentage from an item.
    
    Args:
        ark: ArkUIAutomation instance
        item_element: Detected UI element for the item
        
    Returns:
        Durability percentage (float) or None if not found
    """
    # Similar to read_item_count, but focus on the durability bar area
    # This is a placeholder - actual implementation would need to be customized
    # based on the exact UI layout in ARK
    return None

def read_item_name_from_tooltip(ark, tooltip_element):
    """
    Read the item name from a tooltip.
    
    Args:
        ark: ArkUIAutomation instance
        tooltip_element: Detected UI element for the tooltip
        
    Returns:
        Item name (string) or None if not found
    """
    if not tooltip_element:
        return None
    
    # Get tooltip coordinates
    x1, y1, x2, y2 = tooltip_element['coords']
    
    # Get screenshot
    img = ark.sct.grab(ark.monitor)
    img_np = np.array(img)
    screen = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
    
    # Extract the top part of the tooltip (where name is typically shown)
    name_region_height = min(30, (y2 - y1) // 3)  # Assume name is in top third or 30px
    name_region = screen[y1:y1+name_region_height, x1:x2]
    
    # If the region is too small, return None
    if name_region.size == 0 or name_region.shape[0] < 10 or name_region.shape[1] < 10:
        return None
    
    # Try to read the text
    name = read_text(name_region, preprocess_type='ark_ui')
    
    return name

if __name__ == "__main__":
    # Test OCR functionality
    import argparse
    
    parser = argparse.ArgumentParser(description="Test OCR on an image")
    parser.add_argument("--image", "-i", required=True, help="Path to image")
    parser.add_argument("--preprocess", "-p", default="default", 
                      choices=["default", "adaptive", "ark_ui"], help="Preprocessing type")
    parser.add_argument("--engine", "-e", default="auto", 
                      choices=["auto", "tesseract", "easyocr"], help="OCR engine")
    
    args = parser.parse_args()
    
    # Load image
    image = cv2.imread(args.image)
    if image is None:
        print(f"Error: Could not load image {args.image}")
        exit(1)
    
    # Perform OCR
    text = read_text(image, args.preprocess, args.engine)
    
    # Print results
    print("\nOCR Results:")
    print("-----------")
    print(text if text else "No text detected")
    
    # Try to extract numbers
    number = read_number(image, args.preprocess)
    if number is not None:
        print(f"\nDetected number: {number}")
    
    # Display image and preprocessing
    processed = preprocess_image(image, args.preprocess)
    
    cv2.imshow("Original", image)
    cv2.imshow("Processed", processed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
