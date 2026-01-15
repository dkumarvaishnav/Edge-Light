# Edge Light - Overlay Window
# Creates a solid ring light around screen edges

from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QBrush

from constants import (
    COLOR_TEMP_MIN, COLOR_TEMP_MAX, COLOR_TEMP_MAP,
    BRIGHTNESS_MIN, BRIGHTNESS_MAX,
    GLOW_WIDTH_MIN, GLOW_WIDTH_MAX,
    EDGE_ALL, EDGE_TOP_ONLY, EDGE_TOP_SIDES, EDGE_SIDES_ONLY
)


def interpolate_color_temperature(temp: int) -> tuple:
    """
    Interpolate RGB values for a given color temperature.
    Uses linear interpolation between known temperature points.
    """
    temps = sorted(COLOR_TEMP_MAP.keys())
    
    temp = max(COLOR_TEMP_MIN, min(COLOR_TEMP_MAX, temp))
    
    lower_temp = temps[0]
    upper_temp = temps[-1]
    
    for i, t in enumerate(temps):
        if t <= temp:
            lower_temp = t
        if t >= temp:
            upper_temp = t
            break
    
    if lower_temp == upper_temp:
        return COLOR_TEMP_MAP[lower_temp]
    
    ratio = (temp - lower_temp) / (upper_temp - lower_temp)
    lower_rgb = COLOR_TEMP_MAP[lower_temp]
    upper_rgb = COLOR_TEMP_MAP[upper_temp]
    
    r = int(lower_rgb[0] + ratio * (upper_rgb[0] - lower_rgb[0]))
    g = int(lower_rgb[1] + ratio * (upper_rgb[1] - lower_rgb[1]))
    b = int(lower_rgb[2] + ratio * (upper_rgb[2] - lower_rgb[2]))
    
    return (r, g, b)


class GlowOverlay(QWidget):
    """
    Transparent overlay window that renders a solid colored ring
    around selected screen edges - the ring light effect.
    """
    
    def __init__(self):
        super().__init__()
        
        self._brightness = 60
        self._color_temp = 4500
        self._glow_width = 175
        self._enabled = False
        self._edge_selection = EDGE_ALL
        
        self._setup_window()
    
    def _setup_window(self):
        """Configure window properties for transparent overlay."""
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.WindowTransparentForInput
        )
        
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        self._update_geometry()
    
    def _update_geometry(self):
        """Update overlay to cover the entire screen."""
        desktop = QDesktopWidget()
        screen_rect = desktop.screenGeometry(desktop.primaryScreen())
        self.setGeometry(screen_rect)
    
    def set_brightness(self, brightness: int):
        """Set brightness level (0-100)."""
        self._brightness = max(BRIGHTNESS_MIN, min(BRIGHTNESS_MAX, brightness))
        if self._enabled:
            self.update()
    
    def set_color_temperature(self, temp: int):
        """Set color temperature (2700K-6500K)."""
        self._color_temp = max(COLOR_TEMP_MIN, min(COLOR_TEMP_MAX, temp))
        if self._enabled:
            self.update()
    
    def set_glow_width(self, width: int):
        """Set glow width in pixels (solid ring thickness)."""
        self._glow_width = max(GLOW_WIDTH_MIN, min(GLOW_WIDTH_MAX, width))
        if self._enabled:
            self.update()
    
    def set_edge_selection(self, selection: str):
        """Set which edges to display."""
        self._edge_selection = selection
        if self._enabled:
            self.update()
    
    def get_edge_selection(self) -> str:
        """Get current edge selection."""
        return self._edge_selection
    
    def set_enabled(self, enabled: bool):
        """Enable or disable the overlay."""
        self._enabled = enabled
        if enabled:
            self._update_geometry()
            self.show()
            self.update()
        else:
            self.hide()
    
    def is_enabled(self) -> bool:
        """Check if overlay is enabled."""
        return self._enabled
    
    def toggle(self):
        """Toggle overlay on/off."""
        self.set_enabled(not self._enabled)
    
    def paintEvent(self, event):
        """Render the ring light effect."""
        if not self._enabled:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        r, g, b = interpolate_color_temperature(self._color_temp)
        solid_alpha = int(55 + (self._brightness / 100) * 200)
        
        width = self.width()
        height = self.height()
        ring_width = self._glow_width
        
        self._draw_selected_edges(painter, r, g, b, solid_alpha, width, height, ring_width)
        
        painter.end()
    
    def _draw_selected_edges(self, painter, r, g, b, alpha, width, height, ring_width):
        """Draw only the selected edges."""
        
        color = QColor(r, g, b, alpha)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(color))
        
        selection = self._edge_selection
        
        # Determine which edges to draw
        draw_top = selection in (EDGE_ALL, EDGE_TOP_ONLY, EDGE_TOP_SIDES)
        draw_bottom = selection == EDGE_ALL
        draw_left = selection in (EDGE_ALL, EDGE_TOP_SIDES, EDGE_SIDES_ONLY)
        draw_right = selection in (EDGE_ALL, EDGE_TOP_SIDES, EDGE_SIDES_ONLY)
        
        # Calculate vertical bar positions based on what's drawn
        side_top = ring_width if draw_top else 0
        side_bottom = height - ring_width if draw_bottom else height
        side_height = side_bottom - side_top
        
        # Draw edges
        if draw_top:
            painter.drawRect(0, 0, width, ring_width)
        
        if draw_bottom:
            painter.drawRect(0, height - ring_width, width, ring_width)
        
        if draw_left:
            painter.drawRect(0, side_top, ring_width, side_height)
        
        if draw_right:
            painter.drawRect(width - ring_width, side_top, ring_width, side_height)
