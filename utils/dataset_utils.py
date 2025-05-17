"""
Utility functions for dataset preparation and management.
"""
import os
import cv2
import numpy as np
from pathlib import Path
import random
import shutil
import time

def create_directory(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    return False

def get_image_files(directory, image_extensions=['.jpg', '.jpeg', '.png', '.bmp']):
    """Get all image files in a directory."""
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(list(Path(directory).glob(f"*{ext}")))
    
    return image_files

def verify_dataset(dataset_path):
    """
    Verify dataset integrity.
    
    Args:
        dataset_path: Path to the YOLOv8 dataset
        
    Returns:
        dict: Dataset statistics
    """
    stats = {
        'train_images': 0,
        'train_labels': 0,
        'val_images': 0,
        'val_labels': 0,
        'missing_train_labels': [],
        'missing_val_labels': [],
        'empty_labels': [],
        'class_distribution': {}
    }
    
    # Check training images and labels
    train_images_dir = os.path.join(dataset_path, 'train', 'images')
    train_labels_dir = os.path.join(dataset_path, 'train', 'labels')
    
    if os.path.exists(train_images_dir):
        train_images = get_image_files(train_images_dir)
        stats['train_images'] = len(train_images)
        
        for img_path in train_images:
            label_path = Path(os.path.join(train_labels_dir, img_path.stem + '.txt'))
            
            if label_path.exists():
                stats['train_labels'] += 1
                
                # Check if label file is empty
                if os.path.getsize(label_path) == 0:
                    stats['empty_labels'].append(str(label_path))
                
                # Count class distribution
                with open(label_path, 'r') as f:
                    for line in f:
                        values = line.strip().split()
                        if len(values) >= 5:
                            cls_id = int(values[0])
                            if cls_id not in stats['class_distribution']:
                                stats['class_distribution'][cls_id] = 0
                            stats['class_distribution'][cls_id] += 1
            else:
                stats['missing_train_labels'].append(str(img_path))
    
    # Check validation images and labels
    val_images_dir = os.path.join(dataset_path, 'val', 'images')
    val_labels_dir = os.path.join(dataset_path, 'val', 'labels')
    
    if os.path.exists(val_images_dir):
        val_images = get_image_files(val_images_dir)
        stats['val_images'] = len(val_images)
        
        for img_path in val_images:
            label_path = Path(os.path.join(val_labels_dir, img_path.stem + '.txt'))
            
            if label_path.exists():
                stats['val_labels'] += 1
                
                # Check if label file is empty
                if os.path.getsize(label_path) == 0:
                    stats['empty_labels'].append(str(label_path))
                
                # Count class distribution
                with open(label_path, 'r') as f:
                    for line in f:
                        values = line.strip().split()
                        if len(values) >= 5:
                            cls_id = int(values[0])
                            if cls_id not in stats['class_distribution']:
                                stats['class_distribution'][cls_id] = 0
                            stats['class_distribution'][cls_id] += 1
            else:
                stats['missing_val_labels'].append(str(img_path))
    
    return stats

def extract_frames_from_video(video_path, output_dir, frame_interval=30):
    """
    Extract frames from a video file at specified intervals.
    
    Args:
        video_path: Path to video file
        output_dir: Directory to save extracted frames
        frame_interval: Number of frames to skip between extractions
    
    Returns:
        int: Number of frames extracted
    """
    # Create output directory
    create_directory(output_dir)
    
    # Open video file
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        print(f"Error: Could not open video {video_path}")
        return 0
    
    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    
    print(f"Video: {video_path}")
    print(f"FPS: {fps}")
    print(f"Total frames: {frame_count}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Extracting frames every {frame_interval} frames...")
    
    # Extract frames
    count = 0
    frame_id = 0
    
    while True:
        ret, frame = video.read()
        
        if not ret:
            break
        
        if frame_id % frame_interval == 0:
            # Save frame
            output_path = os.path.join(output_dir, f"frame_{count:06d}.jpg")
            cv2.imwrite(output_path, frame)
            count += 1
        
        frame_id += 1
        
        # Display progress
        if frame_id % 100 == 0:
            progress = frame_id / frame_count * 100
            print(f"Progress: {progress:.1f}% ({frame_id}/{frame_count})")
    
    # Release resources
    video.release()
    
    print(f"Extracted {count} frames to {output_dir}")
    return count

def balance_dataset(dataset_path, max_per_class=500, output_path=None):
    """
    Balance the dataset by limiting the number of images per class.
    
    Args:
        dataset_path: Path to the YOLOv8 dataset
        max_per_class: Maximum number of images per class
        output_path: Path to save the balanced dataset (optional)
        
    Returns:
        dict: Statistics before and after balancing
    """
    # Verify dataset
    before_stats = verify_dataset(dataset_path)
    
    # Get class distribution
    class_distribution = before_stats['class_distribution']
    
    # Find classes with too many samples
    classes_to_balance = {cls_id: count for cls_id, count in class_distribution.items() if count > max_per_class}
    
    if not classes_to_balance:
        print("Dataset is already balanced.")
        return {"before": before_stats, "after": before_stats}
    
    print(f"Classes to balance: {classes_to_balance}")
    
    # Create a temporary directory for balanced dataset if no output path is provided
    if output_path is None:
        output_path = dataset_path + "_balanced"
    
    # Copy dataset structure
    for split in ['train', 'val']:
        for subdir in ['images', 'labels']:
            create_directory(os.path.join(output_path, split, subdir))
    
    # Process each split
    for split in ['train', 'val']:
        images_dir = os.path.join(dataset_path, split, 'images')
        labels_dir = os.path.join(dataset_path, split, 'labels')
        
        # Get all image files
        image_files = get_image_files(images_dir)
        
        # Count instances of each class in each image
        image_classes = {}
        
        for img_path in image_files:
            label_path = Path(os.path.join(labels_dir, img_path.stem + '.txt'))
            
            if label_path.exists() and os.path.getsize(label_path) > 0:
                image_classes[str(img_path)] = []
                
                with open(label_path, 'r') as f:
                    for line in f:
                        values = line.strip().split()
                        if len(values) >= 5:
                            cls_id = int(values[0])
                            image_classes[str(img_path)].append(cls_id)
        
        # Count how many images to keep for each class
        class_counts = {cls_id: 0 for cls_id in classes_to_balance}
        
        # Select images to copy
        images_to_copy = set()
        
        # First, add images that don't have any classes to balance
        for img_path, classes in image_classes.items():
            if not any(cls_id in classes_to_balance for cls_id in classes):
                images_to_copy.add(img_path)
        
        # Then, add images that have classes to balance until we reach the max
        for img_path, classes in image_classes.items():
            if img_path in images_to_copy:
                continue
                
            relevant_classes = [cls_id for cls_id in classes if cls_id in classes_to_balance]
            
            can_add = True
            for cls_id in relevant_classes:
                if class_counts[cls_id] >= max_per_class:
                    can_add = False
                    break
            
            if can_add:
                images_to_copy.add(img_path)
                for cls_id in relevant_classes:
                    class_counts[cls_id] += 1
        
        # Copy selected images and their labels
        for img_path in images_to_copy:
            img_path = Path(img_path)
            label_path = Path(os.path.join(labels_dir, img_path.stem + '.txt'))
            
            # Destination paths
            dest_img_path = os.path.join(output_path, split, 'images', img_path.name)
            dest_label_path = os.path.join(output_path, split, 'labels', label_path.name)
            
            # Copy files
            shutil.copy(img_path, dest_img_path)
            shutil.copy(label_path, dest_label_path)
    
    # Verify balanced dataset
    after_stats = verify_dataset(output_path)
    
    print(f"Original dataset: {before_stats['train_images']} training images, {before_stats['val_images']} validation images")
    print(f"Balanced dataset: {after_stats['train_images']} training images, {after_stats['val_images']} validation images")
    
    return {"before": before_stats, "after": after_stats, "balanced_path": output_path}

def augment_dataset(dataset_path, output_path, augmentation_factor=2):
    """
    Augment the dataset by creating modified copies of images.
    
    Args:
        dataset_path: Path to the YOLOv8 dataset
        output_path: Path to save the augmented dataset
        augmentation_factor: How many augmented copies to create for each image
        
    Returns:
        dict: Statistics before and after augmentation
    """
    # Create output directory structure
    for split in ['train', 'val']:
        for subdir in ['images', 'labels']:
            create_directory(os.path.join(output_path, split, subdir))
    
    # Copy original data and augment
    for split in ['train', 'val']:
        images_dir = os.path.join(dataset_path, split, 'images')
        labels_dir = os.path.join(dataset_path, split, 'labels')
        
        # Get all image files
        image_files = get_image_files(images_dir)
        
        for img_path in image_files:
            # Copy original image and label
            original_img_path = str(img_path)
            original_label_path = os.path.join(labels_dir, img_path.stem + '.txt')
            
            # Check if label exists
            if not os.path.exists(original_label_path):
                continue
            
            # Destination paths for original
            dest_img_path = os.path.join(output_path, split, 'images', img_path.name)
            dest_label_path = os.path.join(output_path, split, 'labels', img_path.stem + '.txt')
            
            # Copy original files
            shutil.copy(original_img_path, dest_img_path)
            shutil.copy(original_label_path, dest_label_path)
            
            # Read image and labels
            img = cv2.imread(original_img_path)
            if img is None:
                continue
                
            with open(original_label_path, 'r') as f:
                labels = f.readlines()
            
            # Generate augmented versions
            for i in range(augmentation_factor):
                # Create augmented filename
                aug_img_path = os.path.join(output_path, split, 'images', f"{img_path.stem}_aug{i+1}{img_path.suffix}")
                aug_label_path = os.path.join(output_path, split, 'labels', f"{img_path.stem}_aug{i+1}.txt")
                
                # Apply augmentations - for UI we'll use mild adjustments
                # Brightness and contrast change
                img_aug = img.copy()
                
                # Random brightness adjustment (0.8-1.2)
                alpha = 0.8 + random.random() * 0.4
                beta = random.randint(-10, 10)
                img_aug = cv2.convertScaleAbs(img_aug, alpha=alpha, beta=beta)
                
                # Save augmented image
                cv2.imwrite(aug_img_path, img_aug)
                
                # Copy labels (no geometric transformations, so labels unchanged)
                with open(aug_label_path, 'w') as f:
                    f.writelines(labels)
    
    # Verify augmented dataset
    before_stats = verify_dataset(dataset_path)
    after_stats = verify_dataset(output_path)
    
    print(f"Original dataset: {before_stats['train_images']} training images, {before_stats['val_images']} validation images")
    print(f"Augmented dataset: {after_stats['train_images']} training images, {after_stats['val_images']} validation images")
    
    return {"before": before_stats, "after": after_stats}