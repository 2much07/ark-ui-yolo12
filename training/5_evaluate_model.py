"""
Evaluate YOLOv8 model for ARK UI Detection.
"""
import os
import argparse
import yaml
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
from ultralytics import YOLO
from tqdm import tqdm

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.visualization import visualize_predictions, create_evaluation_report

def load_classes(data_yaml):
    """Load class names from data.yaml file."""
    with open(data_yaml, 'r') as f:
        data = yaml.safe_load(f)
    return data['names']

def evaluate_model(weights_path, data_yaml, validation_images=None, conf_threshold=0.25, iou_threshold=0.7):
    """
    Evaluate YOLOv8 model on validation images.
    
    Args:
        weights_path: Path to trained model weights
        data_yaml: Path to data.yaml file
        validation_images: Path to validation images (optional)
        conf_threshold: Confidence threshold for detections
        iou_threshold: IoU threshold for NMS
    """
    print("\n=== ARK UI Detector Evaluation ===")
    print(f"Model: {weights_path}")
    print(f"Data: {data_yaml}")
    print(f"Confidence threshold: {conf_threshold}")
    print(f"IoU threshold: {iou_threshold}")
    print("===================================\n")
    
    # Load model
    model = YOLO(weights_path)
    
    # Load class names
    class_names = load_classes(data_yaml)
    
    # Validate on validation dataset
    print("Validating model on validation dataset...")
    metrics = model.val(data=data_yaml, conf=conf_threshold, iou=iou_threshold, verbose=True)
    
    print("\n=== Validation Results ===")
    print(f"mAP50: {metrics.box.map50:.4f}")
    print(f"mAP50-95: {metrics.box.map:.4f}")
    print(f"Precision: {metrics.box.precision:.4f}")
    print(f"Recall: {metrics.box.recall:.4f}")
    
    # If validation images are provided, visualize some predictions
    if validation_images:
        visualize_predictions(
            model, 
            validation_images, 
            class_names, 
            conf_threshold=conf_threshold,
            num_samples=5, 
            output_dir="evaluation_results"
        )
    
    # Create detailed evaluation report
    create_evaluation_report(metrics, class_names, "evaluation_results")
    
    return metrics

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate YOLOv8 for ARK UI Detection")
    parser.add_argument("--weights", "-w", required=True, help="Path to trained weights")
    parser.add_argument("--data", "-d", default="training/config/ark_ui_data.yaml", help="Path to data.yaml")
    parser.add_argument("--images", "-i", default=None, help="Path to validation images")
    parser.add_argument("--conf", "-c", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--iou", type=float, default=0.7, help="IoU threshold")
    
    args = parser.parse_args()
    
    # If no validation images provided, try to use the validation set from data.yaml
    if args.images is None:
        try:
            with open(args.data, 'r') as f:
                data_config = yaml.safe_load(f)
            
            if 'path' in data_config and 'val' in data_config:
                val_path = os.path.join(data_config['path'], data_config['val'])
                if os.path.exists(val_path):
                    args.images = val_path
        except Exception as e:
            print(f"Error determining validation path: {e}")
    
    evaluate_model(args.weights, args.data, args.images, args.conf, args.iou)
    
    print("\nNext step: Run 'python -m automation.examples.inventory_manager --weights your_model.pt' to test automation.")