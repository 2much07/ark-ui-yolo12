"""
Train YOLOv8 model for ARK UI Detection with enhanced support for state-specific UI elements.
"""
import os
import yaml
import argparse
from ultralytics import YOLO
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.visualization import plot_training_results

def load_config(config_path):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def train_model(data_yaml, model_config, output_dir, pretrained_weights=None):
    """
    Train YOLOv8 model for ARK UI detection.
    
    Args:
        data_yaml: Path to data.yaml
        model_config: Path to model configuration
        output_dir: Directory to save results
        pretrained_weights: Path to pretrained weights (optional)
    """
    # Load model configuration
    config = load_config(model_config)
    
    # Use specified or default model
    model_path = pretrained_weights if pretrained_weights else config.get('model', 'yolov8s.pt')
    
    # Create run name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"ark_ui_detector_{timestamp}"
    
    # Load data.yaml to check class count
    with open(data_yaml, 'r') as f:
        data_config = yaml.safe_load(f)
    
    num_classes = len(data_config['names'])
    print(f"Training for {num_classes} classes")
    
    # Adjust batch size based on class count
    batch_size = config.get('batch', 16)
    if num_classes > 200:
        suggested_batch = max(4, batch_size // 2)  # Reduce batch size for large class counts
        print(f"Large class count detected ({num_classes} classes)")
        print(f"Reducing batch size from {batch_size} to {suggested_batch}")
        batch_size = suggested_batch
    
    # Recommend larger model for large class counts
    if pretrained_weights is None and num_classes > 300:
        model_size = model_path.split('yolov8')[1].split('.')[0]
        if model_size == 's' or model_size == 'n' or model_size == '':
            print("WARNING: Large class set detected. Consider using a larger model for better performance.")
            print("For example: yolov8m.pt or yolov8l.pt instead of yolov8s.pt")
    
    # Load model
    model = YOLO(model_path)
    
    # Prepare training arguments
    train_args = {
        'data': data_yaml,
        'epochs': config.get('epochs', 100),
        'batch': batch_size,
        'imgsz': config.get('imgsz', 640),
        'patience': config.get('patience', 20),
        'optimizer': config.get('optimizer', 'AdamW'),
        'lr0': config.get('lr0', 0.001),
        'lrf': config.get('lrf', 0.01),
        'momentum': config.get('momentum', 0.937),
        'weight_decay': config.get('weight_decay', 0.0005),
        'warmup_epochs': config.get('warmup_epochs', 3),
        'warmup_momentum': config.get('warmup_momentum', 0.8),
        'warmup_bias_lr': config.get('warmup_bias_lr', 0.1),
        'name': run_name,
        'project': output_dir,
        'exist_ok': True,
        'pretrained': True,
        'verbose': True,
        'device': 0 if config.get('device', None) is None else config.get('device'),
        'workers': config.get('workers', 8)
    }
    
    # Add more frequent checkpoints for large class sets
    if num_classes > 200:
        save_period = min(5, config.get('save_period', 10))  # Save more frequently
        train_args['save_period'] = save_period
    else:
        train_args['save_period'] = config.get('save_period', 10)
    
    # Add augmentation parameters
    augmentation_params = [
        'mosaic', 'mixup', 'copy_paste', 'degrees', 'translate', 
        'scale', 'shear', 'perspective', 'flipud', 'fliplr',
        'hsv_h', 'hsv_s', 'hsv_v'
    ]
    
    for param in augmentation_params:
        if param in config:
            train_args[param] = config[param]
    
    # For UI state detection, minimize color and position augmentations
    if any('status_' in class_name for class_name in data_config['names'].values()):
        print("State-specific UI classes detected. Adjusting augmentation parameters...")
        
        # Fine-tune augmentations for state detection
        train_args['hsv_h'] = min(0.01, train_args.get('hsv_h', 0.015))  # Minimal hue change
        train_args['hsv_s'] = min(0.1, train_args.get('hsv_s', 0.2))     # Reduced saturation
        train_args['hsv_v'] = min(0.1, train_args.get('hsv_v', 0.2))     # Reduced value/brightness
    
    # Print training configuration
    print("\n=== ARK UI Detector Training Configuration ===")
    print(f"Model: {model_path}")
    print(f"Data: {data_yaml}")
    print(f"Output directory: {os.path.join(output_dir, run_name)}")
    print(f"Epochs: {train_args['epochs']}")
    print(f"Batch size: {train_args['batch']}")
    print(f"Image size: {train_args['imgsz']}")
    print(f"Device: {train_args['device']}")
    print(f"Classes: {num_classes}")
    
    # Check for state-specific classes
    state_classes = sum(1 for name in data_config['names'].values() if any(x in name for x in 
                                                            ['_low', '_medium', '_full', '_active', '_inactive']))
    if state_classes > 0:
        print(f"State-specific classes: {state_classes}")
    
    print("===============================================\n")
    
    # Start training
    print("Starting training...")
    try:
        results = model.train(**train_args)
        
        # Print results summary
        print("\n=== Training Complete ===")
        print(f"Results saved to {os.path.join(output_dir, run_name)}")
        print(f"Best model: {os.path.join(output_dir, run_name, 'weights', 'best.pt')}")
        
        # Create results directory
        results_dir = os.path.join(output_dir, run_name, 'results')
        os.makedirs(results_dir, exist_ok=True)
        
        # Plot training results
        try:
            results_csv = os.path.join(output_dir, run_name, 'results.csv')
            if os.path.exists(results_csv):
                plot_training_results(results_csv, results_dir)
                print(f"Training plots saved to {results_dir}")
        except Exception as e:
            print(f"Warning: Could not generate result plots: {e}")
        
        return os.path.join(output_dir, run_name, 'weights', 'best.pt')
    except Exception as e:
        print(f"Error during training: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train YOLOv8 for ARK UI Detection")
    parser.add_argument("--data", "-d", default="config/ark_ui_data.yaml", help="Path to data.yaml")
    parser.add_argument("--config", "-c", default="config/model_config.yaml", help="Path to model configuration")
    parser.add_argument("--output", "-o", default="runs", help="Output directory")
    parser.add_argument("--weights", "-w", default=None, help="Path to pretrained weights")
    parser.add_argument("--device", type=str, default=None, help="Device to use (e.g., '0' for GPU 0, 'cpu' for CPU)")
    
    args = parser.parse_args()
    
    # Update config file if device specified
    if args.device:
        config_path = args.config
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            config['device'] = args.device
            
            with open(config_path, 'w') as f:
                yaml.dump(config, f)
            
            print(f"Updated config file to use device: {args.device}")
    
    # Create config directory if it doesn't exist
    os.makedirs(os.path.dirname(args.config), exist_ok=True)
    
    # If config file doesn't exist, create it with default values
    if not os.path.exists(args.config):
        default_config = {
            'model': 'yolov8s.pt',
            'epochs': 100,
            'batch': 16,
            'imgsz': 640,
            'patience': 20,
            'optimizer': 'AdamW',
            'lr0': 0.001,
            'lrf': 0.01,
            'momentum': 0.937,
            'weight_decay': 0.0005,
            'warmup_epochs': 3,
            'warmup_momentum': 0.8,
            'warmup_bias_lr': 0.1,
            'save_period': 10,
            'device': args.device if args.device else 0,
            'workers': 8,
            'mosaic': 0.0,
            'mixup': 0.0,
            'copy_paste': 0.0,
            'degrees': 0.0,
            'translate': 0.1,
            'scale': 0.1,
            'shear': 0.0,
            'perspective': 0.0,
            'flipud': 0.0,
            'fliplr': 0.0,
            'hsv_h': 0.015,
            'hsv_s': 0.2,
            'hsv_v': 0.2
        }
        
        os.makedirs(os.path.dirname(args.config), exist_ok=True)
        with open(args.config, 'w') as f:
            yaml.dump(default_config, f)
        
        print(f"Created default config file at {args.config}")
    
    best_model_path = train_model(args.data, args.config, args.output, args.weights)
    
    if best_model_path:
        print(f"\nNext step: Run 'python training/5_evaluate_model.py --weights {best_model_path}' to evaluate your model.")
    else:
        print("\nTraining failed. Please check error messages above.")