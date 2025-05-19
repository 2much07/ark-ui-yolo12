"""
Main launcher for ARK UI Automation System with YOLOv12 support.
This script provides a unified interface to run the various automation examples.
"""
import os
import sys
import argparse
import logging
import time
import importlib.util

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("ark_automation.log")
    ]
)
logger = logging.getLogger('ark_automation')

def load_script(script_name):
    """
    Dynamically load a script module.
    
    Args:
        script_name: Name of the script to load (without .py)
        
    Returns:
        Loaded module or None if not found
    """
    # Check for built-in examples
    example_path = os.path.join('examples', f"{script_name}.py")
    
    if os.path.exists(example_path):
        # Load built-in example
        spec = importlib.util.spec_from_file_location(script_name, example_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    # Check for custom script
    if os.path.exists(f"{script_name}.py"):
        # Load custom script
        spec = importlib.util.spec_from_file_location(script_name, f"{script_name}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    logger.error(f"Script not found: {script_name}")
    return None

def list_available_scripts():
    """List all available automation scripts."""
    print("\nAvailable Automation Scripts (YOLOv12 Compatible):")
    print("--------------------------------------------")
    
    # List built-in examples
    examples_dir = 'examples'
    if os.path.exists(examples_dir):
        example_files = [f[:-3] for f in os.listdir(examples_dir) 
                       if f.endswith('.py') and not f.startswith('_')]
        
        if example_files:
            print("\nBuilt-in Examples:")
            for script in sorted(example_files):
                print(f"  - {script}")
    
    # List custom scripts
    custom_scripts = [f[:-3] for f in os.listdir('.') 
                    if f.endswith('.py') and not f.startswith('_') 
                    and f != 'run_automation.py'
                    and f != 'ark_ui_automation.py'
                    and f != 'detection_visualizer.py']
    
    if custom_scripts:
        print("\nCustom Scripts:")
        for script in sorted(custom_scripts):
            print(f"  - {script}")
    
    print("\nUsage: python run_automation.py --script <script_name> --weights <model_weights>")
    print("Add --help to see all options for a specific script")
    
    print("\nExample: python run_automation.py --script inventory_manager --weights runs/ark_ui_detector/weights/best.pt")

def main():
    parser = argparse.ArgumentParser(description="ARK UI Automation System Launcher (YOLOv12 Compatible)")
    parser.add_argument("--script", "-s", help="Script to run")
    parser.add_argument("--weights", "-w", help="Path to trained YOLOv12 model weights")
    parser.add_argument("--list", "-l", action="store_true", help="List available scripts")
    parser.add_argument("--visualize", "-v", action="store_true", help="Run detection visualizer")
    parser.add_argument("--confidence", "-c", type=float, default=0.4, help="Detection confidence threshold")
    
    # First parsing to check for --list and --visualize flags
    args, remaining = parser.parse_known_args()
    
    if args.list:
        list_available_scripts()
        return
    
    if args.visualize:
        # Run the detection visualizer
        if not args.weights:
            logger.error("No model weights specified for visualization")
            return
        
        try:
            # Import the detection visualizer directly
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from detection_visualizer import real_time_detection
            logger.info("Starting YOLOv12 detection visualizer...")
            real_time_detection(args.weights, conf_threshold=args.confidence)
        except ImportError:
            logger.error("Failed to import detection_visualizer.py")
        return
    
    if not args.script:
        parser.print_help()
        list_available_scripts()
        return
    
    if not args.weights:
        logger.error("No model weights specified")
        return
    
    # Create examples directory if it doesn't exist
    os.makedirs('examples', exist_ok=True)
    
    # Check if inventory_manager.py exists and copy it to examples if needed
    if args.script == 'inventory_manager' and not os.path.exists(os.path.join('examples', 'inventory_manager.py')):
        if os.path.exists('inventory_manager.py'):
            try:
                import shutil
                shutil.copy('inventory_manager.py', os.path.join('examples', 'inventory_manager.py'))
                logger.info(f"Copied inventory_manager.py to examples directory")
            except Exception as e:
                logger.error(f"Failed to copy inventory_manager.py: {e}")
    
    # Load the specified script
    script_module = load_script(args.script)
    
    if script_module is None:
        return
    
    # Check if the script has a main function
    if not hasattr(script_module, 'main'):
        logger.error(f"Script {args.script} does not have a main function")
        return
    
    # Prepare arguments for the script
    sys.argv = [f"{args.script}.py"] + remaining
    if "--weights" not in remaining and "-w" not in remaining:
        sys.argv.extend(["--weights", args.weights])
    if "--confidence" not in remaining and "-c" not in remaining:
        sys.argv.extend(["--confidence", str(args.confidence)])
    
    # Run the script's main function
    logger.info(f"Running script: {args.script} with YOLOv12 model")
    start_time = time.time()
    
    try:
        script_module.main()
        end_time = time.time()
        logger.info(f"Script {args.script} completed in {end_time - start_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Error running script {args.script}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()