"""
Dataset preparation for ARK UI Detection.
This script prepares the dataset for training by organizing files and creating train/val splits.
"""
import os
import shutil
import random
import yaml
from pathlib import Path
import argparse
import sys

# Define ARK UI Classes
ARK_UI_CLASSES = [
    # Status elements
    'health_bar',         # Character health bar (red)
    'stamina_bar',        # Character stamina bar (green)
    'food_bar',           # Character food bar (orange)
    'water_bar',          # Character water/hydration bar (blue)
    'weight_bar',         # Character weight indicator
    'oxygen_bar',         # Oxygen bar when underwater (cyan)
    'torpidity_bar',      # Torpidity bar (purple)
    'xp_bar',             # Experience bar at bottom
    'level_icon',         # Level up notification icon
    
    # Alert messages
    'starvation_alert',   # "You're starving" red message
    'dehydration_alert',  # Water shortage alert
    'overweight_alert',   # "Too much weight" message
    'level_alert',        # "Level up is available" message
    'death_message',      # Death screen text
    'tribe_message',      # Tribe notifications
    
    # Inventory elements
    'inventory_slot',     # Individual inventory square
    'inventory_item',     # Item in inventory 
    'item_stack_count',   # Number on stacked items
    'item_durability',    # Durability bar on items
    'search_bar',         # Inventory search field
    'weight_indicator',   # Current/max weight display
    'transfer_all',       # Transfer all items button
    'drop_item',          # Drop item button
    
    # Item popup elements
    'item_name',          # Item name in tooltip
    'item_description',   # Item description text
    'craftable_label',    # "Craftable" indicator
    'blueprint_label',    # "Blueprint" indicator
    'engram_label',       # "Engram" label
    
    # Tab navigation
    'inventory_tab',      # Inventory tab
    'crafting_tab',       # Crafting tab
    'engram_tab',         # Engram tab
    'cosmetics_tab',      # Cosmetics/skins tab
    'tribe_tab',          # Tribe management tab
    'structure_tab',      # Structure tab for buildings
    
    # Map elements
    'map_marker',         # Icons on map
    'player_location',    # Player location indicator
    'beacon_marker',      # Beacon/drop markers
    'bed_marker',         # Bed/spawn point marker
    'waypoint',           # Custom waypoint marker
    
    # Menu buttons
    'back_button',        # Back button
    'close_button',       # X/close button
    'option_button',      # Settings/options button
    'craft_button',       # Craft button in crafting menu
    'learn_button',       # Learn button for engrams
    'unlock_button',      # Unlock button
    'transfer_button',    # Transfer button between inventories
    
    # Creature elements
    'taming_bar',         # Taming progress bar
    'breeding_bar',       # Breeding/maturation bar
    'creature_stats',     # Creature statistics panel
    'creature_inventory', # Creature inventory button
    'imprint_icon',       # Imprint icon/indicator
    
    # Structure elements
    'structure_health',   # Structure health bar
    'structure_name',     # Structure name label
    'storage_label',      # Storage count (e.g., "349/350")
    'fuel_indicator',     # Fuel level indicator
    'power_indicator',    # Power indicator (on/off)
    
    # HUD elements
    'compass',            # Top compass bar
    'hotbar',             # Bottom item hotbar
    'extended_hotbar',    # Extended radial hotbar (when open)
    'emote_wheel',        # Emote selection wheel
    'whistle_menu',       # Dino whistle command menu
    
    # Special menus
    'tek_element',        # Tek tier related UI elements
    'cryopod_menu',       # Cryopod interface elements
    'tek_transmitter',    # Tek transmitter elements
    'obelisk_terminal',   # Obelisk upload/download interface
    'mission_terminal',   # Mission/quest terminal interface
]

def create_directory(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    return False

def split_dataset(source_path, dataset_path, train_ratio=0.8):
    """
    Split the dataset into training and validation sets.
    
    Args:
        source_path: Path containing images and labels (from Roboflow or LabelImg)
        dataset_path: Path for the organized YOLOv8 dataset
        train_ratio: Portion of data to use for training (0.8 = 80% train, 20% val)
    """
    # Create directory structure
    create_directory(os.path.join(dataset_path, "train", "images"))
    create_directory(os.path.join(dataset_path, "train", "labels"))
    create_directory(os.path.join(dataset_path, "val", "images"))
    create_directory(os.path.join(dataset_path, "val", "labels"))
    
    print(f"Created directory structure in {dataset_path}")
    
    # Get all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = []
    
    # Check different possible directory structures
    for ext in image_extensions:
        # Check for flat structure
        image_files.extend(list(Path(source_path).glob(f"*{ext}")))
        
        # Check for Roboflow structure
        image_files.extend(list(Path(source_path).glob(f"train/images/*{ext}")))
        image_files.extend(list(Path(source_path).glob(f"valid/images/*{ext}")))
        image_files.extend(list(Path(source_path).glob(f"test/images/*{ext}")))
    
    # Remove duplicates
    image_files = list(set(image_files))
    
    if not image_files:
        print(f"No image files found in {source_path}")
        return False
    
    print(f"Found {len(image_files)} image files")
    
    # Shuffle and split
    random.shuffle(image_files)
    train_count = int(len(image_files) * train_ratio)
    
    train_files = image_files[:train_count]
    val_files = image_files[train_count:]
    
    print(f"Splitting into {len(train_files)} training and {len(val_files)} validation images")
    
    # Process training files
    successful_train_copies = 0
    for img_path in train_files:
        # Get corresponding label file
        label_path = find_label_file(img_path, source_path)
        
        if not label_path:
            print(f"Warning: No label file found for {img_path}")
            continue
        
        # Copy files
        if copy_dataset_file(img_path, label_path, dataset_path, "train"):
            successful_train_copies += 1
    
    # Process validation files
    successful_val_copies = 0
    for img_path in val_files:
        # Get corresponding label file
        label_path = find_label_file(img_path, source_path)
        
        if not label_path:
            print(f"Warning: No label file found for {img_path}")
            continue
        
        # Copy files
        if copy_dataset_file(img_path, label_path, dataset_path, "val"):
            successful_val_copies += 1
    
    print(f"\nDataset split complete:")
    print(f"- Training: {successful_train_copies}/{len(train_files)} files copied")
    print(f"- Validation: {successful_val_copies}/{len(val_files)} files copied")
    
    return successful_train_copies > 0 and successful_val_copies > 0

def find_label_file(img_path, source_path):
    """Find the corresponding label file for an image."""
    # Try direct .txt conversion
    label_path = Path(str(img_path).replace(img_path.suffix, '.txt'))
    if label_path.exists():
        return label_path
    
    # Check for Roboflow structure
    if 'images' in str(img_path):
        potential_label_path = Path(str(img_path).replace('images', 'labels').replace(img_path.suffix, '.txt'))
        if potential_label_path.exists():
            return potential_label_path
    
    # Search root directory
    potential_label_path = Path(os.path.join(source_path, img_path.stem + '.txt'))
    if potential_label_path.exists():
        return potential_label_path
    
    # Search labels directory
    potential_label_path = Path(os.path.join(source_path, 'labels', img_path.stem + '.txt'))
    if potential_label_path.exists():
        return potential_label_path
    
    return None

def copy_dataset_file(img_path, label_path, dataset_path, split):
    """Copy image and label files to appropriate directories."""
    try:
        # Copy image
        dest_img_path = os.path.join(dataset_path, split, "images", img_path.name)
        shutil.copy(img_path, dest_img_path)
        
        # Copy label
        dest_label_path = os.path.join(dataset_path, split, "labels", label_path.name)
        shutil.copy(label_path, dest_label_path)
        
        return True
    except Exception as e:
        print(f"Error copying files: {e}")
        return False

def create_data_yaml(dataset_path, classes, yaml_path):
    """
    Create the data.yaml file required by YOLOv8.
    
    Args:
        dataset_path: Path to the dataset
        classes: List of class names
        yaml_path: Path to save the yaml file
    """
    # Create class dictionary
    class_dict = {i: name for i, name in enumerate(classes)}
    
    # Create yaml content
    data = {
        'path': os.path.abspath(dataset_path),
        'train': os.path.join('train', 'images'),
        'val': os.path.join('val', 'images'),
        'names': class_dict
    }
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(yaml_path), exist_ok=True)
    
    # Write yaml file
    with open(yaml_path, 'w') as f:
        yaml.dump(data, f, sort_keys=False)
    
    print(f"Created data.yaml at {yaml_path}")
    return True

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
        train_images = [f for f in os.listdir(train_images_dir) 
                       if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        stats['train_images'] = len(train_images)
        
        for img_file in train_images:
            label_file = img_file.rsplit('.', 1)[0] + '.txt'
            label_path = os.path.join(train_labels_dir, label_file)
            
            if os.path.exists(label_path):
                stats['train_labels'] += 1
                
                # Check if label file is empty
                if os.path.getsize(label_path) == 0:
                    stats['empty_labels'].append(label_path)
                
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
                stats['missing_train_labels'].append(os.path.join(train_images_dir, img_file))
    
    # Check validation images and labels
    val_images_dir = os.path.join(dataset_path, 'val', 'images')
    val_labels_dir = os.path.join(dataset_path, 'val', 'labels')
    
    if os.path.exists(val_images_dir):
        val_images = [f for f in os.listdir(val_images_dir) 
                     if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        stats['val_images'] = len(val_images)
        
        for img_file in val_images:
            label_file = img_file.rsplit('.', 1)[0] + '.txt'
            label_path = os.path.join(val_labels_dir, label_file)
            
            if os.path.exists(label_path):
                stats['val_labels'] += 1
                
                # Check if label file is empty
                if os.path.getsize(label_path) == 0:
                    stats['empty_labels'].append(label_path)
                
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
                stats['missing_val_labels'].append(os.path.join(val_images_dir, img_file))
    
    return stats

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare dataset for YOLOv8 training")
    parser.add_argument("--source", "-s", default="dataset", help="Source directory with images and labels")
    parser.add_argument("--output", "-o", default="dataset_yolo", help="Output directory for organized dataset")
    parser.add_argument("--train-ratio", "-t", type=float, default=0.8, help="Training data ratio (0.8 = 80% train, 20% val)")
    parser.add_argument("--config", "-c", default="config/ark_ui_data.yaml", help="Path to save data.yaml")
    
    args = parser.parse_args()
    
    # Process the dataset
    if split_dataset(args.source, args.output, args.train_ratio):
        create_data_yaml(args.output, ARK_UI_CLASSES, args.config)
        
        # Verify dataset
        stats = verify_dataset(args.output)
        
        print("\nDataset preparation complete! Your dataset is ready for training.")
        print(f"- Training images: {stats['train_images']}")
        print(f"- Training labels: {stats['train_labels']}")
        print(f"- Validation images: {stats['val_images']}")
        print(f"- Validation labels: {stats['val_labels']}")
        print(f"- Classes: {len(ARK_UI_CLASSES)}")
        
        if stats['missing_train_labels'] or stats['missing_val_labels']:
            print("\nWarning: Some images don't have corresponding label files.")
            print(f"- Missing training labels: {len(stats['missing_train_labels'])}")
            print(f"- Missing validation labels: {len(stats['missing_val_labels'])}")
        
        if stats['empty_labels']:
            print(f"\nWarning: {len(stats['empty_labels'])} empty label files detected.")
        
        print(f"\nNext step: Run 'python 4_train_model.py' to start training your model.")
    else:
        print("\nError: Dataset preparation failed. Please check your source directory.")
