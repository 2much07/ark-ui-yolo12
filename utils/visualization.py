"""
Utility functions for visualizing UI detections.
"""
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import yaml
import pandas as pd

def visualize_dataset_samples(dataset_path, data_yaml, num_samples=5, output_dir="visualization"):
    """
    Visualize random samples from the dataset with annotations.
    
    Args:
        dataset_path: Path to the YOLOv8 dataset
        data_yaml: Path to data.yaml file
        num_samples: Number of samples to visualize
        output_dir: Directory to save visualizations
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load class names
    with open(data_yaml, 'r') as f:
        data = yaml.safe_load(f)
    class_names = data['names']
    
    # Define colors for different classes
    np.random.seed(42)
    colors = {cls_id: tuple(map(int, np.random.randint(0, 255, size=3))) for cls_id in class_names}
    
    # Get training images
    train_images_dir = os.path.join(dataset_path, 'train', 'images')
    train_labels_dir = os.path.join(dataset_path, 'train', 'labels')
    
    if not os.path.exists(train_images_dir):
        print(f"Training images directory not found: {train_images_dir}")
        return
    
    # Get image files
    image_files = []
    for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
        image_files.extend(list(Path(train_images_dir).glob(f"*{ext}")))
    
    if not image_files:
        print(f"No image files found in {train_images_dir}")
        return
    
    # Select random samples
    if len(image_files) > num_samples:
        import random
        image_files = random.sample(image_files, num_samples)
    
    # Process each sample
    for img_path in image_files:
        # Get corresponding label file
        label_path = Path(os.path.join(train_labels_dir, img_path.stem + '.txt'))
        
        if not label_path.exists():
            print(f"Label file not found: {label_path}")
            continue
        
        # Read image
        img = cv2.imread(str(img_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Get image dimensions
        height, width, _ = img.shape
        
        # Read labels
        with open(label_path, 'r') as f:
            for line in f:
                values = line.strip().split()
                if len(values) >= 5:
                    cls_id = int(values[0])
                    x_center = float(values[1]) * width
                    y_center = float(values[2]) * height
                    w = float(values[3]) * width
                    h = float(values[4]) * height
                    
                    # Calculate bounding box coordinates
                    x1 = int(x_center - w / 2)
                    y1 = int(y_center - h / 2)
                    x2 = int(x_center + w / 2)
                    y2 = int(y_center + h / 2)
                    
                    # Draw bounding box
                    color = colors[cls_id]
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                    
                    # Put class name
                    label = class_names[cls_id]
                    cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Save visualized image
        output_path = os.path.join(output_dir, f"sample_{img_path.stem}.jpg")
        plt.figure(figsize=(12, 8))
        plt.imshow(img)
        plt.axis('off')
        plt.title(f"Sample: {img_path.name}")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
    
    print(f"Visualization samples saved to {output_dir}")

def plot_training_results(results_csv, output_dir="visualization"):
    """
    Plot training metrics from a results.csv file generated during training.
    
    Args:
        results_csv: Path to results.csv file
        output_dir: Directory to save plots
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load results
    try:
        results = pd.read_csv(results_csv)
    except Exception as e:
        print(f"Error loading results file: {e}")
        return
    
    # Plot metrics
    metrics = [
        {'name': 'loss', 'columns': ['train/box_loss', 'train/cls_loss', 'train/dfl_loss'], 'title': 'Training Losses'},
        {'name': 'mAP', 'columns': ['metrics/mAP50(B)', 'metrics/mAP50-95(B)'], 'title': 'Validation mAP'},
        {'name': 'precision_recall', 'columns': ['metrics/precision(B)', 'metrics/recall(B)'], 'title': 'Precision and Recall'}
    ]
    
    for metric in metrics:
        plt.figure(figsize=(10, 6))
        
        for column in metric['columns']:
            if column in results.columns:
                plt.plot(results['epoch'], results[column], label=column)
        
        plt.title(metric['title'])
        plt.xlabel('Epoch')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        output_path = os.path.join(output_dir, f"{metric['name']}_plot.png")
        plt.savefig(output_path)
        plt.close()
    
    print(f"Training metric plots saved to {output_dir}")

def visualize_predictions(model, validation_images, class_names, conf_threshold=0.25, num_samples=5, output_dir="evaluation_results"):
    """
    Visualize model predictions on validation images.
    
    Args:
        model: YOLO model
        validation_images: Path to validation images
        class_names: Dictionary of class names
        conf_threshold: Confidence threshold for detections
        num_samples: Number of samples to visualize
        output_dir: Directory to save visualizations
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get validation images
    if os.path.isdir(validation_images):
        # If a directory is provided, get all image files
        image_paths = []
        for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            image_paths.extend(list(Path(validation_images).glob(f"*{ext}")))
    else:
        # If a single file is provided, use it
        image_paths = [Path(validation_images)]
    
    if not image_paths:
        print(f"No validation images found in {validation_images}")
        return
    
    # Select random samples
    if len(image_paths) > num_samples:
        import random
        image_paths = random.sample(image_paths, num_samples)
    
    print(f"\nVisualizing predictions on {len(image_paths)} validation images...")
    
    # Process each image
    for i, img_path in enumerate(image_paths):
        # Read image
        img = cv2.imread(str(img_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Create a figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
        
        # Original image
        ax1.imshow(img)
        ax1.set_title("Original Image")
        ax1.axis("off")
        
        # Run inference
        results = model.predict(source=img, conf=conf_threshold)[0]
        
        # Create a copy for drawing
        img_with_boxes = img.copy()
        
        # Define colors for different classes
        np.random.seed(42)
        colors = {}
        
        # Draw bounding boxes
        for box in results.boxes.cpu().numpy():
            x1, y1, x2, y2 = box.xyxy[0].astype(int)
            conf = box.conf[0]
            cls_id = int(box.cls[0])
            
            # Get class name
            cls_name = class_names.get(cls_id, f"Unknown-{cls_id}")
            
            # Get color for this class
            if cls_id not in colors:
                colors[cls_id] = tuple(map(int, np.random.randint(0, 255, size=3)))
            color = colors[cls_id]
            
            # Draw bounding box
            cv2.rectangle(img_with_boxes, (x1, y1), (x2, y2), color, 2)
            
            # Put class name and confidence
            label = f"{cls_name} {conf:.2f}"
            cv2.putText(img_with_boxes, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Show image with detections
        ax2.imshow(img_with_boxes)
        ax2.set_title("Predictions")
        ax2.axis("off")
        
        # Adjust layout and save figure
        plt.tight_layout()
        output_path = os.path.join(output_dir, f"prediction_{img_path.stem}.png")
        plt.savefig(output_path)
        plt.close()
    
    print(f"Prediction visualizations saved to {output_dir}")

def create_confusion_matrix(model, validation_images, class_names, output_dir="evaluation_results", conf_threshold=0.25):
    """
    Create a confusion matrix for model predictions.
    
    Args:
        model: YOLO model
        validation_images: Path to validation images
        class_names: Dictionary of class names
        output_dir: Directory to save visualization
        conf_threshold: Confidence threshold for detections
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get validation images and labels
    val_images_dir = validation_images
    val_labels_dir = validation_images.replace('images', 'labels')
    
    if not os.path.exists(val_images_dir) or not os.path.exists(val_labels_dir):
        print(f"Validation images or labels directory not found")
        return
    
    # Get image files
    image_files = []
    for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
        image_files.extend(list(Path(val_images_dir).glob(f"*{ext}")))
    
    if not image_files:
        print(f"No image files found in {val_images_dir}")
        return
    
    # Initialize confusion matrix
    num_classes = len(class_names)
    conf_matrix = np.zeros((num_classes, num_classes))
    
    # Process each image
    for img_path in image_files:
        # Get corresponding label file
        label_path = Path(os.path.join(val_labels_dir, img_path.stem + '.txt'))
        
        if not label_path.exists():
            continue
        
        # Read image
        img = cv2.imread(str(img_path))
        
        # Get image dimensions
        height, width, _ = img.shape
        
        # Read ground truth labels
        true_labels = []
        with open(label_path, 'r') as f:
            for line in f:
                values = line.strip().split()
                if len(values) >= 5:
                    cls_id = int(values[0])
                    x_center = float(values[1]) * width
                    y_center = float(values[2]) * height
                    w = float(values[3]) * width
                    h = float(values[4]) * height
                    
                    # Calculate bounding box coordinates
                    x1 = int(x_center - w / 2)
                    y1 = int(y_center - h / 2)
                    x2 = int(x_center + w / 2)
                    y2 = int(y_center + h / 2)
                    
                    true_labels.append({
                        'cls_id': cls_id,
                        'bbox': [x1, y1, x2, y2]
                    })
        
        # Run inference
        results = model.predict(source=img, conf=conf_threshold)[0]
        
        # Get predicted labels
        pred_labels = []
        for box in results.boxes.cpu().numpy():
            x1, y1, x2, y2 = box.xyxy[0].astype(int)
            conf = box.conf[0]
            cls_id = int(box.cls[0])
            
            pred_labels.append({
                'cls_id': cls_id,
                'bbox': [x1, y1, x2, y2],
                'conf': conf
            })
        
        # Match predictions to ground truth
        matched_true = set()
        
        for pred in pred_labels:
            best_iou = 0.5  # IoU threshold
            best_match = None
            
            for i, true in enumerate(true_labels):
                if i in matched_true:
                    continue
                
                # Calculate IoU
                iou = calculate_iou(pred['bbox'], true['bbox'])
                
                if iou > best_iou:
                    best_iou = iou
                    best_match = i
            
            if best_match is not None:
                # Record match in confusion matrix
                true_cls = true_labels[best_match]['cls_id']
                pred_cls = pred['cls_id']
                
                conf_matrix[true_cls, pred_cls] += 1
                matched_true.add(best_match)
            else:
                # False positive
                pred_cls = pred['cls_id']
                # No true class, so use pred_cls for both axes
                conf_matrix[pred_cls, pred_cls] += 0  # Don't count false positives in confusion matrix
    
    # Plot confusion matrix
    plt.figure(figsize=(12, 10))
    plt.imshow(conf_matrix, interpolation='nearest', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.colorbar()
    
    # Add axis labels
    tick_marks = np.arange(num_classes)
    plt.xticks(tick_marks, [class_names[i] for i in range(num_classes)], rotation=90)
    plt.yticks(tick_marks, [class_names[i] for i in range(num_classes)])
    
    # Add text
    thresh = conf_matrix.max() / 2
    for i in range(num_classes):
        for j in range(num_classes):
            plt.text(j, i, format(conf_matrix[i, j], 'd'),
                     horizontalalignment="center",
                     color="white" if conf_matrix[i, j] > thresh else "black")
    
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    
    # Save confusion matrix
    output_path = os.path.join(output_dir, 'confusion_matrix.png')
    plt.savefig(output_path)
    plt.close()
    
    print(f"Confusion matrix saved to {output_path}")

def calculate_iou(bbox1, bbox2):
    """Calculate IoU between two bounding boxes."""
    # Extract coordinates
    x1_1, y1_1, x2_1, y2_1 = bbox1
    x1_2, y1_2, x2_2, y2_2 = bbox2
    
    # Calculate area of intersection
    x_left = max(x1_1, x1_2)
    y_top = max(y1_1, y1_2)
    x_right = min(x2_1, x2_2)
    y_bottom = min(y2_1, y2_2)
    
    if x_right < x_left or y_bottom < y_top:
        return 0.0
    
    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    
    # Calculate area of both bounding boxes
    bbox1_area = (x2_1 - x1_1) * (y2_1 - y1_1)
    bbox2_area = (x2_2 - x1_2) * (y2_2 - y1_2)
    
    # Calculate IoU
    iou = intersection_area / float(bbox1_area + bbox2_area - intersection_area)
    
    return iou