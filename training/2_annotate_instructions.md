# ARK: Survival Ascended UI Detection - Enhanced Annotation Guide

This comprehensive guide will help you accurately annotate ARK: Survival Ascended screenshots for training your YOLOv8 model with state-specific UI elements.

## Preferred Annotation Tool: Roboflow

We recommend using Roboflow for annotating your ARK UI screenshots:

1. Go to [Roboflow](https://roboflow.com/) and create a free account
2. Create a new project named "ARK-Ascended-UI-Detector"
3. Select "Object Detection" as the project type
4. Select "YOLOv8" as the annotation format

## Uploading Screenshots

1. Click "Upload" and select all screenshots from your screenshots folder
2. Wait for the upload to complete
3. Begin annotating using the Roboflow interface

## Key Annotation Principles for ARK Ascended

### Status Bar States
Unlike basic detection, we're annotating status bars with specific states:
- Use `status_health_low` when health bar is nearly empty (red, critical)
- Use `status_health_medium` when health bar is roughly 30-70% full
- Use `status_health_full` when health bar is mostly full

Apply this same state-specific approach to stamina, food, water, oxygen, weight, and torpor bars.

### Split-Screen Inventory System
ARK Ascended uses a split-screen inventory system:
- **Left Side**: Player inventory (always your character's inventory)
- **Right Side**: Entity inventory (structure, dino, or other interactive object)

Always use the correct side-specific classes:
- Use `player_inventory_slot_empty` for empty slots on the left side
- Use `player_inventory_slot_filled` for filled slots on the left side
- Use `entity_inventory_slot_empty` for empty slots on the right side
- Use `entity_inventory_slot_filled` for filled slots on the right side

### Button States
Annotate buttons with their specific states:
- Use `craft_button_active` when the craft button is clickable
- Use `craft_button_inactive` when the craft button is grayed out/unavailable
- Use `button_highlighted` when a button is being hovered over
- Use `button_pressed` when a button appears pressed down

## Main Annotation Categories

### Basic UI Elements (0-24)
- UI panels, scrollbars, dividers
- HUD elements (compass, hotbar, crosshair)
- Chat systems and interaction prompts

### Status Indicators (25-49)
- Health, stamina, food, water bars in different states (low/medium/full)
- Weight indicator states (low/medium/heavy)
- Torpidity states (low/medium/high)
- Oxygen and XP-related indicators

### Alert Messages (50-69)
- Starvation, dehydration, encumbered warnings
- Temperature alerts
- Death messages
- Taming notifications
- Enemy proximity warnings

### Player Inventory - Left Side (70-99)
- Player inventory slots (empty vs. filled)
- Player-side durability indicators
- Character model elements
- Armor slots and equipment interfaces
- Transfer buttons specific to player side

### Entity Inventory - Right Side (100-129)
- Entity inventory slots (empty vs. filled)
- Structure and creature names
- Dino-specific controls
- Fuel and power indicators
- Entity weight indicators

### Item Tooltip & Details (130-154)
- Item name/description in tooltips
- Item quality indicators
- Spoilage timers
- Item action menu options

### Crafting & Engrams (155-184)
- Crafting buttons in different states
- Material requirement indicators
- Engram availability and status
- Crafting queue elements

### Tab Navigation (185-204)
- Inventory tabs (selected vs. unselected)
- Crafting tabs
- Character tabs
- Structure tabs

### Map Elements (205-229)
- Map markers for various locations and resources
- Player and tribe member markers
- Waypoint controls
- Map navigation elements

### Button Elements (230-249)
- Standard UI buttons in various states
- Special action buttons
- Creature management buttons

### Creature & Taming Elements (250-274)
- Taming progress bars in different states
- Creature stat displays
- Breeding and maturation indicators
- Imprinting controls

### Structure Interface Elements (275-294)
- Structure health indicators
- Building placement indicators
- Power and resource indicators
- Structure management controls

### Special Menu Interfaces (295-319)
- Tek-related interfaces
- Terminal interfaces
- Special crafting stations
- Mission interfaces

### Character Stats Interface (320-339)
- Stat values and modifiers
- Level displays
- Mutation counters
- XP indicators

### Tribe Interface Elements (340-359)
- Tribe member lists and indicators
- Tribe log entries
- Permission settings
- Tribe management buttons

### Common Resources (360-399)
- Stone, wood, thatch, fiber, etc.
- Advanced resources like element
- Meat and food resources
- Berries and plants

### Tools, Weapons & Equipment (400-449)
- Various tools and weapons
- Ammunition
- Utility items
- Specialized equipment

### Armor & Clothing (450-474)
- Different armor tiers and pieces
- Specialized armor types
- Tek armor components

### Structures & Building (475-499)
- Building components
- Crafting stations
- Storage structures
- Advanced structures

### Creature-Related Items (500-519)
- Saddles and creature equipment
- Cryopods
- Breeding items
- Taming tools

### Advanced Elements & Systems (520-539)
- Tek systems
- Special creature interfaces
- DLC-specific interfaces

### Event-Specific UI (540-549)
- Seasonal event interfaces
- Special mission UIs
- Racing and mini-game elements

## Annotation Best Practices

### Draw Precise Boxes
- Draw tight bounding boxes around each UI element
- Include the complete element (for bars, include the full bar)
- For text elements, include the complete text area

### State-Based Annotation
- Pay attention to the state of UI elements
- Annotate the same bar differently based on fill level
- Annotate buttons differently based on active/inactive state

### Focus on Split-Screen Inventory
- Clearly distinguish between player (left) and entity (right) inventory elements
- Be consistent with side-specific annotation

### Handle Overlapping Elements
- When UI elements overlap, annotate both elements separately
- For an item in a slot, annotate both the slot and the item

### Prioritize Common Elements
- Focus on frequently used UI elements first
- Pay special attention to inventory, status bars, and interactive elements

## Export Settings

After annotation, go to the "Generate" tab and use these settings:

### Preprocessing:
- Resize: 640x640 (maintain aspect ratio with padding)
- Auto-orient: ON
- Image quality: 100%

### Augmentations (optimal for UI detection):
- Flip: OFF (UI elements have fixed orientation)
- 90° Rotations: OFF (UI is always properly oriented)
- Brightness: ±20% (accounts for different lighting)
- Blur: Up to 1px (minor blur tolerance)
- Noise: Up to 1% (slight noise tolerance)

Generate the dataset and download in YOLOv8 format, then extract the downloaded ZIP to your project's dataset folder.

## Tips for High-Quality Annotation

1. **Capture Diverse Gameplay**: Get screenshots from different game phases, UI states, and scenarios
2. **Focus on State Recognition**: Annotate the same UI element in different states (e.g., health bar when low vs. full)
3. **Annotate in Batches**: Group similar screenshots together for consistent annotation
4. **Verify Your Work**: Periodically check your annotations for consistency
5. **Prioritize Interactive Elements**: Focus on elements that will be crucial for automation

This detailed annotation guide will help you build a high-quality dataset that can recognize not just UI elements, but their specific states and contexts, enabling much more sophisticated automation.