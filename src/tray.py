# Edge Light - System Tray Interface
# Provides system tray icon with settings controls

import os
import sys
from PyQt5.QtWidgets import (
    QSystemTrayIcon, QMenu, QAction, QWidgetAction,
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
    QPushButton, QFrame, QApplication, QCheckBox, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont

from constants import (
    APP_NAME, APP_VERSION,
    BRIGHTNESS_MIN, BRIGHTNESS_MAX,
    COLOR_TEMP_MIN, COLOR_TEMP_MAX,
    GLOW_WIDTH_MIN, GLOW_WIDTH_MAX,
    EDGE_OPTIONS, EDGE_ALL,
)


def get_icon_path():
    """Get the path to the icon file."""
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'icon.ico')


def create_default_icon():
    """Load the custom icon or create a fallback."""
    icon_path = get_icon_path()
    
    if os.path.exists(icon_path):
        return QIcon(icon_path)
    
    # Fallback: create a simple colored icon
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QColor(255, 200, 100))
    painter.setPen(QColor(255, 180, 80))
    painter.drawEllipse(12, 12, 40, 40)
    
    painter.setPen(QColor(255, 220, 120))
    painter.setBrush(QColor(255, 220, 120))
    import math
    for i in range(8):
        angle = i * 45
        rad = math.radians(angle)
        x1 = 32 + int(24 * math.cos(rad))
        y1 = 32 + int(24 * math.sin(rad))
        x2 = 32 + int(30 * math.cos(rad))
        y2 = 32 + int(30 * math.sin(rad))
        painter.drawLine(x1, y1, x2, y2)
    
    painter.end()
    return QIcon(pixmap)


class HotkeyButton(QPushButton):
    """Button that captures key combinations when clicked."""
    
    hotkeyChanged = pyqtSignal(str)
    
    def __init__(self, hotkey_str: str = "alt+shift+l", label: str = "", parent=None):
        super().__init__(parent)
        self._hotkey_str = hotkey_str
        self._label = label
        self._recording = False
        self._pressed_modifiers = set()
        self._pressed_key = ""
        
        self._update_display()
        self._apply_style()
    
    def _apply_style(self):
        """Apply button styling."""
        self.setStyleSheet("""
            QPushButton {
                background-color: #2A2A2A;
                color: #B0B0B0;
                border: 1px solid #505050;
                border-radius: 4px;
                padding: 8px 10px;
                font-size: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #353535;
                border-color: #606060;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
        """)
    
    def _format_hotkey(self, hotkey_str: str) -> str:
        """Format hotkey string for display."""
        from hotkey import hotkey_to_display_string
        return hotkey_to_display_string(hotkey_str)
    
    def _update_display(self):
        """Update button text."""
        if self._recording:
            if self._pressed_modifiers or self._pressed_key:
                parts = list(self._pressed_modifiers) + ([self._pressed_key.upper()] if self._pressed_key else [])
                self.setText("+".join(parts) + "...")
            else:
                self.setText("Press keys...")
            self.setStyleSheet("""
                QPushButton {
                    background-color: #3D3D15;
                    color: #FFD070;
                    border: 1px solid #806020;
                    border-radius: 4px;
                    padding: 8px 10px;
                    font-size: 10px;
                }
            """)
        else:
            display = self._format_hotkey(self._hotkey_str)
            if self._label:
                self.setText(f"{self._label}\n{display}")
            else:
                self.setText(display)
            self._apply_style()
    
    def set_hotkey(self, hotkey_str: str):
        """Set the hotkey without emitting signal."""
        self._hotkey_str = hotkey_str
        self._update_display()
    
    def get_hotkey(self) -> str:
        """Get current hotkey string."""
        return self._hotkey_str
    
    def mousePressEvent(self, event):
        """Start recording on click."""
        if not self._recording:
            self._recording = True
            self._pressed_modifiers = set()
            self._pressed_key = ""
            self._update_display()
            self.setFocus()
        super().mousePressEvent(event)
    
    def keyPressEvent(self, event):
        """Capture key press."""
        if not self._recording:
            return super().keyPressEvent(event)
        
        key = event.key()
        
        if key == Qt.Key_Control:
            self._pressed_modifiers.add("Ctrl")
        elif key == Qt.Key_Shift:
            self._pressed_modifiers.add("Shift")
        elif key == Qt.Key_Alt:
            self._pressed_modifiers.add("Alt")
        elif key == Qt.Key_Meta:
            self._pressed_modifiers.add("Win")
        elif key == Qt.Key_Escape:
            self._recording = False
            self._update_display()
        elif key not in (Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt, Qt.Key_Meta):
            key_char = event.text().lower()
            if key_char and key_char.isalnum():
                self._pressed_key = key_char
                self._complete_recording()
        
        self._update_display()
    
    def focusOutEvent(self, event):
        """Cancel recording on focus loss."""
        if self._recording:
            self._recording = False
            self._update_display()
        super().focusOutEvent(event)
    
    def _complete_recording(self):
        """Complete the hotkey recording."""
        if self._pressed_modifiers and self._pressed_key:
            parts = []
            if "Ctrl" in self._pressed_modifiers:
                parts.append("ctrl")
            if "Alt" in self._pressed_modifiers:
                parts.append("alt")
            if "Shift" in self._pressed_modifiers:
                parts.append("shift")
            if "Win" in self._pressed_modifiers:
                parts.append("win")
            parts.append(self._pressed_key)
            
            new_hotkey = "+".join(parts)
            self._hotkey_str = new_hotkey
            self.hotkeyChanged.emit(new_hotkey)
        
        self._recording = False
        self._update_display()


class SliderWidget(QWidget):
    """Custom slider widget with label and value display."""
    
    valueChanged = pyqtSignal(int)
    
    def __init__(self, label: str, min_val: int, max_val: int, 
                 value: int, suffix: str = "", parent=None):
        super().__init__(parent)
        
        self.suffix = suffix
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(3)
        
        header = QHBoxLayout()
        
        self.label = QLabel(label)
        self.label.setStyleSheet("color: #E0E0E0; font-weight: bold; font-size: 11px;")
        header.addWidget(self.label)
        header.addStretch()
        
        self.value_label = QLabel(f"{value}{suffix}")
        self.value_label.setStyleSheet("color: #B0B0B0; font-size: 11px;")
        header.addWidget(self.value_label)
        
        layout.addLayout(header)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(min_val)
        self.slider.setMaximum(max_val)
        self.slider.setValue(value)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #404040;
                height: 6px;
                background: #303030;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #FFD070;
                border: 1px solid #CC9F40;
                width: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }
            QSlider::handle:horizontal:hover {
                background: #FFE090;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF8C00, stop:1 #FFD070);
                border-radius: 3px;
            }
        """)
        self.slider.valueChanged.connect(self._on_value_changed)
        layout.addWidget(self.slider)
    
    def _on_value_changed(self, value):
        self.value_label.setText(f"{value}{self.suffix}")
        self.valueChanged.emit(value)
    
    def set_value(self, value):
        self.slider.setValue(value)
    
    def value(self):
        return self.slider.value()


class SettingsPopup(QWidget):
    """Popup window for settings sliders."""
    
    brightnessChanged = pyqtSignal(int)
    temperatureChanged = pyqtSignal(int)
    widthChanged = pyqtSignal(int)
    edgeSelectionChanged = pyqtSignal(str)
    toggleRequested = pyqtSignal()
    autostartChanged = pyqtSignal(bool)
    hotkeyToggleChanged = pyqtSignal(str)
    hotkeyPanelChanged = pyqtSignal(str)
    quitRequested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowFlags(
            Qt.Popup | 
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the popup UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #1E1E1E;
                border: 1px solid #404040;
                border-radius: 10px;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Title
        title = QLabel(f"⚡ {APP_NAME}")
        title.setStyleSheet("""
            color: #FFD070;
            font-size: 16px;
            font-weight: bold;
            padding-bottom: 5px;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Separator
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.HLine)
        sep1.setStyleSheet("background-color: #404040;")
        sep1.setFixedHeight(1)
        layout.addWidget(sep1)
        
        # Brightness slider
        self.brightness_slider = SliderWidget(
            "💡 Brightness", 
            BRIGHTNESS_MIN, BRIGHTNESS_MAX, 
            60, "%"
        )
        self.brightness_slider.valueChanged.connect(self.brightnessChanged)
        layout.addWidget(self.brightness_slider)
        
        # Temperature slider
        self.temp_slider = SliderWidget(
            "🌡️ Color Temperature",
            COLOR_TEMP_MIN, COLOR_TEMP_MAX,
            4500, "K"
        )
        self.temp_slider.valueChanged.connect(self.temperatureChanged)
        layout.addWidget(self.temp_slider)
        
        # Width slider
        self.width_slider = SliderWidget(
            "📐 Glow Width",
            GLOW_WIDTH_MIN, GLOW_WIDTH_MAX,
            175, "px"
        )
        self.width_slider.valueChanged.connect(self.widthChanged)
        layout.addWidget(self.width_slider)
        
        # Edge Selection section
        edge_header = QLabel("📍 Edge Selection")
        edge_header.setStyleSheet("color: #E0E0E0; font-weight: bold; font-size: 11px; padding: 5px 10px 0px 10px;")
        layout.addWidget(edge_header)
        
        # Edge selection buttons in a row
        edge_row = QHBoxLayout()
        edge_row.setSpacing(4)
        edge_row.setContentsMargins(10, 0, 10, 5)
        
        self.edge_buttons = {}
        for edge_id, edge_label in EDGE_OPTIONS:
            btn = QPushButton(edge_label)
            btn.setCheckable(True)
            btn.setProperty("edge_id", edge_id)
            btn.clicked.connect(lambda checked, eid=edge_id: self._on_edge_selected(eid))
            self.edge_buttons[edge_id] = btn
            edge_row.addWidget(btn)
        
        self._update_edge_button_styles()
        layout.addLayout(edge_row)
        
        # Separator
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        sep2.setStyleSheet("background-color: #404040;")
        sep2.setFixedHeight(1)
        layout.addWidget(sep2)
        
        # Toggle button
        self.toggle_btn = QPushButton("🔆 Turn ON")
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D5A27;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3D7A37;
            }
            QPushButton:pressed {
                background-color: #1D4A17;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggleRequested)
        layout.addWidget(self.toggle_btn)
        
        # Hotkey section header
        hotkey_header = QLabel("⌨️ Keyboard Shortcuts")
        hotkey_header.setStyleSheet("color: #909090; font-size: 11px; padding-top: 5px;")
        hotkey_header.setAlignment(Qt.AlignCenter)
        layout.addWidget(hotkey_header)
        
        # Two hotkey buttons side by side
        hotkey_row = QHBoxLayout()
        hotkey_row.setSpacing(8)
        
        # Toggle hotkey button
        self.hotkey_toggle_btn = HotkeyButton("alt+shift+l", "🔆 Toggle")
        self.hotkey_toggle_btn.hotkeyChanged.connect(self.hotkeyToggleChanged)
        self.hotkey_toggle_btn.setFixedHeight(50)
        hotkey_row.addWidget(self.hotkey_toggle_btn)
        
        # Panel hotkey button
        self.hotkey_panel_btn = HotkeyButton("alt+shift+p", "⚙️ Panel")
        self.hotkey_panel_btn.hotkeyChanged.connect(self.hotkeyPanelChanged)
        self.hotkey_panel_btn.setFixedHeight(50)
        hotkey_row.addWidget(self.hotkey_panel_btn)
        
        layout.addLayout(hotkey_row)
        
        # Hotkey hint
        hint_label = QLabel("Click a button to change its hotkey")
        hint_label.setStyleSheet("color: #505050; font-size: 9px;")
        hint_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint_label)
        
        # Separator
        sep3 = QFrame()
        sep3.setFrameShape(QFrame.HLine)
        sep3.setStyleSheet("background-color: #404040;")
        sep3.setFixedHeight(1)
        layout.addWidget(sep3)
        
        # Auto-start checkbox
        self.autostart_checkbox = QCheckBox("🚀 Start with Windows")
        self.autostart_checkbox.setStyleSheet("""
            QCheckBox {
                color: #B0B0B0;
                font-size: 11px;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 3px;
                border: 1px solid #505050;
                background: #303030;
            }
            QCheckBox::indicator:checked {
                background: #FFD070;
                border-color: #CC9F40;
            }
            QCheckBox::indicator:hover {
                border-color: #707070;
            }
        """)
        self.autostart_checkbox.stateChanged.connect(
            lambda state: self.autostartChanged.emit(state == Qt.Checked)
        )
        layout.addWidget(self.autostart_checkbox)
        
        # Quit button
        quit_btn = QPushButton("✕ Quit Edge Light")
        quit_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #808080;
                border: 1px solid #404040;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #402020;
                color: #FF6060;
                border-color: #602020;
            }
        """)
        quit_btn.clicked.connect(self.quitRequested)
        layout.addWidget(quit_btn)
        
        main_layout.addWidget(container)
        self.setFixedWidth(290)
    
    def update_toggle_button(self, enabled: bool):
        """Update toggle button text and style based on state."""
        if enabled:
            self.toggle_btn.setText("🔅 Turn OFF")
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #5A2727;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 20px;
                    font-size: 13px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #7A3737;
                }
                QPushButton:pressed {
                    background-color: #4A1717;
                }
            """)
        else:
            self.toggle_btn.setText("🔆 Turn ON")
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2D5A27;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 20px;
                    font-size: 13px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3D7A37;
                }
                QPushButton:pressed {
                    background-color: #1D4A17;
                }
            """)
    
    def set_values(self, brightness: int, temperature: int, width: int):
        """Set all slider values."""
        self.brightness_slider.set_value(brightness)
        self.temp_slider.set_value(temperature)
        self.width_slider.set_value(width)
    
    def set_hotkey_toggle(self, hotkey_str: str):
        """Set the toggle hotkey button display."""
        self.hotkey_toggle_btn.set_hotkey(hotkey_str)
    
    def set_hotkey_panel(self, hotkey_str: str):
        """Set the panel hotkey button display."""
        self.hotkey_panel_btn.set_hotkey(hotkey_str)
    
    def set_autostart(self, enabled: bool):
        """Set auto-start checkbox state without triggering signal."""
        self.autostart_checkbox.blockSignals(True)
        self.autostart_checkbox.setChecked(enabled)
        self.autostart_checkbox.blockSignals(False)
    
    def set_edge_selection(self, selection: str):
        """Set the current edge selection."""
        self._current_edge = selection
        self._update_edge_button_styles()
    
    def _on_edge_selected(self, edge_id: str):
        """Handle edge button click."""
        self._current_edge = edge_id
        self._update_edge_button_styles()
        self.edgeSelectionChanged.emit(edge_id)
    
    def _update_edge_button_styles(self):
        """Update edge button styles based on selection."""
        current = getattr(self, '_current_edge', EDGE_ALL)
        
        for edge_id, btn in self.edge_buttons.items():
            if edge_id == current:
                btn.setChecked(True)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #FFD070;
                        color: #1E1E1E;
                        border: none;
                        border-radius: 4px;
                        padding: 6px 8px;
                        font-size: 9px;
                        font-weight: bold;
                    }
                """)
            else:
                btn.setChecked(False)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2A2A2A;
                        color: #909090;
                        border: 1px solid #404040;
                        border-radius: 4px;
                        padding: 6px 8px;
                        font-size: 9px;
                    }
                    QPushButton:hover {
                        background-color: #353535;
                        color: #B0B0B0;
                    }
                """)


class TrayManager(QObject):
    """Manages the system tray icon and menu."""
    
    # Signal to open popup (for hotkey)
    openPanelRequested = pyqtSignal()
    
    def __init__(self, overlay, settings_manager, hotkey_manager=None):
        super().__init__()
        
        self.overlay = overlay
        self.settings = settings_manager
        self.hotkey_manager = hotkey_manager
        
        self._setup_tray()
        self._setup_popup()
        self._load_settings()
        
        # Connect panel open signal
        self.openPanelRequested.connect(self._show_popup)
    
    def _setup_tray(self):
        """Setup system tray icon."""
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(create_default_icon())
        self.tray_icon.setToolTip(f"{APP_NAME} - Click to open settings")
        self.tray_icon.activated.connect(self._on_tray_activated)
        self.tray_icon.show()
    
    def _setup_popup(self):
        """Setup settings popup."""
        self.popup = SettingsPopup()
        
        self.popup.brightnessChanged.connect(self._on_brightness_changed)
        self.popup.temperatureChanged.connect(self._on_temperature_changed)
        self.popup.widthChanged.connect(self._on_width_changed)
        self.popup.edgeSelectionChanged.connect(self._on_edge_selection_changed)
        self.popup.toggleRequested.connect(self._on_toggle)
        self.popup.autostartChanged.connect(self._on_autostart_changed)
        self.popup.hotkeyToggleChanged.connect(self._on_hotkey_toggle_changed)
        self.popup.hotkeyPanelChanged.connect(self._on_hotkey_panel_changed)
        self.popup.quitRequested.connect(self._on_quit)
    
    def _load_settings(self):
        """Load settings and apply to UI."""
        brightness = self.settings.get('brightness', 60)
        temperature = self.settings.get('color_temperature', 4500)
        width = self.settings.get('glow_width', 175)
        enabled = self.settings.get('enabled', False)
        hotkey_toggle = self.settings.get('hotkey_toggle', 'alt+shift+l')
        hotkey_panel = self.settings.get('hotkey_panel', 'alt+shift+p')
        edge_selection = self.settings.get('edge_selection', EDGE_ALL)
        
        from autostart import is_autostart_enabled
        autostart_enabled = is_autostart_enabled()
        
        self.popup.set_values(brightness, temperature, width)
        self.popup.update_toggle_button(enabled)
        self.popup.set_autostart(autostart_enabled)
        self.popup.set_hotkey_toggle(hotkey_toggle)
        self.popup.set_hotkey_panel(hotkey_panel)
        self.popup.set_edge_selection(edge_selection)
        
        self.overlay.set_brightness(brightness)
        self.overlay.set_color_temperature(temperature)
        self.overlay.set_glow_width(width)
        self.overlay.set_edge_selection(edge_selection)
        if enabled:
            self.overlay.set_enabled(True)
    
    def set_hotkey_manager(self, manager):
        """Set the hotkey manager reference."""
        self.hotkey_manager = manager
    
    def _on_tray_activated(self, reason):
        """Handle tray icon click."""
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self._show_popup()
    
    def _show_popup(self):
        """Show the settings popup near the tray icon."""
        geometry = self.tray_icon.geometry()
        
        popup_x = geometry.x() - self.popup.width() // 2 + geometry.width() // 2
        popup_y = geometry.y() - self.popup.height() - 10
        
        screen = QApplication.desktop().screenGeometry()
        if popup_x < 10:
            popup_x = 10
        if popup_x + self.popup.width() > screen.width() - 10:
            popup_x = screen.width() - self.popup.width() - 10
        if popup_y < 10:
            popup_y = geometry.y() + geometry.height() + 10
        
        self.popup.move(popup_x, popup_y)
        self.popup.show()
        self.popup.raise_()
        self.popup.activateWindow()
    
    def _on_brightness_changed(self, value):
        self.overlay.set_brightness(value)
        self.settings.set('brightness', value)
    
    def _on_temperature_changed(self, value):
        self.overlay.set_color_temperature(value)
        self.settings.set('color_temperature', value)
    
    def _on_width_changed(self, value):
        self.overlay.set_glow_width(value)
        self.settings.set('glow_width', value)
    
    def _on_edge_selection_changed(self, selection: str):
        self.overlay.set_edge_selection(selection)
        self.settings.set('edge_selection', selection)
    
    def _on_autostart_changed(self, enabled: bool):
        from autostart import set_autostart
        success = set_autostart(enabled)
        if success:
            status = "enabled" if enabled else "disabled"
            self.show_notification("Auto-Start", f"Auto-start {status}")
    
    def _on_hotkey_toggle_changed(self, hotkey_str: str):
        self.settings.set('hotkey_toggle', hotkey_str)
        if self.hotkey_manager:
            self.hotkey_manager.update_hotkey('toggle', hotkey_str)
        
        from hotkey import hotkey_to_display_string
        display = hotkey_to_display_string(hotkey_str)
        self.show_notification("Toggle Hotkey", f"New hotkey: {display}")
    
    def _on_hotkey_panel_changed(self, hotkey_str: str):
        self.settings.set('hotkey_panel', hotkey_str)
        if self.hotkey_manager:
            self.hotkey_manager.update_hotkey('panel', hotkey_str)
        
        from hotkey import hotkey_to_display_string
        display = hotkey_to_display_string(hotkey_str)
        self.show_notification("Panel Hotkey", f"New hotkey: {display}")
    
    def _on_toggle(self):
        self.toggle()
    
    def toggle(self):
        """Toggle the overlay on/off."""
        enabled = not self.overlay.is_enabled()
        self.overlay.set_enabled(enabled)
        self.settings.set('enabled', enabled)
        self.popup.update_toggle_button(enabled)
    
    def open_panel(self):
        """Toggle the settings panel visibility (for hotkey use)."""
        if self.popup.isVisible():
            self.popup.hide()
        else:
            self._show_popup()
    
    def _on_quit(self):
        self.popup.hide()
        self.tray_icon.hide()
        QApplication.quit()
    
    def show_notification(self, title: str, message: str):
        self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 2000)
