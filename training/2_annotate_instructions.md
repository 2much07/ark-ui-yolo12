### 2_annotate_instructions.md

Annotation Instructions for ARK: Survival Ascended UI Detection
This guide will help you annotate your ARK: Survival Ascended screenshots for training the YOLOv8 model.
Preferred Annotation Tool: Roboflow
We recommend using Roboflow for annotating your ARK UI screenshots:

Go to Roboflow and create a free account
Create a new project named "ARK-Ascended-UI-Detector"
Select "Object Detection" as the project type
Select "YOLOv8" as the annotation format

Uploading Screenshots

Click "Upload" and select all screenshots from your screenshots folder
Wait for the upload to complete
Begin annotating using the Roboflow interface

ARK UI Classes to Create
Create the following classes in your Roboflow project:
Status UI Elements

health_bar - Character health bar (red)
stamina_bar - Character stamina bar (green)
food_bar - Character food bar (orange)
water_bar - Character water/hydration bar (blue)
weight_bar - Character weight indicator
oxygen_bar - Oxygen bar when underwater (cyan)
torpidity_bar - Torpidity bar (purple)
xp_bar - Experience bar at bottom
level_icon - Level up notification icon

Alert Messages

starvation_alert - "You're starving" red message
dehydration_alert - Water shortage alert
overweight_alert - "Too much weight" message
level_alert - "Level up is available" message
death_message - Death screen text
tribe_message - Tribe notifications

Inventory Elements

inventory_slot - Individual inventory square
inventory_item - Item in inventory
item_stack_count - Number on stacked items
item_durability - Durability bar on items
search_bar - Inventory search field
weight_indicator - Current/max weight display
transfer_all - Transfer all items button
drop_item - Drop item button

Item Popups

item_name - Item name in tooltip
item_description - Item description text
craftable_label - "Craftable" indicator
blueprint_label - "Blueprint" indicator
engram_label - "Engram" label

Navigation Tabs

inventory_tab - Inventory tab
crafting_tab - Crafting tab
engram_tab - Engram tab
cosmetics_tab - Cosmetics/skins tab
tribe_tab - Tribe management tab
structure_tab - Structure tab for buildings

Map Elements

map_marker - Icons on map
player_location - Player location indicator
beacon_marker - Beacon/drop markers
bed_marker - Bed/spawn point marker
waypoint - Custom waypoint marker

Buttons

back_button - Back button
close_button - X/close button
option_button - Settings/options button
craft_button - Craft button in crafting menu
learn_button - Learn button for engrams
unlock_button - Unlock button
transfer_button - Transfer button between inventories

Creature UI

taming_bar - Taming progress bar
breeding_bar - Breeding/maturation bar
creature_stats - Creature statistics panel
creature_inventory - Creature inventory button
imprint_icon - Imprint icon/indicator

Structure UI

structure_health - Structure health bar
structure_name - Structure name label
storage_label - Storage count (e.g., "349/350")
fuel_indicator - Fuel level indicator
power_indicator - Power indicator (on/off)

HUD Elements

compass - Top compass bar
hotbar - Bottom item hotbar
extended_hotbar - Extended radial hotbar (when open)
emote_wheel - Emote selection wheel
whistle_menu - Dino whistle command menu

Special UI

tek_element - Tek tier related UI elements
cryopod_menu - Cryopod interface elements
tek_transmitter - Tek transmitter elements
obelisk_terminal - Obelisk upload/download interface
mission_terminal - Mission/quest terminal interface

Annotation Guidelines

Draw Precise Boxes

Draw tight bounding boxes around each UI element
Include the complete element (for bars, include the full bar, not just the filled portion)
For text elements, include the complete text area


Be Consistent

Use the same approach for similar elements
All inventory slots should be annotated the same way
All buttons of the same type should have similar sized boxes


Include All Instances

Label every instance of each class in each image
Don't skip partially visible UI elements


Prioritize Important Elements

Focus on interactive elements (buttons, tabs, slots)
Ensure status bars and alerts are well-annotated
Pay special attention to inventory items and slots


Handle Overlapping Elements

When UI elements overlap, annotate both elements
For an item in a slot, annotate both the slot and the item



Exporting Your Dataset

After annotation, go to "Generate" tab
Set preprocessing:

Resize: 640x640 (maintain aspect ratio with padding)
Auto-orient: ON
Image quality: 100%


Set augmentations (optimal for UI detection):

Flip: OFF (UI elements have fixed orientation)
90° Rotations: OFF (UI is always properly oriented)
Brightness: ±20% (accounts for different lighting)
Blur: Up to 1px (minor blur tolerance)
Noise: Up to 1% (slight noise tolerance)


Generate dataset and download in YOLOv8 format
Extract the downloaded ZIP to the dataset folder in your project

Advanced: Label Specific Items
For better automation, consider creating specific classes for common items:

item_pike
item_sword
item_metal_ingot
item_narcotics
item_raw_meat
item_cooked_meat

This allows the automation system to specifically target these items.


```markdown
# Annotation Instructions for ARK UI Detector

This guide walks you through annotating your ARK UI screenshots using Roboflow (free tier).

## Setup Roboflow

1. Go to [Roboflow](https://roboflow.com/) and create a free account
2. Create a new project called "ARK-UI-Detector"
3. Select "Object Detection" as the project type
4. Select "YOLOv8" as the annotation format

## Upload Images

1. Click "Upload" and select all the screenshots in your `screenshots` folder
2. Wait for the upload to complete

## Create Classes

Create the following classes in Roboflow:

1. `status_bar` - Health, stamina, food, water bars
2. `inventory_slot` - Individual inventory slots
3. `item_popup` - Tooltips and item descriptions
4. `nav_tab` - Navigation tabs (Inventory, Crafting, etc.)
5. `button` - Clickable buttons
6. `warning_message` - Alert messages
7. `map_marker` - Icons on the map
8. `player_stats` - Player level, XP, points
9. `menu_header` - Menu titles and headers
10. `item_icon` - Individual item icons
11. `structure_info` - Structure information panels

## Annotation Best Practices

- Draw tight bounding boxes around each UI element
- Be consistent with similar elements (all inventory slots should be annotated the same way)
- Include complete elements (for health bars, include the full bar, not just the filled portion)
- For overlapping elements, annotate both (like an item icon and its inventory slot)
- Annotate at least 200 images for good results

## Export Dataset

1. After annotation, go to "Generate" tab
2. Set preprocessing:
   - Resize: 640x640 (maintain aspect ratio with padding)
   - Auto-orient: ON
   - Image quality: 100%

3. Set augmentations:
   - Flip: Horizontal only (OFF)
   - 90° Rotations: 0
   - Brightness: ±25%
   - Blur: 0-1px
   - Noise: Up to 1% of pixels

4. Generate dataset and download in YOLOv8 format
5. Extract the downloaded ZIP file to the `dataset` folder in your project

## Alternative: Using LabelImg Instead

If you prefer a desktop application:

1. Download [LabelImg](https://github.com/heartexlabs/labelImg/releases)
2. Open your screenshots folder
3. Set format to YOLO
4. Create the same classes listed above
5. Save annotations in the same folder as images
```