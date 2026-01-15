# Edge Light - Constants and Default Configuration

APP_NAME = "Edge Light"
APP_VERSION = "1.1.0"

# Edge selection options
EDGE_ALL = "all"
EDGE_TOP_ONLY = "top"
EDGE_TOP_SIDES = "top_sides"
EDGE_SIDES_ONLY = "sides"

EDGE_OPTIONS = [
    (EDGE_ALL, "All Edges"),
    (EDGE_TOP_ONLY, "Top Only"),
    (EDGE_TOP_SIDES, "Top + Sides"),
    (EDGE_SIDES_ONLY, "Sides Only"),
]

# Default settings
DEFAULT_SETTINGS = {
    "enabled": False,
    "brightness": 60,              # 0-100 (percentage)
    "color_temperature": 4500,     # 2700K (warm) to 6500K (cool)
    "glow_width": 175,             # pixels (150-200 default range)
    "hotkey_toggle": "alt+shift+l",    # Toggle light on/off
    "hotkey_panel": "alt+shift+p",     # Open settings panel
    "edge_selection": EDGE_ALL,        # Which edges to light up
}

# Setting ranges
BRIGHTNESS_MIN = 0
BRIGHTNESS_MAX = 100

COLOR_TEMP_MIN = 2700   # Warm (orange/yellow)
COLOR_TEMP_MAX = 6500   # Cool (blue/white)

GLOW_WIDTH_MIN = 50
GLOW_WIDTH_MAX = 400

# Settings file location (relative to executable)
SETTINGS_FILENAME = "edgelight_settings.json"

# Color temperature to RGB mapping reference points
COLOR_TEMP_MAP = {
    2700: (255, 180, 107),   # Warm (incandescent)
    3000: (255, 191, 125),   # Soft warm
    3500: (255, 206, 151),   # Warm white
    4000: (255, 219, 175),   # Neutral warm
    4500: (255, 231, 198),   # Neutral
    5000: (255, 242, 221),   # Neutral cool
    5500: (255, 250, 244),   # Daylight
    6000: (248, 250, 255),   # Cool daylight
    6500: (235, 245, 255),   # Cool (blueish)
}
