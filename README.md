# ARK Ascended UI Detector & Automation System

A complete solution for detecting and automating UI interactions in ARK: Survival Ascended using YOLOv8 object detection.

## Quick Start Guide

### 1. Install Requirements

```bash
pip install ultralytics opencv-python pyautogui mss keyboard numpy pyyaml
```

### 2. Collect Training Data

```bash
python 1_collect_screenshots.py --interval 3 --limit 200
```

### 3. Annotate Your Screenshots

Follow the instructions in `2_annotate_instructions.md` to annotate your screenshots using Roboflow (free tier).

### 4. Prepare Your Dataset

```bash
python 3_prepare_dataset.py --source dataset --output dataset_yolo
```

### 5. Train Your Model

```bash
python 4_train_model.py
```

### 6. Test Real-time Detection

```bash
python detection_visualizer.py --weights runs/ark_ui_detector_*/weights/best.pt
```

### 7. Use Automation Example

```bash
python run_automation.py --script inventory_manager --weights runs/ark_ui_detector_*/weights/best.pt
```

## Project Structure

- `1_collect_screenshots.py` - Tool to capture gameplay screenshots
- `2_annotate_instructions.md` - Guide for labeling UI elements
- `3_prepare_dataset.py` - Script to organize your dataset for training
- `4_train_model.py` - YOLOv8 training script
- `model_config.yaml` - YOLOv8 configuration
- `detection_visualizer.py` - Real-time visualization tool
- `ark_ui_automation.py` - Core automation class
- `inventory_manager.py` - Example automation script
- `run_automation.py` - Automation script launcher

## Customization

1. **Train with your own data**:
   - Collect ARK screenshots using the provided tool
   - Label them according to the annotation guide
   - Train the model with your custom dataset

2. **Create custom automation scripts**:
   - Use `inventory_manager.py` as a template
   - Create new scripts in the `examples` folder
   - Run them with `run_automation.py`

## Example Commands

### Training with GPU #1

```bash
python 4_train_model.py --device 1
```

### Running with Lower Confidence Threshold

```bash
python run_automation.py --script inventory_manager --weights your_model.pt --confidence 0.3
```

### Just Testing Detection

```bash
python run_automation.py --visualize --weights your_model.pt
```

## Notes

- For best results, use screenshots from your specific game configuration (resolution, UI scale)
- This system is designed for education and experimentation purposes only
- Always ensure automation complies with the game's terms of service