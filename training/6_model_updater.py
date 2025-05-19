"""
Update YOLOv12 model for ARK UI Detection with new data.
This script allows updating an existing model with new data or adding new classes,
with special support for upgrading to state-specific UI detection.
"""
import os
import argparse
import yaml
import sys
import random
from ultralytics import YOLO
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def update_model(weights_path, data_yaml, output_dir, epochs=50, batch_size=16):
    """
    Update the model with new data.
    
    Args:
        weights_path: Path to existing model weights
        data_yaml: Path to data.yaml for the updated dataset
        output_dir: Directory to save results
        epochs: Number of additional training epochs
        batch_size: Batch size for training
        
    Returns:
        Path to the updated model
    """
    print("\n=== ARK UI Detector Model Update ===")
    print(f"Base model: {weights_path}")
    print(f"Data: {data_yaml}")
    print(f"Epochs: {epochs}")
    print(f"Batch size: {batch_size}")
    print("====================================\n")
    
    """
    Update model to recognize state-specific UI elements.
    """
    # Create run name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"ark_ui_detector_state_specific_{timestamp}"
    
    # Load model
    model = YOLO(weights_path)
    
    # Prepare training arguments
    train_args = {
        'data': data_yaml,
        'epochs': epochs,
        'imgsz': 640,
        'batch': batch_size,
        'name': run_name,
        'project': output_dir,
        'exist_ok': True,
        'patience': 30,  # Increased patience for learning complex state differences
        'mosaic': 0.0,   # Disable mosaic for UI state detection
        'mixup': 0.0,    # Disable mixup for UI state detection
        'hsv_h': 0.01,   # Minimal hue augmentation to preserve UI colors
        'hsv_s': 0.1,    # Minimal saturation augmentation
        'hsv_v': 0.1,    # Minimal value augmentation
        'translate': 0.05, # Minimal translation
        'scale': 0.05,   # Minimal scaling
        'fliplr': 0.0,   # No flipping for UI
        'flipud': 0.0,   # No flipping for UI
        
        # YOLOv12 specific parameters
        'attention': 'flash',  # Use FlashAttention on your 3090 Ti
        'v12_head': True       # Use YOLOv12 detection head
    }
    
    # Start training
    print("Starting state-specific model update...")
    results = model.train(**train_args)
    
    # Get best model path
    best_model_path = os.path.join(output_dir, run_name, 'weights', 'best.pt')
    
    # Print results summary
    print("\n=== Update Complete ===")
    print(f"Results saved to {os.path.join(output_dir, run_name)}")
    print(f"Updated model: {best_model_path}")
    
    return best_model_path

def add_new_classes(weights_path, data_yaml, output_dir, epochs=100, batch_size=16):
    """
    Update the model to detect new classes.
    
    Args:
        weights_path: Path to existing model weights
        data_yaml: Path to data.yaml with new classes
        output_dir: Directory to save results
        epochs: Number of training epochs
        batch_size: Batch size for training
        
    Returns:
        Path to the updated model
    """
    print("\n=== ARK UI Detector New Classes Addition ===")
    print(f"Base model: {weights_path}")
    print(f"Data with new classes: {data_yaml}")
    print(f"Epochs: {epochs}")
    print(f"Batch size: {batch_size}")
    print("============================================\n")
    
    # Load data.yaml to check new classes
    with open(data_yaml, 'r') as f:
        data_config = yaml.safe_load(f)
    
    num_classes = len(data_config['names'])
    print(f"Training for {num_classes} classes")
    
    # Create run name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"ark_ui_detector_new_classes_{timestamp}"
    
    # Load model
    model = YOLO(weights_path)
    
    # Prepare training arguments
    train_args = {
        'data': data_yaml,
        'epochs': epochs,
        'imgsz': 640,
        'batch': batch_size,
        'name': run_name,
        'project': output_dir,
        'exist_ok': True,
    }
    
    # Start training
    print("Starting training with new classes...")
    results = model.train(**train_args)
    
    # Get best model path
    best_model_path = os.path.join(output_dir, run_name, 'weights', 'best.pt')
    
    # Print results summary
    print("\n=== Training Complete ===")
    print(f"Results saved to {os.path.join(output_dir, run_name)}")
    print(f"Updated model: {best_model_path}")
    
    return best_model_path

def create_class_mapping_file(old_data_yaml, new_data_yaml, output_file):
    """
    Create a file mapping old class IDs to new class IDs.
    
    Args:
        old_data_yaml: Path to old data.yaml
        new_data_yaml: Path to new data.yaml
        output_file: Path to save mapping file
    """
    # Load old classes
    with open(old_data_yaml, 'r') as f:
        old_data = yaml.safe_load(f)
    
    old_classes = old_data['names']
    
    # Load new classes
    with open(new_data_yaml, 'r') as f:
        new_data = yaml.safe_load(f)
    
    new_classes = new_data['names']
    
    # Create mapping
    mapping = {}
    
    # 1. Direct name matches
    for old_id, old_name in old_classes.items():
        for new_id, new_name in new_classes.items():
            if old_name == new_name:
                mapping[old_id] = new_id
                break
    
    # 2. State-specific mapping (map generic classes to specific states)
    state_mappings = {
        'health_bar': ['status_health_low', 'status_health_medium', 'status_health_full'],
        'stamina_bar': ['status_stamina_low', 'status_stamina_medium', 'status_stamina_full'],
        'food_bar': ['status_food_low', 'status_food_medium', 'status_food_full'],
        'water_bar': ['status_water_low', 'status_water_medium', 'status_water_full'],
        'inventory_slot': ['player_inventory_slot_empty', 'player_inventory_slot_filled'],
        'inventory_item': ['player_item_icon', 'entity_item_icon']
    }
    
    # Find unmapped old classes
    unmapped_old_ids = [old_id for old_id in old_classes.keys() if old_id not in mapping]
    
    # Try to map generic classes to state-specific ones
    for old_id in unmapped_old_ids:
        old_name = old_classes[old_id]
        if old_name in state_mappings:
            # Map to the medium/default state when available
            for new_id, new_name in new_classes.items():
                if new_name in state_mappings[old_name]:
                    # Prefer medium state when available
                    if 'medium' in new_name or 'default' in new_name:
                        mapping[old_id] = new_id
                        break
            
            # If no medium state found, use the first available state
            if old_id not in mapping:
                for new_id, new_name in new_classes.items():
                    if new_name in state_mappings[old_name]:
                        mapping[old_id] = new_id
                        break
    
    # 3. Try to find the closest matching name for remaining unmapped classes
    still_unmapped = [old_id for old_id in unmapped_old_ids if old_id not in mapping]
    for old_id in still_unmapped:
        old_name = old_classes[old_id]
        
        # Try to find a partial match by prefix
        best_match = None
        best_match_score = 0
        
        for new_id, new_name in new_classes.items():
            # Skip already mapped new IDs to avoid duplicates
            if new_id in mapping.values():
                continue
                
            # Simple similarity score based on common prefix
            if '_' in old_name and '_' in new_name:
                old_prefix = old_name.split('_')[0]
                new_prefix = new_name.split('_')[0]
                
                if old_prefix == new_prefix:
                    # Calculate similarity score based on word overlap
                    old_parts = set(old_name.split('_'))
                    new_parts = set(new_name.split('_'))
                    overlap = len(old_parts.intersection(new_parts))
                    score = overlap / max(len(old_parts), len(new_parts))
                    
                    if score > best_match_score:
                        best_match_score = score
                        best_match = new_id
        
        # If we found a reasonable match, use it
        if best_match is not None and best_match_score > 0.5:
            mapping[old_id] = best_match
    
    # Save mapping
    with open(output_file, 'w') as f:
        yaml.dump(mapping, f, sort_keys=True)
    
    # Report mapping statistics
    total_old_classes = len(old_classes)
    mapped_classes = len(mapping)
    
    print(f"Class mapping saved to {output_file}")
    print(f"Mapped {mapped_classes}/{total_old_classes} classes ({mapped_classes/total_old_classes*100:.1f}%)")
    print(f"Unmapped classes: {total_old_classes - mapped_classes}")
    
    return mapping

def update_model_with_states(weights_path, data_yaml, output_dir, epochs=100, batch_size=8):
    """
    Update model to recognize state-specific UI elements.
    This mode is specifically for upgrading from basic UI detection to state-specific detection.
    
    Args:
        weights_path: Path to existing model weights
        data_yaml: Path to data.yaml with state-specific classes
        output_dir: Directory to save results
        epochs: Number of training epochs
        batch_size: Batch size for training
        
    Returns:
        Path to the updated model
    """
    print("\n=== ARK UI Detector State-Specific Update ===")
    print(f"Base model: {weights_path}")
    print(f"Data with state classes: {data_yaml}")
    print(f"Epochs: {epochs}")
    print(f"Batch size: {batch_size}")
    print("================================================\n")
    
    # Load data.yaml to check for state-specific classes
    with open(data_yaml, 'r') as f:
        data_config = yaml.safe_load(f)
    
    # Check for state-specific classes
    state_class_count = sum(1 for name in data_config['names'].values() 
                            if any(state in name for state in 
                                 ['_low', '_medium', '_full', '_active', '_inactive', 
                                  '_empty', '_filled', '_highlighted', '_pressed']))
    
    print(f"Detected {state_class_count} state-specific classes")
    
    if state_class_count < 10:
        print("Warning: Few state-specific classes found. This model may not fully benefit from state detection.")
    
    # Create run name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"ark_ui_detector_state_specific_{timestamp}"
    
    # Load model
    model = YOLO(weights_path)
    
    # Prepare training arguments
    train_args = {
        'data': data_yaml,
        'epochs': epochs,
        'imgsz': 640,
        'batch': batch_size,
        'name': run_name,
        'project': output_dir,
        'exist_ok': True,
        'patience': 30,  # Increased patience for learning complex state differences
        'mosaic': 0.0,   # Disable mosaic for UI state detection
        'mixup': 0.0,    # Disable mixup for UI state detection
        'hsv_h': 0.01,   # Minimal hue augmentation to preserve UI colors
        'hsv_s': 0.1,    # Minimal saturation augmentation
        'hsv_v': 0.1,    # Minimal value augmentation
        'translate': 0.05, # Minimal translation
        'scale': 0.05,   # Minimal scaling
        'fliplr': 0.0,   # No flipping for UI
        'flipud': 0.0,   # No flipping for UI
    }
    
    # Start training
    print("Starting state-specific model update...")
    results = model.train(**train_args)
    
    # Get best model path
    best_model_path = os.path.join(output_dir, run_name, 'weights', 'best.pt')
    
    # Print results summary
    print("\n=== State Update Complete ===")
    print(f"Results saved to {os.path.join(output_dir, run_name)}")
    print(f"Updated model: {best_model_path}")
    
    return best_model_path

def list_state_specific_classes(data_yaml):
    """List state-specific classes in the dataset."""
    with open(data_yaml, 'r') as f:
        data_config = yaml.safe_load(f)
    
    state_classes = {}
    
    for cls_id, cls_name in data_config['names'].items():
        # Check if this is a state-specific class
        if any(state in cls_name for state in 
              ['_low', '_medium', '_full', '_high', '_active', '_inactive', 
               '_empty', '_filled', '_highlighted', '_pressed']):
            
            # Extract the base element name
            if '_' in cls_name:
                parts = cls_name.split('_')
                state = parts[-1]
                base_name = '_'.join(parts[:-1])
                
                if base_name not in state_classes:
                    state_classes[base_name] = []
                
                state_classes[base_name].append({
                    'id': cls_id,
                    'name': cls_name,
                    'state': state
                })
    
    # Print state-specific class groups
    if state_classes:
        print("\nState-specific classes found:")
        for base_name, states in state_classes.items():
            print(f"\n{base_name} states:")
            for state_info in states:
                print(f"  - {state_info['id']}: {state_info['name']} (state: {state_info['state']})")
    else:
        print("\nNo state-specific classes found in this dataset.")
        print("Consider upgrading to state-specific detection for better automation capabilities.")
    
    return state_classes

def main():
    parser = argparse.ArgumentParser(description="Update ARK UI Detection model")
    parser.add_argument("--weights", "-w", required=True, help="Path to existing model weights")
    parser.add_argument("--data", "-d", default="training/config/ark_ui_data.yaml", help="Path to data.yaml")
    parser.add_argument("--output", "-o", default="runs", help="Output directory")
    parser.add_argument("--epochs", "-e", type=int, default=50, help="Number of training epochs")
    parser.add_argument("--batch", "-b", type=int, default=16, help="Batch size")
    parser.add_argument("--new-classes", "-n", action="store_true", help="Add new classes to model")
    parser.add_argument("--state-update", "-s", action="store_true", 
                     help="Update model to recognize state-specific UI elements")
    parser.add_argument("--old-data", help="Path to old data.yaml for class mapping")
    parser.add_argument("--mapping", help="Path to save/load class mapping file")
    parser.add_argument("--list-states", "-l", action="store_true", 
                      help="List state-specific classes in the dataset")
    
    args = parser.parse_args()
    
    # Check if data.yaml exists
    if not os.path.exists(args.data):
        print(f"Error: {args.data} not found")
        return
    
    # List state-specific classes if requested
    if args.list_states:
        list_state_specific_classes(args.data)
        return
    
    # Handle class mapping
    if (args.new_classes or args.state_update) and args.old_data and args.mapping:
        create_class_mapping_file(args.old_data, args.data, args.mapping)
    
    # Choose update mode
    if args.state_update:
        # Update model for state-specific detection
        updated_model_path = update_model_with_states(
            args.weights, args.data, args.output, args.epochs, args.batch
        )
    elif args.new_classes:
        # Update model with new classes
        updated_model_path = add_new_classes(
            args.weights, args.data, args.output, args.epochs, args.batch
        )
    else:
        # Regular update with new data
        updated_model_path = update_model(
            args.weights, args.data, args.output, args.epochs, args.batch
        )
    
    print(f"\nNext step: Run 'python training/5_evaluate_model.py --weights {updated_model_path}' to evaluate your updated model.")

if __name__ == "__main__":
    main()