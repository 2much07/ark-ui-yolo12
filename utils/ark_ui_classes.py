"""
ARK UI class definitions.
This file contains the comprehensive list of UI classes for ARK: Survival Ascended.
"""

# Complete list of ARK UI classes for detection - Enhanced Super Complete Version
ARK_UI_CLASSES = [
    # Basic UI Structural Elements (0-9)
    'ui_panel_background',          # Base panel background
    'ui_panel_border',              # Panel border/frame
    'ui_scrollbar',                 # Scrollbar element
    'ui_scrollbar_handle',          # Scrollbar drag handle
    'ui_divider',                   # Visual divider between sections
    'ui_highlight',                 # Currently selected element highlight
    'ui_dropdown_arrow',            # Dropdown menu arrow indicator
    'ui_checkbox_empty',            # Unchecked checkbox
    'ui_checkbox_filled',           # Checked checkbox
    'ui_slider',                    # Slider control element
    
    # Main HUD Elements (10-24)
    'hud_compass',                 # Top compass
    'hud_hotbar',                  # Bottom hotbar
    'hud_crosshair',               # Aiming crosshair
    'hud_interaction_prompt',      # "Press E to interact" text
    'hud_whistle_wheel',           # Dino whistle command wheel
    'hud_emote_wheel',             # Player emote wheel
    'hud_quickchat_wheel',         # Quick chat wheel
    'hud_extended_ui_toggle',      # Toggle for extended UI
    'hud_chat_box',                # Chat message display area
    'hud_chat_input',              # Chat text input field
    'hud_tribe_log_popup',         # Tribe log popup notification
    'hud_gps_coordinates',         # GPS coordinates display
    'hud_temperature_display',     # Current temperature display
    'hud_active_buffs',            # Active status effects/buffs
    'hud_active_debuffs',          # Active negative effects/debuffs
    
    # Status Indicators (25-49)
    'status_health_low',           # Health bar when low (critical)
    'status_health_medium',        # Health bar when medium
    'status_health_full',          # Health bar when full/high
    'status_stamina_low',          # Stamina bar when low
    'status_stamina_medium',       # Stamina bar when medium
    'status_stamina_full',         # Stamina bar when full
    'status_food_low',             # Food bar when low
    'status_food_medium',          # Food bar when medium
    'status_food_full',            # Food bar when full
    'status_water_low',            # Water bar when low
    'status_water_medium',         # Water bar when medium
    'status_water_full',           # Water bar when full
    'status_weight_low',           # Weight when low (mostly empty)
    'status_weight_medium',        # Weight when medium
    'status_weight_heavy',         # Weight when high/encumbered
    'status_torpor_low',           # Torpidity bar when low
    'status_torpor_medium',        # Torpidity bar when medium
    'status_torpor_high',          # Torpidity bar when high
    'status_xp_gained',            # XP gain popup/notification
    'status_level_up_available',   # Level up indicator
    'status_effect_icons',         # Status effect icons
    'status_oxygen_low',           # Oxygen bar when low
    'status_oxygen_medium',        # Oxygen bar when medium
    'status_oxygen_full',          # Oxygen bar when full
    'status_fortitude_indicator',  # Fortitude status indicator
    
    # Alert Messages (50-69)
    'alert_starvation',            # Starvation warning
    'alert_dehydration',           # Dehydration warning
    'alert_encumbered',            # Too heavy/encumbered warning
    'alert_too_hot',               # Temperature too hot warning
    'alert_too_cold',              # Temperature too cold warning
    'alert_level_up',              # Level up notification
    'alert_tribe_message',         # Tribe notification
    'alert_death_message',         # Death screen text
    'alert_taming_complete',       # Taming completed notification
    'alert_insufficient_engrams',  # Not enough engram points
    'alert_structure_blocked',     # Structure placement blocked
    'alert_enemy_player_nearby',   # Enemy player nearby warning
    'alert_server_message',        # Server announcement
    'alert_disconnection_warning', # Server disconnection warning
    'alert_item_broken',           # Item broken notification
    'alert_creature_starving',     # Creature starving warning
    'alert_creature_dying',        # Creature low health warning
    'alert_imprint_available',     # Imprinting available notification
    'alert_gasoline_low',          # Generator low fuel warning
    'alert_element_low',           # Tek structure low element warning
    
    # Player Inventory - Left Side (70-99)
    'player_inventory_title',      # "Inventory" title text
    'player_inventory_slot_empty', # Empty inventory slot
    'player_inventory_slot_filled', # Filled inventory slot
    'player_item_icon',            # Item in player inventory
    'player_item_stack_count',     # Stack count number
    'player_item_durability_high', # Item durability bar (high)
    'player_item_durability_med',  # Item durability bar (medium)
    'player_item_durability_low',  # Item durability bar (low/critical)
    'player_search_bar',           # Inventory search field
    'player_weight_current',       # Current weight number
    'player_weight_max',           # Maximum weight number
    'player_weight_slider',        # Weight slider/visual indicator
    'player_transfer_all_button',  # Transfer all items button (right arrow)
    'player_drop_item_button',     # Drop item button
    'player_character_model',      # 3D character model
    'player_armor_slot_head',      # Head armor slot
    'player_armor_slot_chest',     # Chest armor slot
    'player_armor_slot_gloves',    # Gloves armor slot
    'player_armor_slot_legs',      # Legs armor slot
    'player_armor_slot_feet',      # Feet armor slot
    'player_armor_slot_shield',    # Shield slot
    'player_quick_bar_slot',       # Hotbar quick slot assignment
    'player_sort_button',          # Sort inventory button
    'player_filter_button',        # Filter inventory button
    'player_folder_tab',           # Folder/category tab
    'player_folder_item_count',    # Item count in folder
    'player_blueprint_icon',       # Blueprint icon overlay
    'player_item_equipped_marker', # Equipped item indicator
    'player_item_favorite_marker', # Favorited item indicator
    'player_quick_access_bar',     # Quick access bar
    
    # Entity Inventory - Right Side (100-129)
    'entity_inventory_title',     # Entity name title text
    'entity_inventory_slot_empty', # Empty entity inventory slot
    'entity_inventory_slot_filled', # Filled entity inventory slot
    'entity_item_icon',           # Item in entity inventory
    'entity_item_stack_count',    # Stack count in entity inventory
    'entity_item_durability',     # Item durability in entity inventory
    'entity_search_bar',          # Entity inventory search field
    'entity_weight_current',      # Entity current weight number
    'entity_weight_max',          # Entity maximum weight number
    'entity_weight_slider',       # Entity weight slider/indicator
    'entity_transfer_all_button', # Transfer all to player button (left arrow)
    'entity_drop_item_button',    # Drop item from entity button
    'entity_model',               # Entity 3D model (if shown)
    'structure_name',             # Structure name title
    'structure_content_count',    # Content count (e.g., "50/100")
    'dino_name',                  # Dinosaur name title
    'dino_level',                 # Dinosaur level display
    'dino_stats_button',          # View dinosaur stats button
    'dino_inventory_button',      # View dinosaur inventory button
    'dino_behavior_setting',      # Dinosaur behavior setting
    'dino_following_setting',     # Dinosaur following setting
    'dino_options_button',        # Dinosaur options button
    'dino_saddle_slot',           # Dinosaur saddle slot
    'dino_armor_slot',            # Dinosaur armor slot
    'structure_power_indicator',  # Structure power indicator (on/off)
    'structure_fuel_level',       # Structure fuel level indicator
    'structure_options_button',   # Structure options button
    'remote_use_button',          # Remote use/access button
    'remote_inventory_button',    # Remote inventory button
    'transfer_to_container_text', # "Transfer to [container]" text
    
    # Item Tooltip & Details (130-154)
    'item_tooltip_background',    # Item tooltip background panel
    'item_tooltip_title',         # Item name in tooltip
    'item_tooltip_description',   # Item description text
    'item_tooltip_weight',        # Item weight value
    'item_tooltip_durability',    # Item durability details
    'item_spoil_timer',           # Spoilage timer for perishables
    'item_tooltip_stats',         # Item stats (weapons/armor)
    'item_tooltip_requirements',  # Item usage requirements
    'item_tooltip_engram_req',    # Engram requirements for blueprint
    'item_tooltip_blueprint',     # "Blueprint:" indicator text
    'item_tooltip_quality_prim',  # Primitive quality indicator
    'item_tooltip_quality_common', # Common quality indicator
    'item_tooltip_quality_rare',  # Rare quality indicator
    'item_tooltip_quality_epic',  # Epic quality indicator
    'item_tooltip_quality_legend', # Legendary quality indicator
    'item_tooltip_quality_asc',   # Ascendant quality indicator
    'item_tooltip_crafted_by',    # "Crafted by:" information
    'item_tooltip_repair_cost',   # Repair cost information
    'item_equip_option',          # "Equip" option in context menu
    'item_drop_option',           # "Drop" option in context menu
    'item_transfer_option',       # "Transfer" option in context menu
    'item_split_option',          # "Split Stack" option in context menu
    'item_consume_option',        # "Consume" option in context menu
    'item_rename_option',         # "Rename" option in context menu
    'item_demolish_timer',        # Demolish countdown timer
    
    # Crafting & Engrams (155-184)
    'craft_button_active',        # Craft button when clickable
    'craft_button_inactive',      # Craft button when unavailable
    'crafting_queue_slot_empty',  # Empty crafting queue slot
    'crafting_queue_slot_occupied', # Occupied crafting queue slot
    'crafting_progress_bar_idle', # Crafting progress bar (idle)
    'crafting_progress_bar_active', # Crafting progress bar (active)
    'required_materials_sufficient', # Materials indicator (sufficient)
    'required_materials_insufficient', # Materials indicator (insufficient)
    'blueprint_availability_icon', # Blueprint available indicator
    'craft_all_button',           # "Craft All" button
    'craft_one_button',           # "Craft 1" button
    'crafting_speed_modifier',    # Crafting speed modifier display
    'engram_points_available',    # Available engram points display
    'engram_icon_locked',         # Locked engram icon
    'engram_icon_available',      # Available engram icon
    'engram_icon_learned',        # Learned engram icon
    'engram_level_requirement',   # Level requirement for engram
    'engram_points_cost',         # Engram points cost display
    'engram_search_bar',          # Engram search field
    'engram_filter_button',       # Engram filter options button
    'engram_category_tab',        # Engram category tab
    'tek_engram_category',        # Tek tier engram category
    'engram_hide_learned_toggle', # Toggle to hide learned engrams
    'engram_item_icon',           # Engram item preview icon
    'learn_button_active',        # "Learn" button when active
    'learn_button_inactive',      # "Learn" button when inactive
    'mindwipe_tonic_indicator',   # Mindwipe tonic availability
    'crafting_station_required',  # Required crafting station indicator
    'crafting_requirement_met',   # Requirement met checkmark
    'crafting_requirement_unmet', # Requirement unmet X mark
    
    # Tab Navigation (185-204)
    'inventory_tab',              # Inventory tab
    'inventory_tab_selected',     # Inventory tab when selected
    'crafting_tab',               # Crafting tab
    'crafting_tab_selected',      # Crafting tab when selected
    'engram_tab',                 # Engram tab
    'engram_tab_selected',        # Engram tab when selected
    'character_tab',              # Character stats tab
    'character_tab_selected',     # Character tab when selected
    'tribe_tab',                  # Tribe management tab
    'tribe_tab_selected',         # Tribe tab when selected
    'structure_tab',              # Structure options tab
    'structure_tab_selected',     # Structure tab when selected
    'spawn_map_tab',              # Spawn location tab
    'spawn_map_tab_selected',     # Spawn location tab when selected
    'tek_teleport_tab',           # Tek teleporter tab
    'tek_teleport_tab_selected',  # Tek teleporter tab when selected
    'cosmetic_tab',               # Cosmetics/skins tab
    'cosmetic_tab_selected',      # Cosmetics tab when selected
    'tribute_tab',                # Tribute tab
    'tribute_tab_selected',       # Tribute tab when selected
    
    # Map Elements (205-229)
    'map_background',             # Map background/terrain
    'map_player_marker',          # Player location marker
    'map_tribe_member_marker',    # Tribe member marker
    'map_tamed_dino_marker',      # Tamed dino location marker
    'map_bed_marker',             # Bed spawn point marker
    'map_base_marker',            # Base/structure marker
    'map_waypoint_marker',        # Custom waypoint marker
    'map_obelisk_marker',         # Obelisk marker
    'map_cave_entrance_marker',   # Cave entrance marker
    'map_beacon_marker',          # Drop beacon marker
    'map_mission_marker',         # Mission start location marker
    'map_boss_terminal_marker',   # Boss terminal marker
    'map_supply_drop_marker',     # Supply drop marker
    'map_explorer_note_marker',   # Explorer note marker
    'map_glitch_marker',          # Glitch/corruption marker
    'map_resource_node_marker',   # Resource node marker
    'map_charging_station_marker', # Charge station marker
    'map_ocean_depth_indicator',  # Ocean depth coloration
    'map_coordinates_display',    # Map coordinates display
    'map_zoom_in_button',         # Map zoom in control
    'map_zoom_out_button',        # Map zoom out control
    'map_filter_button',          # Map filter options button
    'map_place_waypoint_button',  # Place waypoint button
    'map_clear_waypoint_button',  # Clear waypoint button
    'map_region_name_text',       # Region/biome name display
    
    # Button Elements (230-249)
    'button_default',             # Standard button
    'button_highlighted',         # Button when highlighted/hovered
    'button_pressed',             # Button when pressed
    'button_disabled',            # Button when disabled
    'back_button',                # Back/return button
    'close_button',               # Close/X button
    'option_button',              # Options/settings button
    'accept_button',              # Accept/confirm button
    'cancel_button',              # Cancel button
    'pin_button',                 # Pin item button
    'unpin_button',               # Unpin item button
    'transfer_button',            # Transfer button
    'rename_button',              # Rename button
    'sort_button',                # Sort items button
    'unclaim_button',             # Unclaim dino button
    'enable_wandering_button',    # Enable wandering button
    'disable_wandering_button',   # Disable wandering button
    'enable_mating_button',       # Enable mating button
    'disable_mating_button',      # Disable mating button
    'destroy_button',             # Destroy/demolish button
    
    # Creature & Taming Elements (250-274)
    'taming_progress_bar_empty',  # Taming progress bar (empty)
    'taming_progress_bar_partial', # Taming progress bar (partially filled)
    'taming_progress_bar_full',   # Taming progress bar (nearly complete)
    'taming_effectiveness_high',  # Taming effectiveness indicator (high)
    'taming_effectiveness_medium', # Taming effectiveness indicator (medium)
    'taming_effectiveness_low',   # Taming effectiveness indicator (low)
    'creature_health_bar',        # Creature health bar
    'creature_stamina_bar',       # Creature stamina bar
    'creature_food_bar',          # Creature food bar
    'creature_torpidity_bar',     # Creature torpidity bar
    'creature_level_text',        # Creature level display
    'creature_gender_male',       # Male gender icon
    'creature_gender_female',     # Female gender icon
    'creature_xp_bar',            # Creature XP bar
    'maturation_progress_bar',    # Baby dino maturation progress
    'incubation_progress_bar',    # Egg incubation progress
    'gestation_progress_bar',     # Pregnancy gestation progress
    'imprint_icon',               # Imprinting icon/indicator
    'imprint_progress_bar',       # Imprinting progress bar
    'imprint_timer',              # Time until next imprint
    'creature_stat_points',       # Available stat points indicator
    'creature_stat_increase_button', # Stat increase button
    'creature_mutation_counter',  # Mutation counter
    'cryopod_cooldown_timer',     # Cryopod cooldown timer
    'cryopod_creature_preview',   # Creature preview in cryopod
    
    # Structure Interface Elements (275-294)
    'structure_health_bar',       # Structure health bar
    'structure_shield_bar',       # Tek shield strength bar
    'structure_inventory_button', # Structure inventory button
    'structure_transfer_button',  # Transfer to structure button
    'structure_options_menu',     # Structure options menu
    'structure_demolish_option',  # Demolish structure option
    'structure_pickup_option',    # Pick up structure option
    'structure_paint_option',     # Paint structure option
    'structure_change_pin_option', # Change pin code option
    'structure_snap_points',      # Structure snap points
    'structure_placement_valid',  # Valid placement indicator
    'structure_placement_invalid', # Invalid placement indicator
    'structure_powered_indicator', # Powered indicator (green)
    'structure_unpowered_indicator', # Unpowered indicator (red)
    'generator_fuel_level',       # Generator fuel level indicator
    'electrical_wire_connection', # Electrical wire connection point
    'water_pipe_connection',      # Water pipe connection point
    'gas_pipe_connection',        # Gas pipe connection point
    'storage_capacity_indicator', # Storage capacity indicator (e.g., "50/100")
    'auto_turret_ammo_indicator', # Auto-turret ammunition indicator
    
    # Special Menu Interfaces (295-319)
    'tek_element_icon',           # Tek element resource icon
    'tek_teleporter_interface',   # Tek teleporter menu
    'tek_transmitter_interface',  # Tek transmitter menu
    'tek_replicator_interface',   # Tek replicator crafting menu
    'obelisk_interface',          # Obelisk terminal interface
    'tribute_terminal_interface', # Tribute terminal interface
    'city_terminal_interface',    # City terminal interface 
    'mission_terminal_interface', # Mission terminal interface
    'cryofridge_interface',       # Cryofridge storage interface
    'cooking_pot_interface',      # Cooking pot recipe interface
    'industrial_cooker_interface', # Industrial cooker interface
    'fabricator_interface',       # Fabricator crafting interface
    'chemistry_bench_interface',  # Chemistry bench interface
    'tek_cloning_interface',      # Tek cloning chamber interface
    'tek_dedicated_storage',      # Tek dedicated storage interface
    'tek_trough_interface',       # Tek trough interface
    'upload_creature_button',     # Upload creature button
    'download_creature_button',   # Download creature button
    'upload_item_button',         # Upload item button
    'download_item_button',       # Download item button
    'boss_arena_teleport_button', # Boss arena teleport button
    'genesis_mission_list',       # Genesis mission selection list
    'fjordur_realm_portal',       # Fjordur realm portal interface
    'cave_entrance_transfer',     # Cave entrance transfer interface
    'ascension_terminal',         # Ascension terminal interface
    
    # Character Stats Interface (320-339)
    'character_stat_health',      # Health stat in character menu
    'character_stat_stamina',     # Stamina stat in character menu
    'character_stat_oxygen',      # Oxygen stat in character menu
    'character_stat_food',        # Food stat in character menu
    'character_stat_water',       # Water stat in character menu
    'character_stat_weight',      # Weight stat in character menu
    'character_stat_melee',       # Melee damage stat in character menu
    'character_stat_speed',       # Movement speed stat in character menu
    'character_stat_fortitude',   # Fortitude stat in character menu
    'character_stat_crafting',    # Crafting skill stat in character menu
    'character_level_display',    # Character level display
    'character_xp_bar',           # Character XP bar
    'character_xp_to_next_level', # XP needed for next level
    'character_stat_points',      # Available stat points counter
    'character_stat_increase_button', # Stat increase button
    'character_total_level_cap',  # Total level cap display
    'character_ascension_level',  # Ascension level indicator
    'character_chibi_level',      # Chibi-pet level display
    'character_mutation_counter', # Character mutation counter
    'character_mindwipe_reminder', # Mindwipe availability reminder
    
    # Tribe Interface Elements (340-359)
    'tribe_name_display',         # Tribe name display
    'tribe_rank_display',         # Player's tribe rank display
    'tribe_member_list',          # Tribe member list
    'tribe_member_entry',         # Individual tribe member entry
    'tribe_member_online',        # Online tribe member indicator
    'tribe_member_offline',       # Offline tribe member indicator
    'tribe_log_tab',              # Tribe log tab
    'tribe_log_entry',            # Individual tribe log entry
    'tribe_alliance_tab',         # Tribe alliance management tab
    'tribe_governance_tab',       # Tribe governance settings tab
    'tribe_rank_management',      # Tribe rank management interface
    'tribe_permissions_setting',  # Tribe permissions settings
    'tribe_pincode_setting',      # Tribe PIN code setting
    'tribe_tame_claim_setting',   # Tribe tame claiming setting
    'tribe_structure_ownership',  # Tribe structure ownership setting
    'tribe_invitation_button',    # Invite to tribe button
    'tribe_kick_button',          # Remove from tribe button
    'tribe_promote_button',       # Promote member button
    'tribe_demote_button',        # Demote member button
    'tribe_leave_button',         # Leave tribe button
    
    # Common Resources (360-399)
    'inventory_item_stone',       # Stone resource
    'inventory_item_wood',        # Wood resource
    'inventory_item_thatch',      # Thatch resource
    'inventory_item_fiber',       # Fiber resource
    'inventory_item_hide',        # Hide resource
    'inventory_item_metal',       # Metal resource
    'inventory_item_flint',       # Flint resource
    'inventory_item_crystal',     # Crystal resource
    'inventory_item_obsidian',    # Obsidian resource
    'inventory_item_silica_pearls', # Silica Pearls resource
    'inventory_item_oil',         # Oil resource
    'inventory_item_element',     # Element resource
    'inventory_item_element_shard', # Element Shard resource
    'inventory_item_element_dust', # Element Dust resource
    'inventory_item_polymer',     # Polymer resource
    'inventory_item_organic_polymer', # Organic Polymer resource
    'inventory_item_cementing_paste', # Cementing Paste resource
    'inventory_item_chitin',      # Chitin resource
    'inventory_item_keratin',     # Keratin resource
    'inventory_item_pelt',        # Pelt resource
    'inventory_item_electronics', # Electronics resource
    'inventory_item_gasoline',    # Gasoline resource
    'inventory_item_metal_ingot', # Metal Ingot resource
    'inventory_item_narcotics',   # Narcotics item
    'inventory_item_stimulant',   # Stimulant item
    'inventory_item_raw_meat',    # Raw Meat food
    'inventory_item_cooked_meat', # Cooked Meat food
    'inventory_item_spoiled_meat', # Spoiled Meat
    'inventory_item_raw_prime',   # Raw Prime Meat
    'inventory_item_cooked_prime', # Cooked Prime Meat
    'inventory_item_kibble',      # Kibble food
    'inventory_item_berry_mejo',  # Mejoberry
    'inventory_item_berry_narco', # Narcoberry
    'inventory_item_berry_stim',  # Stimberry
    'inventory_item_berry_amar',  # Amarberry
    'inventory_item_berry_azul',  # Azulberry
    'inventory_item_berry_tinto', # Tintoberry
    'inventory_item_rare_flower', # Rare Flower 
    'inventory_item_rare_mushroom', # Rare Mushroom
    'inventory_item_sap',         # Tree Sap
    
    # Tools, Weapons & Equipment (400-449)
    'inventory_item_stone_pick',  # Stone Pickaxe
    'inventory_item_stone_hatchet', # Stone Hatchet
    'inventory_item_metal_pick',  # Metal Pickaxe
    'inventory_item_metal_hatchet', # Metal Hatchet
    'inventory_item_spear',       # Spear
    'inventory_item_pike',        # Pike
    'inventory_item_bow',         # Bow
    'inventory_item_crossbow',    # Crossbow
    'inventory_item_simple_pistol', # Simple Pistol
    'inventory_item_longneck_rifle', # Longneck Rifle
    'inventory_item_shotgun',     # Shotgun
    'inventory_item_fab_rifle',   # Fabricated Rifle
    'inventory_item_rocket_launcher', # Rocket Launcher
    'inventory_item_c4_charge',   # C4 Explosive
    'inventory_item_grappling_hook', # Grappling Hook
    'inventory_item_parachute',   # Parachute
    'inventory_item_whip',        # Whip
    'inventory_item_bola',        # Bola
    'inventory_item_sickle',      # Sickle
    'inventory_item_harpoon',     # Harpoon Gun
    'inventory_item_tranq_arrow', # Tranquilizer Arrow
    'inventory_item_tranq_dart',  # Tranquilizer Dart
    'inventory_item_simple_bullet', # Simple Bullet
    'inventory_item_advanced_bullet', # Advanced Rifle Bullet
    'inventory_item_shotgun_shell', # Shotgun Shell
    'inventory_item_flamethrower', # Flamethrower
    'inventory_item_chainsaw',    # Chainsaw
    'inventory_item_mining_drill', # Mining Drill
    'inventory_item_tek_rifle',   # Tek Rifle
    'inventory_item_tek_sword',   # Tek Sword
    'inventory_item_tek_grenade', # Tek Grenade
    'inventory_item_compound_bow', # Compound Bow
    'inventory_item_sword',       # Metal Sword
    'inventory_item_shield',      # Shield
    'inventory_item_waterskin',   # Waterskin
    'inventory_item_canteen',     # Canteen
    'inventory_item_spyglass',    # Spyglass
    'inventory_item_compass',     # Compass
    'inventory_item_gps',         # GPS Device
    'inventory_item_radio',       # Radio
    'inventory_item_gas_collector', # Gas Collector
    'inventory_item_glider_suit', # Glider Suit
    'inventory_item_tek_hover_skiff', # Tek Hover Skiff
    'inventory_item_gas_mask',    # Gas Mask
    'inventory_item_scuba_mask',  # Scuba Mask
    'inventory_item_scuba_tank',  # Scuba Tank
    'inventory_item_fur_armor',   # Fur Armor (generic)
    'inventory_item_ghillie_armor', # Ghillie Armor (generic)
    'inventory_item_riot_armor',  # Riot Armor (generic)
    'inventory_item_tek_armor',   # Tek Armor (generic)
    
    # Armor & Clothing (450-474)
    'inventory_item_cloth_helmet', # Cloth Helmet
    'inventory_item_cloth_shirt', # Cloth Shirt
    'inventory_item_cloth_pants', # Cloth Pants
    'inventory_item_cloth_boots', # Cloth Boots
    'inventory_item_hide_helmet', # Hide Helmet
    'inventory_item_hide_chest',  # Hide Chestpiece
    'inventory_item_hide_pants',  # Hide Pants
    'inventory_item_hide_boots',  # Hide Boots
    'inventory_item_chitin_helmet', # Chitin Helmet
    'inventory_item_chitin_chest', # Chitin Chestpiece
    'inventory_item_chitin_pants', # Chitin Pants
    'inventory_item_chitin_boots', # Chitin Boots
    'inventory_item_flak_helmet', # Flak Helmet
    'inventory_item_flak_chest',  # Flak Chestpiece
    'inventory_item_flak_pants',  # Flak Pants
    'inventory_item_flak_boots',  # Flak Boots
    'inventory_item_riot_helmet', # Riot Helmet
    'inventory_item_riot_chest',  # Riot Chestpiece
    'inventory_item_riot_pants',  # Riot Pants
    'inventory_item_riot_boots',  # Riot Boots
    'inventory_item_tek_helmet',  # Tek Helmet
    'inventory_item_tek_chest',   # Tek Chestpiece
    'inventory_item_tek_pants',   # Tek Pants
    'inventory_item_tek_boots',   # Tek Boots
    'inventory_item_tek_gauntlets', # Tek Gauntlets
    
    # Structures & Building (475-499)
    'inventory_item_thatch_foundation', # Thatch Foundation
    'inventory_item_wood_foundation', # Wood Foundation
    'inventory_item_stone_foundation', # Stone Foundation
    'inventory_item_metal_foundation', # Metal Foundation
    'inventory_item_tek_foundation', # Tek Foundation
    'inventory_item_wall',        # Wall (generic)
    'inventory_item_ceiling',     # Ceiling (generic)
    'inventory_item_doorframe',   # Doorframe (generic)
    'inventory_item_door',        # Door (generic)
    'inventory_item_campfire',    # Campfire
    'inventory_item_fireplace',   # Stone Fireplace
    'inventory_item_cooking_pot', # Cooking Pot
    'inventory_item_mortar_pestle', # Mortar and Pestle
    'inventory_item_forge',       # Refining Forge
    'inventory_item_smithy',      # Smithy
    'inventory_item_fabricator',  # Fabricator
    'inventory_item_generator',   # Electrical Generator
    'inventory_item_ind_forge',   # Industrial Forge
    'inventory_item_ind_grill',   # Industrial Grill
    'inventory_item_chem_bench',  # Chemistry Bench
    'inventory_item_storage_box', # Storage Box
    'inventory_item_large_box',   # Large Storage Box
    'inventory_item_vault',       # Vault
    'inventory_item_refrigerator', # Refrigerator
    'inventory_item_preserving_bin', # Preserving Bin
    
    # Creature-Related Items (500-519)
    'inventory_item_saddle',      # Saddle (generic)
    'inventory_item_platform_saddle', # Platform Saddle (generic)
    'inventory_item_tek_saddle',  # Tek Saddle (generic)
    'inventory_item_cryopod',     # Cryopod
    'inventory_item_cryopod_filled', # Filled Cryopod
    'inventory_item_egg',         # Creature Egg (generic)
    'inventory_item_fert_egg',    # Fertilized Egg (generic)
    'inventory_item_kibble_basic', # Basic Kibble
    'inventory_item_kibble_simple', # Simple Kibble
    'inventory_item_kibble_regular', # Regular Kibble
    'inventory_item_kibble_superior', # Superior Kibble
    'inventory_item_kibble_exceptional', # Exceptional Kibble
    'inventory_item_kibble_extraordinary', # Extraordinary Kibble
    'inventory_item_breeding_pair', # Breeding Pair icon
    'inventory_item_imprint_food', # Imprint food request item
    'inventory_item_leash',       # Creature Leash
    'inventory_item_creature_finder', # Creature Finder
    'inventory_item_taxidermy_tool', # Taxidermy Tool
    'inventory_item_creature_mask', # Creature Costume (generic)
    'inventory_item_taming_food', # Taming Food (generic)
    
    # Advanced Elements & Systems (520-539)
    'tek_generator_interface',    # Tek Generator Interface
    'tek_crop_plot_interface',    # Tek Crop Plot Interface
    'creature_camera_view',       # Creature-mounted camera view
    'tek_sensor_interface',       # Tek Sensor interface
    'tek_remote_camera',          # Tek Remote Surveillance
    'holo_projector_interface',   # Holo-Projector interface
    'manage_hex_store',           # Manage Genesis Hexagon Store
    'megachelon_planter',         # Megachelon back planter interface
    'aquatic_tames_oxygen_interface', # Aquatic creature oxygen interface
    'genesis_shop_interface',     # Genesis HLNA Shop interface
    'mission_tracker',           # Mission objective tracker
    'boss_fight_timer',          # Boss fight time remaining
    'astrodelphis_energy',       # Astrodelphis stardust energy meter
    'noglin_brain_jack_interface', # Noglin brain-jack interface
    'exo_mek_interface',         # Exo-Mek control interface
    'maewing_baby_milk_meter',   # Maewing milk storage meter
    'shadowmane_charge_meter',   # Shadowmane charge meter
    'gacha_crafting_interface',  # Gacha item production interface
    'stryder_interface',         # Stryder harvesting interface
    'enforcer_interface',        # Enforcer interface
    
    # Event-Specific UI (540-549)
    'holiday_event_interface',   # Holiday event UI
    'easter_egg_hunt_tracker',   # Easter egg hunt progress tracker
    'summer_bash_interface',     # Summer bash event interface
    'fear_evolved_interface',    # Fear Evolved event interface
    'winter_wonderland_interface', # Winter Wonderland interface
    'valentines_day_interface',  # Valentine's Day event interface
    'eggcellent_adventure_ui',   # Eggcellent Adventure UI
    'genesis_race_timer',        # Genesis race mission timer
    'genesis_hunt_tracker',      # Genesis hunt mission tracker
    'genesis_fishing_meter',     # Genesis fishing mission meter
]

# Common specific item classes (a subset of the full list)
COMMON_ITEMS = [
    # Resources
    'inventory_item_stone',            # Stone resource
    'inventory_item_wood',             # Wood resource
    'inventory_item_thatch',           # Thatch resource
    'inventory_item_fiber',            # Fiber resource
    'inventory_item_hide',             # Hide resource
    'inventory_item_metal',            # Metal resource
    'inventory_item_flint',            # Flint resource
    'inventory_item_crystal',          # Crystal resource
    'inventory_item_obsidian',         # Obsidian resource
    'inventory_item_silica_pearls',    # Silica Pearls resource
    'inventory_item_oil',              # Oil resource
    'inventory_item_element',          # Element resource
    'inventory_item_polymer',          # Polymer resource
    'inventory_item_cementing_paste',  # Cementing Paste resource
    'inventory_item_narcotics',        # Narcotics item
    'inventory_item_stimulant',        # Stimulant item
    'inventory_item_raw_meat',         # Raw Meat food
    'inventory_item_cooked_meat',      # Cooked Meat food
    
    # Tools and weapons
    'inventory_item_stone_pick',       # Stone Pickaxe
    'inventory_item_stone_hatchet',    # Stone Hatchet
    'inventory_item_metal_pick',       # Metal Pickaxe
    'inventory_item_metal_hatchet',    # Metal Hatchet
    'inventory_item_spear',            # Spear
    'inventory_item_pike',             # Pike
    'inventory_item_bow',              # Bow
    'inventory_item_crossbow',         # Crossbow
    
    # Armor
    'inventory_item_cloth_helmet',     # Cloth Helmet
    'inventory_item_cloth_shirt',      # Cloth Shirt
    'inventory_item_cloth_pants',      # Cloth Pants
    'inventory_item_cloth_boots',      # Cloth Boots
    'inventory_item_hide_helmet',      # Hide Helmet
    'inventory_item_hide_chest',       # Hide Chestpiece
    'inventory_item_hide_pants',       # Hide Pants
    'inventory_item_hide_boots',       # Hide Boots
    
    # Structures
    'inventory_item_campfire',         # Campfire
    'inventory_item_mortar_pestle',    # Mortar and Pestle
    'inventory_item_forge',            # Refining Forge
    'inventory_item_smithy',           # Smithy
    'inventory_item_storage_box',      # Storage Box
]

# Combine classes
ALL_ARK_UI_CLASSES = ARK_UI_CLASSES + COMMON_ITEMS