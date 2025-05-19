"""
ARK UI Classes - Comprehensive hierarchical classification system
Complete implementation with proper inheritance structure for all ARK UI elements

This module provides class definitions for ARK: Survival Ascended UI elements with proper hierarchy:
UIElement → Category → Subcategory → Specific Elements

Color mappings and attributes are maintained throughout the inheritance chain.
"""

import os
import yaml
from collections import defaultdict
import re


# Base class for all UI elements
class UIElement:
    """Base class for all UI elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        self.name = name
        self.color = color
        self.type = element_type
        self.attributes = attributes or {}
        self.bounds = None  # Bounding box when detected
        self.confidence = 0.0  # Detection confidence score

    def __str__(self):
        return f"{self.name} ({self.type})"
    
    def set_detection_info(self, bounds, confidence):
        """Set detection information"""
        self.bounds = bounds
        self.confidence = confidence
        
    def get_color_code(self):
        """Get color code based on element type"""
        return self.color


###############################
# HUD ELEMENTS
###############################

class HUDElements(UIElement):
    """Base class for HUD Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "HUD Elements"


class HUDHealthIndicators(HUDElements):
    """Class for health-related HUD indicators"""
    def __init__(self, name, color="#c80000", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Health Indicators"
        
    # Element definitions
    hud_healthbar = "hud_healthbar"
    hud_healthbar_full = "hud_healthbar_full" 
    hud_healthbar_medium = "hud_healthbar_medium"
    hud_healthbar_low = "hud_healthbar_low"
    

class HUDStaminaIndicators(HUDElements):
    """Class for stamina-related HUD indicators"""
    def __init__(self, name, color="#00d43c", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Stamina Indicators"
        
    # Element definitions
    hud_staminabar = "hud_staminabar"
    hud_staminabar_full = "hud_staminabar_full"
    hud_staminabar_medium = "hud_staminabar_medium"
    hud_staminabar_low = "hud_staminabar_low"


class HUDFoodIndicators(HUDElements):
    """Class for food-related HUD indicators"""
    def __init__(self, name, color="#ff9a00", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Food Indicators"
        
    # Element definitions
    hud_foodbar = "hud_foodbar"
    hud_foodbar_full = "hud_foodbar_full"
    hud_foodbar_medium = "hud_foodbar_medium" 
    hud_foodbar_low = "hud_foodbar_low"


class HUDWaterIndicators(HUDElements):
    """Class for water-related HUD indicators"""
    def __init__(self, name, color="#00a9ff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Water Indicators"
        
    # Element definitions
    hud_waterbar = "hud_waterbar"
    hud_waterbar_full = "hud_waterbar_full"
    hud_waterbar_medium = "hud_waterbar_medium"
    hud_waterbar_low = "hud_waterbar_low"


class HUDOxygenIndicators(HUDElements):
    """Class for oxygen-related HUD indicators"""
    def __init__(self, name, color="#00c3ff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Oxygen Indicators"
        
    # Element definitions
    hud_oxygenbar = "hud_oxygenbar"
    hud_oxygenbar_full = "hud_oxygenbar_full"
    hud_oxygenbar_medium = "hud_oxygenbar_medium"
    hud_oxygenbar_low = "hud_oxygenbar_low"


class HUDWeightIndicators(HUDElements):
    """Class for weight-related HUD indicators"""
    def __init__(self, name, color="#a0a0a0", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Weight Indicators"
        
    # Element definitions
    hud_weightbar = "hud_weightbar"
    hud_weightbar_light = "hud_weightbar_light"
    hud_weightbar_medium = "hud_weightbar_medium"
    hud_weightbar_heavy = "hud_weightbar_heavy"
    hud_weightbar_overweight = "hud_weightbar_overweight"


class HUDTorpidityIndicators(HUDElements):
    """Class for torpidity-related HUD indicators"""
    def __init__(self, name, color="#9b59b6", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Torpidity Indicators"
        
    # Element definitions
    hud_torpiditybar = "hud_torpiditybar"
    hud_torpiditybar_low = "hud_torpiditybar_low"
    hud_torpiditybar_medium = "hud_torpiditybar_medium"
    hud_torpiditybar_high = "hud_torpiditybar_high"


class HUDExperienceIndicators(HUDElements):
    """Class for experience-related HUD indicators"""
    def __init__(self, name, color="#f1c40f", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Experience Indicators"
        
    # Element definitions
    hud_xp_bar = "hud_xp_bar"
    hud_levelup_alert = "hud_levelup_alert"
    hud_xp_notification = "hud_xp_notification"


class HUDCompassElements(HUDElements):
    """Class for compass-related HUD elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Compass Elements"
        
    # Element definitions
    hud_compass = "hud_compass"
    hud_compass_north = "hud_compass_north"
    hud_compass_east = "hud_compass_east"
    hud_compass_south = "hud_compass_south"
    hud_compass_west = "hud_compass_west"
    hud_compass_degrees = "hud_compass_degrees"
    hud_compass_direction = "hud_compass_direction"
    hud_gps_coordinates = "hud_gps_coordinates"
    hud_altitude_indicator = "hud_altitude_indicator"
    hud_depth_indicator = "hud_depth_indicator"


class HUDTemperatureIndicators(HUDElements):
    """Class for temperature-related HUD indicators"""
    def __init__(self, name, color="#e74c3c", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Temperature Indicators"
        
    # Element definitions
    hud_temperature_indicator = "hud_temperature_indicator"
    hud_temperature_hot = "hud_temperature_hot"
    hud_temperature_comfortable = "hud_temperature_comfortable"
    hud_temperature_cold = "hud_temperature_cold"


class HUDBuffIndicators(HUDElements):
    """Class for buff-related HUD indicators"""
    def __init__(self, name, color="#2ecc71", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Buff Indicators"
        
    # Element definitions
    hud_buff_icon = "hud_buff_icon"
    hud_buff_icon_generalized = "hud_buff_icon_generalized"
    hud_buff_icon_food = "hud_buff_icon_food"
    hud_buff_icon_water = "hud_buff_icon_water"
    hud_buff_icon_shelter = "hud_buff_icon_shelter"
    hud_buff_icon_mating = "hud_buff_icon_mating"


class HUDDebuffIndicators(HUDElements):
    """Class for debuff-related HUD indicators"""
    def __init__(self, name, color="#e74c3c", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Debuff Indicators"
        
    # Element definitions
    hud_debuff_icon = "hud_debuff_icon"
    hud_buff_icon_encumbered = "hud_buff_icon_encumbered"
    hud_buff_icon_hypothermia = "hud_buff_icon_hypothermia"
    hud_buff_icon_hyperthermia = "hud_buff_icon_hyperthermia"
    hud_buff_icon_poisoned = "hud_buff_icon_poisoned"
    hud_buff_icon_diseased = "hud_buff_icon_diseased"
    hud_buff_icon_broken_bone = "hud_buff_icon_broken_bone"


class HUDChatElements(HUDElements):
    """Class for chat-related HUD elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Chat Elements"
        
    # Element definitions
    hud_chat_window = "hud_chat_window"
    hud_chat_input = "hud_chat_input"
    hud_chat_global_tab = "hud_chat_global_tab"
    hud_chat_local_tab = "hud_chat_local_tab"
    hud_chat_tribe_tab = "hud_chat_tribe_tab"
    hud_chat_alliance_tab = "hud_chat_alliance_tab"
    hud_tribe_log = "hud_tribe_log"
    hud_tribe_log_entry = "hud_tribe_log_entry"
    hud_death_message = "hud_death_message"
    hud_taming_notification = "hud_taming_notification"
    hud_server_message = "hud_server_message"


class HUDCrosshairElements(HUDElements):
    """Class for crosshair-related HUD elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Crosshair Elements"
        
    # Element definitions
    hud_crosshair_default = "hud_crosshair_default"
    hud_crosshair_harvesting = "hud_crosshair_harvesting"
    hud_crosshair_ranged = "hud_crosshair_ranged"
    hud_crosshair_spyglass = "hud_crosshair_spyglass"


class HUDInteractionPrompts(HUDElements):
    """Class for interaction prompt HUD elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Interaction Prompts"
        
    # Element definitions
    hud_interaction_prompt = "hud_interaction_prompt"
    hud_pickup_prompt = "hud_pickup_prompt"
    hud_mount_prompt = "hud_mount_prompt"
    hud_access_prompt = "hud_access_prompt"


class HUDWheelMenus(HUDElements):
    """Class for wheel menu HUD elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Wheel Menus"
        
    # Element definitions
    hud_whistle_wheel = "hud_whistle_wheel"
    hud_emote_wheel = "hud_emote_wheel"
    hud_quickchat_wheel = "hud_quickchat_wheel"


class HUDWaypointElements(HUDElements):
    """Class for waypoint-related HUD elements"""
    def __init__(self, name, color="#3498db", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Waypoint Elements"
        
    # Element definitions
    hud_waypoint_marker = "hud_waypoint_marker"
    hud_waypoint_distance = "hud_waypoint_distance"
    hud_objective_marker = "hud_objective_marker"
    hud_mission_timer = "hud_mission_timer"
    hud_boss_arena_timer = "hud_boss_arena_timer"


class HUDNameTags(HUDElements):
    """Class for name tag HUD elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Name Tags"
        
    # Element definitions
    hud_player_name_tag = "hud_player_name_tag"
    hud_tamed_dino_name_tag = "hud_tamed_dino_name_tag"
    hud_wild_dino_name_tag = "hud_wild_dino_name_tag"
    hud_structure_name_tag = "hud_structure_name_tag"
    hud_tribe_name_tag = "hud_tribe_name_tag"
    hud_ally_indicator = "hud_ally_indicator"
    hud_enemy_indicator = "hud_enemy_indicator"
    hud_neutral_indicator = "hud_neutral_indicator"


class HUDMarkerElements(HUDElements):
    """Class for marker-related HUD elements"""
    def __init__(self, name, color="#3498db", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Marker Elements"
        
    # Element definitions
    hud_hlna_icon = "hud_hlna_icon"
    hud_hlna_message = "hud_hlna_message"
    hud_resource_node_marker = "hud_resource_node_marker"
    hud_explorer_note_marker = "hud_explorer_note_marker"
    hud_supply_drop_marker = "hud_supply_drop_marker"
    hud_beaver_dam_marker = "hud_beaver_dam_marker"
    hud_artifact_marker = "hud_artifact_marker"


class HUDWarningElements(HUDElements):
    """Class for warning-related HUD elements"""
    def __init__(self, name, color="#e74c3c", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Warning Elements"
        
    # Element definitions
    hud_radiation_warning = "hud_radiation_warning"
    hud_gas_warning = "hud_gas_warning"
    hud_element_warning = "hud_element_warning"


class HUDTekElements(HUDElements):
    """Class for Tek-related HUD elements"""
    def __init__(self, name, color="#3498db", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tek HUD Elements"
        
    # Element definitions
    hud_tek_visor_overlay = "hud_tek_visor_overlay"
    hud_tek_visor_target = "hud_tek_visor_target"
    hud_tek_visor_stats = "hud_tek_visor_stats"
    hud_tek_punch_charge = "hud_tek_punch_charge"


class HUDOverlayElements(HUDElements):
    """Class for overlay-related HUD elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Overlay Elements"
        
    # Element definitions
    hud_spyglass_overlay = "hud_spyglass_overlay"
    hud_spyglass_info = "hud_spyglass_info"
    hud_taxidermy_camera = "hud_taxidermy_camera"
    hud_paintbrush_color_picker = "hud_paintbrush_color_picker"
    hud_paintbrush_brush_size = "hud_paintbrush_brush_size"
    hud_creature_stats_overlay = "hud_creature_stats_overlay"
    hud_structure_health_overlay = "hud_structure_health_overlay"
    hud_resource_yields_popup = "hud_resource_yields_popup"


###############################
# QUICKBAR ELEMENTS
###############################

class QuickbarElements(UIElement):
    """Base class for Quickbar Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Quickbar Elements"


class QuickbarSlots(QuickbarElements):
    """Class for quickbar slot elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Quickbar Slots"
        
    # Element definitions
    quickbar_background = "quickbar_background"
    quickbar_slot_1 = "quickbar_slot_1"
    quickbar_slot_2 = "quickbar_slot_2"
    quickbar_slot_3 = "quickbar_slot_3"
    quickbar_slot_4 = "quickbar_slot_4"
    quickbar_slot_5 = "quickbar_slot_5"
    quickbar_slot_6 = "quickbar_slot_6"
    quickbar_slot_7 = "quickbar_slot_7"
    quickbar_slot_8 = "quickbar_slot_8"
    quickbar_slot_9 = "quickbar_slot_9"
    quickbar_slot_0 = "quickbar_slot_0"
    quickbar_slot_filled = "quickbar_slot_filled"
    quickbar_slot_empty = "quickbar_slot_empty"
    quickbar_slot_selected = "quickbar_slot_selected"


class QuickbarIndicators(QuickbarElements):
    """Class for quickbar indicator elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Quickbar Indicators"
        
    # Element definitions
    quickbar_selector = "quickbar_selector"
    quickbar_item_name = "quickbar_item_name"
    quickbar_item_count = "quickbar_item_count"
    quickbar_item_durability_high = "quickbar_item_durability_high"
    quickbar_item_durability_medium = "quickbar_item_durability_medium"
    quickbar_item_durability_low = "quickbar_item_durability_low"
    quickbar_weapon_ammo_count = "quickbar_weapon_ammo_count"
    quickbar_weapon_reload_prompt = "quickbar_weapon_reload_prompt"
    quickbar_item_cooldown = "quickbar_item_cooldown"
    quickbar_item_keybind = "quickbar_item_keybind"
    quickbar_item_equip_animation = "quickbar_item_equip_animation"
    quickbar_contextual_action = "quickbar_contextual_action"


class QuickbarHotkeys(QuickbarElements):
    """Class for quickbar hotkey elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Quickbar Hotkeys"
        
    # Element definitions
    quickbar_hotkey_1 = "quickbar_hotkey_1"
    quickbar_hotkey_2 = "quickbar_hotkey_2"
    quickbar_hotkey_3 = "quickbar_hotkey_3"
    quickbar_hotkey_4 = "quickbar_hotkey_4"
    quickbar_hotkey_5 = "quickbar_hotkey_5"
    quickbar_hotkey_6 = "quickbar_hotkey_6"
    quickbar_hotkey_7 = "quickbar_hotkey_7"
    quickbar_hotkey_8 = "quickbar_hotkey_8"
    quickbar_hotkey_9 = "quickbar_hotkey_9"
    quickbar_hotkey_0 = "quickbar_hotkey_0"


###############################
# INVENTORY ELEMENTS
###############################

class InventoryElements(UIElement):
    """Base class for Inventory Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Inventory Elements"


class InventoryPanels(InventoryElements):
    """Class for inventory panel elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Inventory Panels"
        
    # Element definitions
    inventory_background = "inventory_background"
    inventory_player_region = "inventory_player_region"
    inventory_entity_region = "inventory_entity_region"
    inventory_player_model = "inventory_player_model"
    inventory_player_stats = "inventory_player_stats"
    inventory_toolbar = "inventory_toolbar"
    inventory_close_button = "inventory_close_button"


class InventorySlots(InventoryElements):
    """Class for inventory slot elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Inventory Slots"
        
    # Element definitions
    inventory_player_slot_empty = "inventory_player_slot_empty"
    inventory_player_slot_filled = "inventory_player_slot_filled"
    inventory_item_icon = "inventory_item_icon"
    inventory_item_stack_count = "inventory_item_stack_count"
    inventory_item_durability_high = "inventory_item_durability_high"
    inventory_item_durability_medium = "inventory_item_durability_medium"
    inventory_item_durability_low = "inventory_item_durability_low"
    inventory_item_broken_indicator = "inventory_item_broken_indicator"


class InventoryQualityIndicators(InventoryElements):
    """Class for inventory quality indicator elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Quality Indicators"
        
    # Element definitions
    inventory_item_quality_primitive = "inventory_item_quality_primitive"
    inventory_item_quality_ramshackle = "inventory_item_quality_ramshackle"
    inventory_item_quality_apprentice = "inventory_item_quality_apprentice"
    inventory_item_quality_journeyman = "inventory_item_quality_journeyman"
    inventory_item_quality_mastercraft = "inventory_item_quality_mastercraft"
    inventory_item_quality_ascendant = "inventory_item_quality_ascendant"


class InventoryItemSpecials(InventoryElements):
    """Class for special inventory item elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Item Specials"
        
    # Element definitions
    inventory_item_blueprint_icon = "inventory_item_blueprint_icon"
    inventory_item_blueprint_text = "inventory_item_blueprint_text"
    inventory_item_equipped_marker = "inventory_item_equipped_marker"
    inventory_item_favorite_marker = "inventory_item_favorite_marker"
    inventory_item_spoil_timer = "inventory_item_spoil_timer"
    inventory_item_repair_cost = "inventory_item_repair_cost"


class InventoryControls(InventoryElements):
    """Class for inventory control elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Inventory Controls"
        
    # Element definitions
    inventory_search_bar = "inventory_search_bar"
    inventory_search_icon = "inventory_search_icon"
    inventory_search_results = "inventory_search_results"
    inventory_transfer_right_button = "inventory_transfer_right_button"
    inventory_transfer_left_button = "inventory_transfer_left_button"
    inventory_transfer_item_button = "inventory_transfer_item_button"
    inventory_weight_current = "inventory_weight_current"
    inventory_weight_max = "inventory_weight_max"
    inventory_weight_percentage = "inventory_weight_percentage"
    inventory_weight_progress_bar = "inventory_weight_progress_bar"
    inventory_sort_button = "inventory_sort_button"
    inventory_drop_button = "inventory_drop_button"
    inventory_drop_all_button = "inventory_drop_all_button"
    inventory_split_stack_slider = "inventory_split_stack_slider"
    inventory_remote_use_button = "inventory_remote_use_button"


class InventoryArmorSlots(InventoryElements):
    """Class for inventory armor slot elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Armor Slots"
        
    # Element definitions
    inventory_armor_slot_head = "inventory_armor_slot_head"
    inventory_armor_slot_chest = "inventory_armor_slot_chest"
    inventory_armor_slot_hands = "inventory_armor_slot_hands"
    inventory_armor_slot_legs = "inventory_armor_slot_legs"
    inventory_armor_slot_feet = "inventory_armor_slot_feet"
    inventory_armor_slot_shield = "inventory_armor_slot_shield"


class InventoryTooltips(InventoryElements):
    """Class for inventory tooltip elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tooltips"
        
    # Element definitions
    inventory_item_tooltip = "inventory_item_tooltip"
    inventory_item_tooltip_title = "inventory_item_tooltip_title"
    inventory_item_tooltip_description = "inventory_item_tooltip_description"
    inventory_item_tooltip_weight = "inventory_item_tooltip_weight"
    inventory_item_tooltip_stats = "inventory_item_tooltip_stats"
    inventory_item_tooltip_durability = "inventory_item_tooltip_durability"
    inventory_item_tooltip_effects = "inventory_item_tooltip_effects"


class InventoryContextMenu(InventoryElements):
    """Class for inventory context menu elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Context Menu"
        
    # Element definitions
    inventory_item_context_menu = "inventory_item_context_menu"
    inventory_item_context_option_equip = "inventory_item_context_option_equip"
    inventory_item_context_option_drop = "inventory_item_context_option_drop"
    inventory_item_context_option_drop_all = "inventory_item_context_option_drop_all"
    inventory_item_context_option_transfer = "inventory_item_context_option_transfer"
    inventory_item_context_option_transfer_all = "inventory_item_context_option_transfer_all"
    inventory_item_context_option_split = "inventory_item_context_option_split"
    inventory_item_context_option_consume = "inventory_item_context_option_consume"
    inventory_item_context_option_examine = "inventory_item_context_option_examine"
    inventory_item_context_option_rename = "inventory_item_context_option_rename"
    inventory_item_context_option_repair = "inventory_item_context_option_repair"


class InventoryFolders(InventoryElements):
    """Class for inventory folder elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Folders"
        
    # Element definitions
    inventory_folder_tab = "inventory_folder_tab"
    inventory_folder_icon = "inventory_folder_icon"
    inventory_folder_name = "inventory_folder_name"
    inventory_folder_item_count = "inventory_folder_item_count"
    inventory_scroll_bar = "inventory_scroll_bar"
    inventory_scroll_up_button = "inventory_scroll_up_button"
    inventory_scroll_down_button = "inventory_scroll_down_button"


class EntityInventoryElements(InventoryElements):
    """Class for entity inventory elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Entity Inventory"
        
    # Element definitions
    inventory_entity_slot_empty = "inventory_entity_slot_empty"
    inventory_entity_slot_filled = "inventory_entity_slot_filled"
    inventory_entity_name = "inventory_entity_name"
    inventory_structure_type = "inventory_structure_type"
    inventory_entity_level = "inventory_entity_level"
    inventory_entity_model = "inventory_entity_model"
    inventory_entity_inventory_slots_count = "inventory_entity_inventory_slots_count"


class SpecialInventoryElements(InventoryElements):
    """Class for special inventory elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Special Inventories"
        
    # Element definitions
    inventory_beacon_countdown = "inventory_beacon_countdown"
    inventory_tek_transmitter_interface = "inventory_tek_transmitter_interface"
    inventory_obelisk_interface = "inventory_obelisk_interface"
    inventory_genesis_mission_interface = "inventory_genesis_mission_interface"
    inventory_cryopod_contents = "inventory_cryopod_contents"
    inventory_artifact_slot = "inventory_artifact_slot"
    inventory_boss_tribute_slot = "inventory_boss_tribute_slot"
    inventory_tek_element_count = "inventory_tek_element_count"


class TerminalTabs(InventoryElements):
    """Class for terminal tab elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Terminal Tabs"
        
    # Element definitions
    inventory_terminal_download_tab = "inventory_terminal_download_tab"
    inventory_terminal_upload_tab = "inventory_terminal_upload_tab"
    inventory_terminal_creature_tab = "inventory_terminal_creature_tab"
    inventory_terminal_data_tab = "inventory_terminal_data_tab"


###############################
# TAB ELEMENTS
###############################

class TabElements(UIElement):
    """Base class for Tab Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Tab Elements"


class InventoryTabs(TabElements):
    """Class for inventory tab elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Inventory Tabs"
        
    # Element definitions
    tab_inventory_active = "tab_inventory_active"
    tab_inventory_inactive = "tab_inventory_inactive"
    tab_crafting_active = "tab_crafting_active"
    tab_crafting_inactive = "tab_crafting_inactive"
    tab_engrams_active = "tab_engrams_active"
    tab_engrams_inactive = "tab_engrams_inactive"


class CharacterTabs(TabElements):
    """Class for character tab elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Character Tabs"
        
    # Element definitions
    tab_tribe_active = "tab_tribe_active"
    tab_tribe_inactive = "tab_tribe_inactive"
    tab_stats_active = "tab_stats_active"
    tab_stats_inactive = "tab_stats_inactive"
    tab_notes_active = "tab_notes_active"
    tab_notes_inactive = "tab_notes_inactive"
    tab_map_active = "tab_map_active"
    tab_map_inactive = "tab_map_inactive"


class DinoTabs(TabElements):
    """Class for dino tab elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Dino Tabs"
        
    # Element definitions
    tab_dino_stats_active = "tab_dino_stats_active"
    tab_dino_stats_inactive = "tab_dino_stats_inactive"
    tab_dino_inventory_active = "tab_dino_inventory_active"
    tab_dino_inventory_inactive = "tab_dino_inventory_inactive"
    tab_dino_behavior_active = "tab_dino_behavior_active"
    tab_dino_behavior_inactive = "tab_dino_behavior_inactive"


class TerminalTabs(TabElements):
    """Class for terminal tab elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Terminal Tabs"
        
    # Element definitions
    tab_spawn_selection_active = "tab_spawn_selection_active"
    tab_spawn_selection_inactive = "tab_spawn_selection_inactive"
    tab_tribute_active = "tab_tribute_active"
    tab_tribute_inactive = "tab_tribute_inactive"
    tab_upload_active = "tab_upload_active"
    tab_upload_inactive = "tab_upload_inactive"
    tab_download_active = "tab_download_active"
    tab_download_inactive = "tab_download_inactive"
    tab_recipes_active = "tab_recipes_active"
    tab_recipes_inactive = "tab_recipes_inactive"
    tab_cluster_active = "tab_cluster_active"
    tab_cluster_inactive = "tab_cluster_inactive"
    tab_missions_active = "tab_missions_active"
    tab_missions_inactive = "tab_missions_inactive"
    tab_genesis_biomes_active = "tab_genesis_biomes_active"
    tab_genesis_biomes_inactive = "tab_genesis_biomes_inactive"


###############################
# CRAFTING ELEMENTS
###############################

class CraftingElements(UIElement):
    """Base class for Crafting Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Crafting Elements"


class CraftingPanels(CraftingElements):
    """Class for crafting panel elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Crafting Panels"
        
    # Element definitions
    crafting_item_panel = "crafting_item_panel"
    crafting_item_icon = "crafting_item_icon"
    crafting_item_name = "crafting_item_name"
    crafting_item_description = "crafting_item_description"
    crafting_materials_header = "crafting_materials_header"
    crafting_materials_required = "crafting_materials_required"
    crafting_materials_sufficient = "crafting_materials_sufficient"
    crafting_materials_insufficient = "crafting_materials_insufficient"
    crafting_button_active = "crafting_button_active"
    crafting_button_inactive = "crafting_button_inactive"


class CraftingControls(CraftingElements):
    """Class for crafting control elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Crafting Controls"
        
    # Element definitions
    crafting_blueprint_header = "crafting_blueprint_header"
    crafting_button_craft_one = "crafting_button_craft_one"
    crafting_button_craft_all = "crafting_button_craft_all"
    crafting_button_craft_custom = "crafting_button_craft_custom"
    crafting_amount_selector = "crafting_amount_selector"
    crafting_checkbox_craftall = "crafting_checkbox_craftall"
    crafting_time_estimate = "crafting_time_estimate"


class CraftingQueue(CraftingElements):
    """Class for crafting queue elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Crafting Queue"
        
    # Element definitions
    crafting_queue_header = "crafting_queue_header"
    crafting_queue_slot = "crafting_queue_slot"
    crafting_queue_slot_empty = "crafting_queue_slot_empty"
    crafting_queue_slot_occupied = "crafting_queue_slot_occupied"
    crafting_queue_item_name = "crafting_queue_item_name"
    crafting_queue_item_icon = "crafting_queue_item_icon"
    crafting_queue_progress_text = "crafting_queue_progress_text"
    crafting_queue_cancel_button = "crafting_queue_cancel_button"
    crafting_progress_bar_inactive = "crafting_progress_bar_inactive"
    crafting_progress_bar_active = "crafting_progress_bar_active"


class CraftingStationInfo(CraftingElements):
    """Class for crafting station information elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Station Info"
        
    # Element definitions
    crafting_station_icon = "crafting_station_icon"
    crafting_station_name = "crafting_station_name"
    crafting_station_level = "crafting_station_level"


class CraftingFilters(CraftingElements):
    """Class for crafting filter elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Crafting Filters"
        
    # Element definitions
    crafting_search_bar = "crafting_search_bar"
    crafting_search_icon = "crafting_search_icon"
    crafting_filter_button = "crafting_filter_button"
    crafting_filter_dropdown = "crafting_filter_dropdown"
    crafting_filter_option_all = "crafting_filter_option_all"
    crafting_filter_option_armor = "crafting_filter_option_armor"
    crafting_filter_option_weapons = "crafting_filter_option_weapons"
    crafting_filter_option_Structure = "crafting_filter_option_Structure"
    crafting_filter_option_consumables = "crafting_filter_option_consumables"
    crafting_filter_option_resources = "crafting_filter_option_resources"
    crafting_filter_option_tools = "crafting_filter_option_tools"


class CraftingSorting(CraftingElements):
    """Class for crafting sorting elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Crafting Sorting"
        
    # Element definitions
    crafting_sort_button = "crafting_sort_button"
    crafting_sort_dropdown = "crafting_sort_dropdown"
    crafting_sort_option_alphabetical = "crafting_sort_option_alphabetical"
    crafting_sort_option_level = "crafting_sort_option_level"
    crafting_sort_option_craftable = "crafting_sort_option_craftable"
    crafting_category_header = "crafting_category_header"


class CraftingBoosts(CraftingElements):
    """Class for crafting boost elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Crafting Boosts"
        
    # Element definitions
    crafting_skill_boost_indicator = "crafting_skill_boost_indicator"
    crafting_speed_multiplier = "crafting_speed_multiplier"
    crafting_blueprint_quality_indicator = "crafting_blueprint_quality_indicator"
    crafting_blueprint_bonus_text = "crafting_blueprint_bonus_text"
    crafting_mindwipe_reminder = "crafting_mindwipe_reminder"


class CraftingRequirements(CraftingElements):
    """Class for crafting requirement elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Crafting Requirements"
        
    # Element definitions
    crafting_engram_points_cost = "crafting_engram_points_cost"
    crafting_level_requirement = "crafting_level_requirement"
    crafting_tek_element_cost = "crafting_tek_element_cost"


class CraftingResourceCosts(CraftingElements):
    """Class for crafting resource cost elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Resource Costs"
        
    # Element definitions
    crafting_crystal_cost = "crafting_crystal_cost"
    crafting_metal_cost = "crafting_metal_cost"
    crafting_wood_cost = "crafting_wood_cost"
    crafting_thatch_cost = "crafting_thatch_cost"
    crafting_stone_cost = "crafting_stone_cost"
    crafting_hide_cost = "crafting_hide_cost"
    crafting_fiber_cost = "crafting_fiber_cost"
    crafting_chitin_cost = "crafting_chitin_cost"
    crafting_keratin_cost = "crafting_keratin_cost"
    crafting_obsidian_cost = "crafting_obsidian_cost"
    crafting_polymer_cost = "crafting_polymer_cost"
    crafting_electronics_cost = "crafting_electronics_cost"
    crafting_cementing_paste_cost = "crafting_cementing_paste_cost"
    crafting_silica_pearls_cost = "crafting_silica_pearls_cost"
    crafting_oil_cost = "crafting_oil_cost"
    crafting_pelt_cost = "crafting_pelt_cost"
    crafting_black_pearl_cost = "crafting_black_pearl_cost"
    crafting_narcotics_cost = "crafting_narcotics_cost"
    crafting_stimulant_cost = "crafting_stimulant_cost"
    crafting_biotoxin_cost = "crafting_biotoxin_cost"
    crafting_congealed_gas_cost = "crafting_congealed_gas_cost"
    crafting_element_shard_cost = "crafting_element_shard_cost"
    crafting_element_dust_cost = "crafting_element_dust_cost"
    crafting_mutagel_cost = "crafting_mutagel_cost"
    crafting_ammunition_cost = "crafting_ammunition_cost"


###############################
# ENGRAM ELEMENTS
###############################

class EngramElements(UIElement):
    """Base class for Engram Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Engram Elements"


class EngramIcons(EngramElements):
    """Class for engram icon elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Engram Icons"
        
    # Element definitions
    engram_icon_available = "engram_icon_available"
    engram_icon_learned = "engram_icon_learned"
    engram_icon_locked = "engram_icon_locked"
    engram_icon_dlc_locked = "engram_icon_dlc_locked"
    engram_highlight_new = "engram_highlight_new"


class EngramPoints(EngramElements):
    """Class for engram point elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Engram Points"
        
    # Element definitions
    engram_points_display = "engram_points_display"
    engram_points_total = "engram_points_total"
    engram_points_spent = "engram_points_spent"
    engram_points_available = "engram_points_available"
    engram_level_requirement = "engram_level_requirement"


class EngramControls(EngramElements):
    """Class for engram control elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Engram Controls"
        
    # Element definitions
    engram_learn_button_active = "engram_learn_button_active"
    engram_learn_button_inactive = "engram_learn_button_inactive"
    engram_learn_multiple_button = "engram_learn_multiple_button"
    engram_auto_unlock_checkbox = "engram_auto_unlock_checkbox"
    engram_prerequisite_warning = "engram_prerequisite_warning"


class EngramItems(EngramElements):
    """Class for engram item elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Engram Items"
        
    # Element definitions
    engram_item_icon = "engram_item_icon"
    engram_item_name = "engram_item_name"
    engram_item_description = "engram_item_description"


class EngramSearch(EngramElements):
    """Class for engram search elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Engram Search"
        
    # Element definitions
    engram_search_bar = "engram_search_bar"
    engram_search_icon = "engram_search_icon"
    engram_search_results = "engram_search_results"
    engram_point_cost = "engram_point_cost"


class EngramCategories(EngramElements):
    """Class for engram category elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Engram Categories"
        
    # Element definitions
    engram_category_tab = "engram_category_tab"
    engram_category_icon = "engram_category_icon"
    engram_category_name = "engram_category_name"
    engram_category_progress = "engram_category_progress"
    engram_show_unlocked_toggle = "engram_show_unlocked_toggle"
    engram_hide_locked_toggle = "engram_hide_locked_toggle"


class EngramTooltips(EngramElements):
    """Class for engram tooltip elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Engram Tooltips"
        
    # Element definitions
    engram_tooltip = "engram_tooltip"
    engram_tooltip_name = "engram_tooltip_name"
    engram_tooltip_description = "engram_tooltip_description"
    engram_tooltip_level = "engram_tooltip_level"
    engram_tooltip_cost = "engram_tooltip_cost"


class EngramDLCIcons(EngramElements):
    """Class for engram DLC icon elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "DLC Icons"
        
    # Element definitions
    engram_dlc_icon = "engram_dlc_icon"
    engram_tek_icon = "engram_tek_icon"
    engram_genesis_icon = "engram_genesis_icon"
    engram_aberration_icon = "engram_aberration_icon"
    engram_scorched_earth_icon = "engram_scorched_earth_icon"
    engram_extinction_icon = "engram_extinction_icon"
    engram_fjordur_icon = "engram_fjordur_icon"
    engram_valguero_icon = "engram_valguero_icon"
    engram_crystal_isles_icon = "engram_crystal_isles_icon"
    engram_lost_island_icon = "engram_lost_island_icon"
    engram_gen1_icon = "engram_gen1_icon"
    engram_gen2_icon = "engram_gen2_icon"
    engram_primitive_plus_icon = "engram_primitive_plus_icon"
    engram_boss_unlock_icon = "engram_boss_unlock_icon"
    engram_mission_unlock_icon = "engram_mission_unlock_icon"


class EngramNavigation(EngramElements):
    """Class for engram navigation elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Engram Navigation"
        
    # Element definitions
    engram_scroll_bar = "engram_scroll_bar"
    engram_scroll_up_button = "engram_scroll_up_button"
    engram_scroll_down_button = "engram_scroll_down_button"
    engram_tech_tier_marker = "engram_tech_tier_marker"
    engram_level_marker = "engram_level_marker"


###############################
# DINO ELEMENTS
###############################

class DinoElements(UIElement):
    """Base class for Dino Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Dino Elements"


class DinoInventory(DinoElements):
    """Class for dino inventory elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Dino Inventory"
        
    # Element definitions
    dino_inventory_name = "dino_inventory_name"
    dino_inventory_level = "dino_inventory_level"
    dino_health_bar = "dino_health_bar"
    dino_stamina_bar = "dino_stamina_bar"
    dino_food_bar = "dino_food_bar"
    dino_torpidity_bar = "dino_torpidity_bar"
    dino_weight_bar = "dino_weight_bar"
    dino_options_button = "dino_options_button"
    dino_follow_setting = "dino_follow_setting"
    dino_behavior_setting = "dino_behavior_setting"
    dino_saddle_slot = "dino_saddle_slot"
    dino_stats_increase_button = "dino_stats_increase_button"


class DinoBehavior(DinoElements):
    """Class for dino behavior elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Dino Behavior"
        
    # Element definitions
    dino_behavior_aggressive = "dino_behavior_aggressive"
    dino_behavior_neutral = "dino_behavior_neutral"
    dino_behavior_passive = "dino_behavior_passive"
    dino_behavior_passive_flee = "dino_behavior_passive_flee"
    dino_follow_distance_close = "dino_follow_distance_close"
    dino_follow_distance_medium = "dino_follow_distance_medium"
    dino_follow_distance_far = "dino_follow_distance_far"
    dino_follow_distance_furthest = "dino_follow_distance_furthest"


class DinoTargeting(DinoElements):
    """Class for dino targeting elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Dino Targeting"
        
    # Element definitions
    dino_targeting_setting = "dino_targeting_setting"
    dino_targeting_low_hp = "dino_targeting_low_hp"
    dino_targeting_high_dmg = "dino_targeting_high_dmg"
    dino_mating_toggle = "dino_mating_toggle"
    dino_wandering_toggle = "dino_wandering_toggle"
    dino_turret_mode_toggle = "dino_turret_mode_toggle"
    dino_harvest_setting = "dino_harvest_setting"
    dino_enable_ally_looking = "dino_enable_ally_looking"
    dino_victim_item_collection = "dino_victim_item_collection"


class DinoStats(DinoElements):
    """Class for dino stat elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Dino Stats"
        
    # Element definitions
    dino_stats_background = "dino_stats_background"
    dino_stats_header = "dino_stats_header"
    dino_stats_species = "dino_stats_species"
    dino_stats_level = "dino_stats_level"
    dino_stats_xp_bar = "dino_stats_xp_bar"
    dino_stats_xp_to_next_level = "dino_stats_xp_to_next_level"
    dino_stat_health = "dino_stat_health"
    dino_stat_health_value = "dino_stat_health_value"
    dino_stat_health_increase_button = "dino_stat_health_increase_button"
    dino_stat_stamina = "dino_stat_stamina"
    dino_stat_stamina_value = "dino_stat_stamina_value"
    dino_stat_stamina_increase_button = "dino_stat_stamina_increase_button"
    dino_stat_oxygen = "dino_stat_oxygen"
    dino_stat_oxygen_value = "dino_stat_oxygen_value"
    dino_stat_oxygen_increase_button = "dino_stat_oxygen_increase_button"
    dino_stat_food = "dino_stat_food"
    dino_stat_food_value = "dino_stat_food_value"
    dino_stat_food_increase_button = "dino_stat_food_increase_button"
    dino_stat_weight = "dino_stat_weight"
    dino_stat_weight_value = "dino_stat_weight_value"
    dino_stat_weight_increase_button = "dino_stat_weight_increase_button"
    dino_stat_melee = "dino_stat_melee"
    dino_stat_melee_value = "dino_stat_melee_value"
    dino_stat_melee_increase_button = "dino_stat_melee_increase_button"
    dino_stat_speed = "dino_stat_speed"
    dino_stat_speed_value = "dino_stat_speed_value"
    dino_stat_speed_increase_button = "dino_stat_speed_increase_button"
    dino_stat_torpor = "dino_stat_torpor"
    dino_stat_torpor_value = "dino_stat_torpor_value"


class DinoImprinting(DinoElements):
    """Class for dino imprinting elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Dino Imprinting"
        
    # Element definitions
    dino_imprinting_status = "dino_imprinting_status"
    dino_imprinting_quality = "dino_imprinting_quality"
    dino_imprinting_progress = "dino_imprinting_progress"
    dino_imprinting_timer = "dino_imprinting_timer"
    dino_unclaim_button = "dino_unclaim_button"
    dino_rename_button = "dino_rename_button"
    dino_color_regions = "dino_color_regions"
    dino_mutation_counter_paternal = "dino_mutation_counter_paternal"
    dino_mutation_counter_maternal = "dino_mutation_counter_maternal"
    dino_ancestry_button = "dino_ancestry_button"
    dino_gender_indicator = "dino_gender_indicator"


class DinoAbilities(DinoElements):
    """Class for dino ability elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Dino Abilities"
        
    # Element definitions
    dino_special_ability_cooldown = "dino_special_ability_cooldown"
    dino_special_ability_button = "dino_special_ability_button"
    dino_pack_buff_indicator = "dino_pack_buff_indicator"
    dino_mate_boost_indicator = "dino_mate_boost_indicator"
    dino_wild_stats = "dino_wild_stats"
    dino_tamed_bonus = "dino_tamed_bonus"
    dino_imprint_bonus = "dino_imprint_bonus"


class TamingElements(DinoElements):
    """Class for taming-related elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Taming Elements"
        
    # Element definitions
    taming_effectiveness_bar = "taming_effectiveness_bar"
    taming_progress_bar = "taming_progress_bar"
    taming_food_timer = "taming_food_timer"
    taming_torpor_bar = "taming_torpor_bar"
    taming_progress_bar_empty = "taming_progress_bar_empty"
    taming_progress_bar_partial = "taming_progress_bar_partial"
    taming_progress_bar_full = "taming_progress_bar_full"
    taming_effectiveness_high = "taming_effectiveness_high"
    taming_effectiveness_medium = "taming_effectiveness_medium"
    taming_effectiveness_low = "taming_effectiveness_low"


###############################
# STRUCTURE ELEMENTS
###############################

class StructureElements(UIElement):
    """Base class for Structure Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Structure Elements"


class StructureInfo(StructureElements):
    """Class for structure information elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Structure Info"
        
    # Element definitions
    structure_name_label = "structure_name_label"
    structure_inventory_button = "structure_inventory_button"
    structure_options_button = "structure_options_button"
    structure_power_indicator = "structure_power_indicator"
    structure_fuel_level = "structure_fuel_level"
    structure_pin_code_input = "structure_pin_code_input"
    structure_demolish_timer = "structure_demolish_timer"
    structure_health_bar = "structure_health_bar"
    structure_shield_bar = "structure_shield_bar"
    structure_transfer_button = "structure_transfer_button"


class StructureOptions(StructureElements):
    """Class for structure option elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Structure Options"
        
    # Element definitions
    structure_options_menu = "structure_options_menu"
    structure_demolish_option = "structure_demolish_option"
    structure_pickup_option = "structure_pickup_option"
    structure_paint_option = "structure_paint_option"
    structure_change_pin_option = "structure_change_pin_option"


class StructurePlacement(StructureElements):
    """Class for structure placement elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Structure Placement"
        
    # Element definitions
    structure_snap_points = "structure_snap_points"
    structure_placement_valid = "structure_placement_valid"
    structure_placement_invalid = "structure_placement_invalid"
    structure_placement_preview = "structure_placement_preview"
    structure_placement_obstruction = "structure_placement_obstruction"
    structure_placement_foundation_required = "structure_placement_foundation_required"
    structure_placement_support_required = "structure_placement_support_required"
    structure_placement_enemy_foundation = "structure_placement_enemy_foundation"
    structure_placement_enemy_territory = "structure_placement_enemy_territory"
    structure_placement_snap_point = "structure_placement_snap_point"
    structure_placement_snap_preview = "structure_placement_snap_preview"


class StructurePower(StructureElements):
    """Class for structure power elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Structure Power"
        
    # Element definitions
    structure_powered_indicator = "structure_powered_indicator"
    structure_unpowered_indicator = "structure_unpowered_indicator"
    generator_fuel_level = "generator_fuel_level"
    electrical_wire_connection = "electrical_wire_connection"
    water_pipe_connection = "water_pipe_connection"
    gas_pipe_connection = "gas_pipe_connection"
    storage_capacity_indicator = "storage_capacity_indicator"
    auto_turret_ammo_indicator = "auto_turret_ammo_indicator"


###############################
# MAP ELEMENTS
###############################

class MapElements(UIElement):
    """Base class for Map Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Map Elements"


class MapBackground(MapElements):
    """Class for map background elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Map Background"
        
    # Element definitions
    map_background = "map_background"
    map_background_terrain = "map_background_terrain"
    map_background_ocean = "map_background_ocean"
    map_grid_lines = "map_grid_lines"
    map_grid_labels = "map_grid_labels"
    map_biome_boundaries = "map_biome_boundaries"
    map_biome_name_label = "map_biome_name_label"


class MapMarkers(MapElements):
    """Class for map marker elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Map Markers"
        
    # Element definitions
    map_player_marker = "map_player_marker"
    map_player_marker_direction = "map_player_marker_direction"
    map_player_text_label = "map_player_text_label"
    map_tribe_member_marker = "map_tribe_member_marker"
    map_tribe_member_text_label = "map_tribe_member_text_label"
    map_tamed_dino_marker = "map_tamed_dino_marker"
    map_tamed_dino_text_label = "map_tamed_dino_text_label"
    map_tamed_dino_type_icon = "map_tamed_dino_type_icon"
    map_bed_marker = "map_bed_marker"
    map_bed_text_label = "map_bed_text_label"


class MapBaseMarkers(MapElements):
    """Class for map base marker elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Base Markers"
        
    # Element definitions
    map_base_marker = "map_base_marker"
    map_base_text_label = "map_base_text_label"
    map_waypoint_marker = "map_waypoint_marker"
    map_waypoint_text_label = "map_waypoint_text_label"
    map_waypoint_distance = "map_waypoint_distance"


class MapObeliskMarkers(MapElements):
    """Class for map obelisk marker elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Obelisk Markers"
        
    # Element definitions
    map_obelisk_marker_red = "map_obelisk_marker_red"
    map_obelisk_marker_blue = "map_obelisk_marker_blue"
    map_obelisk_marker_green = "map_obelisk_marker_green"
    map_terminal_marker = "map_terminal_marker"
    map_cave_entrance_marker = "map_cave_entrance_marker"
    map_underwater_cave_marker = "map_underwater_cave_marker"


class MapBeaconMarkers(MapElements):
    """Class for map beacon marker elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Beacon Markers"
        
    # Element definitions
    map_beacon_marker_white = "map_beacon_marker_white"
    map_beacon_marker_green = "map_beacon_marker_green"
    map_beacon_marker_blue = "map_beacon_marker_blue"
    map_beacon_marker_purple = "map_beacon_marker_purple"
    map_beacon_marker_yellow = "map_beacon_marker_yellow"
    map_beacon_marker_red = "map_beacon_marker_red"


class MapSpecialMarkers(MapElements):
    """Class for map special marker elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Special Markers"
        
    # Element definitions
    map_mission_marker = "map_mission_marker"
    map_boss_terminal_marker = "map_boss_terminal_marker"
    map_supply_drop_marker = "map_supply_drop_marker"
    map_explorer_note_marker = "map_explorer_note_marker"
    map_glitch_marker = "map_glitch_marker"
    map_resource_node_marker = "map_resource_node_marker"
    map_charging_station_marker = "map_charging_station_marker"


class MapWaterElements(MapElements):
    """Class for map water-related elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Water Elements"
        
    # Element definitions
    map_ocean_depth_indicator = "map_ocean_depth_indicator"
    map_shallow_water_indicator = "map_shallow_water_indicator"
    map_deep_water_indicator = "map_deep_water_indicator"
    map_danger_zone_indicator = "map_danger_zone_indicator"
    map_radiation_zone = "map_radiation_zone"


class MapBiomeIndicators(MapElements):
    """Class for map biome indicator elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Biome Indicators"
        
    # Element definitions
    map_snow_biome_indicator = "map_snow_biome_indicator"
    map_desert_biome_indicator = "map_desert_biome_indicator"
    map_redwood_biome_indicator = "map_redwood_biome_indicator"
    map_swamp_biome_indicator = "map_swamp_biome_indicator"


class MapCoordinates(MapElements):
    """Class for map coordinate elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Coordinates"
        
    # Element definitions
    map_coordinates_display = "map_coordinates_display"
    map_latitude_display = "map_latitude_display"
    map_longitude_display = "map_longitude_display"
    map_altitude_display = "map_altitude_display"


class MapControls(MapElements):
    """Class for map control elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Map Controls"
        
    # Element definitions
    map_zoom_in_button = "map_zoom_in_button"
    map_zoom_out_button = "map_zoom_out_button"
    map_zoom_level_indicator = "map_zoom_level_indicator"
    map_filter_button = "map_filter_button"
    map_filter_panel = "map_filter_panel"
    map_place_waypoint_button = "map_place_waypoint_button"
    map_clear_waypoint_button = "map_clear_waypoint_button"
    map_fast_travel_button = "map_fast_travel_button"


class MapAdditionalInfo(MapElements):
    """Class for map additional information elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Additional Info"
        
    # Element definitions
    map_region_name_text = "map_region_name_text"
    map_weather_indicator = "map_weather_indicator"
    map_fog_of_war = "map_fog_of_war"
    map_discovered_area = "map_discovered_area"
    map_genesis_mission_zones = "map_genesis_mission_zones"
    map_genesis_teleport_points = "map_genesis_teleport_points"
    map_server_border = "map_server_border"


class MinimapElements(MapElements):
    """Class for minimap elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Minimap"
        
    # Element definitions
    map_minimap_frame = "map_minimap_frame"
    map_minimap_terrain = "map_minimap_terrain"
    map_minimap_player_marker = "map_minimap_player_marker"
    map_minimap_north_indicator = "map_minimap_north_indicator"


###############################
# ALERT ELEMENTS
###############################

class AlertElements(UIElement):
    """Base class for Alert Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Alert Elements"


class HealthAlerts(AlertElements):
    """Class for health-related alert elements"""
    def __init__(self, name, color="#e74c3c", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Health Alerts"
        
    # Element definitions
    alert_starvation = "alert_starvation"
    alert_dehydration = "alert_dehydration"
    alert_encumbered = "alert_encumbered"
    alert_too_hot = "alert_too_hot"
    alert_too_cold = "alert_too_cold"


class NotificationAlerts(AlertElements):
    """Class for notification alert elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Notification Alerts"
        
    # Element definitions
    alert_level_up = "alert_level_up"
    alert_tribe_message = "alert_tribe_message"
    alert_death_message = "alert_death_message"
    alert_taming_complete = "alert_taming_complete"
    alert_insufficient_engrams = "alert_insufficient_engrams"
    alert_structure_blocked = "alert_structure_blocked"
    alert_enemy_player_nearby = "alert_enemy_player_nearby"
    alert_server_message = "alert_server_message"
    alert_disconnection_warning = "alert_disconnection_warning"


class WarningAlerts(AlertElements):
    """Class for warning alert elements"""
    def __init__(self, name, color="#e74c3c", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Warning Alerts"
        
    # Element definitions
    alert_item_broken = "alert_item_broken"
    alert_creature_starving = "alert_creature_starving"
    alert_creature_dying = "alert_creature_dying"
    alert_imprint_available = "alert_imprint_available"
    alert_gasoline_low = "alert_gasoline_low"
    alert_element_low = "alert_element_low"
    alert_enemy_nearby = "alert_enemy_nearby"
    alert_structure_blocked = "alert_structure_blocked"
    alert_taming_complete = "alert_taming_complete"


###############################
# PLAYER STATS ELEMENTS
###############################

class PlayerStatsElements(UIElement):
    """Base class for Player Stats Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Player Stats Elements"


class PlayerStatsPanels(PlayerStatsElements):
    """Class for player stats panel elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Stats Panels"
        
    # Element definitions
    player_stats_background = "player_stats_background"
    player_stats_header = "player_stats_header"


class PlayerHealthStats(PlayerStatsElements):
    """Class for player health stat elements"""
    def __init__(self, name, color="#e74c3c", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Health Stats"
        
    # Element definitions
    player_stat_health = "player_stat_health"
    player_stat_health_value = "player_stat_health_value"
    player_stat_health_increase_button = "player_stat_health_increase_button"


class PlayerStaminaStats(PlayerStatsElements):
    """Class for player stamina stat elements"""
    def __init__(self, name, color="#2ecc71", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Stamina Stats"
        
    # Element definitions
    player_stat_stamina = "player_stat_stamina"
    player_stat_stamina_value = "player_stat_stamina_value"
    player_stat_stamina_increase_button = "player_stat_stamina_increase_button"


class PlayerOxygenStats(PlayerStatsElements):
    """Class for player oxygen stat elements"""
    def __init__(self, name, color="#3498db", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Oxygen Stats"
        
    # Element definitions
    player_stat_oxygen = "player_stat_oxygen"
    player_stat_oxygen_value = "player_stat_oxygen_value"
    player_stat_oxygen_increase_button = "player_stat_oxygen_increase_button"


class PlayerFoodStats(PlayerStatsElements):
    """Class for player food stat elements"""
    def __init__(self, name, color="#f1c40f", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Food Stats"
        
    # Element definitions
    player_stat_food = "player_stat_food"
    player_stat_food_value = "player_stat_food_value"
    player_stat_food_increase_button = "player_stat_food_increase_button"


class PlayerWaterStats(PlayerStatsElements):
    """Class for player water stat elements"""
    def __init__(self, name, color="#3498db", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Water Stats"
        
    # Element definitions
    player_stat_water = "player_stat_water"
    player_stat_water_value = "player_stat_water_value"
    player_stat_water_increase_button = "player_stat_water_increase_button"


class PlayerWeightStats(PlayerStatsElements):
    """Class for player weight stat elements"""
    def __init__(self, name, color="#95a5a6", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Weight Stats"
        
    # Element definitions
    player_stat_weight = "player_stat_weight"
    player_stat_weight_value = "player_stat_weight_value"
    player_stat_weight_increase_button = "player_stat_weight_increase_button"


class PlayerMeleeStats(PlayerStatsElements):
    """Class for player melee stat elements"""
    def __init__(self, name, color="#e74c3c", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Melee Stats"
        
    # Element definitions
    player_stat_melee = "player_stat_melee"
    player_stat_melee_value = "player_stat_melee_value"
    player_stat_melee_increase_button = "player_stat_melee_increase_button"


class PlayerSpeedStats(PlayerStatsElements):
    """Class for player speed stat elements"""
    def __init__(self, name, color="#2ecc71", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Speed Stats"
        
    # Element definitions
    player_stat_speed = "player_stat_speed"
    player_stat_speed_value = "player_stat_speed_value"
    player_stat_speed_increase_button = "player_stat_speed_increase_button"


class PlayerFortitudeStats(PlayerStatsElements):
    """Class for player fortitude stat elements"""
    def __init__(self, name, color="#e67e22", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Fortitude Stats"
        
    # Element definitions
    player_stat_fortitude = "player_stat_fortitude"
    player_stat_fortitude_value = "player_stat_fortitude_value"
    player_stat_fortitude_increase_button = "player_stat_fortitude_increase_button"


class PlayerCraftingStats(PlayerStatsElements):
    """Class for player crafting stat elements"""
    def __init__(self, name, color="#9b59b6", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Crafting Stats"
        
    # Element definitions
    player_stat_crafting = "player_stat_crafting"
    player_stat_crafting_value = "player_stat_crafting_value"
    player_stat_crafting_increase_button = "player_stat_crafting_increase_button"


class PlayerLevelElements(PlayerStatsElements):
    """Class for player level elements"""
    def __init__(self, name, color="#f1c40f", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Level Elements"
        
    # Element definitions
    player_level_display = "player_level_display"
    player_xp_bar = "player_xp_bar"
    player_xp_to_next_level = "player_xp_to_next_level"
    player_levelup_points = "player_levelup_points"
    player_total_levels_applied = "player_total_levels_applied"
    player_max_level_warning = "player_max_level_warning"
    player_stat_tooltip = "player_stat_tooltip"
    player_stat_percentage_bonus = "player_stat_percentage_bonus"
    player_ascension_level = "player_ascension_level"
    player_mindwipe_button = "player_mindwipe_button"


class PlayerSpecialStats(PlayerStatsElements):
    """Class for player special stat elements"""
    def __init__(self, name, color="#3498db", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Special Stats"
        
    # Element definitions
    player_tek_implant_status = "player_tek_implant_status"
    player_mutation_counter = "player_mutation_counter"
    player_pheromone_status = "player_pheromone_status"
    player_reset_stats_button = "player_reset_stats_button"
    player_stat_wild_value = "player_stat_wild_value"
    player_stat_tamed_bonus = "player_stat_tamed_bonus"
    player_stat_level_contribution = "player_stat_level_contribution"


###############################
# TRIBE ELEMENTS
###############################

class TribeElements(UIElement):
    """Base class for Tribe Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Tribe Elements"


class TribeManagementPanels(TribeElements):
    """Class for tribe management panel elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Management Panels"
        
    # Element definitions
    tribe_management_background = "tribe_management_background"
    tribe_management_header = "tribe_management_header"
    tribe_name_display = "tribe_name_display"
    tribe_owner_indicator = "tribe_owner_indicator"
    tribe_rank_display = "tribe_rank_display"


class TribeMembers(TribeElements):
    """Class for tribe member elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tribe Members"
        
    # Element definitions
    tribe_member_list = "tribe_member_list"
    tribe_member_entry = "tribe_member_entry"
    tribe_member_name = "tribe_member_name"
    tribe_member_rank = "tribe_member_rank"
    tribe_member_level = "tribe_member_level"
    tribe_member_online_status = "tribe_member_online_status"
    tribe_member_online = "tribe_member_online"
    tribe_member_offline = "tribe_member_offline"
    tribe_member_last_online = "tribe_member_last_online"


class TribeLog(TribeElements):
    """Class for tribe log elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tribe Log"
        
    # Element definitions
    tribe_log_tab = "tribe_log_tab"
    tribe_log_container = "tribe_log_container"
    tribe_log_entry = "tribe_log_entry"
    tribe_log_timestamp = "tribe_log_timestamp"
    tribe_log_filter = "tribe_log_filter"
    tribe_log_clear_button = "tribe_log_clear_button"


class TribeAlliances(TribeElements):
    """Class for tribe alliance elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tribe Alliances"
        
    # Element definitions
    tribe_alliance_tab = "tribe_alliance_tab"
    tribe_alliance_list = "tribe_alliance_list"
    tribe_alliance_entry = "tribe_alliance_entry"
    tribe_alliance_request_button = "tribe_alliance_request_button"
    tribe_alliance_accept_button = "tribe_alliance_accept_button"
    tribe_alliance_reject_button = "tribe_alliance_reject_button"


class TribeGovernance(TribeElements):
    """Class for tribe governance elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tribe Governance"
        
    # Element definitions
    tribe_governance_tab = "tribe_governance_tab"
    tribe_governance_settings = "tribe_governance_settings"
    tribe_rank_management = "tribe_rank_management"
    tribe_rank_entry = "tribe_rank_entry"
    tribe_rank_name = "tribe_rank_name"
    tribe_rank_permissions = "tribe_rank_permissions"
    tribe_permissions_setting = "tribe_permissions_setting"


class TribePermissions(TribeElements):
    """Class for tribe permission elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tribe Permissions"
        
    # Element definitions
    tribe_permission_Structure = "tribe_permission_Structure"
    tribe_permission_access = "tribe_permission_access"
    tribe_permission_dinos = "tribe_permission_dinos"
    tribe_permission_inventories = "tribe_permission_inventories"
    tribe_permission_unclaim = "tribe_permission_unclaim"
    tribe_permission_invite = "tribe_permission_invite"
    tribe_permission_promote = "tribe_permission_promote"
    tribe_permission_demote = "tribe_permission_demote"
    tribe_permission_kick = "tribe_permission_kick"


class TribeSettings(TribeElements):
    """Class for tribe setting elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tribe Settings"
        
    # Element definitions
    tribe_pincode_setting = "tribe_pincode_setting"
    tribe_pincode_toggle = "tribe_pincode_toggle"
    tribe_tame_claim_setting = "tribe_tame_claim_setting"
    tribe_structure_ownership = "tribe_structure_ownership"
    tribe_invitation_button = "tribe_invitation_button"
    tribe_invitation_field = "tribe_invitation_field"
    tribe_kick_button = "tribe_kick_button"
    tribe_promote_button = "tribe_promote_button"
    tribe_demote_button = "tribe_demote_button"
    tribe_leave_button = "tribe_leave_button"
    tribe_disband_button = "tribe_disband_button"




class TribeAdvancedSettings(TribeElements):
    """Class for tribe advanced setting elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Advanced Settings"
        
    # Element definitions
    tribe_taxes_setting = "tribe_taxes_setting"
    tribe_stats_panel = "tribe_stats_panel"
    tribe_territory_map = "tribe_territory_map"
    tribe_member_notes = "tribe_member_notes"
    tribe_message_of_the_day = "tribe_message_of_the_day"
    tribe_government_type = "tribe_government_type"


###############################
# STRUCTURE PLACEMENT ELEMENTS
###############################

class StructurePlacementElements(UIElement):
    """Base class for Structure Placement Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Structure Placement Elements"


class PlacementValidation(StructurePlacementElements):
    """Class for placement validation elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Placement Validation"
        
    # Element definitions
    structure_placement_valid = "structure_placement_valid"
    structure_placement_invalid = "structure_placement_invalid"
    structure_placement_distance_indicator = "structure_placement_distance_indicator"
    structure_placement_angle_indicator = "structure_placement_angle_indicator"
    structure_placement_align_indicator = "structure_placement_align_indicator"
    structure_placement_underwater_indicator = "structure_placement_underwater_indicator"
    structure_placement_no_underwater = "structure_placement_no_underwater"


class PlacementControls(StructurePlacementElements):
    """Class for placement control elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Placement Controls"
        
    # Element definitions
    structure_placement_rotation_controls = "structure_placement_rotation_controls"
    structure_placement_radius_indicator = "structure_placement_radius_indicator"
    structure_placement_ceiling_height = "structure_placement_ceiling_height"
    structure_placement_wall_height = "structure_placement_wall_height"
    structure_placement_water_pipe_connection = "structure_placement_water_pipe_connection"
    structure_placement_electrical_connection = "structure_placement_electrical_connection"
    structure_placement_level_indicator = "structure_placement_level_indicator"


class PlacementResources(StructurePlacementElements):
    """Class for placement resource elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Placement Resources"
        
    # Element definitions
    structure_placement_resource_costs = "structure_placement_resource_costs"
    structure_placement_insufficient_resources = "structure_placement_insufficient_resources"
    structure_placement_structure_limit = "structure_placement_structure_limit"
    structure_placement_platform_limit = "structure_placement_platform_limit"
    structure_placement_platform_restriction = "structure_placement_platform_restriction"
    structure_placement_tek_requirement = "structure_placement_tek_requirement"
    structure_placement_dlc_requirement = "structure_placement_dlc_requirement"
    structure_placement_boss_unlock_required = "structure_placement_boss_unlock_required"


class PlacementTimers(StructurePlacementElements):
    """Class for placement timer elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Placement Timers"
        
    # Element definitions
    structure_placement_pickup_timer = "structure_placement_pickup_timer"
    structure_placement_demolish_refund = "structure_placement_demolish_refund"
    structure_placement_element_range = "structure_placement_element_range"
    structure_placement_tek_shield_range = "structure_placement_tek_shield_range"
    structure_placement_turret_range = "structure_placement_turret_range"


class PlacementEnvironment(StructurePlacementElements):
    """Class for placement environment elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Placement Environment"
        
    # Element definitions
    structure_placement_greenhouse_effect = "structure_placement_greenhouse_effect"
    structure_placement_crop_plot_fertility = "structure_placement_crop_plot_fertility"
    structure_placement_temperature_effect = "structure_placement_temperature_effect"
    structure_placement_air_conditioner_range = "structure_placement_air_conditioner_range"
    structure_placement_generator_range = "structure_placement_generator_range"
    structure_placement_hatchery_range = "structure_placement_hatchery_range"
    structure_placement_trap_trigger_range = "structure_placement_trap_trigger_range"


class PlacementSpecials(StructurePlacementElements):
    """Class for placement special elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Placement Specials"
        
    # Element definitions
    structure_placement_dino_gate_clearance = "structure_placement_dino_gate_clearance"
    structure_placement_ceiling_stability = "structure_placement_ceiling_stability"
    structure_placement_foundation_stability = "structure_placement_foundation_stability"
    structure_placement_pvp_restriction = "structure_placement_pvp_restriction"
    structure_placement_foundation_depth = "structure_placement_foundation_depth"
    structure_placement_terrain_flatten = "structure_placement_terrain_flatten"
    structure_placement_dedi_storage_selection = "structure_placement_dedi_storage_selection"
    structure_placement_pipe_intersection = "structure_placement_pipe_intersection"
    structure_placement_irrigation_status = "structure_placement_irrigation_status"
    structure_placement_wind_turbine_efficiency = "structure_placement_wind_turbine_efficiency"
    structure_placement_no_build_zone = "structure_placement_no_build_zone"


###############################
# ELECTRICAL SYSTEM ELEMENTS
###############################

class ElectricalSystemElements(UIElement):
    """Base class for Electrical System Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Electrical System Elements"


class ElectricalInterface(ElectricalSystemElements):
    """Class for electrical interface elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Electrical Interface"
        
    # Element definitions
    electrical_system_background = "electrical_system_background"
    electrical_system_title = "electrical_system_title"
    electrical_system_powered_indicator = "electrical_system_powered_indicator"
    electrical_system_unpowered_indicator = "electrical_system_unpowered_indicator"
    electrical_system_consumption_display = "electrical_system_consumption_display"
    electrical_system_generation_display = "electrical_system_generation_display"
    electrical_system_range_indicator = "electrical_system_range_indicator"
    electrical_system_connection_points = "electrical_system_connection_points"
    electrical_system_cable_indicator = "electrical_system_cable_indicator"


class ElectricalDevices(ElectricalSystemElements):
    """Class for electrical device elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Electrical Devices"
        
    # Element definitions
    electrical_system_device_list = "electrical_system_device_list"
    electrical_system_device_entry = "electrical_system_device_entry"
    electrical_system_device_name = "electrical_system_device_name"
    electrical_system_device_power_draw = "electrical_system_device_power_draw"
    electrical_system_device_status = "electrical_system_device_status"
    electrical_system_device_range = "electrical_system_device_range"
    electrical_system_device_toggle = "electrical_system_device_toggle"


class ElectricalCircuits(ElectricalSystemElements):
    """Class for electrical circuit elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Electrical Circuits"
        
    # Element definitions
    electrical_system_circuit_group = "electrical_system_circuit_group"
    electrical_system_circuit_selector = "electrical_system_circuit_selector"
    electrical_system_junction_status = "electrical_system_junction_status"
    electrical_system_add_connection_button = "electrical_system_add_connection_button"
    electrical_system_remove_connection_button = "electrical_system_remove_connection_button"


class ElectricalGenerators(ElectricalSystemElements):
    """Class for electrical generator elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Electrical Generators"
        
    # Element definitions
    electrical_system_generator_fuel_level = "electrical_system_generator_fuel_level"
    electrical_system_generator_fuel_slot = "electrical_system_generator_fuel_slot"
    electrical_system_generator_efficiency = "electrical_system_generator_efficiency"
    electrical_system_generator_output = "electrical_system_generator_output"
    electrical_system_battery_charge = "electrical_system_battery_charge"
    electrical_system_battery_duration = "electrical_system_battery_duration"
    electrical_system_battery_charging_indicator = "electrical_system_battery_charging_indicator"
    electrical_system_battery_discharging_indicator = "electrical_system_battery_discharging_indicator"
    electrical_system_solar_panel_efficiency = "electrical_system_solar_panel_efficiency"
    electrical_system_wind_turbine_efficiency = "electrical_system_wind_turbine_efficiency"


class ElectricalSettings(ElectricalSystemElements):
    """Class for electrical setting elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Electrical Settings"
        
    # Element definitions
    electrical_system_auto_power_toggle = "electrical_system_auto_power_toggle"
    electrical_system_timer_setting = "electrical_system_timer_setting"
    electrical_system_schedule_button = "electrical_system_schedule_button"
    electrical_system_schedule_entry = "electrical_system_schedule_entry"
    electrical_system_on_time_selector = "electrical_system_on_time_selector"
    electrical_system_off_time_selector = "electrical_system_off_time_selector"
    electrical_system_day_selector = "electrical_system_day_selector"
    electrical_system_pin_code_field = "electrical_system_pin_code_field"
    electrical_system_lock_button = "electrical_system_lock_button"
    electrical_system_unlock_button = "electrical_system_unlock_button"
    electrical_system_tribe_access_toggle = "electrical_system_tribe_access_toggle"
    electrical_system_public_access_toggle = "electrical_system_public_access_toggle"


class ElectricalGrid(ElectricalSystemElements):
    """Class for electrical grid elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Electrical Grid"
        
    # Element definitions
    electrical_system_power_grid_map = "electrical_system_power_grid_map"
    electrical_system_grid_segment = "electrical_system_grid_segment"
    electrical_system_redundancy_indicator = "electrical_system_redundancy_indicator"
    electrical_system_overload_warning = "electrical_system_overload_warning"
    electrical_system_short_circuit_warning = "electrical_system_short_circuit_warning"
    electrical_system_gasoline_efficiency = "electrical_system_gasoline_efficiency"
    electrical_system_tek_generator_element = "electrical_system_tek_generator_element"
    electrical_system_tek_generator_range = "electrical_system_tek_generator_range"
    electrical_system_tek_generator_devices = "electrical_system_tek_generator_devices"


class ElectricalAdvanced(ElectricalSystemElements):
    """Class for electrical advanced elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Electrical Advanced"
        
    # Element definitions
    electrical_system_device_priority = "electrical_system_device_priority"
    electrical_system_unconnected_warning = "electrical_system_unconnected_warning"
    electrical_system_device_hover_info = "electrical_system_device_hover_info"
    electrical_system_cable_management = "electrical_system_cable_management"
    electrical_system_cable_color_selector = "electrical_system_cable_color_selector"
    electrical_system_cable_visibility_toggle = "electrical_system_cable_visibility_toggle"
    electrical_system_wireless_connection = "electrical_system_wireless_connection"
    electrical_system_transmitter_status = "electrical_system_transmitter_status"
    electrical_system_receiver_status = "electrical_system_receiver_status"
    electrical_system_frequency_selector = "electrical_system_frequency_selector"


class ElectricalMonitoring(ElectricalSystemElements):
    """Class for electrical monitoring elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Electrical Monitoring"
        
    # Element definitions
    electrical_system_energy_consumption_graph = "electrical_system_energy_consumption_graph"
    electrical_system_peak_usage_display = "electrical_system_peak_usage_display"
    electrical_system_power_fluctuation = "electrical_system_power_fluctuation"
    electrical_system_backup_power_status = "electrical_system_backup_power_status"
    electrical_system_alarm_system_button = "electrical_system_alarm_system_button"
    electrical_system_alarm_notification = "electrical_system_alarm_notification"
    electrical_system_remote_power_button = "electrical_system_remote_power_button"
    electrical_system_disconnect_button = "electrical_system_disconnect_button"
    electrical_system_reconnect_button = "electrical_system_reconnect_button"
    electrical_system_rename_device_button = "electrical_system_rename_device_button"
    electrical_system_signal_indicator = "electrical_system_signal_indicator"


###############################
# TRANSFER INTERFACE ELEMENTS
###############################

class TransferInterfaceElements(UIElement):
    """Base class for Transfer Interface Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Transfer Interface Elements"


class TransferBackground(TransferInterfaceElements):
    """Class for transfer background elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Transfer Background"
        
    # Element definitions
    transfer_interface_background = "transfer_interface_background"
    transfer_interface_title = "transfer_interface_title"


class TransferServerList(TransferInterfaceElements):
    """Class for transfer server list elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Server List"
        
    # Element definitions
    transfer_interface_server_list = "transfer_interface_server_list"
    transfer_interface_server_entry = "transfer_interface_server_entry"
    transfer_interface_server_name = "transfer_interface_server_name"
    transfer_interface_server_type = "transfer_interface_server_type"
    transfer_interface_server_population = "transfer_interface_server_population"
    transfer_interface_server_ping = "transfer_interface_server_ping"
    transfer_interface_server_version = "transfer_interface_server_version"
    transfer_interface_server_official = "transfer_interface_server_official"
    transfer_interface_server_unofficial = "transfer_interface_server_unofficial"
    transfer_interface_server_modded = "transfer_interface_server_modded"
    transfer_interface_server_cluster = "transfer_interface_server_cluster"
    transfer_interface_server_favorite = "transfer_interface_server_favorite"
    transfer_interface_server_recent = "transfer_interface_server_recent"
    transfer_interface_server_password = "transfer_interface_server_password"


class TransferSearch(TransferInterfaceElements):
    """Class for transfer search elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Transfer Search"
        
    # Element definitions
    transfer_interface_server_filter = "transfer_interface_server_filter"
    transfer_interface_search_bar = "transfer_interface_search_bar"
    transfer_interface_search_icon = "transfer_interface_search_icon"
    transfer_interface_sort_button = "transfer_interface_sort_button"
    transfer_interface_sort_options = "transfer_interface_sort_options"
    transfer_interface_refresh_button = "transfer_interface_refresh_button"


class TransferButtons(TransferInterfaceElements):
    """Class for transfer button elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Transfer Buttons"
        
    # Element definitions
    transfer_interface_join_button = "transfer_interface_join_button"
    transfer_interface_cancel_button = "transfer_interface_cancel_button"
    transfer_interface_select_button = "transfer_interface_select_button"


class TransferTabs(TransferInterfaceElements):
    """Class for transfer tab elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Transfer Tabs"
        
    # Element definitions
    transfer_interface_player_tab = "transfer_interface_player_tab"
    transfer_interface_item_tab = "transfer_interface_item_tab"
    transfer_interface_dino_tab = "transfer_interface_dino_tab"


class TransferPlayers(TransferInterfaceElements):
    """Class for transfer player elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Transfer Players"
        
    # Element definitions
    transfer_interface_player_select = "transfer_interface_player_select"
    transfer_interface_player_entry = "transfer_interface_player_entry"
    transfer_interface_player_name = "transfer_interface_player_name"
    transfer_interface_player_level = "transfer_interface_player_level"
    transfer_interface_player_tribe = "transfer_interface_player_tribe"
    transfer_interface_player_server = "transfer_interface_player_server"
    transfer_interface_player_preview = "transfer_interface_player_preview"
    transfer_interface_player_last_played = "transfer_interface_player_last_played"
    transfer_interface_download_player_button = "transfer_interface_download_player_button"
    transfer_interface_upload_player_button = "transfer_interface_upload_player_button"
    transfer_interface_create_player_button = "transfer_interface_create_player_button"


class TransferItems(TransferInterfaceElements):
    """Class for transfer item elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Transfer Items"
        
    # Element definitions
    transfer_interface_item_storage = "transfer_interface_item_storage"
    transfer_interface_item_slot = "transfer_interface_item_slot"
    transfer_interface_item_icon = "transfer_interface_item_icon"
    transfer_interface_item_name = "transfer_interface_item_name"
    transfer_interface_item_count = "transfer_interface_item_count"
    transfer_interface_item_tooltip = "transfer_interface_item_tooltip"
    transfer_interface_download_item_button = "transfer_interface_download_item_button"
    transfer_interface_upload_item_button = "transfer_interface_upload_item_button"


class TransferDinos(TransferInterfaceElements):
    """Class for transfer dino elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Transfer Dinos"
        
    # Element definitions
    transfer_interface_dino_storage = "transfer_interface_dino_storage"
    transfer_interface_dino_entry = "transfer_interface_dino_entry"
    transfer_interface_dino_icon = "transfer_interface_dino_icon"
    transfer_interface_dino_name = "transfer_interface_dino_name"
    transfer_interface_dino_level = "transfer_interface_dino_level"
    transfer_interface_dino_gender = "transfer_interface_dino_gender"
    transfer_interface_dino_stats = "transfer_interface_dino_stats"
    transfer_interface_dino_preview = "transfer_interface_dino_preview"
    transfer_interface_download_dino_button = "transfer_interface_download_dino_button"
    transfer_interface_upload_dino_button = "transfer_interface_upload_dino_button"


class TransferStatus(TransferInterfaceElements):
    """Class for transfer status elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Transfer Status"
        
    # Element definitions
    transfer_interface_transfer_cooldown = "transfer_interface_transfer_cooldown"
    transfer_interface_cooldown_icon = "transfer_interface_cooldown_icon"
    transfer_interface_storage_slots = "transfer_interface_storage_slots"
    transfer_interface_storage_used = "transfer_interface_storage_used"
    transfer_interface_storage_total = "transfer_interface_storage_total"
    transfer_interface_weight_indicator = "transfer_interface_weight_indicator"
    transfer_interface_weight_limit = "transfer_interface_weight_limit"
    transfer_interface_weight_warning = "transfer_interface_weight_warning"
    transfer_interface_timer_countdown = "transfer_interface_timer_countdown"
    transfer_interface_transfer_rules = "transfer_interface_transfer_rules"
    transfer_interface_prohibited_items = "transfer_interface_prohibited_items"
    transfer_interface_prohibited_dinos = "transfer_interface_prohibited_dinos"
    transfer_interface_event_warning = "transfer_interface_event_warning"
    transfer_interface_tek_warning = "transfer_interface_tek_warning"
    transfer_interface_element_warning = "transfer_interface_element_warning"


class TransferConfirmation(TransferInterfaceElements):
    """Class for transfer confirmation elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Transfer Confirmation"
        
    # Element definitions
    transfer_interface_connection_status = "transfer_interface_connection_status"
    transfer_interface_transfer_progress = "transfer_interface_transfer_progress"
    transfer_interface_transfer_error = "transfer_interface_transfer_error"
    transfer_interface_confirmation_prompt = "transfer_interface_confirmation_prompt"
    transfer_interface_confirm_button = "transfer_interface_confirm_button"
    transfer_interface_decline_button = "transfer_interface_decline_button"
    transfer_interface_password_field = "transfer_interface_password_field"


class TransferFilters(TransferInterfaceElements):
    """Class for transfer filter elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Transfer Filters"
        
    # Element definitions
    transfer_interface_cluster_filter = "transfer_interface_cluster_filter"
    transfer_interface_official_filter = "transfer_interface_official_filter"
    transfer_interface_unofficial_filter = "transfer_interface_unofficial_filter"
    transfer_interface_favorites_filter = "transfer_interface_favorites_filter"
    transfer_interface_recent_filter = "transfer_interface_recent_filter"
    transfer_interface_history_button = "transfer_interface_history_button"
    transfer_interface_history_list = "transfer_interface_history_list"
    transfer_interface_history_entry = "transfer_interface_history_entry"


class TransferServerInfo(TransferInterfaceElements):
    """Class for transfer server info elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Server Info"
        
    # Element definitions
    transfer_interface_server_info_panel = "transfer_interface_server_info_panel"
    transfer_interface_map_indicator = "transfer_interface_map_indicator"
    transfer_interface_rates_display = "transfer_interface_rates_display"
    transfer_interface_event_display = "transfer_interface_event_display"
    transfer_interface_server_rules = "transfer_interface_server_rules"
    transfer_interface_server_mods = "transfer_interface_server_mods"
    transfer_interface_mod_entry = "transfer_interface_mod_entry"
    transfer_interface_tribute_requirements = "transfer_interface_tribute_requirements"
    transfer_interface_tribute_slot = "transfer_interface_tribute_slot"


###############################
# SETTINGS MENU ELEMENTS
###############################

class SettingsMenuElements(UIElement):
    """Base class for Settings Menu Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Settings Menu Elements"


class SettingsBackground(SettingsMenuElements):
    """Class for settings background elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Settings Background"
        
    # Element definitions
    settings_menu_background = "settings_menu_background"
    settings_menu_title = "settings_menu_title"


class SettingsTabs(SettingsMenuElements):
    """Class for settings tab elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Settings Tabs"
        
    # Element definitions
    settings_category_tabs = "settings_category_tabs"
    settings_tab_general = "settings_tab_general"
    settings_tab_graphics = "settings_tab_graphics"
    settings_tab_audio = "settings_tab_audio"
    settings_tab_controls = "settings_tab_controls"
    settings_tab_game = "settings_tab_game"
    settings_tab_server = "settings_tab_server"
    settings_tab_interface = "settings_tab_interface"
    settings_tab_advanced = "settings_tab_advanced"


class SettingsSections(SettingsMenuElements):
    """Class for settings section elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Settings Sections"
        
    # Element definitions
    settings_section_header = "settings_section_header"
    settings_option_row = "settings_option_row"
    settings_option_name = "settings_option_name"
    settings_option_description = "settings_option_description"
    settings_option_value = "settings_option_value"


class SettingsControls(SettingsMenuElements):
    """Class for settings control elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Settings Controls"
        
    # Element definitions
    settings_slider_control = "settings_slider_control"
    settings_slider_value = "settings_slider_value"
    settings_dropdown_control = "settings_dropdown_control"
    settings_dropdown_option = "settings_dropdown_option"
    settings_checkbox_control = "settings_checkbox_control"
    settings_checkbox_checked = "settings_checkbox_checked"
    settings_checkbox_unchecked = "settings_checkbox_unchecked"
    settings_radio_button = "settings_radio_button"
    settings_radio_selected = "settings_radio_selected"
    settings_radio_unselected = "settings_radio_unselected"
    settings_input_field = "settings_input_field"
    settings_input_value = "settings_input_value"
    settings_button_control = "settings_button_control"


class SettingsActions(SettingsMenuElements):
    """Class for settings action elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Settings Actions"
        
    # Element definitions
    settings_reset_button = "settings_reset_button"
    settings_apply_button = "settings_apply_button"
    settings_save_button = "settings_save_button"
    settings_cancel_button = "settings_cancel_button"


###############################
# HOLIDAY EVENT ELEMENTS
###############################

class HolidayEventElements(UIElement):
    """Base class for Holiday Event Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Holiday Event Elements"


class HolidayInterfaces(HolidayEventElements):
    """Class for holiday interface elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Holiday Interfaces"
        
    # Element definitions
    holiday_event_interface = "holiday_event_interface"
    easter_egg_hunt_tracker = "easter_egg_hunt_tracker"
    summer_bash_interface = "summer_bash_interface"
    fear_evolved_interface = "fear_evolved_interface"
    winter_wonderland_interface = "winter_wonderland_interface"
    valentines_day_interface = "valentines_day_interface"
    eggcellent_adventure_ui = "eggcellent_adventure_ui"


class GenesisMissions(HolidayEventElements):
    """Class for Genesis mission elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Genesis Missions"
        
    # Element definitions
    genesis_race_timer = "genesis_race_timer"
    genesis_hunt_tracker = "genesis_hunt_tracker"
    genesis_fishing_meter = "genesis_fishing_meter"


###############################
# TEK ELEMENTS
###############################

class TekElements(UIElement):
    """Base class for Tek Elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Tek Elements"


class TekInterfaces(TekElements):
    """Class for tek interface elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tek Interfaces"
        
    # Element definitions
    tek_generator_interface = "tek_generator_interface"
    tek_crop_plot_interface = "tek_crop_plot_interface"
    creature_camera_view = "creature_camera_view"
    tek_sensor_interface = "tek_sensor_interface"
    tek_remote_camera = "tek_remote_camera"
    holo_projector_interface = "holo_projector_interface"
    megachelon_planter = "megachelon_planter"


class TekCreatureUI(TekElements):
    """Class for tek creature UI elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tek Creature UI"
        
    # Element definitions
    aquatic_tames_oxygen_interface = "aquatic_tames_oxygen_interface"
    astrodelphis_energy = "astrodelphis_energy"
    noglin_brain_jack_interface = "noglin_brain_jack_interface"
    exo_mek_interface = "exo_mek_interface"
    maewing_baby_milk_meter = "maewing_baby_milk_meter"
    shadowmane_charge_meter = "shadowmane_charge_meter"
    gacha_crafting_interface = "gacha_crafting_interface"
    stryder_interface = "stryder_interface"
    enforcer_interface = "enforcer_interface"


class TekResources(TekElements):
    """Class for tek resource elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tek Resources"
        
    # Element definitions
    tek_element_icon = "tek_element_icon"
    tek_element_count = "tek_element_count"
    tek_element_shard_icon = "tek_element_shard_icon"
    tek_element_shard_count = "tek_element_shard_count"
    tek_element_dust_icon = "tek_element_dust_icon"
    tek_element_dust_count = "tek_element_dust_count"


class TekTransmitter(TekElements):
    """Class for tek transmitter elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tek Transmitter"
        
    # Element definitions
    tek_transmitter_interface = "tek_transmitter_interface"
    tek_transmitter_upload_tab = "tek_transmitter_upload_tab"
    tek_transmitter_download_tab = "tek_transmitter_download_tab"
    tek_transmitter_creatures_tab = "tek_transmitter_creatures_tab"
    tek_transmitter_items_tab = "tek_transmitter_items_tab"
    tek_transmitter_data_tab = "tek_transmitter_data_tab"
    tek_transmitter_upload_timer = "tek_transmitter_upload_timer"
    tek_transmitter_download_timer = "tek_transmitter_download_timer"
    tek_transmitter_upload_button = "tek_transmitter_upload_button"
    tek_transmitter_download_button = "tek_transmitter_download_button"
    tek_transmitter_item_list = "tek_transmitter_item_list"
    tek_transmitter_creature_list = "tek_transmitter_creature_list"


class TekTeleporter(TekElements):
    """Class for tek teleporter elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tek Teleporter"
        
    # Element definitions
    tek_teleporter_interface = "tek_teleporter_interface"
    tek_teleporter_location_list = "tek_teleporter_location_list"
    tek_teleporter_location_entry = "tek_teleporter_location_entry"
    tek_teleporter_teleport_button = "tek_teleporter_teleport_button"
    tek_teleporter_add_location_button = "tek_teleporter_add_location_button"
    tek_teleporter_rename_button = "tek_teleporter_rename_button"
    tek_teleporter_remove_button = "tek_teleporter_remove_button"


class TekAdvancedStructures(TekElements):
    """Class for tek advanced structure elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Advanced Structures"
        
    # Element definitions
    tek_replicator_interface = "tek_replicator_interface"
    tek_replicator_crafting_tab = "tek_replicator_crafting_tab"
    tek_replicator_inventory_tab = "tek_replicator_inventory_tab"
    tek_replicator_element_slot = "tek_replicator_element_slot"
    tek_cloning_interface = "tek_cloning_interface"
    tek_cloning_dino_preview = "tek_cloning_dino_preview"
    tek_cloning_progress_bar = "tek_cloning_progress_bar"
    tek_cloning_cost_display = "tek_cloning_cost_display"
    tek_cloning_start_button = "tek_cloning_start_button"
    tek_cloning_cancel_button = "tek_cloning_cancel_button"


class TekStorage(TekElements):
    """Class for tek storage elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tek Storage"
        
    # Element definitions
    tek_dedicated_storage = "tek_dedicated_storage"
    tek_dedicated_storage_type = "tek_dedicated_storage_type"
    tek_dedicated_storage_count = "tek_dedicated_storage_count"
    tek_dedicated_storage_capacity = "tek_dedicated_storage_capacity"


class TekGenerator(TekElements):
    """Class for tek generator elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tek Generator"
        
    # Element definitions
    tek_generator_interface = "tek_generator_interface"
    tek_generator_range_display = "tek_generator_range_display"
    tek_generator_element_level = "tek_generator_element_level"
    tek_generator_power_indicator = "tek_generator_power_indicator"
    tek_generator_connected_devices = "tek_generator_connected_devices"


class TekShield(TekElements):
    """Class for tek shield elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tek Shield"
        
    # Element definitions
    tek_shield_interface = "tek_shield_interface"
    tek_shield_range_display = "tek_shield_range_display"
    tek_shield_strength_display = "tek_shield_strength_display"
    tek_shield_damage_indicator = "tek_shield_damage_indicator"


class TekTrough(TekElements):
    """Class for tek trough elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tek Trough"
        
    # Element definitions
    tek_trough_interface = "tek_trough_interface"
    tek_trough_food_list = "tek_trough_food_list"
    tek_trough_range_display = "tek_trough_range_display"
    tek_trough_status_indicator = "tek_trough_status_indicator"


class TekVehicles(TekElements):
    """Class for tek vehicle elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tek Vehicles"
        
    # Element definitions
    tek_hover_skiff_controls = "tek_hover_skiff_controls"
    tek_hover_skiff_altitude = "tek_hover_skiff_altitude"
    tek_hover_skiff_speed = "tek_hover_skiff_speed"
    tek_hover_skiff_fuel = "tek_hover_skiff_fuel"
    tek_hover_skiff_passenger_list = "tek_hover_skiff_passenger_list"


class TekSensor(TekElements):
    """Class for tek sensor elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tek Sensor"
        
    # Element definitions
    tek_sensor_interface = "tek_sensor_interface"
    tek_sensor_range_setting = "tek_sensor_range_setting"
    tek_sensor_mode_setting = "tek_sensor_mode_setting"
    tek_sensor_entity_filter = "tek_sensor_entity_filter"
    tek_sensor_alert_setting = "tek_sensor_alert_setting"


class TekVisor(TekElements):
    """Class for tek visor elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tek Visor"
        
    # Element definitions
    tek_visor_overlay = "tek_visor_overlay"
    tek_visor_mode_selector = "tek_visor_mode_selector"
    tek_visor_night_vision = "tek_visor_night_vision"
    tek_visor_entity_scan = "tek_visor_entity_scan"
    tek_visor_resource_scan = "tek_visor_resource_scan"
    tek_visor_stats_display = "tek_visor_stats_display"
    tek_visor_range_indicator = "tek_visor_range_indicator"
    tek_visor_battery_indicator = "tek_visor_battery_indicator"


class TekArmor(TekElements):
    """Class for tek armor elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tek Armor"
        
    # Element definitions
    tek_gauntlet_punch_charge = "tek_gauntlet_punch_charge"
    tek_gauntlet_cooldown = "tek_gauntlet_cooldown"
    tek_boots_speed_indicator = "tek_boots_speed_indicator"
    tek_boots_jump_indicator = "tek_boots_jump_indicator"
    tek_chestpiece_flight_fuel = "tek_chestpiece_flight_fuel"
    tek_chestpiece_flight_speed = "tek_chestpiece_flight_speed"
    tek_chestpiece_flight_altitude = "tek_chestpiece_flight_altitude"


class TekWeapons(TekElements):
    """Class for tek weapon elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tek Weapons"
        
    # Element definitions
    tek_rifle_charge_indicator = "tek_rifle_charge_indicator"
    tek_rifle_mode_selector = "tek_rifle_mode_selector"
    tek_rifle_ammo_display = "tek_rifle_ammo_display"
    tek_grenade_launcher_charge = "tek_grenade_launcher_charge"


class TekCreatures(TekElements):
    """Class for tek creature elements"""
    def __init__(self, name, color="#00ccff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Tek Creatures"
        
    # Element definitions
    tek_stryder_interface = "tek_stryder_interface"
    tek_stryder_module_slots = "tek_stryder_module_slots"
    tek_stryder_resource_capacity = "tek_stryder_resource_capacity"
    tek_stryder_farming_indicator = "tek_stryder_farming_indicator"
    tek_megachelon_platform = "tek_megachelon_platform"
    tek_megachelon_planter = "tek_megachelon_planter"
    tek_megachelon_greenhouse = "tek_megachelon_greenhouse"
    tek_enforce_mode_interface = "tek_enforce_mode_interface"


###############################
# BOSS ARENA ELEMENTS
###############################

class BossArenaElements(UIElement):
    """Base class for Boss Arena Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Boss Arena Elements"


class BossEntryInterface(BossArenaElements):
    """Class for boss entry interface elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Entry Interface"
        
    # Element definitions
    boss_arena_entry_interface = "boss_arena_entry_interface"
    boss_arena_tribute_slots = "boss_arena_tribute_slots"
    boss_arena_artifact_slots = "boss_arena_artifact_slots"
    boss_arena_player_list = "boss_arena_player_list"
    boss_arena_tame_list = "boss_arena_tame_list"
    boss_arena_difficulty_selector = "boss_arena_difficulty_selector"
    boss_arena_timer_countdown = "boss_arena_timer_countdown"
    boss_arena_start_button = "boss_arena_start_button"
    boss_arena_cancel_button = "boss_arena_cancel_button"


class BossFightElements(BossArenaElements):
    """Class for boss fight elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Boss Fight"
        
    # Element definitions
    boss_fight_timer = "boss_fight_timer"
    boss_fight_player_list = "boss_fight_player_list"
    boss_fight_player_entry = "boss_fight_player_entry"
    boss_fight_tame_list = "boss_fight_tame_list"
    boss_fight_tame_entry = "boss_fight_tame_entry"
    boss_health_bar = "boss_health_bar"
    boss_health_percentage = "boss_health_percentage"
    boss_name_display = "boss_name_display"
    boss_damage_indicator = "boss_damage_indicator"


class BossAttackWarnings(BossArenaElements):
    """Class for boss attack warning elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Attack Warnings"
        
    # Element definitions
    boss_attack_warning = "boss_attack_warning"
    boss_special_attack_warning = "boss_special_attack_warning"
    boss_minion_spawned_alert = "boss_minion_spawned_alert"
    boss_environment_hazard = "boss_environment_hazard"
    boss_arena_safe_zone = "boss_arena_safe_zone"
    boss_arena_danger_zone = "boss_arena_danger_zone"
    boss_phase_transition = "boss_phase_transition"


class BossArenaExit(BossArenaElements):
    """Class for boss arena exit elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Arena Exit"
        
    # Element definitions
    boss_arena_exit_timer = "boss_arena_exit_timer"
    boss_arena_teleport_indicator = "boss_arena_teleport_indicator"
    boss_arena_item_reward_list = "boss_arena_item_reward_list"
    boss_arena_tekgram_unlocked = "boss_arena_tekgram_unlocked"
    boss_arena_defeat_message = "boss_arena_defeat_message"
    boss_arena_victory_message = "boss_arena_victory_message"
    boss_arena_disconnect_warning = "boss_arena_disconnect_warning"
    boss_arena_player_death_marker = "boss_arena_player_death_marker"
    boss_arena_respawn_timer = "boss_arena_respawn_timer"
    boss_arena_spectator_mode = "boss_arena_spectator_mode"
    boss_arena_damage_leaderboard = "boss_arena_damage_leaderboard"


class BossArtifactElements(BossArenaElements):
    """Class for boss artifact elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Artifact Elements"
        
    # Element definitions
    boss_artifact_collection_notification = "boss_artifact_collection_notification"
    boss_arena_tek_suit_activation = "boss_arena_tek_suit_activation"
    boss_arena_element_reward = "boss_arena_element_reward"
    boss_arena_experience_reward = "boss_arena_experience_reward"
    boss_arena_ascension_cutscene = "boss_arena_ascension_cutscene"
    boss_arena_reward_multiplier = "boss_arena_reward_multiplier"
    boss_arena_cave_progress = "boss_arena_cave_progress"
    boss_arena_required_items_list = "boss_arena_required_items_list"
    boss_arena_missing_items = "boss_arena_missing_items"
    boss_arena_element_buffer = "boss_arena_element_buffer"


class BossDifficultyElements(BossArenaElements):
    """Class for boss difficulty elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Difficulty Elements"
        
    # Element definitions
    boss_arena_difficulty_icon = "boss_arena_difficulty_icon"
    boss_arena_previous_record = "boss_arena_previous_record"
    boss_arena_tribe_limit = "boss_arena_tribe_limit"
    boss_arena_dino_limit = "boss_arena_dino_limit"
    boss_arena_dino_type_restriction = "boss_arena_dino_type_restriction"
    boss_arena_enrage_timer = "boss_arena_enrage_timer"
    boss_arena_cinematic_skip = "boss_arena_cinematic_skip"


###############################
# EVENT INTERFACE ELEMENTS
###############################

class EventInterfaceElements(UIElement):
    """Base class for Event Interface Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Event Interface Elements"


class EventBackground(EventInterfaceElements):
    """Class for event background elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Event Background"
        
    # Element definitions
    event_interface_background = "event_interface_background"
    event_title_header = "event_title_header"
    event_description_text = "event_description_text"
    event_timer_countdown = "event_timer_countdown"
    event_progress_bar = "event_progress_bar"


class EventObjectives(EventInterfaceElements):
    """Class for event objective elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Event Objectives"
        
    # Element definitions
    event_objective_list = "event_objective_list"
    event_objective_entry = "event_objective_entry"
    event_objective_complete_marker = "event_objective_complete_marker"
    event_reward_preview = "event_reward_preview"
    event_reward_list = "event_reward_list"
    event_reward_item = "event_reward_item"


class EventLeaderboard(EventInterfaceElements):
    """Class for event leaderboard elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Event Leaderboard"
        
    # Element definitions
    event_leaderboard = "event_leaderboard"
    event_leaderboard_entry = "event_leaderboard_entry"
    event_participation_count = "event_participation_count"
    event_difficulty_indicator = "event_difficulty_indicator"
    event_location_marker = "event_location_marker"


class EventControls(EventInterfaceElements):
    """Class for event control elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Event Controls"
        
    # Element definitions
    event_start_button = "event_start_button"
    event_cancel_button = "event_cancel_button"
    event_restart_button = "event_restart_button"


###############################
# DEATH SCREEN ELEMENTS
###############################

class DeathScreenElements(UIElement):
    """Base class for Death Screen Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Death Screen Elements"


class DeathScreenBackground(DeathScreenElements):
    """Class for death screen background elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Death Screen Background"
        
    # Element definitions
    death_screen_background = "death_screen_background"
    death_screen_title = "death_screen_title"
    death_message_display = "death_message_display"
    death_level_lost_indicator = "death_level_lost_indicator"
    death_item_lost_list = "death_item_lost_list"
    death_item_lost_entry = "death_item_lost_entry"


class DeathRespawnElements(DeathScreenElements):
    """Class for death respawn elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Respawn Elements"
        
    # Element definitions
    death_respawn_timer = "death_respawn_timer"
    death_location_coordinates = "death_location_coordinates"
    death_map_marker = "death_map_marker"
    death_respawn_button = "death_respawn_button"
    death_harvest_body_indicator = "death_harvest_body_indicator"
    death_spectate_button = "death_spectate_button"
    death_tribe_notify_indicator = "death_tribe_notify_indicator"


class DeathRespawnLocations(DeathScreenElements):
    """Class for death respawn location elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Respawn Locations"
        
    # Element definitions
    death_respawn_location_list = "death_respawn_location_list"
    death_respawn_location_entry = "death_respawn_location_entry"
    death_respawn_bed_entry = "death_respawn_bed_entry"
    death_respawn_sleeping_bag_entry = "death_respawn_sleeping_bag_entry"
    death_respawn_random_entry = "death_respawn_random_entry"
    death_respawn_location_cooldown = "death_respawn_location_cooldown"
    death_respawn_location_icon = "death_respawn_location_icon"
    death_respawn_location_name = "death_respawn_location_name"
    death_respawn_region_selector = "death_respawn_region_selector"
    death_respawn_map_view = "death_respawn_map_view"


class DeathCorpseElements(DeathScreenElements):
    """Class for death corpse elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Corpse Elements"
        
    # Element definitions
    death_body_decay_timer = "death_body_decay_timer"
    death_tribe_corpse_marker = "death_tribe_corpse_marker"
    death_tribe_corpse_name = "death_tribe_corpse_name"
    death_respawn_search_bar = "death_respawn_search_bar"
    death_respawn_filter = "death_respawn_filter"
    death_respawn_sort_button = "death_respawn_sort_button"


class DeathDetailsElements(DeathScreenElements):
    """Class for death details elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Death Details"
        
    # Element definitions
    death_obituary_text = "death_obituary_text"
    death_killed_by_display = "death_killed_by_display"
    death_tribe_bed_category = "death_tribe_bed_category"
    death_personal_bed_category = "death_personal_bed_category"
    death_public_bed_category = "death_public_bed_category"
    death_respawn_header = "death_respawn_header"
    death_screen_tip = "death_screen_tip"


class DeathScreenControls(DeathScreenElements):
    """Class for death screen control elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Death Screen Controls"
        
    # Element definitions
    death_screen_close_button = "death_screen_close_button"
    death_item_recovery_info = "death_item_recovery_info"
    death_xp_penalty_display = "death_xp_penalty_display"
    death_player_level_display = "death_player_level_display"
    death_tribe_icon = "death_tribe_icon"
    death_transfer_warning = "death_transfer_warning"
    death_retrievable_body_marker = "death_retrievable_body_marker"
    death_retrievable_body_timer = "death_retrievable_body_timer"


class DeathCauseElements(DeathScreenElements):
    """Class for death cause elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Death Cause"
        
    # Element definitions
    death_environment_killed = "death_environment_killed"
    death_player_killed = "death_player_killed"
    death_creature_killed = "death_creature_killed"
    death_suicide_indicator = "death_suicide_indicator"
    death_disconnect_warning = "death_disconnect_warning"
    death_respawn_confirmation = "death_respawn_confirmation"
    death_item_protected_tag = "death_item_protected_tag"
    death_reconnect_button = "death_reconnect_button"
    death_return_to_menu = "death_return_to_menu"


###############################
# BREEDING INTERFACE ELEMENTS
###############################

class BreedingInterfaceElements(UIElement):
    """Base class for Breeding Interface Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Breeding Interface Elements"


class BreedingBackground(BreedingInterfaceElements):
    """Class for breeding background elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Breeding Background"
        
    # Element definitions
    breeding_interface_background = "breeding_interface_background"
    breeding_interface_header = "breeding_interface_header"
    breeding_male_stats_panel = "breeding_male_stats_panel"
    breeding_female_stats_panel = "breeding_female_stats_panel"
    breeding_compatibility_indicator = "breeding_compatibility_indicator"


class BreedingControls(BreedingInterfaceElements):
    """Class for breeding control elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Breeding Controls"
        
    # Element definitions
    breeding_enable_mating_button = "breeding_enable_mating_button"
    breeding_disable_mating_button = "breeding_disable_mating_button"
    breeding_mating_progress_bar = "breeding_mating_progress_bar"
    breeding_mating_cooldown_timer = "breeding_mating_cooldown_timer"
    breeding_gestation_progress_bar = "breeding_gestation_progress_bar"
    breeding_gestation_timer = "breeding_gestation_timer"


class BreedingEggs(BreedingInterfaceElements):
    """Class for breeding egg elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Breeding Eggs"
        
    # Element definitions
    breeding_egg_incubation_bar = "breeding_egg_incubation_bar"
    breeding_egg_incubation_timer = "breeding_egg_incubation_timer"
    breeding_egg_temperature_indicator = "breeding_egg_temperature_indicator"
    breeding_egg_temperature_bar = "breeding_egg_temperature_bar"
    breeding_egg_too_hot_warning = "breeding_egg_too_hot_warning"
    breeding_egg_too_cold_warning = "breeding_egg_too_cold_warning"
    breeding_egg_health_bar = "breeding_egg_health_bar"
    breeding_egg_inventory_icon = "breeding_egg_inventory_icon"
    breeding_egg_fertility_status = "breeding_egg_fertility_status"
    breeding_egg_claim_button = "breeding_egg_claim_button"
    breeding_egg_destroy_button = "breeding_egg_destroy_button"
    breeding_egg_pickup_button = "breeding_egg_pickup_button"
    breeding_egg_drop_button = "breeding_egg_drop_button"
    breeding_egg_spoil_timer = "breeding_egg_spoil_timer"


class BreedingMutations(BreedingInterfaceElements):
    """Class for breeding mutation elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Breeding Mutations"
        
    # Element definitions
    breeding_mutation_indicator = "breeding_mutation_indicator"
    breeding_mutation_counter = "breeding_mutation_counter"
    breeding_baby_claim_prompt = "breeding_baby_claim_prompt"
    breeding_baby_name_field = "breeding_baby_name_field"


class BreedingImprinting(BreedingInterfaceElements):
    """Class for breeding imprinting elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Breeding Imprinting"
        
    # Element definitions
    breeding_baby_imprint_status = "breeding_baby_imprint_status"
    breeding_imprint_progress_bar = "breeding_imprint_progress_bar"
    breeding_imprint_quality = "breeding_imprint_quality"
    breeding_imprint_timer = "breeding_imprint_timer"
    breeding_imprint_action_icon = "breeding_imprint_action_icon"
    breeding_imprint_success_indicator = "breeding_imprint_success_indicator"


class BreedingMaturation(BreedingInterfaceElements):
    """Class for breeding maturation elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Breeding Maturation"
        
    # Element definitions
    breeding_maturation_progress_bar = "breeding_maturation_progress_bar"
    breeding_maturation_timer = "breeding_maturation_timer"
    breeding_food_consumption_rate = "breeding_food_consumption_rate"
    breeding_juvenile_food_warning = "breeding_juvenile_food_warning"
    breeding_baby_inventory_button = "breeding_baby_inventory_button"
    breeding_food_trough_link = "breeding_food_trough_link"


class BreedingAncestry(BreedingInterfaceElements):
    """Class for breeding ancestry elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Breeding Ancestry"
        
    # Element definitions
    breeding_ancestry_button = "breeding_ancestry_button"
    breeding_ancestry_tree = "breeding_ancestry_tree"
    breeding_ancestry_entry = "breeding_ancestry_entry"
    breeding_stat_inheritance_display = "breeding_stat_inheritance_display"
    breeding_stat_mutation_highlight = "breeding_stat_mutation_highlight"
    breeding_color_inheritance_display = "breeding_color_inheritance_display"
    breeding_color_region_indicator = "breeding_color_region_indicator"
    breeding_region_mutation_highlight = "breeding_region_mutation_highlight"
    breeding_best_stat_indicator = "breeding_best_stat_indicator"


class BreedingStatusInformation(BreedingInterfaceElements):
    """Class for breeding status information elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Status Information"
        
    # Element definitions
    breeding_mate_boost_indicator = "breeding_mate_boost_indicator"
    breeding_creature_gender_icon = "breeding_creature_gender_icon"
    breeding_creature_gender_text = "breeding_creature_gender_text"
    breeding_growth_phases_display = "breeding_growth_phases_display"
    breeding_growth_phase_indicator = "breeding_growth_phase_indicator"
    breeding_cuddle_button = "breeding_cuddle_button"
    breeding_walk_button = "breeding_walk_button"
    breeding_feed_button = "breeding_feed_button"


class BreedingAdvanced(BreedingInterfaceElements):
    """Class for breeding advanced elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Breeding Advanced"
        
    # Element definitions
    breeding_cryopod_timer = "breeding_cryopod_timer"
    breeding_cryosickness_timer = "breeding_cryosickness_timer"
    breeding_clone_vs_parent = "breeding_clone_vs_parent"
    breeding_generation_counter = "breeding_generation_counter"
    breeding_linebreeding_indicator = "breeding_linebreeding_indicator"
    breeding_mutation_probability = "breeding_mutation_probability"
    breeding_breeding_cooldown = "breeding_breeding_cooldown"
    breeding_wandering_warning = "breeding_wandering_warning"


###############################
# STRUCTURE STORAGE ELEMENTS
###############################

class StructureElements(UIElement):
    """Base class for Structure Storage Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Structure Storage Elements"


class StructureBackground(StructureElements):
    """Class for structure background elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Structure Background"
        
    # Element definitions
    structure_background = "structure_background"
    structure_title = "structure_title"
    structure_type_icon = "structure_type_icon"
    structure_slots_count = "structure_slots_count"
    structure_weight_indicator = "structure_weight_indicator"
    structure_weight_bar = "structure_weight_bar"
    structure_current_weight = "structure_current_weight"
    structure_max_weight = "structure_max_weight"


class StructureSearch(StructureElements):
    """Class for structure search elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Structure Search"
        
    # Element definitions
    structure_search_bar = "structure_search_bar"
    structure_search_icon = "structure_search_icon"
    structure_search_results = "structure_search_results"
    structure_close_button = "structure_close_button"
    structure_transfer_all_button = "structure_transfer_all_button"
    structure_transfer_one_button = "structure_transfer_one_button"
    structure_sort_button = "structure_sort_button"


class StructureSlots(StructureElements):
    """Class for structure slot elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Structure Slots"
        
    # Element definitions
    structure_slot_empty = "structure_slot_empty"
    structure_slot_filled = "structure_slot_filled"
    structure_item_icon = "structure_item_icon"
    structure_item_name = "structure_item_name"
    structure_item_count = "structure_item_count"
    structure_item_durability = "structure_item_durability"
    structure_item_quality = "structure_item_quality"
    structure_item_spoil_timer = "structure_item_spoil_timer"
    structure_grid_view = "structure_grid_view"
    structure_list_view = "structure_list_view"
    structure_filter_button = "structure_filter_button"
    structure_filter_dropdown = "structure_filter_dropdown"


class StructureScrolling(StructureElements):
    """Class for structure scrolling elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Structure Scrolling"
        
    # Element definitions
    structure_scroll_bar = "structure_scroll_bar"
    structure_scroll_up_button = "structure_scroll_up_button"
    structure_scroll_down_button = "structure_scroll_down_button"
    structure_tab_inventory = "structure_tab_inventory"
    structure_tab_contents = "structure_tab_contents"
    structure_pin_code_field = "structure_pin_code_field"
    structure_locked_indicator = "structure_locked_indicator"
    structure_unlocked_indicator = "structure_unlocked_indicator"


class StructureAccess(StructureElements):
    """Class for structure access elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Structure Access"
        
    # Element definitions
    structure_tribe_access_icon = "structure_tribe_access_icon"
    structure_public_access_icon = "structure_public_access_icon"
    structure_remote_access_icon = "structure_remote_access_icon"
    structure_auto_sort_toggle = "structure_auto_sort_toggle"
    structure_transfer_mode_toggle = "structure_transfer_mode_toggle"
    structure_preserve_multiplier = "structure_preserve_multiplier"
    structure_powered_indicator = "structure_powered_indicator"
    structure_unpowered_indicator = "structure_unpowered_indicator"


class StructureManagement(StructureElements):
    """Class for structure management elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Structure Management"
        
    # Element definitions
    structure_rename_button = "structure_rename_button"
    structure_destroy_button = "structure_destroy_button"
    structure_repair_button = "structure_repair_button"
    structure_pickup_timer = "structure_pickup_timer"
    structure_demolish_timer = "structure_demolish_timer"
    structure_lock_button = "structure_lock_button"
    structure_unlock_button = "structure_unlock_button"
    structure_tribe_only_toggle = "structure_tribe_only_toggle"
    structure_pin_code_toggle = "structure_pin_code_toggle"
    structure_unlock_for_all_toggle = "structure_unlock_for_all_toggle"


class StructureFolders(StructureElements):
    """Class for structure folder elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Structure Folders"
        
    # Element definitions
    structure_folder_create_button = "structure_folder_create_button"
    structure_folder_icon = "structure_folder_icon"
    structure_folder_name = "structure_folder_name"
    structure_category_tabs = "structure_category_tabs"
    structure_category_icon = "structure_category_icon"
    structure_context_menu = "structure_context_menu"
    structure_damage_indicator = "structure_damage_indicator"
    structure_health_bar = "structure_health_bar"
    structure_transfer_history = "structure_transfer_history"
    structure_item_tooltip = "structure_item_tooltip"
    structure_attachments_tab = "structure_attachments_tab"
    structure_attachment_slot = "structure_attachment_slot"
    structure_link_indicator = "structure_link_indicator"
    structure_slots_upgrade = "structure_slots_upgrade"


###############################
# CRAFTING STATION ELEMENTS
###############################

class CraftingStationElements(UIElement):
    """Base class for Crafting Station Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Crafting Station Elements"


class CraftingStationBackground(CraftingStationElements):
    """Class for crafting station background elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Crafting Station Background"
        
    # Element definitions
    crafting_station_background = "crafting_station_background"
    crafting_station_title = "crafting_station_title"
    crafting_station_type_icon = "crafting_station_type_icon"
    crafting_station_level_indicator = "crafting_station_level_indicator"
    crafting_station_tab_inventory = "crafting_station_tab_inventory"
    crafting_station_tab_crafting = "crafting_station_tab_crafting"
    crafting_station_tab_engrams = "crafting_station_tab_engrams"
    crafting_station_slots_count = "crafting_station_slots_count"
    crafting_station_weight_indicator = "crafting_station_weight_indicator"
    crafting_station_weight_bar = "crafting_station_weight_bar"
    crafting_station_current_weight = "crafting_station_current_weight"
    crafting_station_max_weight = "crafting_station_max_weight"


class CraftingStationSearch(CraftingStationElements):
    """Class for crafting station search elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Crafting Station Search"
        
    # Element definitions
    crafting_station_search_bar = "crafting_station_search_bar"
    crafting_station_search_results = "crafting_station_search_results"
    crafting_station_close_button = "crafting_station_close_button"
    crafting_station_transfer_all_button = "crafting_station_transfer_all_button"
    crafting_station_sort_button = "crafting_station_sort_button"
    crafting_station_slot_empty = "crafting_station_slot_empty"
    crafting_station_slot_filled = "crafting_station_slot_filled"
    crafting_station_item_icon = "crafting_station_item_icon"
    crafting_station_item_count = "crafting_station_item_count"
    crafting_station_item_durability = "crafting_station_item_durability"


class CraftingStationItems(CraftingStationElements):
    """Class for crafting station item elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Crafting Station Items"
        
    # Element definitions
    crafting_station_crafting_list = "crafting_station_crafting_list"
    crafting_station_crafting_item = "crafting_station_crafting_item"
    crafting_station_blueprint_crafting = "crafting_station_blueprint_crafting"
    crafting_station_materials_required = "crafting_station_materials_required"
    crafting_station_materials_available = "crafting_station_materials_available"
    crafting_station_materials_missing = "crafting_station_materials_missing"
    crafting_station_craft_button = "crafting_station_craft_button"
    crafting_station_craft_all_button = "crafting_station_craft_all_button"
    crafting_station_craft_amount_selector = "crafting_station_craft_amount_selector"


class CraftingStationQueue(CraftingStationElements):
    """Class for crafting station queue elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Crafting Station Queue"
        
    # Element definitions
    crafting_station_crafting_queue = "crafting_station_crafting_queue"
    crafting_station_queue_item = "crafting_station_queue_item"
    crafting_station_progress_bar = "crafting_station_progress_bar"
    crafting_station_time_remaining = "crafting_station_time_remaining"
    crafting_station_speed_multiplier = "crafting_station_speed_multiplier"
    crafting_station_fuel_slot = "crafting_station_fuel_slot"
    crafting_station_fuel_icon = "crafting_station_fuel_icon"
    crafting_station_fuel_level = "crafting_station_fuel_level"
    crafting_station_powered_indicator = "crafting_station_powered_indicator"
    crafting_station_unpowered_indicator = "crafting_station_unpowered_indicator"


class CraftingStationModifiers(CraftingStationElements):
    """Class for crafting station modifier elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Crafting Station Modifiers"
        
    # Element definitions
    crafting_station_blueprint_modifier = "crafting_station_blueprint_modifier"
    crafting_station_skill_modifier = "crafting_station_skill_modifier"
    crafting_station_bulk_craft_toggle = "crafting_station_bulk_craft_toggle"
    crafting_station_resource_pull_button = "crafting_station_resource_pull_button"
    crafting_station_craft_one_button = "crafting_station_craft_one_button"
    crafting_station_pin_recipe_button = "crafting_station_pin_recipe_button"
    crafting_station_unpinned_recipes = "crafting_station_unpinned_recipes"
    crafting_station_pinned_recipes = "crafting_station_pinned_recipes"
    crafting_station_recipe_pin_icon = "crafting_station_recipe_pin_icon"
    crafting_station_queue_cancel_button = "crafting_station_queue_cancel_button"
    crafting_station_quick_access_slots = "crafting_station_quick_access_slots"


class CraftingStationFilters(CraftingStationElements):
    """Class for crafting station filter elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Crafting Station Filters"
        
    # Element definitions
    crafting_station_filter_button = "crafting_station_filter_button"
    crafting_station_filter_dropdown = "crafting_station_filter_dropdown"
    crafting_station_recipe_level_requirement = "crafting_station_recipe_level_requirement"
    crafting_station_recipe_station_requirement = "crafting_station_recipe_station_requirement"
    crafting_station_recipe_dlc_requirement = "crafting_station_recipe_dlc_requirement"
    crafting_station_tek_requirement = "crafting_station_tek_requirement"
    crafting_station_custom_recipe_button = "crafting_station_custom_recipe_button"
    crafting_station_recipe_slider = "crafting_station_recipe_slider"
    crafting_station_recipe_ingredient_slot = "crafting_station_recipe_ingredient_slot"
    crafting_station_recipe_name_field = "crafting_station_recipe_name_field"
    crafting_station_recipe_save_button = "crafting_station_recipe_save_button"
    crafting_station_recipe_load_button = "crafting_station_recipe_load_button"
    crafting_station_recipe_delete_button = "crafting_station_recipe_delete_button"
    crafting_station_recipe_list = "crafting_station_recipe_list"
    crafting_station_recipe_entry = "crafting_station_recipe_entry"


class CraftingStationSlots(CraftingStationElements):
    """Class for crafting station slot elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Crafting Station Slots"
        
    # Element definitions
    crafting_station_input_slots = "crafting_station_input_slots"
    crafting_station_output_slots = "crafting_station_output_slots"
    crafting_station_blueprint_slots = "crafting_station_blueprint_slots"
    crafting_station_ingredient_tooltip = "crafting_station_ingredient_tooltip"
    crafting_station_craft_amount_field = "crafting_station_craft_amount_field"
    crafting_station_learning_progress = "crafting_station_learning_progress"
    crafting_station_durability_crafting = "crafting_station_durability_crafting"
    crafting_station_upgrade_slot = "crafting_station_upgrade_slot"
    crafting_station_augment_slot = "crafting_station_augment_slot"


###############################
# PAINTING INTERFACE ELEMENTS
###############################

class PaintingInterfaceElements(UIElement):
    """Base class for Painting Interface Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Painting Interface Elements"


class PaintingBackground(PaintingInterfaceElements):
    """Class for painting background elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Painting Background"
        
    # Element definitions
    painting_interface_background = "painting_interface_background"
    painting_interface_title = "painting_interface_title"
    painting_interface_canvas = "painting_interface_canvas"
    painting_interface_color_palette = "painting_interface_color_palette"
    painting_interface_color_picker = "painting_interface_color_picker"
    painting_interface_color_preview = "painting_interface_color_preview"


class PaintingColorControls(PaintingInterfaceElements):
    """Class for painting color control elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Color Controls"
        
    # Element definitions
    painting_interface_rgb_sliders = "painting_interface_rgb_sliders"
    painting_interface_red_slider = "painting_interface_red_slider"
    painting_interface_green_slider = "painting_interface_green_slider"
    painting_interface_blue_slider = "painting_interface_blue_slider"
    painting_interface_hue_slider = "painting_interface_hue_slider"
    painting_interface_saturation_slider = "painting_interface_saturation_slider"
    painting_interface_value_slider = "painting_interface_value_slider"
    painting_interface_brush_size_slider = "painting_interface_brush_size_slider"
    painting_interface_brush_preview = "painting_interface_brush_preview"
    painting_interface_opacity_slider = "painting_interface_opacity_slider"


class PaintingTools(PaintingInterfaceElements):
    """Class for painting tool elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Painting Tools"
        
    # Element definitions
    painting_interface_tool_selector = "painting_interface_tool_selector"
    painting_interface_brush_tool = "painting_interface_brush_tool"
    painting_interface_eraser_tool = "painting_interface_eraser_tool"
    painting_interface_dropper_tool = "painting_interface_dropper_tool"
    painting_interface_fill_tool = "painting_interface_fill_tool"
    painting_interface_line_tool = "painting_interface_line_tool"
    painting_interface_rectangle_tool = "painting_interface_rectangle_tool"
    painting_interface_circle_tool = "painting_interface_circle_tool"
    painting_interface_spray_tool = "painting_interface_spray_tool"
    painting_interface_text_tool = "painting_interface_text_tool"
    painting_interface_mirror_tool = "painting_interface_mirror_tool"


class PaintingRegions(PaintingInterfaceElements):
    """Class for painting region elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Painting Regions"
        
    # Element definitions
    painting_interface_region_selector = "painting_interface_region_selector"
    painting_interface_region_1_button = "painting_interface_region_1_button"
    painting_interface_region_2_button = "painting_interface_region_2_button"
    painting_interface_region_3_button = "painting_interface_region_3_button"
    painting_interface_region_4_button = "painting_interface_region_4_button"
    painting_interface_region_5_button = "painting_interface_region_5_button"
    painting_interface_region_6_button = "painting_interface_region_6_button"
    painting_interface_region_indicator = "painting_interface_region_indicator"


class PaintingActions(PaintingInterfaceElements):
    """Class for painting action elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Painting Actions"
        
    # Element definitions
    painting_interface_save_button = "painting_interface_save_button"
    painting_interface_load_button = "painting_interface_load_button"
    painting_interface_clear_button = "painting_interface_clear_button"
    painting_interface_undo_button = "painting_interface_undo_button"
    painting_interface_redo_button = "painting_interface_redo_button"
    painting_interface_saved_paintings = "painting_interface_saved_paintings"
    painting_interface_painting_entry = "painting_interface_painting_entry"
    painting_interface_painting_preview = "painting_interface_painting_preview"
    painting_interface_painting_name = "painting_interface_painting_name"
    painting_interface_rename_button = "painting_interface_rename_button"
    painting_interface_delete_button = "painting_interface_delete_button"
    painting_interface_import_button = "painting_interface_import_button"
    painting_interface_export_button = "painting_interface_export_button"
    painting_interface_copy_button = "painting_interface_copy_button"
    painting_interface_paste_button = "painting_interface_paste_button"


class PaintingCanvasControls(PaintingInterfaceElements):
    """Class for painting canvas control elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Canvas Controls"
        
    # Element definitions
    painting_interface_grid_toggle = "painting_interface_grid_toggle"
    painting_interface_grid_size_slider = "painting_interface_grid_size_slider"
    painting_interface_snap_to_grid_toggle = "painting_interface_snap_to_grid_toggle"
    painting_interface_canvas_zoom_in = "painting_interface_canvas_zoom_in"
    painting_interface_canvas_zoom_out = "painting_interface_canvas_zoom_out"
    painting_interface_canvas_pan_tool = "painting_interface_canvas_pan_tool"
    painting_interface_canvas_reset_view = "painting_interface_canvas_reset_view"


class PaintingBrushSettings(PaintingInterfaceElements):
    """Class for painting brush setting elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Brush Settings"
        
    # Element definitions
    painting_interface_brush_style_selector = "painting_interface_brush_style_selector"
    painting_interface_brush_hardness_slider = "painting_interface_brush_hardness_slider"
    painting_interface_brush_spacing_slider = "painting_interface_brush_spacing_slider"
    painting_interface_brush_angle_slider = "painting_interface_brush_angle_slider"
    painting_interface_brush_preview_window = "painting_interface_brush_preview_window"
    painting_interface_texture_selector = "painting_interface_texture_selector"
    painting_interface_texture_preview = "painting_interface_texture_preview"


class PaintingLayers(PaintingInterfaceElements):
    """Class for painting layer elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Painting Layers"
        
    # Element definitions
    painting_interface_layer_list = "painting_interface_layer_list"
    painting_interface_layer_entry = "painting_interface_layer_entry"
    painting_interface_layer_visibility = "painting_interface_layer_visibility"
    painting_interface_layer_opacity = "painting_interface_layer_opacity"
    painting_interface_add_layer_button = "painting_interface_add_layer_button"
    painting_interface_delete_layer_button = "painting_interface_delete_layer_button"
    painting_interface_merge_layers_button = "painting_interface_merge_layers_button"
    painting_interface_layer_order_up = "painting_interface_layer_order_up"
    painting_interface_layer_order_down = "painting_interface_layer_order_down"
    painting_interface_layer_name = "painting_interface_layer_name"


class PaintingText(PaintingInterfaceElements):
    """Class for painting text elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Painting Text"
        
    # Element definitions
    painting_interface_text_input_field = "painting_interface_text_input_field"
    painting_interface_font_selector = "painting_interface_font_selector"
    painting_interface_font_size_slider = "painting_interface_font_size_slider"
    painting_interface_text_bold_toggle = "painting_interface_text_bold_toggle"
    painting_interface_text_italic_toggle = "painting_interface_text_italic_toggle"
    painting_interface_text_underline_toggle = "painting_interface_text_underline_toggle"
    painting_interface_text_alignment = "painting_interface_text_alignment"


class PaintingTemplates(PaintingInterfaceElements):
    """Class for painting template elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Painting Templates"
        
    # Element definitions
    painting_interface_tribe_logo_template = "painting_interface_tribe_logo_template"
    painting_interface_template_selector = "painting_interface_template_selector"
    painting_interface_flag_template = "painting_interface_flag_template"
    painting_interface_pattern_selector = "painting_interface_pattern_selector"
    painting_interface_apply_template_button = "painting_interface_apply_template_button"
    painting_interface_recent_colors = "painting_interface_recent_colors"
    painting_interface_custom_colors = "painting_interface_custom_colors"
    painting_interface_add_to_custom_button = "painting_interface_add_to_custom_button"


###############################
# CAVE ELEMENTS
###############################

class CaveElements(UIElement):
    """Base class for Cave Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Cave Elements"


class CaveEntranceElements(CaveElements):
    """Class for cave entrance elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Cave Entrance"
        
    # Element definitions
    cave_entrance_marker = "cave_entrance_marker"
    cave_entrance_name_display = "cave_entrance_name_display"
    cave_entrance_difficulty_rating = "cave_entrance_difficulty_rating"
    cave_entrance_level_requirement = "cave_entrance_level_requirement"
    cave_entrance_temperature_warning = "cave_entrance_temperature_warning"
    cave_entrance_resource_indicator = "cave_entrance_resource_indicator"
    cave_entrance_artifact_indicator = "cave_entrance_artifact_indicator"
    cave_entrance_gas_warning = "cave_entrance_gas_warning"
    cave_entrance_water_warning = "cave_entrance_water_warning"
    cave_entrance_dino_restriction = "cave_entrance_dino_restriction"
    cave_entrance_coordinates = "cave_entrance_coordinates"
    cave_entrance_transfer_prompt = "cave_entrance_transfer_prompt"


class CaveHazardElements(CaveElements):
    """Class for cave hazard elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Cave Hazards"
        
    # Element definitions
    cave_gas_meter = "cave_gas_meter"
    cave_gas_warning_icon = "cave_gas_warning_icon"
    cave_gas_mask_indicator = "cave_gas_mask_indicator"
    cave_radiation_meter = "cave_radiation_meter"
    cave_radiation_warning_icon = "cave_radiation_warning_icon"
    cave_radiation_suit_indicator = "cave_radiation_suit_indicator"
    cave_temperature_extreme_indicator = "cave_temperature_extreme_indicator"
    cave_hazard_warning_icon = "cave_hazard_warning_icon"


class CaveArtifactElements(CaveElements):
    """Class for cave artifact elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Cave Artifacts"
        
    # Element definitions
    cave_artifact_glow = "cave_artifact_glow"
    cave_artifact_container = "cave_artifact_container"
    cave_artifact_name = "cave_artifact_name"
    cave_artifact_description = "cave_artifact_description"
    cave_artifact_collect_prompt = "cave_artifact_collect_prompt"
    cave_artifact_collect_button = "cave_artifact_collect_button"
    cave_artifact_cooldown_timer = "cave_artifact_cooldown_timer"
    cave_artifact_inventory_icon = "cave_artifact_inventory_icon"


class CaveNavigationElements(CaveElements):
    """Class for cave navigation elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Cave Navigation"
        
    # Element definitions
    cave_exit_marker = "cave_exit_marker"
    cave_exit_distance = "cave_exit_distance"
    cave_loot_crate_marker = "cave_loot_crate_marker"
    cave_loot_crate_timer = "cave_loot_crate_timer"
    cave_map_overlay = "cave_map_overlay"
    cave_map_corridor = "cave_map_corridor"
    cave_map_chamber = "cave_map_chamber"
    cave_map_water_area = "cave_map_water_area"
    cave_map_hazard_area = "cave_map_hazard_area"
    cave_depth_indicator = "cave_depth_indicator"
    cave_altitude_indicator = "cave_altitude_indicator"


class CaveStructuralElements(CaveElements):
    """Class for cave structural elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Cave Structure"
        
    # Element definitions
    cave_structural_integrity = "cave_structural_integrity"
    cave_ceiling_collapse_warning = "cave_ceiling_collapse_warning"
    cave_stalactite_warning = "cave_stalactite_warning"
    cave_floor_collapse_warning = "cave_floor_collapse_warning"
    cave_enemy_spawner_marker = "cave_enemy_spawner_marker"
    cave_enemy_spawner_active = "cave_enemy_spawner_active"
    cave_enemy_spawner_cooldown = "cave_enemy_spawner_cooldown"


class CaveBossElements(CaveElements):
    """Class for cave boss elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Cave Boss"
        
    # Element definitions
    cave_boss_arena_entrance = "cave_boss_arena_entrance"
    cave_boss_arena_requirements = "cave_boss_arena_requirements"
    cave_boss_tribute_terminal = "cave_boss_tribute_terminal"
    cave_boss_tribute_slots = "cave_boss_tribute_slots"
    cave_boss_activate_button = "cave_boss_activate_button"
    cave_boss_entry_countdown = "cave_boss_entry_countdown"
    cave_artifact_slot = "cave_artifact_slot"
    cave_tribute_slot = "cave_tribute_slot"
    cave_tribute_required_count = "cave_tribute_required_count"


class CaveWaterElements(CaveElements):
    """Class for cave water elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Cave Water"
        
    # Element definitions
    cave_water_depth_indicator = "cave_water_depth_indicator"
    cave_water_current_indicator = "cave_water_current_indicator"
    cave_swim_stamina_indicator = "cave_swim_stamina_indicator"
    cave_oxygen_depletion_warning = "cave_oxygen_depletion_warning"


class CaveTekElements(CaveElements):
    """Class for cave tek elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Cave Tek"
        
    # Element definitions
    cave_tek_door_interface = "cave_tek_door_interface"
    cave_tek_door_unlock_requirements = "cave_tek_door_unlock_requirements"
    cave_note_discovery = "cave_note_discovery"
    cave_note_content = "cave_note_content"
    cave_note_reward = "cave_note_reward"
    cave_note_collection_progress = "cave_note_collection_progress"


class CaveClimbingElements(CaveElements):
    """Class for cave climbing elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Cave Climbing"
        
    # Element definitions
    cave_grapple_point_marker = "cave_grapple_point_marker"
    cave_climbing_pick_point = "cave_climbing_pick_point"
    cave_zipline_anchor_point = "cave_zipline_anchor_point"
    cave_zipline_active = "cave_zipline_active"
    cave_swinging_vine_marker = "cave_swinging_vine_marker"


class CavePuzzleElements(CaveElements):
    """Class for cave puzzle elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Cave Puzzles"
        
    # Element definitions
    cave_puzzle_interface = "cave_puzzle_interface"
    cave_puzzle_clue = "cave_puzzle_clue"
    cave_puzzle_interact_prompt = "cave_puzzle_interact_prompt"
    cave_puzzle_solution_input = "cave_puzzle_solution_input"
    cave_puzzle_success_indicator = "cave_puzzle_success_indicator"
    cave_puzzle_failure_indicator = "cave_puzzle_failure_indicator"
    cave_puzzle_reset_button = "cave_puzzle_reset_button"
    cave_reward_chest_marker = "cave_reward_chest_marker"


class CaveCompletionElements(CaveElements):
    """Class for cave completion elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Cave Completion"
        
    # Element definitions
    cave_completion_reward = "cave_completion_reward"
    cave_completion_timer = "cave_completion_timer"
    cave_record_time = "cave_record_time"
    cave_checkpoint_marker = "cave_checkpoint_marker"
    cave_checkpoint_activated = "cave_checkpoint_activated"


###############################
# CREATURE RIDING ELEMENTS
###############################

class CreatureRidingElements(UIElement):
    """Base class for Creature Riding Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Creature Riding Elements"


class CreatureRidingControls(CreatureRidingElements):
    """Class for creature riding control elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Riding Controls"
        
    # Element definitions
    creature_riding_controls_overlay = "creature_riding_controls_overlay"
    creature_riding_health_bar = "creature_riding_health_bar"
    creature_riding_stamina_bar = "creature_riding_stamina_bar"
    creature_riding_food_bar = "creature_riding_food_bar"
    creature_riding_oxygen_bar = "creature_riding_oxygen_bar"
    creature_riding_weight_bar = "creature_riding_weight_bar"
    creature_riding_xp_bar = "creature_riding_xp_bar"
    creature_riding_name_display = "creature_riding_name_display"
    creature_riding_level_display = "creature_riding_level_display"


class CreatureRidingAbilities(CreatureRidingElements):
    """Class for creature riding ability elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Riding Abilities"
        
    # Element definitions
    creature_riding_special_ability_icon = "creature_riding_special_ability_icon"
    creature_riding_special_ability_cooldown = "creature_riding_special_ability_cooldown"
    creature_riding_special_ability_active = "creature_riding_special_ability_active"
    creature_riding_special_ability_hotkey = "creature_riding_special_ability_hotkey"
    creature_riding_attack_indicator = "creature_riding_attack_indicator"
    creature_riding_secondary_attack_indicator = "creature_riding_secondary_attack_indicator"
    creature_riding_tertiary_attack_indicator = "creature_riding_tertiary_attack_indicator"


class CreatureRidingMovement(CreatureRidingElements):
    """Class for creature riding movement elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Riding Movement"
        
    # Element definitions
    creature_riding_movement_controls = "creature_riding_movement_controls"
    creature_riding_jump_indicator = "creature_riding_jump_indicator"
    creature_riding_sprint_indicator = "creature_riding_sprint_indicator"
    creature_riding_land_indicator = "creature_riding_land_indicator"
    creature_riding_dismount_indicator = "creature_riding_dismount_indicator"
    creature_riding_control_scheme = "creature_riding_control_scheme"
    creature_riding_camera_mode = "creature_riding_camera_mode"
    creature_riding_first_person_view = "creature_riding_first_person_view"
    creature_riding_third_person_view = "creature_riding_third_person_view"


class CreatureRidingMeters(CreatureRidingElements):
    """Class for creature riding meter elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Riding Meters"
        
    # Element definitions
    creature_riding_speed_indicator = "creature_riding_speed_indicator"
    creature_riding_altitude_indicator = "creature_riding_altitude_indicator"
    creature_riding_depth_indicator = "creature_riding_depth_indicator"
    creature_riding_barrel_roll_indicator = "creature_riding_barrel_roll_indicator"
    creature_riding_spin_indicator = "creature_riding_spin_indicator"
    creature_riding_roar_indicator = "creature_riding_roar_indicator"
    creature_riding_bite_indicator = "creature_riding_bite_indicator"
    creature_riding_harvest_indicator = "creature_riding_harvest_indicator"
    creature_riding_charge_indicator = "creature_riding_charge_indicator"
    creature_riding_breath_attack_indicator = "creature_riding_breath_attack_indicator"


class CreatureRidingAttacks(CreatureRidingElements):
    """Class for creature riding attack elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Riding Attacks"
        
    # Element definitions
    creature_riding_flame_indicator = "creature_riding_flame_indicator"
    creature_riding_poison_indicator = "creature_riding_poison_indicator"
    creature_riding_lightning_indicator = "creature_riding_lightning_indicator"
    creature_riding_tek_saddle_element = "creature_riding_tek_saddle_element"
    creature_riding_tek_saddle_shield = "creature_riding_tek_saddle_shield"
    creature_riding_tek_saddle_laser = "creature_riding_tek_saddle_laser"
    creature_riding_tek_saddle_dash = "creature_riding_tek_saddle_dash"
    creature_riding_turret_mode_indicator = "creature_riding_turret_mode_indicator"
    creature_riding_turret_ammo_counter = "creature_riding_turret_ammo_counter"


class CreatureRidingPassengers(CreatureRidingElements):
    """Class for creature riding passenger elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Riding Passengers"
        
    # Element definitions
    creature_riding_passenger_indicator = "creature_riding_passenger_indicator"
    creature_riding_passenger_count = "creature_riding_passenger_count"
    creature_riding_passenger_list = "creature_riding_passenger_list"
    creature_riding_passenger_name = "creature_riding_passenger_name"
    creature_riding_switch_seat_indicator = "creature_riding_switch_seat_indicator"
    creature_riding_platform_structure_count = "creature_riding_platform_structure_count"
    creature_riding_platform_weight = "creature_riding_platform_weight"


class CreatureRidingStatusEffects(CreatureRidingElements):
    """Class for creature riding status effect elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Riding Status Effects"
        
    # Element definitions
    creature_riding_damage_indicator = "creature_riding_damage_indicator"
    creature_riding_creature_buff_icon = "creature_riding_creature_buff_icon"
    creature_riding_pack_bonus_icon = "creature_riding_pack_bonus_icon"
    creature_riding_mate_boost_icon = "creature_riding_mate_boost_icon"
    creature_riding_imprint_bonus_icon = "creature_riding_imprint_bonus_icon"
    creature_riding_fall_damage_warning = "creature_riding_fall_damage_warning"
    creature_riding_torpor_warning = "creature_riding_torpor_warning"
    creature_riding_starving_warning = "creature_riding_starving_warning"
    creature_riding_exhaustion_warning = "creature_riding_exhaustion_warning"
    creature_riding_encumbered_warning = "creature_riding_encumbered_warning"
    creature_riding_injured_warning = "creature_riding_injured_warning"
    creature_riding_drowning_warning = "creature_riding_drowning_warning"
    creature_riding_temperature_warning = "creature_riding_temperature_warning"
    creature_riding_territory_warning = "creature_riding_territory_warning"


class CreatureRidingAdditionalInfo(CreatureRidingElements):
    """Class for creature riding additional info elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Additional Info"
        
    # Element definitions
    creature_riding_attack_cooldown = "creature_riding_attack_cooldown"
    creature_riding_gathering_efficiency = "creature_riding_gathering_efficiency"
    creature_riding_resource_gathered_popup = "creature_riding_resource_gathered_popup"
    creature_riding_experience_gained_popup = "creature_riding_experience_gained_popup"
    creature_riding_whistlewheel_indicator = "creature_riding_whistlewheel_indicator"
    creature_riding_behavior_indicator = "creature_riding_behavior_indicator"
    creature_riding_follow_distance_indicator = "creature_riding_follow_distance_indicator"
    creature_riding_inventory_access_indicator = "creature_riding_inventory_access_indicator"


###############################
# LOOT CRATE ELEMENTS
###############################

class LootCrateElements(UIElement):
    """Base class for Loot Crate Elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.category = "Loot Crate Elements"


class LootCrateBackground(LootCrateElements):
    """Class for loot crate background elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Loot Crate Background"
        
    # Element definitions
    loot_crate_background = "loot_crate_background"
    loot_crate_title = "loot_crate_title"
    loot_crate_color_indicator = "loot_crate_color_indicator"
    loot_crate_timer = "loot_crate_timer"
    loot_crate_slot_empty = "loot_crate_slot_empty"
    loot_crate_slot_filled = "loot_crate_slot_filled"
    loot_crate_item_icon = "loot_crate_item_icon"
    loot_crate_item_name = "loot_crate_item_name"
    loot_crate_item_count = "loot_crate_item_count"
    loot_crate_item_quality = "loot_crate_item_quality"
    loot_crate_item_blueprint_icon = "loot_crate_item_blueprint_icon"


class LootCrateControls(LootCrateElements):
    """Class for loot crate control elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Loot Crate Controls"
        
    # Element definitions
    loot_crate_close_button = "loot_crate_close_button"
    loot_crate_take_all_button = "loot_crate_take_all_button"
    loot_crate_transfer_all_button = "loot_crate_transfer_all_button"
    loot_crate_sort_button = "loot_crate_sort_button"
    loot_crate_filter_button = "loot_crate_filter_button"
    loot_crate_search_bar = "loot_crate_search_bar"


class LootCrateRarity(LootCrateElements):
    """Class for loot crate rarity elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Loot Crate Rarity"
        
    # Element definitions
    loot_crate_rarity_white = "loot_crate_rarity_white"
    loot_crate_rarity_green = "loot_crate_rarity_green"
    loot_crate_rarity_blue = "loot_crate_rarity_blue"
    loot_crate_rarity_purple = "loot_crate_rarity_purple"
    loot_crate_rarity_yellow = "loot_crate_rarity_yellow"
    loot_crate_rarity_red = "loot_crate_rarity_red"


class LootCrateUnlock(LootCrateElements):
    """Class for loot crate unlock elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Loot Crate Unlock"
        
    # Element definitions
    loot_crate_locked_indicator = "loot_crate_locked_indicator"
    loot_crate_unlock_prompt = "loot_crate_unlock_prompt"
    loot_crate_pin_code_field = "loot_crate_pin_code_field"
    loot_crate_unlock_button = "loot_crate_unlock_button"
    loot_crate_tribute_required = "loot_crate_tribute_required"
    loot_crate_tribute_slot = "loot_crate_tribute_slot"
    loot_crate_tribute_item = "loot_crate_tribute_item"
    loot_crate_tribute_count = "loot_crate_tribute_count"


class LootCrateEffects(LootCrateElements):
    """Class for loot crate effect elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Loot Crate Effects"
        
    # Element definitions
    loot_crate_beacon_light = "loot_crate_beacon_light"
    loot_crate_beacon_ring = "loot_crate_beacon_ring"
    loot_crate_drop_location = "loot_crate_drop_location"
    loot_crate_drop_altitude = "loot_crate_drop_altitude"
    loot_crate_landing_countdown = "loot_crate_landing_countdown"
    loot_crate_available_notification = "loot_crate_available_notification"
    loot_crate_map_marker = "loot_crate_map_marker"
    loot_crate_coordinates_display = "loot_crate_coordinates_display"


class LootCrateInfo(LootCrateElements):
    """Class for loot crate info elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Loot Crate Info"
        
    # Element definitions
    loot_crate_contents_preview = "loot_crate_contents_preview"
    loot_crate_level_requirement = "loot_crate_level_requirement"
    loot_crate_tribe_access_indicator = "loot_crate_tribe_access_indicator"
    loot_crate_first_open_bonus = "loot_crate_first_open_bonus"
    loot_crate_item_glow_effect = "loot_crate_item_glow_effect"
    loot_crate_mission_reward = "loot_crate_mission_reward"
    loot_crate_mission_tier = "loot_crate_mission_tier"
    loot_crate_tribe_lock_timer = "loot_crate_tribe_lock_timer"
    loot_crate_unlock_reward = "loot_crate_unlock_reward"


class LootCrateSpecial(LootCrateElements):
    """Class for loot crate special elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Loot Crate Special"
        
    # Element definitions
    loot_crate_special_event_indicator = "loot_crate_special_event_indicator"
    loot_crate_holiday_theme = "loot_crate_holiday_theme"
    loot_crate_tek_variant = "loot_crate_tek_variant"
    loot_crate_genesis_variant = "loot_crate_genesis_variant"
    loot_crate_cave_variant = "loot_crate_cave_variant"
    loot_crate_underwater_variant = "loot_crate_underwater_variant"
    loot_crate_artifact_container = "loot_crate_artifact_container"
    loot_crate_orbital_supply_drop = "loot_crate_orbital_supply_drop"
    loot_crate_gacha_crystal = "loot_crate_gacha_crystal"
    loot_crate_already_looted = "loot_crate_already_looted"


class LootCrateWaveDefense(LootCrateElements):
    """Class for loot crate wave defense elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Wave Defense"
        
    # Element definitions
    loot_crate_nearby_enemy_warning = "loot_crate_nearby_enemy_warning"
    loot_crate_nearby_allies = "loot_crate_nearby_allies"
    loot_crate_wave_defense_status = "loot_crate_wave_defense_status"
    loot_crate_wave_countdown = "loot_crate_wave_countdown"
    loot_crate_defense_success_bar = "loot_crate_defense_success_bar"
    loot_crate_wave_counter = "loot_crate_wave_counter"
    loot_crate_remaining_enemies = "loot_crate_remaining_enemies"
    loot_crate_deploy_shield_button = "loot_crate_deploy_shield_button"
    loot_crate_repair_shield_button = "loot_crate_repair_shield_button"
    loot_crate_shield_health = "loot_crate_shield_health"
    loot_crate_terminal_health = "loot_crate_terminal_health"
    loot_crate_element_reward = "loot_crate_element_reward"


class LootCrateRewards(LootCrateElements):
    """Class for loot crate reward elements"""
    def __init__(self, name, color="#ffffff", element_type="rectangle", attributes=None):
        super().__init__(name, color, element_type, attributes)
        self.subcategory = "Loot Crate Rewards"
        
    # Element definitions
    loot_crate_duplicate_item_notification = "loot_crate_duplicate_item_notification"
    loot_crate_item_compare = "loot_crate_item_compare"
    loot_crate_claim_button = "loot_crate_claim_button"
    loot_crate_discard_button = "loot_crate_discard_button"
    loot_crate_item_tooltip = "loot_crate_item_tooltip"


###############################
# HELPER FUNCTIONS
###############################

def get_ui_element_class(element_name):
    """
    Get the appropriate UI element class based on the element name
    
    Args:
        element_name (str): Name of the UI element
        
    Returns:
        class: The UI element class that should handle this element
    """
    element_name = element_name.lower()
    
    # Check for HUD elements
    if element_name.startswith("hud_health") or "healthbar" in element_name:
        return HUDHealthIndicators
    elif element_name.startswith("hud_stamina") or "staminabar" in element_name:
        return HUDStaminaIndicators
    elif element_name.startswith("hud_food") or "foodbar" in element_name:
        return HUDFoodIndicators
    elif element_name.startswith("hud_water") or "waterbar" in element_name:
        return HUDWaterIndicators
    elif element_name.startswith("hud_oxygen") or "oxygenbar" in element_name:
        return HUDOxygenIndicators
    elif element_name.startswith("hud_weight") or "weightbar" in element_name:
        return HUDWeightIndicators
    elif element_name.startswith("hud_torpidity") or "torpiditybar" in element_name:
        return HUDTorpidityIndicators
    elif element_name.startswith("hud_xp") or "levelup" in element_name:
        return HUDExperienceIndicators
    elif element_name.startswith("hud_compass") or "gps" in element_name:
        return HUDCompassElements
    elif element_name.startswith("hud_temperature") or "temperature" in element_name:
        return HUDTemperatureIndicators
    elif element_name.startswith("hud_buff") and not "debuff" in element_name:
        return HUDBuffIndicators
    elif element_name.startswith("hud_debuff") or ("hud_buff" in element_name and "disease" in element_name):
        return HUDDebuffIndicators
    elif element_name.startswith("hud_chat") or "tribe_log" in element_name:
        return HUDChatElements
    elif element_name.startswith("hud_crosshair"):
        return HUDCrosshairElements
    elif "prompt" in element_name:
        return HUDInteractionPrompts
    elif "wheel" in element_name:
        return HUDWheelMenus
    elif "waypoint" in element_name or "marker" in element_name:
        return HUDWaypointElements
    elif "name_tag" in element_name:
        return HUDNameTags
    elif "warning" in element_name:
        return HUDWarningElements
    elif "tek_visor" in element_name or "tek_punch" in element_name:
        return HUDTekElements
    elif "overlay" in element_name:
        return HUDOverlayElements
    elif element_name.startswith("hud_"):
        return HUDElements
    
    # Check for Quickbar elements
    elif element_name.startswith("quickbar_slot"):
        return QuickbarSlots
    elif element_name.startswith("quickbar_item") or element_name.startswith("quickbar_weapon") or element_name == "quickbar_selector":
        return QuickbarIndicators
    elif element_name.startswith("quickbar_hotkey"):
        return QuickbarHotkeys
    elif element_name.startswith("quickbar"):
        return QuickbarElements
    
    # Check for Inventory elements
    elif element_name.startswith("inventory_background") or element_name.startswith("inventory_player_region") or element_name.startswith("inventory_entity_region"):
        return InventoryPanels
    elif element_name.startswith("inventory_player_slot") or element_name.startswith("inventory_item_"):
        return InventorySlots
    elif element_name.startswith("inventory_item_quality"):
        return InventoryQualityIndicators
    elif element_name.startswith("inventory_item_blueprint") or element_name.startswith("inventory_item_equipped") or element_name.startswith("inventory_item_favorite"):
        return InventoryItemSpecials
    elif element_name.startswith("inventory_search") or element_name.startswith("inventory_transfer") or element_name.startswith("inventory_weight"):
        return InventoryControls
    elif element_name.startswith("inventory_armor_slot"):
        return InventoryArmorSlots
    elif element_name.startswith("inventory_item_tooltip"):
        return InventoryTooltips
    elif element_name.startswith("inventory_item_context"):
        return InventoryContextMenu
    elif element_name.startswith("inventory_folder"):
        return InventoryFolders
    elif element_name.startswith("inventory_entity"):
        return EntityInventoryElements
    elif element_name.startswith("inventory_terminal") or element_name.startswith("inventory_beacon") or element_name.startswith("inventory_obelisk"):
        return SpecialInventoryElements
    elif element_name.startswith("inventory"):
        return InventoryElements
    
    # Check for Tab elements
    elif element_name.startswith("tab_inventory"):
        return InventoryTabs
    elif element_name.startswith("tab_tribe") or element_name.startswith("tab_stats") or element_name.startswith("tab_notes") or element_name.startswith("tab_map"):
        return CharacterTabs
    elif element_name.startswith("tab_dino"):
        return DinoTabs
    elif element_name.startswith("tab_spawn") or element_name.startswith("tab_tribute") or element_name.startswith("tab_upload") or element_name.startswith("tab_download"):
        return TerminalTabs
    elif element_name.startswith("tab_"):
        return TabElements
    
    # Check for Crafting elements
    elif element_name.startswith("crafting_item_panel") or element_name.startswith("crafting_item_icon") or element_name.startswith("crafting_item_name"):
        return CraftingPanels
    elif element_name.startswith("crafting_button") or element_name.startswith("crafting_blueprint_header"):
        return CraftingControls
    elif element_name.startswith("crafting_queue"):
        return CraftingQueue
    elif element_name.startswith("crafting_station"):
        return CraftingStationInfo
    elif element_name.startswith("crafting_search") or element_name.startswith("crafting_filter"):
        return CraftingFilters
    elif element_name.startswith("crafting_sort"):
        return CraftingSorting
    elif element_name.startswith("crafting_skill") or element_name.startswith("crafting_blueprint_quality"):
        return CraftingBoosts
    elif element_name.startswith("crafting_engram") or element_name.startswith("crafting_level"):
        return CraftingRequirements
    elif "_cost" in element_name and element_name.startswith("crafting_"):
        return CraftingResourceCosts
    elif element_name.startswith("crafting") or element_name.startswith("craft_"):
        return CraftingElements
    
    # Check for Engram elements
    elif element_name.startswith("engram_icon"):
        return EngramIcons
    elif element_name.startswith("engram_points"):
        return EngramPoints
    elif element_name.startswith("engram_learn_button") or element_name.startswith("engram_auto_unlock"):
        return EngramControls
    elif element_name.startswith("engram_item"):
        return EngramItems
    elif element_name.startswith("engram_search"):
        return EngramSearch
    elif element_name.startswith("engram_category"):
        return EngramCategories
    elif element_name.startswith("engram_tooltip"):
        return EngramTooltips
    elif element_name.startswith("engram_") and ("_icon" in element_name):
        return EngramDLCIcons
    elif element_name.startswith("engram_scroll") or element_name.startswith("engram_tech_tier") or element_name.startswith("engram_level_marker"):
        return EngramNavigation
    elif element_name.startswith("engram"):
        return EngramElements
    
    # Check for Dino elements
    elif element_name.startswith("dino_inventory") or element_name.startswith("dino_health_bar") or element_name.startswith("dino_stamina"):
        return DinoInventory
    elif element_name.startswith("dino_behavior"):
        return DinoBehavior
    elif element_name.startswith("dino_targeting") or element_name.startswith("dino_mating") or element_name.startswith("dino_wandering"):
        return DinoTargeting
    elif element_name.startswith("dino_stats_") or element_name.startswith("dino_stat_"):
        return DinoStats
    elif element_name.startswith("dino_imprinting"):
        return DinoImprinting
    elif element_name.startswith("dino_special_ability") or element_name.startswith("dino_pack_buff") or element_name.startswith("dino_mate_boost"):
        return DinoAbilities
    elif element_name.startswith("taming_"):
        return TamingElements
    elif element_name.startswith("dino_"):
        return DinoElements
    
    # Check for Structure elements
    elif element_name.startswith("structure_name") or element_name.startswith("structure_inventory") or element_name.startswith("structure_power_indicator"):
        return StructureInfo
    elif element_name.startswith("structure_options") or element_name.startswith("structure_demolish_option") or element_name.startswith("structure_pickup_option"):
        return StructureOptions
    elif element_name.startswith("structure_snap_points") or element_name.startswith("structure_placement"):
        return StructurePlacement
    elif element_name.startswith("structure_powered") or element_name.startswith("generator_fuel") or element_name.startswith("electrical_wire"):
        return StructurePower
    elif element_name.startswith("structure_background") or element_name.startswith("structure_title") or element_name.startswith("structure_type_icon"):
        return StructureBackground
    elif element_name.startswith("structure_search") or element_name.startswith("structure_close_button") or element_name.startswith("structure_transfer"):
        return StructureSearch
    elif element_name.startswith("structure_slot") or element_name.startswith("structure_item"):
        return StructureSlots
    elif element_name.startswith("structure_scroll"):
        return StructureScrolling
    elif element_name.startswith("structure_tribe_access") or element_name.startswith("structure_public_access") or element_name.startswith("structure_remote_access"):
        return StructureAccess
    elif element_name.startswith("structure_rename") or element_name.startswith("structure_destroy") or element_name.startswith("structure_repair"):
        return StructureManagement
    elif element_name.startswith("structure_folder"):
        return StructureFolders
    elif element_name.startswith("structure_"):
        return StructureElements
    
    # Check for Map elements
    elif element_name.startswith("map_background") or element_name.startswith("map_grid"):
        return MapBackground
    elif element_name.startswith("map_player_marker") or element_name.startswith("map_tribe_member") or element_name.startswith("map_tamed_dino"):
        return MapMarkers
    elif element_name.startswith("map_base_marker") or element_name.startswith("map_waypoint_marker"):
        return MapBaseMarkers
    elif element_name.startswith("map_obelisk_marker") or element_name.startswith("map_terminal_marker") or element_name.startswith("map_cave_entrance"):
        return MapObeliskMarkers
    elif element_name.startswith("map_beacon_marker"):
        return MapBeaconMarkers
    elif element_name.startswith("map_mission_marker") or element_name.startswith("map_boss_terminal") or element_name.startswith("map_supply_drop"):
        return MapSpecialMarkers
    elif element_name.startswith("map_ocean_depth") or element_name.startswith("map_shallow_water") or element_name.startswith("map_deep_water"):
        return MapWaterElements
    elif element_name.startswith("map_snow_biome") or element_name.startswith("map_desert_biome") or element_name.startswith("map_redwood_biome"):
        return MapBiomeIndicators
    elif element_name.startswith("map_coordinates") or element_name.startswith("map_latitude") or element_name.startswith("map_longitude"):
        return MapCoordinates
    elif element_name.startswith("map_zoom") or element_name.startswith("map_filter") or element_name.startswith("map_place_waypoint"):
        return MapControls
    elif element_name.startswith("map_region_name") or element_name.startswith("map_weather") or element_name.startswith("map_fog_of_war"):
        return MapAdditionalInfo
    elif element_name.startswith("map_minimap"):
        return MinimapElements
    elif element_name.startswith("map_"):
        return MapElements
    
    # Check for Alert elements
    elif element_name.startswith("alert_starvation") or element_name.startswith("alert_dehydration") or element_name.startswith("alert_encumbered"):
        return HealthAlerts
    elif element_name.startswith("alert_level_up") or element_name.startswith("alert_tribe_message") or element_name.startswith("alert_death_message"):
        return NotificationAlerts
    elif element_name.startswith("alert_item_broken") or element_name.startswith("alert_creature_starving") or element_name.startswith("alert_creature_dying"):
        return WarningAlerts
    elif element_name.startswith("alert_"):
        return AlertElements
    
    # Check for Player Stats elements
    elif element_name.startswith("player_stats_background") or element_name.startswith("player_stats_header"):
        return PlayerStatsPanels
    elif element_name.startswith("player_stat_health"):
        return PlayerHealthStats
    elif element_name.startswith("player_stat_stamina"):
        return PlayerStaminaStats
    elif element_name.startswith("player_stat_oxygen"):
        return PlayerOxygenStats
    elif element_name.startswith("player_stat_food"):
        return PlayerFoodStats
    elif element_name.startswith("player_stat_water"):
        return PlayerWaterStats
    elif element_name.startswith("player_stat_weight"):
        return PlayerWeightStats
    elif element_name.startswith("player_stat_melee"):
        return PlayerMeleeStats
    elif element_name.startswith("player_stat_speed"):
        return PlayerSpeedStats
    elif element_name.startswith("player_stat_fortitude"):
        return PlayerFortitudeStats
    elif element_name.startswith("player_stat_crafting"):
        return PlayerCraftingStats
    elif element_name.startswith("player_level") or element_name.startswith("player_xp") or element_name.startswith("player_levelup"):
        return PlayerLevelElements
    elif element_name.startswith("player_tek_implant") or element_name.startswith("player_mutation_counter") or element_name.startswith("player_pheromone"):
        return PlayerSpecialStats
    elif element_name.startswith("player_stat_"):
        return PlayerStatsElements
    
    # Check for Tribe elements
    elif element_name.startswith("tribe_management_background") or element_name.startswith("tribe_management_header") or element_name.startswith("tribe_name_display"):
        return TribeManagementPanels
    elif element_name.startswith("tribe_member_list") or element_name.startswith("tribe_member_entry") or element_name.startswith("tribe_member_name"):
        return TribeMembers
    elif element_name.startswith("tribe_log"):
        return TribeLog
    elif element_name.startswith("tribe_alliance"):
        return TribeAlliances
    elif element_name.startswith("tribe_governance") or element_name.startswith("tribe_rank_management") or element_name.startswith("tribe_rank_entry"):
        return TribeGovernance
    elif element_name.startswith("tribe_permission"):
        return TribePermissions
    elif element_name.startswith("tribe_pincode") or element_name.startswith("tribe_tame_claim") or element_name.startswith("tribe_structure_ownership"):
        return TribeSettings
    elif element_name.startswith("tribe_taxes") or element_name.startswith("tribe_stats_panel") or element_name.startswith("tribe_territory_map"):
        return TribeAdvancedSettings
    elif element_name.startswith("tribe_"):
        return TribeElements
    
    # Check for Structure Placement elements
    elif element_name.startswith("structure_placement_valid") or element_name.startswith("structure_placement_invalid") or element_name.startswith("structure_placement_distance"):
        return PlacementValidation
    elif element_name.startswith("structure_placement_rotation") or element_name.startswith("structure_placement_radius") or element_name.startswith("structure_placement_ceiling_height"):
        return PlacementControls
    elif element_name.startswith("structure_placement_resource") or element_name.startswith("structure_placement_structure_limit") or element_name.startswith("structure_placement_platform_limit"):
        return PlacementResources
    elif element_name.startswith("structure_placement_pickup_timer") or element_name.startswith("structure_placement_demolish_refund") or element_name.startswith("structure_placement_element_range"):
        return PlacementTimers
    elif element_name.startswith("structure_placement_greenhouse") or element_name.startswith("structure_placement_crop_plot") or element_name.startswith("structure_placement_temperature_effect"):
        return PlacementEnvironment
    elif element_name.startswith("structure_placement_dino_gate") or element_name.startswith("structure_placement_ceiling_stability") or element_name.startswith("structure_placement_foundation_stability"):
        return PlacementSpecials
    elif element_name.startswith("structure_placement_"):
        return StructurePlacementElements
    
    # Check for Electrical System elements
    elif element_name.startswith("electrical_system_background") or element_name.startswith("electrical_system_title") or element_name.startswith("electrical_system_powered_indicator"):
        return ElectricalInterface
    elif element_name.startswith("electrical_system_device_list") or element_name.startswith("electrical_system_device_entry") or element_name.startswith("electrical_system_device_name"):
        return ElectricalDevices
    elif element_name.startswith("electrical_system_circuit"):
        return ElectricalCircuits
    elif element_name.startswith("electrical_system_generator"):
        return ElectricalGenerators
    elif element_name.startswith("electrical_system_auto_power") or element_name.startswith("electrical_system_timer") or element_name.startswith("electrical_system_schedule"):
        return ElectricalSettings
    elif element_name.startswith("electrical_system_power_grid") or element_name.startswith("electrical_system_grid_segment") or element_name.startswith("electrical_system_redundancy"):
        return ElectricalGrid
    elif element_name.startswith("electrical_system_device_priority") or element_name.startswith("electrical_system_unconnected") or element_name.startswith("electrical_system_device_hover"):
        return ElectricalAdvanced
    elif element_name.startswith("electrical_system_energy") or element_name.startswith("electrical_system_peak_usage") or element_name.startswith("electrical_system_power_fluctuation"):
        return ElectricalMonitoring
    elif element_name.startswith("electrical_system_"):
        return ElectricalSystemElements
    
    # Check for Transfer Interface elements
    elif element_name.startswith("transfer_interface_background") or element_name.startswith("transfer_interface_title"):
        return TransferBackground
    elif element_name.startswith("transfer_interface_server_list") or element_name.startswith("transfer_interface_server_entry") or element_name.startswith("transfer_interface_server_name"):
        return TransferServerList
    elif element_name.startswith("transfer_interface_server_filter") or element_name.startswith("transfer_interface_search") or element_name.startswith("transfer_interface_sort"):
        return TransferSearch
    elif element_name.startswith("transfer_interface_join_button") or element_name.startswith("transfer_interface_cancel_button") or element_name.startswith("transfer_interface_select_button"):
        return TransferButtons
    elif element_name.startswith("transfer_interface_player_tab") or element_name.startswith("transfer_interface_item_tab") or element_name.startswith("transfer_interface_dino_tab"):
        return TransferTabs
    elif element_name.startswith("transfer_interface_player_select") or element_name.startswith("transfer_interface_player_entry") or element_name.startswith("transfer_interface_player_name"):
        return TransferPlayers
    elif element_name.startswith("transfer_interface_item_storage") or element_name.startswith("transfer_interface_item_slot") or element_name.startswith("transfer_interface_item_icon"):
        return TransferItems
    elif element_name.startswith("transfer_interface_dino_storage") or element_name.startswith("transfer_interface_dino_entry") or element_name.startswith("transfer_interface_dino_icon"):
        return TransferDinos
    elif element_name.startswith("transfer_interface_transfer_cooldown") or element_name.startswith("transfer_interface_cooldown_icon") or element_name.startswith("transfer_interface_storage_slots"):
        return TransferStatus
    elif element_name.startswith("transfer_interface_connection_status") or element_name.startswith("transfer_interface_transfer_progress") or element_name.startswith("transfer_interface_transfer_error"):
        return TransferConfirmation
    elif element_name.startswith("transfer_interface_cluster_filter") or element_name.startswith("transfer_interface_official_filter") or element_name.startswith("transfer_interface_unofficial_filter"):
        return TransferFilters
    elif element_name.startswith("transfer_interface_server_info") or element_name.startswith("transfer_interface_map_indicator") or element_name.startswith("transfer_interface_rates_display"):
        return TransferServerInfo
    elif element_name.startswith("transfer_interface_"):
        return TransferInterfaceElements
    
    # Check for Settings Menu elements
    elif element_name.startswith("settings_menu_background") or element_name.startswith("settings_menu_title"):
        return SettingsBackground
    elif element_name.startswith("settings_category_tabs") or element_name.startswith("settings_tab_"):
        return SettingsTabs
    elif element_name.startswith("settings_section_header") or element_name.startswith("settings_option_row") or element_name.startswith("settings_option_name"):
        return SettingsSections
    elif element_name.startswith("settings_slider") or element_name.startswith("settings_dropdown") or element_name.startswith("settings_checkbox"):
        return SettingsControls
    elif element_name.startswith("settings_reset_button") or element_name.startswith("settings_apply_button") or element_name.startswith("settings_save_button"):
        return SettingsActions
    elif element_name.startswith("settings_"):
        return SettingsMenuElements
    
    # Check for Holiday Event elements
    elif element_name.startswith("holiday_event_interface") or element_name.startswith("easter_egg_hunt_tracker") or element_name.startswith("summer_bash_interface"):
        return HolidayInterfaces
    elif element_name.startswith("genesis_race_timer") or element_name.startswith("genesis_hunt_tracker") or element_name.startswith("genesis_fishing_meter"):
        return GenesisMissions
    elif element_name.startswith("holiday_") or element_name.startswith("easter_") or element_name.startswith("summer_bash") or element_name.startswith("fear_evolved") or element_name.startswith("winter_wonderland") or element_name.startswith("valentines_day") or element_name.startswith("eggcellent_adventure"):
        return HolidayEventElements
    
    # Check for Tek elements
    elif element_name.startswith("tek_generator_interface") or element_name.startswith("tek_crop_plot_interface") or element_name.startswith("creature_camera_view"):
        return TekInterfaces
    elif element_name.startswith("aquatic_tames_oxygen_interface") or element_name.startswith("astrodelphis_energy") or element_name.startswith("noglin_brain_jack_interface"):
        return TekCreatureUI
    elif element_name.startswith("tek_element_icon") or element_name.startswith("tek_element_count") or element_name.startswith("tek_element_shard_icon"):
        return TekResources
    elif element_name.startswith("tek_transmitter_interface") or element_name.startswith("tek_transmitter_upload_tab") or element_name.startswith("tek_transmitter_download_tab"):
        return TekTransmitter
    elif element_name.startswith("tek_teleporter_interface") or element_name.startswith("tek_teleporter_location_list") or element_name.startswith("tek_teleporter_location_entry"):
        return TekTeleporter
    elif element_name.startswith("tek_replicator_interface") or element_name.startswith("tek_replicator_crafting_tab") or element_name.startswith("tek_replicator_inventory_tab"):
        return TekAdvancedStructures
    elif element_name.startswith("tek_dedicated_storage") or element_name.startswith("tek_dedicated_storage_type") or element_name.startswith("tek_dedicated_storage_count"):
        return TekStorage
    elif element_name.startswith("tek_generator_interface") or element_name.startswith("tek_generator_range_display") or element_name.startswith("tek_generator_element_level"):
        return TekGenerator
    elif element_name.startswith("tek_shield_interface") or element_name.startswith("tek_shield_range_display") or element_name.startswith("tek_shield_strength_display"):
        return TekShield
    elif element_name.startswith("tek_trough_interface") or element_name.startswith("tek_trough_food_list") or element_name.startswith("tek_trough_range_display"):
        return TekTrough
    elif element_name.startswith("tek_hover_skiff_controls") or element_name.startswith("tek_hover_skiff_altitude") or element_name.startswith("tek_hover_skiff_speed"):
        return TekVehicles
    elif element_name.startswith("tek_sensor_interface") or element_name.startswith("tek_sensor_range_setting") or element_name.startswith("tek_sensor_mode_setting"):
        return TekSensor
    elif element_name.startswith("tek_visor_overlay") or element_name.startswith("tek_visor_mode_selector") or element_name.startswith("tek_visor_night_vision"):
        return TekVisor
    elif element_name.startswith("tek_gauntlet") or element_name.startswith("tek_boots") or element_name.startswith("tek_chestpiece"):
        return TekArmor
    elif element_name.startswith("tek_rifle") or element_name.startswith("tek_grenade"):
        return TekWeapons
    elif element_name.startswith("tek_stryder") or element_name.startswith("tek_megachelon") or element_name.startswith("tek_enforce"):
        return TekCreatures
    elif element_name.startswith("tek_"):
        return TekElements
    
    # Check for Boss Arena elements
    elif element_name.startswith("boss_arena_entry_interface") or element_name.startswith("boss_arena_tribute_slots") or element_name.startswith("boss_arena_artifact_slots"):
        return BossEntryInterface
    elif element_name.startswith("boss_fight_timer") or element_name.startswith("boss_fight_player_list") or element_name.startswith("boss_fight_player_entry"):
        return BossFightElements
    elif element_name.startswith("boss_attack_warning") or element_name.startswith("boss_special_attack_warning") or element_name.startswith("boss_minion_spawned_alert"):
        return BossAttackWarnings
    elif element_name.startswith("boss_arena_exit_timer") or element_name.startswith("boss_arena_teleport_indicator") or element_name.startswith("boss_arena_item_reward_list"):
        return BossArenaExit
    elif element_name.startswith("boss_artifact_collection_notification") or element_name.startswith("boss_arena_tek_suit_activation") or element_name.startswith("boss_arena_element_reward"):
        return BossArtifactElements
    elif element_name.startswith("boss_arena_difficulty_icon") or element_name.startswith("boss_arena_previous_record") or element_name.startswith("boss_arena_tribe_limit"):
        return BossDifficultyElements
    elif element_name.startswith("boss_") or element_name.startswith("boss_arena_"):
        return BossArenaElements
    
    # Check for Event Interface elements
    elif element_name.startswith("event_interface_background") or element_name.startswith("event_title_header") or element_name.startswith("event_description_text"):
        return EventBackground
    elif element_name.startswith("event_objective_list") or element_name.startswith("event_objective_entry") or element_name.startswith("event_objective_complete_marker"):
        return EventObjectives
    elif element_name.startswith("event_leaderboard") or element_name.startswith("event_leaderboard_entry") or element_name.startswith("event_participation_count"):
        return EventLeaderboard
    elif element_name.startswith("event_start_button") or element_name.startswith("event_cancel_button") or element_name.startswith("event_restart_button"):
        return EventControls
    elif element_name.startswith("event_"):
        return EventInterfaceElements
    
    # Check for Death Screen elements
    elif element_name.startswith("death_screen_background") or element_name.startswith("death_screen_title") or element_name.startswith("death_message_display"):
        return DeathScreenBackground
    elif element_name.startswith("death_respawn_timer") or element_name.startswith("death_location_coordinates") or element_name.startswith("death_map_marker"):
        return DeathRespawnElements
    elif element_name.startswith("death_respawn_location_list") or element_name.startswith("death_respawn_location_entry") or element_name.startswith("death_respawn_bed_entry"):
        return DeathRespawnLocations
    elif element_name.startswith("death_body_decay_timer") or element_name.startswith("death_tribe_corpse_marker") or element_name.startswith("death_tribe_corpse_name"):
        return DeathCorpseElements
    elif element_name.startswith("death_obituary_text") or element_name.startswith("death_killed_by_display") or element_name.startswith("death_tribe_bed_category"):
        return DeathDetailsElements
    elif element_name.startswith("death_screen_close_button") or element_name.startswith("death_item_recovery_info") or element_name.startswith("death_xp_penalty_display"):
        return DeathScreenControls
    elif element_name.startswith("death_environment_killed") or element_name.startswith("death_player_killed") or element_name.startswith("death_creature_killed"):
        return DeathCauseElements
    elif element_name.startswith("death_"):
        return DeathScreenElements
    
    # Check for Breeding Interface elements
    elif element_name.startswith("breeding_interface_background") or element_name.startswith("breeding_interface_header") or element_name.startswith("breeding_male_stats_panel"):
        return BreedingBackground
    elif element_name.startswith("breeding_enable_mating_button") or element_name.startswith("breeding_disable_mating_button") or element_name.startswith("breeding_mating_progress_bar"):
        return BreedingControls
    elif element_name.startswith("breeding_egg_incubation") or element_name.startswith("breeding_egg_temperature") or element_name.startswith("breeding_egg_health"):
        return BreedingEggs
    elif element_name.startswith("breeding_mutation_indicator") or element_name.startswith("breeding_mutation_counter") or element_name.startswith("breeding_baby_claim_prompt"):
        return BreedingMutations
    elif element_name.startswith("breeding_baby_imprint_status") or element_name.startswith("breeding_imprint_progress_bar") or element_name.startswith("breeding_imprint_quality"):
        return BreedingImprinting
    elif element_name.startswith("breeding_maturation_progress_bar") or element_name.startswith("breeding_maturation_timer") or element_name.startswith("breeding_food_consumption_rate"):
        return BreedingMaturation
    elif element_name.startswith("breeding_ancestry_button") or element_name.startswith("breeding_ancestry_tree") or element_name.startswith("breeding_ancestry_entry"):
        return BreedingAncestry
    elif element_name.startswith("breeding_mate_boost_indicator") or element_name.startswith("breeding_creature_gender_icon") or element_name.startswith("breeding_creature_gender_text"):
        return BreedingStatusInformation
    elif element_name.startswith("breeding_cryopod_timer") or element_name.startswith("breeding_cryosickness_timer") or element_name.startswith("breeding_clone_vs_parent"):
        return BreedingAdvanced
    elif element_name.startswith("breeding_"):
        return BreedingInterfaceElements
    
    # Check for Crafting Station elements
    elif element_name.startswith("crafting_station_background") or element_name.startswith("crafting_station_title") or element_name.startswith("crafting_station_type_icon"):
        return CraftingStationBackground
    elif element_name.startswith("crafting_station_search_bar") or element_name.startswith("crafting_station_search_results") or element_name.startswith("crafting_station_close_button"):
        return CraftingStationSearch
    elif element_name.startswith("crafting_station_crafting_list") or element_name.startswith("crafting_station_crafting_item") or element_name.startswith("crafting_station_blueprint_crafting"):
        return CraftingStationItems
    elif element_name.startswith("crafting_station_crafting_queue") or element_name.startswith("crafting_station_queue_item") or element_name.startswith("crafting_station_progress_bar"):
        return CraftingStationQueue
    elif element_name.startswith("crafting_station_blueprint_modifier") or element_name.startswith("crafting_station_skill_modifier") or element_name.startswith("crafting_station_bulk_craft_toggle"):
        return CraftingStationModifiers
    elif element_name.startswith("crafting_station_filter_button") or element_name.startswith("crafting_station_filter_dropdown") or element_name.startswith("crafting_station_recipe_level_requirement"):
        return CraftingStationFilters
    elif element_name.startswith("crafting_station_input_slots") or element_name.startswith("crafting_station_output_slots") or element_name.startswith("crafting_station_blueprint_slots"):
        return CraftingStationSlots
    elif element_name.startswith("crafting_station_"):
        return CraftingStationElements
    
    # Check for Painting Interface elements
    elif element_name.startswith("painting_interface_background") or element_name.startswith("painting_interface_title") or element_name.startswith("painting_interface_canvas"):
        return PaintingBackground
    elif element_name.startswith("painting_interface_rgb") or element_name.startswith("painting_interface_red_slider") or element_name.startswith("painting_interface_green_slider"):
        return PaintingColorControls
    elif element_name.startswith("painting_interface_tool_selector") or element_name.startswith("painting_interface_brush_tool") or element_name.startswith("painting_interface_eraser_tool"):
        return PaintingTools
    elif element_name.startswith("painting_interface_region_selector") or element_name.startswith("painting_interface_region_1_button") or element_name.startswith("painting_interface_region_2_button"):
        return PaintingRegions
    elif element_name.startswith("painting_interface_save_button") or element_name.startswith("painting_interface_load_button") or element_name.startswith("painting_interface_clear_button"):
        return PaintingActions
    elif element_name.startswith("painting_interface_grid_toggle") or element_name.startswith("painting_interface_grid_size_slider") or element_name.startswith("painting_interface_snap_to_grid_toggle"):
        return PaintingCanvasControls
    elif element_name.startswith("painting_interface_brush_style_selector") or element_name.startswith("painting_interface_brush_hardness_slider") or element_name.startswith("painting_interface_brush_spacing_slider"):
        return PaintingBrushSettings
    elif element_name.startswith("painting_interface_layer_list") or element_name.startswith("painting_interface_layer_entry") or element_name.startswith("painting_interface_layer_visibility"):
        return PaintingLayers
    elif element_name.startswith("painting_interface_text_input_field") or element_name.startswith("painting_interface_font_selector") or element_name.startswith("painting_interface_font_size_slider"):
        return PaintingText
    elif element_name.startswith("painting_interface_tribe_logo_template") or element_name.startswith("painting_interface_template_selector") or element_name.startswith("painting_interface_flag_template"):
        return PaintingTemplates
    elif element_name.startswith("painting_interface_"):
        return PaintingInterfaceElements
    
    # Check for Cave elements
    elif element_name.startswith("cave_entrance_marker") or element_name.startswith("cave_entrance_name_display") or element_name.startswith("cave_entrance_difficulty_rating"):
        return CaveEntranceElements
    elif element_name.startswith("cave_gas_meter") or element_name.startswith("cave_gas_warning_icon") or element_name.startswith("cave_gas_mask_indicator"):
        return CaveHazardElements
    elif element_name.startswith("cave_artifact_glow") or element_name.startswith("cave_artifact_container") or element_name.startswith("cave_artifact_name"):
        return CaveArtifactElements
    elif element_name.startswith("cave_exit_marker") or element_name.startswith("cave_exit_distance") or element_name.startswith("cave_loot_crate_marker"):
        return CaveNavigationElements
    elif element_name.startswith("cave_structural_integrity") or element_name.startswith("cave_ceiling_collapse_warning") or element_name.startswith("cave_stalactite_warning"):
        return CaveStructuralElements
    elif element_name.startswith("cave_boss_arena_entrance") or element_name.startswith("cave_boss_arena_requirements") or element_name.startswith("cave_boss_tribute_terminal"):
        return CaveBossElements
    elif element_name.startswith("cave_water_depth_indicator") or element_name.startswith("cave_water_current_indicator") or element_name.startswith("cave_swim_stamina_indicator"):
        return CaveWaterElements
    elif element_name.startswith("cave_tek_door_interface") or element_name.startswith("cave_tek_door_unlock_requirements") or element_name.startswith("cave_note_discovery"):
        return CaveTekElements
    elif element_name.startswith("cave_grapple_point_marker") or element_name.startswith("cave_climbing_pick_point") or element_name.startswith("cave_zipline_anchor_point"):
        return CaveClimbingElements
    elif element_name.startswith("cave_puzzle_interface") or element_name.startswith("cave_puzzle_clue") or element_name.startswith("cave_puzzle_interact_prompt"):
        return CavePuzzleElements
    elif element_name.startswith("cave_completion_reward") or element_name.startswith("cave_completion_timer") or element_name.startswith("cave_record_time"):
        return CaveCompletionElements
    elif element_name.startswith("cave_"):
        return CaveElements
    
    # Check for Creature Riding elements
    elif element_name.startswith("creature_riding_controls_overlay") or element_name.startswith("creature_riding_health_bar") or element_name.startswith("creature_riding_stamina_bar"):
        return CreatureRidingControls
    elif element_name.startswith("creature_riding_special_ability_icon") or element_name.startswith("creature_riding_special_ability_cooldown") or element_name.startswith("creature_riding_special_ability_active"):
        return CreatureRidingAbilities
    elif element_name.startswith("creature_riding_movement_controls") or element_name.startswith("creature_riding_jump_indicator") or element_name.startswith("creature_riding_sprint_indicator"):
        return CreatureRidingMovement
    elif element_name.startswith("creature_riding_speed_indicator") or element_name.startswith("creature_riding_altitude_indicator") or element_name.startswith("creature_riding_depth_indicator"):
        return CreatureRidingMeters
    elif element_name.startswith("creature_riding_flame_indicator") or element_name.startswith("creature_riding_poison_indicator") or element_name.startswith("creature_riding_lightning_indicator"):
        return CreatureRidingAttacks
    elif element_name.startswith("creature_riding_passenger_indicator") or element_name.startswith("creature_riding_passenger_count") or element_name.startswith("creature_riding_passenger_list"):
        return CreatureRidingPassengers
    elif element_name.startswith("creature_riding_damage_indicator") or element_name.startswith("creature_riding_creature_buff_icon") or element_name.startswith("creature_riding_pack_bonus_icon"):
        return CreatureRidingStatusEffects
    elif element_name.startswith("creature_riding_attack_cooldown") or element_name.startswith("creature_riding_gathering_efficiency") or element_name.startswith("creature_riding_resource_gathered_popup"):
        return CreatureRidingAdditionalInfo
    elif element_name.startswith("creature_riding_"):
        return CreatureRidingElements
    
    # Check for Loot Crate elements
    elif element_name.startswith("loot_crate_background") or element_name.startswith("loot_crate_title") or element_name.startswith("loot_crate_color_indicator"):
        return LootCrateBackground
    elif element_name.startswith("loot_crate_close_button") or element_name.startswith("loot_crate_take_all_button") or element_name.startswith("loot_crate_transfer_all_button"):
        return LootCrateControls
    elif element_name.startswith("loot_crate_rarity_"):
        return LootCrateRarity
    elif element_name.startswith("loot_crate_locked_indicator") or element_name.startswith("loot_crate_unlock_prompt") or element_name.startswith("loot_crate_pin_code_field"):
        return LootCrateUnlock
    elif element_name.startswith("loot_crate_beacon_light") or element_name.startswith("loot_crate_beacon_ring") or element_name.startswith("loot_crate_drop_location"):
        return LootCrateEffects
    elif element_name.startswith("loot_crate_contents_preview") or element_name.startswith("loot_crate_level_requirement") or element_name.startswith("loot_crate_tribe_access_indicator"):
        return LootCrateInfo
    elif element_name.startswith("loot_crate_special_event_indicator") or element_name.startswith("loot_crate_holiday_theme") or element_name.startswith("loot_crate_tek_variant"):
        return LootCrateSpecial
    elif element_name.startswith("loot_crate_nearby_enemy_warning") or element_name.startswith("loot_crate_nearby_allies") or element_name.startswith("loot_crate_wave_defense_status"):
        return LootCrateWaveDefense
    elif element_name.startswith("loot_crate_duplicate_item_notification") or element_name.startswith("loot_crate_item_compare") or element_name.startswith("loot_crate_claim_button"):
        return LootCrateRewards
    elif element_name.startswith("loot_crate_"):
        return LootCrateElements
    
    # If no match found, return the base class
    return UIElement


def create_ui_element(element_name, color=None, element_type="rectangle", attributes=None):
    """
    Factory function to create a UI element with the appropriate class based on the element name
    
    Args:
        element_name (str): Name of the UI element
        color (str, optional): Color of the UI element. Defaults to None (auto-determined).
        element_type (str, optional): Type of the UI element. Defaults to "rectangle".
        attributes (dict, optional): Additional attributes for the UI element. Defaults to None.
        
    Returns:
        UIElement: An instance of the appropriate UIElement subclass
    """
    element_class = get_ui_element_class(element_name)
    
    # Set default color based on element type if not provided
    if color is None:
        if "health" in element_name:
            color = "#c80000"  # Red for health
        elif "stamina" in element_name:
            color = "#00d43c"  # Green for stamina
        elif "food" in element_name:
            color = "#ff9a00"  # Orange for food
        elif "water" in element_name:
            color = "#00a9ff"  # Light blue for water
        elif "oxygen" in element_name:
            color = "#00c3ff"  # Blue for oxygen
        elif "weight" in element_name:
            color = "#a0a0a0"  # Gray for weight
        elif "tek" in element_name:
            color = "#00ccff"  # Cyan for tek
        elif "boss" in element_name:
            color = "#ff0000"  # Red for boss
        elif "warning" in element_name or "alert" in element_name:
            color = "#ff3300"  # Orange-red for warnings
        else:
            color = "#ffffff"  # White default
    
    return element_class(element_name, color, element_type, attributes)


# Common UI elements registry
UI_ELEMENTS = {
    # HUD Elements
    "hud_healthbar": create_ui_element("hud_healthbar", "#c80000"),
    "hud_healthbar_full": create_ui_element("hud_healthbar_full", "#f004ac8"),
    "hud_healthbar_medium": create_ui_element("hud_healthbar_medium", "#94c800"),
    "hud_healthbar_low": create_ui_element("hud_healthbar_low", "#c80000"),
    "hud_staminabar": create_ui_element("hud_staminabar", "#00d43c"),
    "hud_foodbar": create_ui_element("hud_foodbar", "#ff9a00"),
    "hud_waterbar": create_ui_element("hud_waterbar", "#00a9ff"),
    "hud_oxygenbar": create_ui_element("hud_oxygenbar", "#00c3ff"),
    "hud_weightbar": create_ui_element("hud_weightbar", "#a0a0a0"),
    "hud_torpiditybar": create_ui_element("hud_torpiditybar", "#9b59b6"),
    
    # Quickbar Elements
    "quickbar_background": create_ui_element("quickbar_background"),
    "quickbar_slot_1": create_ui_element("quickbar_slot_1"),
    "quickbar_slot_filled": create_ui_element("quickbar_slot_filled"),
    "quickbar_slot_empty": create_ui_element("quickbar_slot_empty"),
    "quickbar_selector": create_ui_element("quickbar_selector"),
    
    # Inventory Elements
    "inventory_background": create_ui_element("inventory_background"),
    "inventory_player_slot_empty": create_ui_element("inventory_player_slot_empty"),
    "inventory_player_slot_filled": create_ui_element("inventory_player_slot_filled"),
    "inventory_close_button": create_ui_element("inventory_close_button"),
    "inventory_transfer_right_button": create_ui_element("inventory_transfer_right_button"),
    
    # Tab Elements
    "tab_inventory_active": create_ui_element("tab_inventory_active"),
    "tab_crafting_active": create_ui_element("tab_crafting_active"),
    "tab_engrams_active": create_ui_element("tab_engrams_active"),
    
    # Crafting Elements
    "crafting_button_active": create_ui_element("crafting_button_active"),
    "crafting_materials_required": create_ui_element("crafting_materials_required"),
    "crafting_item_icon": create_ui_element("crafting_item_icon"),
    
    # Engram Elements
    "engram_icon_available": create_ui_element("engram_icon_available"),
    "engram_learn_button_active": create_ui_element("engram_learn_button_active"),
    "engram_points_available": create_ui_element("engram_points_available"),
    
    # Dino Elements
    "dino_health_bar": create_ui_element("dino_health_bar", "#c80000"),
    "dino_inventory_name": create_ui_element("dino_inventory_name"),
    "dino_behavior_setting": create_ui_element("dino_behavior_setting"),
    
    # Structure Elements
    "structure_name_label": create_ui_element("structure_name_label"),
    "structure_inventory_button": create_ui_element("structure_inventory_button"),
    "structure_options_button": create_ui_element("structure_options_button"),
    
    # Map Elements
    "map_background": create_ui_element("map_background"),
    "map_player_marker": create_ui_element("map_player_marker"),
    "map_coordinates_display": create_ui_element("map_coordinates_display"),
    
    # Eggcellent Adventure Elements
    "eggcellent_adventure_ui": create_ui_element("eggcellent_adventure_ui", "#c80076"),
    
    # Add more common elements as needed
}
    