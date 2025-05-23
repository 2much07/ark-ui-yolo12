# YOLOv8 Configuration for ARK UI Detection
model: yolov8s.pt  # Use small model as base

# Training parameters
epochs: 100
batch: 16  # Adjust based on GPU memory
imgsz: 640  # Training image size
patience: 20  # Early stopping patience
optimizer: AdamW  # Optimizer
lr0: 0.001  # Initial learning rate
lrf: 0.01  # Final learning rate as a fraction of lr0
momentum: 0.937  # SGD momentum/Adam beta1
weight_decay: 0.0005  # Optimizer weight decay
warmup_epochs: 3  # Warmup epochs
warmup_momentum: 0.8  # Warmup initial momentum
warmup_bias_lr: 0.1  # Warmup initial bias lr
save_period: 10  # Save checkpoint every X epochs

# Augmentation options - optimized for UI detection
mosaic: 0.0  # Disable mosaic for UI detection
mixup: 0.0  # Disable mixup for UI detection
copy_paste: 0.0  # Disable copy-paste
degrees: 0.0  # No rotation for UI elements
translate: 0.1  # Slight translation augmentation
scale: 0.1  # Slight scaling augmentation
shear: 0.0  # No shear
perspective: 0.0  # No perspective
flipud: 0.0  # No vertical flips for UI
fliplr: 0.0  # No horizontal flips for UI
hsv_h: 0.015  # HSV-Hue augmentation
hsv_s: 0.2  # HSV-Saturation augmentation
hsv_v: 0.2  # HSV-Value augmentation

# Hardware settings
device: 0  # Use first GPU, set to 'cpu' for CPU training
workers: 8  # Number of worker threads