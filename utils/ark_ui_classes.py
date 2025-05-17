"""
ARK UI class definitions.
This file contains the list of UI classes for ARK: Survival Ascended.
"""

# List of ARK UI classes for detection
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

# Common specific item classes
COMMON_ITEMS = [
    # Tools and weapons
    'inventory_item_stone_pick',
    'inventory_item_stone_hatchet',
    'inventory_item_spear',
    'inventory_item_pike',
    'inventory_item_bow',
    'inventory_item_crossbow',
    'inventory_item_metal_pick',
    'inventory_item_metal_hatchet',
    
    # Resources
    'inventory_item_stone',
    'inventory_item_wood',
    'inventory_item_thatch',
    'inventory_item_fiber',
    'inventory_item_hide',
    'inventory_item_metal',
    'inventory_item_flint',
    'inventory_item_crystal',
    'inventory_item_obsidian',
    
    # Consumables
    'inventory_item_raw_meat',
    'inventory_item_cooked_meat',
    'inventory_item_berry_mejoberry',
    'inventory_item_berry_amarberry',
    'inventory_item_berry_azulberry',
    'inventory_item_berry_tintoberry',
    'inventory_item_water',
    'inventory_item_medical_brew',
    'inventory_item_stimulant',
    'inventory_item_narcotic',
    
    # Armor
    'inventory_item_cloth_hat',
    'inventory_item_cloth_shirt',
    'inventory_item_cloth_pants',
    'inventory_item_cloth_boots',
    'inventory_item_hide_helmet',
    'inventory_item_hide_chestpiece',
    'inventory_item_hide_pants',
    'inventory_item_hide_boots',
    
    # Structures
    'inventory_item_campfire',
    'inventory_item_mortar_and_pestle',
    'inventory_item_forge',
    'inventory_item_smithy',
    'inventory_item_storage_box',
]

# Combine classes
ALL_ARK_UI_CLASSES = ARK_UI_CLASSES + COMMON_ITEMS