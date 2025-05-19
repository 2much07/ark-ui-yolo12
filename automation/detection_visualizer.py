"""
Real-time UI detection visualizer for ARK: Survival Ascended.
This script shows what the YOLOv12 model is detecting in real-time to help debug and validate.
"""
import os
import time
import cv2
import numpy as np
import argparse
import yaml
import mss
import mss.tools
import sys
from ultralytics import YOLO
import random

def load_classes(data_yaml):
    """Load class names from data.yaml file."""
    if not os.path.exists(data_yaml):
        print(f"Warning: data.yaml not found at {data_yaml}. Using model's built-in class names.")
        return None
    
    with open(data_yaml, 'r') as f:
        data = yaml.safe_load(f)
    return data['names']

def generate_colors(num_classes):
    """Generate distinct colors for different classes."""
    np.random.seed(42)
    colors = {}
    
    for i in range(num_classes):
        colors[i] = tuple(map(int, np.random.randint(0, 255, size=3)))
    
    return colors

def real_time_detection(weights_path, data_yaml=None, conf_threshold=0.4, show_fps=True, delay=0.05):
    """
    Perform real-time UI detection on the game screen with YOLOv12.
    
    Args:
        weights_path: Path to trained YOLOv12 model weights
        data_yaml: Path to data.yaml file (optional)
        conf_threshold: Confidence threshold for detections
        show_fps: Whether to display FPS
        delay: Delay between frames in seconds
    """
    print("\n=== ARK UI Real-time Detector with YOLOv12 ===")
    print(f"Model: {weights_path}")
    print(f"Confidence threshold: {conf_threshold}")
    print("Press 'q' to quit, 'c' to capture screenshot")
    print("Press '+' or '-' to adjust confidence threshold")
    print("==================================\n")
    
    # Load model
    model = YOLO(weights_path)
    
    # Check if using YOLOv12
    is_v12 = hasattr(model.model, 'is_v12') and model.model.is_v12
    if is_v12:
        print("Using YOLOv12 advanced features for better detection")
    
    # Load class names
    class_names = {}
    if data_yaml and os.path.exists(data_yaml):
        class_names = load_classes(data_yaml)
    else:
        class_names = model.names
    
    # Generate colors for classes
    colors = generate_colors(len(class_names))
    
    # Initialize FPS calculation
    fps = 0
    frame_count = 0
    start_time = time.time()
    
    # Create directory for screenshots
    screenshot_dir = "detection_screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    
    # Setup screen capture
    with mss.mss() as sct:
        # Get primary monitor
        monitor = sct.monitors[1]
        
        try:
            while True:
                # Capture screenshot
                frame_start_time = time.time()
                img = sct.grab(monitor)
                img_np = np.array(img)
                frame = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
                
                # Resize for display
                display_height = 720
                display_width = int(frame.shape[1] * (display_height / frame.shape[0]))
                display_frame = cv2.resize(frame, (display_width, display_height))
                
                # Perform detection with YOLOv12
                results = model.predict(source=frame, conf=conf_threshold)
                
                # Process results
                detection_counts = {}
                for result in results:
                    boxes = result.boxes.cpu().numpy()
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0].astype(int)
                        conf = box.conf[0]
                        cls_id = int(box.cls[0])
                        
                        # Track detection counts
                        cls_name = class_names.get(cls_id, f"Unknown-{cls_id}")
                        if cls_name not in detection_counts:
                            detection_counts[cls_name] = 0
                        detection_counts[cls_name] += 1
                        
                        # Scale coordinates for display frame
                        x1_d = int(x1 * (display_width / frame.shape[1]))
                        y1_d = int(y1 * (display_height / frame.shape[0]))
                        x2_d = int(x2 * (display_width / frame.shape[1]))
                        y2_d = int(y2 * (display_height / frame.shape[0]))
                        
                        # Draw bounding box
                        color = colors.get(cls_id, (0, 255, 0))
                        cv2.rectangle(display_frame, (x1_d, y1_d), (x2_d, y2_d), color, 2)
                        
                        # Put class name and confidence
                        label = f"{cls_name}: {conf:.2f}"
                        cv2.putText(display_frame, label, (x1_d, y1_d - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                                  0.5, color, 2)
                
                # Calculate and display FPS
                frame_count += 1
                if frame_count >= 10:
                    end_time = time.time()
                    fps = frame_count / (end_time - start_time)
                    frame_count = 0
                    start_time = time.time()
                
                if show_fps:
                    cv2.putText(display_frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                              1, (0, 255, 0), 2)
                
                # Display confidence threshold
                cv2.putText(display_frame, f"Conf: {conf_threshold:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX,
                          1, (0, 255, 0), 2)
                
                # Display YOLOv12 indicator
                if is_v12:
                    cv2.putText(display_frame, "YOLOv12", (display_width - 120, 30), cv2.FONT_HERSHEY_SIMPLEX,
                              1, (0, 255, 255), 2)
                
                # Display detection counts
                y_pos = 110
                for cls_name, count in sorted(detection_counts.items()):
                    cv2.putText(display_frame, f"{cls_name}: {count}", (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX,
                              0.5, (0, 255, 0), 2)
                    y_pos += 30
                
                # Display the result
                cv2.imshow('ARK UI Detection (YOLOv12)', display_frame)
                
                # Process key presses
                key = cv2.waitKey(1) & 0xFF
                
                # Exit if 'q' is pressed
                if key == ord('q'):
                    break
                
                # Capture screenshot if 'c' is pressed
                if key == ord('c'):
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    screenshot_path = os.path.join(screenshot_dir, f"detection_{timestamp}.png")
                    cv2.imwrite(screenshot_path, display_frame)
                    print(f"Screenshot saved to {screenshot_path}")
                
                # Adjust confidence threshold with + and -
                if key == ord('+') or key == ord('='):
                    conf_threshold = min(conf_threshold + 0.05, 1.0)
                    print(f"Confidence threshold increased to {conf_threshold:.2f}")
                
                if key == ord('-') or key == ord('_'):
                    conf_threshold = max(conf_threshold - 0.05, 0.05)
                    print(f"Confidence threshold decreased to {conf_threshold:.2f}")
                
                # Limit the frame rate
                process_time = time.time() - frame_start_time
                sleep_time = max(0, delay - process_time)
                time.sleep(sleep_time)
        
        except KeyboardInterrupt:
            print("Detection interrupted by user.")
        
        finally:
            cv2.destroyAllWindows()
            print("Real-time detection stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-time ARK UI Detection Visualizer with YOLOv12")
    parser.add_argument("--weights", "-w", required=True, help="Path to trained YOLOv12 weights")
    parser.add_argument("--data", "-d", default=None, help="Path to data.yaml")
    parser.add_argument("--conf", "-c", type=float, default=0.4, help="Confidence threshold")
    parser.add_argument("--delay", type=float, default=0.05, help="Delay between frames in seconds")
    parser.add_argument("--no-fps", action="store_true", help="Hide FPS counter")
    
    args = parser.parse_args()
    
    real_time_detection(args.weights, args.data, args.conf, not args.no_fps, args.delay)