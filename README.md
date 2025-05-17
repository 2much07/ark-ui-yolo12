# ARK Ascended UI Detector & Automation System

A complete solution for detecting and automating UI interactions in ARK: Survival Ascended using YOLOv8 object detection.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Comprehensive Tutorial](#comprehensive-tutorial)
  - [Step 1: Collect Training Data](#step-1-collect-training-data)
  - [Step 2: Annotate Your Screenshots](#step-2-annotate-your-screenshots)
  - [Step 3: Prepare Your Dataset](#step-3-prepare-your-dataset)
  - [Step 4: Train the Model](#step-4-train-the-model)
  - [Step 5: Evaluate Your Model](#step-5-evaluate-your-model)
  - [Step 6: Test Real-time Detection](#step-6-test-real-time-detection)
  - [Step 7: Use Automation Scripts](#step-7-use-automation-scripts)
- [Creating Custom Automation Scripts](#creating-custom-automation-scripts)
- [Updating Your Model](#updating-your-model)
- [Common Examples](#common-examples)
- [FAQ](#faq)
- [Troubleshooting](#troubleshooting)
- [Acknowledgments](#acknowledgments)
- [License](#license)
- [Disclaimer](#disclaimer)

## Overview

This project consists of two main components:

1. **YOLOv8 UI Detector**: Train a custom YOLOv8 model to detect UI elements in ARK: Survival Ascended.
2. **Automation System**: Use the trained model to automate game tasks by interacting with the detected UI elements.

The system first learns to recognize UI elements like buttons, inventory slots, status bars, etc., and then provides a framework to automate interactions with these elements.

## Features

- **Screenshot Collection** - Automatically capture gameplay screenshots for training
- **Dataset Preparation** - Tools to organize and prepare your training data
- **YOLOv8 Training** - Configuration optimized for UI detection
- **Real-time Detection** - Visualize UI elements in real-time
- **Automation Framework** - Build custom automation scripts
- **Example Scripts**:
  - Inventory Management
  - Crafting Helper
  - Taming Assistant
  - Resource Gathering

## Project Structure

```
ark_ui_master/
├── README.md                           # Project overview and instructions
├── requirements.txt                    # Dependencies for both projects
├── setup.py                            # Installation script
│
├── training/                           # YOLOv8 training pipeline
│   ├── 1_screenshot_collector.py       # Screenshot collection script
│   ├── 2_annotate_instructions.md      # Annotation guidelines
│   ├── 3_dataset_preparation.py        # Dataset organization script
│   ├── 4_train_model.py                # YOLOv8 training script
│   ├── 5_evaluate_model.py             # Model evaluation script
│   ├── 6_model_updater.py              # Model updating script
│   └── config/                         # Configuration files
│       ├── ark_ui_data.yaml            # Dataset configuration
│       └── model_config.yaml           # YOLOv8 model configuration
│
├── automation/                         # ARK UI Automation System
│   ├── ark_ui_automation.py            # Main automation class
│   ├── detection_visualizer.py         # Real-time UI visualization tool
│   ├── run_automation.py               # Automation script launcher
│   ├── examples/                       # Example automation scripts
│   │   ├── inventory_manager.py        # Inventory management example
│   │   ├── crafting_helper.py          # Crafting automation example
│   │   ├── taming_assistant.py         # Taming helper example
│   │   └── resource_gatherer.py        # Resource gathering example
│   └── config/                         # Automation configuration
│       └── automation_config.yaml      # Automation settings
│
└── utils/                              # Shared utilities
    ├── dataset_utils.py                # Dataset management utilities
    ├── visualization.py                # Visualization utilities
    ├── ark_ui_classes.py               # ARK UI class definitions
    ├── screenshot_utils.py             # Screenshot processing utilities
    └── ocr_utils.py                    # Optional OCR utilities
```

## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.8+** - The project requires Python 3.8 or newer
- **CUDA-capable NVIDIA GPU** (recommended) - For faster training and inference
- **ARK: Survival Ascended** - The game itself for collecting screenshots and testing automation
- **Admin rights** (Windows) or appropriate permissions - For taking screenshots and simulating inputs

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ark-ui-master.git
cd ark-ui-master
```

### 2. Create a Virtual Environment

```bash
# Create environment
python -m venv ark_env

# Activate environment
# On Windows:
ark_env\Scripts\activate
# On macOS/Linux:
source ark_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The requirements.txt file includes:
```
ultralytics>=8.0.0
torch>=2.0.0
torchvision>=0.15.0
opencv-python>=4.7.0
numpy>=1.23.5
pyautogui>=0.9.53
pillow>=9.5.0
matplotlib>=3.7.1
pyyaml>=6.0
tqdm>=4.65.0
keyboard>=0.13.5
mss>=6.1.0
```

## Comprehensive Tutorial

### Step 1: Collect Training Data

The first step is to collect screenshots from ARK: Survival Ascended to train your model.

**Detailed Instructions:**

1. Launch ARK: Survival Ascended.
2. Open a terminal/command prompt and activate your virtual environment.
3. Run the screenshot collector:

```bash
python training/1_screenshot_collector.py --output dataset --interval 3 --limit 200
```

**Parameters explained:**
- `--output` or `-o`: Directory to save screenshots (default: "dataset")
- `--interval` or `-i`: Time in seconds between screenshots (default: 2)
- `--limit` or `-l`: Maximum number of screenshots to take (default: none)
- `--hotkey`: Key to press to stop the collector (default: "f10")
- `--mode` or `-m`: Game mode tag to add to filenames (e.g., "inventory", "map")

**Tips for effective data collection:**
- Capture various UI states (inventory, crafting, map, etc.)
- Include different lighting conditions
- Capture with different UI scales if applicable
- Try to have good coverage of all UI elements you want to detect
- Collect at least 20-30 images of each UI element type

**Example workflow:**
```bash
# Collect inventory screenshots
python training/1_screenshot_collector.py --output dataset/inventory --interval 2 --limit 50 --mode inventory

# Collect crafting menu screenshots
python training/1_screenshot_collector.py --output dataset/crafting --interval 2 --limit 50 --mode crafting

# Collect map screenshots
python training/1_screenshot_collector.py --output dataset/map --interval 2 --limit 30 --mode map

# Collect general gameplay screenshots
python training/1_screenshot_collector.py --output dataset/gameplay --interval 3 --limit 70
```

During collection, the script will:
1. Wait for you to press any key to begin
2. Capture screenshots at the specified interval
3. Stop when the limit is reached or when you press the hotkey

### Step 2: Annotate Your Screenshots

Annotation involves drawing bounding boxes around UI elements and assigning them classes.

**Detailed Instructions:**

1. Sign up for a free Roboflow account at [roboflow.com](https://roboflow.com)
2. Create a new project named "ARK-Ascended-UI-Detector"
3. Select "Object Detection" as the project type
4. Select "YOLOv8" as the annotation format
5. Upload your screenshots from the dataset folder
6. Annotate your images according to the guidelines in `training/2_annotate_instructions.md`

**Annotation best practices:**
- Draw tight bounding boxes around each UI element
- Be consistent in how you label similar elements
- Include the full element in the box, not just part of it
- Create at least the following classes (you can add more):
  - health_bar - Character health bar (red)
  - stamina_bar - Character stamina bar (green)
  - food_bar - Character food bar (orange)
  - water_bar - Character water/hydration bar (blue)
  - weight_bar - Character weight indicator
  - inventory_tab - Inventory tab
  - crafting_tab - Crafting tab
  - inventory_slot - Individual inventory square
  - inventory_item - Item in inventory
  - close_button - X/close button
  - craft_button - Craft button in crafting menu

For a complete list of recommended classes, refer to the `utils/ark_ui_classes.py` file.

**Exporting your dataset:**
1. After annotation, go to the "Generate" tab in Roboflow
2. Set preprocessing:
   - Resize: 640x640 (maintain aspect ratio with padding)
   - Auto-orient: ON
   - Image quality: 100%
3. Set augmentations (optional but recommended):
   - Flip: OFF (UI elements have fixed orientation)
   - 90° Rotations: OFF (UI is always properly oriented)
   - Brightness: ±20% (accounts for different lighting)
   - Blur: Up to 1px (minor blur tolerance)
   - Noise: Up to 1% (slight noise tolerance)
4. Generate the dataset and download in YOLOv8 format
5. Extract the downloaded ZIP to your project folder

### Step 3: Prepare Your Dataset

Now you need to organize your dataset for YOLOv8 training.

**Detailed Instructions:**

1. Ensure you have your annotated data downloaded from Roboflow
2. Run the dataset preparation script:

```bash
python training/3_dataset_preparation.py --source path/to/downloaded/dataset --output dataset_yolo
```

**Parameters explained:**
- `--source` or `-s`: Source directory with images and labels (default: "dataset")
- `--output` or `-o`: Output directory for organized dataset (default: "dataset_yolo")
- `--train-ratio` or `-t`: Training data ratio (default: 0.8, meaning 80% train, 20% val)
- `--config` or `-c`: Path to save data.yaml (default: "config/ark_ui_data.yaml")

The script will:
1. Split your data into training and validation sets
2. Organize files into the YOLOv8 folder structure
3. Create a data.yaml file with class information
4. Verify the dataset structure and report statistics

**Expected output folder structure:**
```
dataset_yolo/
├── train/
│   ├── images/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── labels/
│       ├── image1.txt
│       ├── image2.txt
│       └── ...
└── val/
    ├── images/
    │   ├── image101.jpg
    │   ├── image102.jpg
    │   └── ...
    └── labels/
        ├── image101.txt
        ├── image102.txt
        └── ...
```

Verify your dataset by checking the summary printed by the script. It should show:
- Number of training images and labels
- Number of validation images and labels
- Class distribution
- Warning for any missing labels

### Step 4: Train the Model

With your dataset prepared, you can now train the YOLOv8 model.

**Detailed Instructions:**

1. Ensure your dataset is prepared (Step 3)
2. Run the training script:

```bash
python training/4_train_model.py --data config/ark_ui_data.yaml
```

**Parameters explained:**
- `--data` or `-d`: Path to data.yaml (default: "config/ark_ui_data.yaml")
- `--config` or `-c`: Path to model configuration (default: "config/model_config.yaml")
- `--output` or `-o`: Output directory (default: "runs")
- `--weights` or `-w`: Path to pretrained weights (optional)
- `--device`: Device to use (e.g., '0' for GPU 0, 'cpu' for CPU)

**Advanced options in model_config.yaml:**
- `model`: Base model to use (default: "yolov8s.pt")
- `epochs`: Number of training epochs (default: 100)
- `batch`: Batch size (default: 16)
- `imgsz`: Training image size (default: 640)
- `patience`: Early stopping patience (default: 20)
- Various augmentation settings

**Training process:**
1. The script loads the base YOLOv8 model
2. Configures training parameters
3. Runs training for the specified number of epochs
4. Saves the best model based on validation performance

**Monitoring the training:**
- The script outputs training progress including:
  - Epoch number
  - Loss values (box loss, class loss, etc.)
  - Metrics (mAP50, mAP50-95, precision, recall)
- Tensorboard logs are saved in the runs directory
- To view training plots, run `tensorboard --logdir runs`

**Training time depends on:**
- Your GPU capability
- Dataset size
- Number of epochs
- Model size (yolov8n is fastest, yolov8x is slowest but potentially more accurate)

### Step 5: Evaluate Your Model

After training, evaluate your model's performance on the validation set.

**Detailed Instructions:**

1. Run the evaluation script:

```bash
python training/5_evaluate_model.py --weights runs/ark_ui_detector_*/weights/best.pt
```

**Parameters explained:**
- `--weights` or `-w`: Path to trained weights (required)
- `--data` or `-d`: Path to data.yaml (default: "config/ark_ui_data.yaml")
- `--images` or `-i`: Path to validation images (optional)
- `--conf` or `-c`: Confidence threshold (default: 0.25)
- `--iou`: IoU threshold (default: 0.7)

The script will:
1. Load your trained model
2. Run validation on the validation dataset
3. Calculate precision, recall, mAP50, and mAP50-95
4. Visualize predictions on sample validation images
5. Create a confusion matrix (if applicable)

**Interpreting the results:**
- **mAP50**: Mean Average Precision at 50% IoU - higher is better
- **mAP50-95**: Mean Average Precision across IoU thresholds from 50% to 95% - higher is better
- **Precision**: How many of the detected objects are correct - higher is better
- **Recall**: How many of the actual objects are detected - higher is better

Look for a balance between precision and recall. A good model typically has:
- mAP50 > 0.8
- Precision > 0.8
- Recall > 0.8

For UI detection, it's often more important to have high precision to avoid incorrect interactions.

### Step 6: Test Real-time Detection

Now test your model's real-time detection capabilities.

**Detailed Instructions:**

1. Launch ARK: Survival Ascended
2. Run the detection visualizer:

```bash
python automation/detection_visualizer.py --weights runs/ark_ui_detector_*/weights/best.pt
```

**Parameters explained:**
- `--weights` or `-w`: Path to trained weights (required)
- `--data` or `-d`: Path to data.yaml (optional)
- `--conf` or `-c`: Confidence threshold (default: 0.4)
- `--delay`: Delay between frames in seconds (default: 0.05)
- `--no-fps`: Hide FPS counter (optional)

**Controls during visualization:**
- Press 'q' to quit
- Press 'c' to capture a screenshot
- Press '+' or '-' to adjust confidence threshold

The visualizer will:
1. Capture your screen in real-time
2. Run the model on each frame
3. Display detected UI elements with bounding boxes
4. Show confidence scores and class names
5. Count detections by class

**Tips for testing:**
- Try different game UI scenes (inventory, map, crafting, etc.)
- Adjust the confidence threshold to see how it affects detections
- Watch for false positives (incorrect detections) and false negatives (missed UI elements)
- Take screenshots of problem areas for future model improvement

### Step 7: Use Automation Scripts

Finally, use the automation scripts to interact with the detected UI elements.

**Detailed Instructions:**

1. Launch ARK: Survival Ascended
2. Run an automation script using the launcher:

```bash
python automation/run_automation.py --script inventory_manager --weights runs/ark_ui_detector_*/weights/best.pt
```

**Parameters explained:**
- `--script` or `-s`: Script to run (required)
- `--weights` or `-w`: Path to trained weights (required)
- `--list` or `-l`: List available scripts (optional)
- `--visualize` or `-v`: Run detection visualizer (optional)
- `--confidence` or `-c`: Detection confidence threshold (default: 0.4)

**Available example scripts:**
- `inventory_manager`: Manage inventory items, sort them, and transfer to storage
- `crafting_helper`: Automate crafting of items using the crafting menu
- `taming_assistant`: Assist with creature taming, applying narcotics and food
- `resource_gatherer`: Help with efficient resource gathering and tool selection

**Script-specific parameters:**
Different scripts accept additional parameters, for example:

```bash
# Inventory Manager
python automation/run_automation.py --script inventory_manager --weights your_model.pt --action transfer

# Crafting Helper
python automation/run_automation.py --script crafting_helper --weights your_model.pt --recipe stone_pick --quantity 5

# Taming Assistant
python automation/run_automation.py --script taming_assistant --weights your_model.pt --creature raptor --monitor --duration 3600

# Resource Gatherer
python automation/run_automation.py --script resource_gatherer --weights your_model.pt --resource wood --duration 60 --multi
```

**How automation works:**
1. The script captures the screen using MSS
2. Detects UI elements using your trained model
3. Uses pyautogui to simulate mouse clicks and keyboard inputs
4. Interacts with the detected UI elements to perform tasks

## Creating Custom Automation Scripts

You can create your own automation scripts to perform specific tasks.

**Step-by-step guide:**

1. Create a new Python file in the `automation/examples` folder (e.g., `my_custom_script.py`)
2. Use the following template:

```python
"""
My custom ARK automation script
"""
import os
import sys
import time
import logging
import argparse

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from ark_ui_automation import ArkUIAutomation

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('my_custom_script')

def my_custom_function(ark):
    """My custom automation function."""
    logger.info("Running my custom function")
    
    # Open inventory
    if not ark.is_element_present('inventory_tab'):
        ark.open_inventory()
    
    # Wait for inventory to appear
    ark.wait_for_element('inventory_slot', timeout=3)
    
    # Find a specific item
    item = ark.find_element('inventory_item')
    
    if item:
        # Click on it
        ark.click_element('inventory_item')
        logger.info("Found and clicked item")
    else:
        logger.warning("No items found")
    
    # Close inventory
    ark.close_inventory()
    
    return True

def main():
    parser = argparse.ArgumentParser(description="My Custom ARK Automation")
    parser.add_argument("--weights", "-w", required=True, help="Path to trained model weights")
    parser.add_argument("--confidence", "-c", type=float, default=0.4, help="Detection confidence threshold")
    
    args = parser.parse_args()
    
    # Initialize the ARK UI automation
    with ArkUIAutomation(args.weights, confidence=args.confidence) as ark:
        logger.info("My custom automation started")
        
        # Run your custom function
        result = my_custom_function(ark)
        
        logger.info("My custom automation completed")

if __name__ == "__main__":
    main()
```

3. Customize the script with your specific automation logic
4. Run your script using the launcher:

```bash
python automation/run_automation.py --script my_custom_script --weights your_model.pt
```

**Key ArkUIAutomation methods:**
- `find_element(element_name, confidence=None)`: Find a specific UI element
- `find_all_elements(element_name, confidence=None)`: Find all instances of a UI element
- `is_element_present(element_name, confidence=None)`: Check if a UI element is present
- `wait_for_element(element_name, timeout=10, confidence=None)`: Wait for a UI element to appear
- `click_element(element_name, confidence=None)`: Click on a UI element
- `double_click_element(element_name, confidence=None)`: Double-click on a UI element
- `right_click_element(element_name, confidence=None)`: Right-click on a UI element
- `drag_element(source_element, target_element)`: Drag one element to another
- `press_key(key)`: Press a keyboard key
- `press_and_hold(key, duration=1.0)`: Press and hold a key for a duration

**ARK-specific methods:**
- `open_inventory()`: Open the inventory
- `close_inventory()`: Close the inventory
- `switch_to_tab(tab_name)`: Switch to a specific tab
- `transfer_all_items(direction='to_container')`: Transfer all items
- `craft_item(item_name, engram_name=None)`: Craft an item
- `drop_item(item_name)`: Drop an item
- `check_player_status()`: Check player status bars
- and more...

**Tips for reliable automation:**
- Always check if elements are present before interacting
- Use `wait_for_element` to ensure UI elements have loaded
- Add appropriate delays between actions
- Handle errors gracefully
- Test thoroughly with different game states

## Updating Your Model

As ARK receives updates or you encounter new UI elements, you may need to update your model.

**Detailed Instructions:**

1. Collect new screenshots with the updated UI elements
2. Annotate them following the same guidelines as before
3. Run the model updater script:

```bash
python training/6_model_updater.py --weights your_best_model.pt --data config/ark_ui_data.yaml
```

**Parameters explained:**
- `--weights` or `-w`: Path to existing model weights (required)
- `--data` or `-d`: Path to data.yaml for the updated dataset (default: "training/config/ark_ui_data.yaml")
- `--output` or `-o`: Output directory (default: "runs")
- `--epochs` or `-e`: Number of additional training epochs (default: 50)
- `--batch` or `-b`: Batch size (default: 16)
- `--new-classes` or `-n`: Add new classes to model (optional)
- `--old-data`: Path to old data.yaml for class mapping (optional)
- `--mapping`: Path to save/load class mapping file (optional)

**Types of updates:**
1. **Fine-tuning** (default): Update the model with new examples of existing classes
2. **Adding new classes** (--new-classes): Add detection for new UI elements

**Example workflow for adding new classes:**
1. Update your dataset with examples of new UI elements
2. Update the class list in `utils/ark_ui_classes.py`
3. Prepare the updated dataset:

```bash
python training/3_dataset_preparation.py --source updated_dataset --output dataset_yolo_updated
```

4. Update the model with new classes:

```bash
python training/6_model_updater.py --weights your_best_model.pt --data config/ark_ui_data_updated.yaml --new-classes --old-data config/ark_ui_data.yaml --mapping class_mapping.yaml
```

## Common Examples

Here are some common usage examples:

### Training with GPU #1

```bash
python training/4_train_model.py --device 1
```

### Running with Lower Confidence Threshold

```bash
python automation/run_automation.py --script inventory_manager --weights your_model.pt --confidence 0.3
```

### Just Testing Detection

```bash
python automation/run_automation.py --visualize --weights your_model.pt
```

### Batch Crafting Multiple Items

```bash
python automation/run_automation.py --script crafting_helper --weights your_model.pt --batch
```

### Starting Long-Term Taming Monitor

```bash
python automation/run_automation.py --script taming_assistant --weights your_model.pt --creature rex --monitor --duration 7200
```

### Multi-Resource Gathering

```bash
python automation/run_automation.py --script resource_gatherer --weights your_model.pt --multi
```

### Listing Available Scripts

```bash
python automation/run_automation.py --list
```

## FAQ

**Q: What GPU do I need for training?**  
A: Any NVIDIA GPU with at least 4GB VRAM should work. More VRAM allows larger batch sizes and potentially faster training. For the best experience, an RTX 2060 or better is recommended.

**Q: How many screenshots do I need for good results?**  
A: For basic UI detection, aim for at least 100-200 annotated screenshots with good coverage of all UI elements. More complex detection may require 500+ images.

**Q: How long does training take?**  
A: Training time depends on your GPU, dataset size, and model complexity. On a mid-range GPU (e.g., RTX 3060), expect 1-3 hours for a complete training session with 100 epochs.

**Q: Can I use a CPU instead of a GPU?**  
A: Yes, but training will be much slower. For inference (running detection), a CPU can be adequate for simple use cases. Add `--device cpu` to use CPU mode.

**Q: How accurate is the UI detection?**  
A: With proper training data and annotation, you can achieve 90%+ accuracy for UI elements. Static UI elements (like inventory slots) typically have higher accuracy than dynamic elements.

**Q: Will this work with modded ARK UI?**  
A: Yes, but you'll need to train on screenshots with the modded UI. Different UI mods may require different training datasets.

**Q: Is this against ARK's terms of service?**  
A: This tool is for educational purposes. Some games consider automation tools against their terms of service. Always check the game's terms before using automation in online play.

**Q: Does this work with other games?**  
A: The framework can be adapted to other games by collecting appropriate screenshots and training a new model.

**Q: How do I add detection for new UI elements?**  
A: Collect screenshots showing the new elements, annotate them, add the new class to your data.yaml, and train an updated model using the model updater script.

**Q: Can this automate PvP or combat?**  
A: The system is primarily designed for UI automation like inventory management and crafting. Combat automation is more complex and requires additional techniques beyond UI detection.

## Troubleshooting

### Common Issues and Solutions

**Error: "ModuleNotFoundError: No module named 'ultralytics'"**  
Solution: Ensure you've installed all requirements with `pip install -r requirements.txt`

**Error: "CUDA out of memory"**  
Solution: Reduce batch size in model_config.yaml, or use a smaller model like yolov8n.pt

**Problem: Model detects UI elements but with low confidence**  
Solution: 
1. Add more training data with clearer examples
2. Increase training epochs
3. Lower the confidence threshold during detection

**Problem: Automation clicks are offset or inaccurate**  
Solution:
1. Ensure you're running the game at the same resolution used during training
2. Check if Windows display scaling is affecting coordinates
3. Try setting `pyautogui.FAILSAFE = False` for troubleshooting

**Problem: Training terminates early without good results**  
Solution:
1. Increase the patience parameter in model_config.yaml
2. Check your dataset for annotation errors
3. Use a larger model (e.g., yolov8m.pt instead of yolov8s.pt)

**Error: "Unable to open capture device"**  
Solution: Make sure you have administrator rights, and no other program is accessing the screen capture API

**Warning: Too many false positives or false negatives**  
Solution:
1. Add more varied training data
2. Balance your dataset across all classes
3. Adjust the confidence threshold
4. Train for more epochs

## Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [ARK: Survival Ascended](https://playark.com/ascended)
- [Roboflow](https://roboflow.com) for annotation tools
- [PyAutoGUI](https://pyautogui.readthedocs.io) for automation
- [MSS](https://python-mss.readthedocs.io) for fast screen capture

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Use at your own risk. Automation tools may violate the terms of service of some games. Always check the ToS before using automation software. The developers of this project are not responsible for any consequences resulting from the use of this software.
