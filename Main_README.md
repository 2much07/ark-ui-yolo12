# ARK Ascended UI Detector & Automation System

A complete solution for detecting and automating UI interactions in ARK: Survival Ascended using YOLOv8 object detection.

## Overview

This project consists of two main components:

1. **YOLOv8 UI Detector**: Train a custom YOLOv8 model to detect UI elements in ARK: Survival Ascended.
2. **Automation System**: Use the trained model to automate game tasks by interacting with the detected UI elements.

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

## Installation

### Requirements

- Python 3.8+
- CUDA-capable NVIDIA GPU (recommended)
- ARK: Survival Ascended

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/ark-ui-detector.git
cd ark-ui-detector
```

2. **Create a virtual environment**

```bash
# Create environment
python -m venv ark_env

# Activate environment
# On Windows:
ark_env\Scripts\activate
# On macOS/Linux:
source ark_env/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

## Quick Start Guide

### 1. Collect Training Data

```bash
# Collect screenshots while playing ARK
python training/1_screenshot_collector.py --interval 3 --limit 200
```

### 2. Annotate Data

1. Follow instructions in `training/2_annotate_instructions.md` to annotate your data
2. Use [Roboflow](https://roboflow.com) for the easiest annotation experience (free tier available)
3. Download your dataset in YOLOv8 format

### 3. Prepare Dataset

```bash
python training/3_dataset_preparation.py --source dataset --output dataset_yolo
```

### 4. Train Model

```bash
python training/4_train_model.py
```

The training process will output the best model weights in `runs/ark_ui_detector_*/weights/best.pt`.

### 5. Evaluate Model

```bash
python training/5_evaluate_model.py --weights runs/ark_ui_detector_*/weights/best.pt
```

### 6. Test Real-time Detection

```bash
python automation/detection_visualizer.py --weights runs/ark_ui_detector_*/weights/best.pt
```

### 7. Run Automation Examples

```bash
python automation/run_automation.py --script inventory_manager --weights runs/ark_ui_detector_*/weights/best.pt
```

## Available Automation Scripts

- **inventory_manager.py** - Manage inventory items, sort them, and transfer to storage
- **crafting_helper.py** - Automate crafting of items using the crafting menu
- **taming_assistant.py** - Assist with creature taming, automatically applying narcotics and food
- **resource_gatherer.py** - Help with efficient resource gathering and tool selection

## Creating Custom Automation Scripts

You can create your own automation scripts by following the example structure:

```python
"""
My custom ARK automation script
"""
import os
import sys
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
    
    # Perform custom actions...
    
    # Close inventory
    ark.close_inventory()
    
    return True

def main():
    parser = argparse.ArgumentParser(description="My Custom ARK Automation")
    parser.add_argument("--weights", "-w", required=True, help="Path to trained model weights")
    
    args = parser.parse_args()
    
    # Initialize the ARK UI automation
    with ArkUIAutomation(args.weights, confidence=0.4) as ark:
        logger.info("My custom automation started")
        
        # Run your custom function
        result = my_custom_function(ark)
        
        logger.info("My custom automation completed")

if __name__ == "__main__":
    main()
```

## Updating the Model

As ARK receives updates or you encounter new UI elements, you can update your model:

```bash
python training/7_model_updater.py --weights your_best_model.pt --data config/ark_ui_data.yaml
```

## Additional Examples

### Starting Taming Monitor

```bash
python automation/run_automation.py --script taming_assistant --weights your_model.pt --creature raptor --monitor --duration 3600
```

### Multi-Resource Gathering

```bash
python automation/run_automation.py --script resource_gatherer --weights your_model.pt --multi
```

### Lower Confidence Threshold

```bash
python automation/run_automation.py --script inventory_manager --weights your_model.pt --confidence 0.3
```

## Tips for Best Results

1. **Collect Diverse Data**: Capture screenshots in various game scenarios and UI states
2. **Annotate Consistently**: Be consistent in how you draw bounding boxes around similar elements
3. **Balance Your Dataset**: Make sure you have enough examples of each UI element
4. **Test Real-time Detection**: Use the detection visualizer to check how well your model works
5. **Start Simple**: Begin with basic automations before attempting complex sequences

## Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [ARK: Survival Ascended](https://playark.com/ascended)
- [Roboflow](https://roboflow.com) for annotation tools

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Use at your own risk. Automation tools may violate the terms of service of some games. Always check the ToS before using automation software.
