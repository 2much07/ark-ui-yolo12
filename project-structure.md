# ARK UI Master: Detection & Automation System

## Project Structure
```
ark_ui_master/
├── README.md                           # Project overview and instructions
├── requirements.txt                    # Dependencies for both projects
├── setup.py                            # Installation script
│
├── training/                           # YOLOv8 training pipeline
│   ├── 1_screenshot_collector.py       # Screenshot collection script
│   ├── 2_annotate_instructions.md      # Annotation guidelines
│   ├── 3_dataset_preparation.py        # Dataset organization script
│   ├── 4_train_model.py                # YOLOv8 training script
│   ├── 5_evaluate_model.py             # Model evaluation script
│   ├── 6_model_updater.py              # Model updating script
│   └── config/                         # Configuration files
│       ├── ark_ui_data.yaml            # Dataset configuration
│       └── model_config.yaml           # YOLOv8 model configuration
│
├── automation/                         # ARK UI Automation System
│   ├── ark_ui_automation.py            # Main automation class
│   ├── detection_visualizer.py         # Real-time UI visualization tool
│   ├── run_automation.py               # Automation script launcher
│   ├── examples/                       # Example automation scripts
│   │   ├── inventory_manager.py        # Inventory management example
│   │   ├── crafting_helper.py          # Crafting automation example
│   │   ├── taming_assistant.py         # Taming helper example
│   │   └── resource_gatherer.py        # Resource gathering example
│   └── config/                         # Automation configuration
│       └── automation_config.yaml      # Automation settings
│
└── utils/                              # Shared utilities
    ├── dataset_utils.py                # Dataset management utilities
    ├── visualization.py                # Visualization utilities
    ├── ark_ui_classes.py               # ARK UI class definitions
    └── screenshot_utils.py             # Screenshot processing utilities
```
