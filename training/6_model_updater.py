"""
Update YOLOv8 model for ARK UI Detection with new data.
This script allows updating an existing model with new data or adding new classes.
"""
import os
import argparse
import yaml
import sys
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
    
    # Create run name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"ark_ui_detector_update_{timestamp}"
    
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
        'resume': True,  # Continue from existing weights
        
        # Reduced augmentation for fine-tuning
        'mosaic': 0.0,
        'mixup': 0.0,
        'degrees': 0.0,
        'translate': 0.1,
        'scale': 0.1,
        'fliplr': 0.0,
        'flipud': 0.0
    }
    
    # Start training
    print("Starting model update...")
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
    
    for old_id, old_name in old_classes.items():
        for new_id, new_name in new_classes.items():
            if old_name == new_name:
                mapping[old_id] = new_id
                break
    
    # Save mapping
    with open(output_file, 'w') as f:
        yaml.dump(mapping, f, sort_keys=True)
    
    print(f"Class mapping saved to {output_file}")
    print(f"Mapped {len(mapping)} classes")
    
    return mapping

def main():
    parser = argparse.ArgumentParser(description="Update ARK UI Detection model")
    parser.add_argument("--weights", "-w", required=True, help="Path to existing model weights")
    parser.add_argument("--data", "-d", default="training/config/ark_ui_data.yaml", help="Path to data.yaml")
    parser.add_argument("--output", "-o", default="runs", help="Output directory")
    parser.add_argument("--epochs", "-e", type=int, default=50, help="Number of training epochs")
    parser.add_argument("--batch", "-b", type=int, default=16, help="Batch size")
    parser.add_argument("--new-classes", "-n", action="store_true", help="Add new classes to model")
    parser.add_argument("--old-data", help="Path to old data.yaml for class mapping")
    parser.add_argument("--mapping", help="Path to save/load class mapping file")
    
    args = parser.parse_args()
    
    # Check if data.yaml exists
    if not os.path.exists(args.data):
        print(f"Error: {args.data} not found")
        return
    
    # Handle class mapping
    if args.new_classes and args.old_data and args.mapping:
        create_class_mapping_file(args.old_data, args.data, args.mapping)
    
    if args.new_classes:
        updated_model_path = add_new_classes(args.weights, args.data, args.output, args.epochs, args.batch)
    else:
        updated_model_path = update_model(args.weights, args.data, args.output, args.epochs, args.batch)
    
    print(f"\nNext step: Run 'python training/5_evaluate_model.py --weights {updated_model_path}' to evaluate your updated model.")

if __name__ == "__main__":
    main()