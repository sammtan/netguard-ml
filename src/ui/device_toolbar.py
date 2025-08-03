"""
Device toolbar at the bottom with tabbed categories
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, 
    QPushButton, QToolButton, QLabel, QToolTip
)
from PySide6.QtCore import Qt, Signal, QTimer, QPoint, QMimeData
from PySide6.QtGui import QDrag, QCursor, QPalette, QColor, QIcon
from src.ui.theme import COLORS
from src.ui.icons import IconManager


class DeviceButton(QToolButton):
    """Button representing a device type"""
    
    def __init__(self, device_type: str, display_name: str):
        super().__init__()
        self.device_type = device_type
        self.display_name = display_name
        
        # Set up button with SVG icon or text fallback
        icon_pixmap = IconManager.get_device_pixmap(device_type, 32, QColor(COLORS['text_primary']))
        
        if not icon_pixmap.isNull():
            self.setIcon(QIcon(icon_pixmap))
            self.setIconSize(icon_pixmap.size())
        else:
            # Fallback to text
            self.setText(IconManager.get_icon_char(device_type))
            self.setStyleSheet(self.styleSheet() + """
                QToolButton {
                    font-size: 16px;
                    font-weight: bold;
                }
            """)
        
        self.setFixedSize(60, 60)
        self.setCheckable(False)
        
        # Style
        self.setStyleSheet(f"""
            QToolButton {{
                background-color: {COLORS['surface_light']};
                border: 2px solid {COLORS['border']};
                border-radius: 8px;
                font-size: 20px;
                font-weight: bold;
                color: {COLORS['text_primary']};
            }}
            QToolButton:hover {{
                background-color: {COLORS['accent_blue']};
                border-color: {COLORS['accent_blue_light']};
            }}
            QToolButton:pressed {{
                background-color: {COLORS['accent_blue_dark']};
            }}
        """)
        
        # Tooltip timer
        self.tooltip_timer = QTimer()
        self.tooltip_timer.timeout.connect(self.show_custom_tooltip)
        self.setMouseTracking(True)
        
    def enterEvent(self, event):
        """Start tooltip timer on hover"""
        self.tooltip_timer.start(500)  # 0.5 seconds
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Stop tooltip timer and hide tooltip"""
        self.tooltip_timer.stop()
        QToolTip.hideText()
        super().leaveEvent(event)
    
    def mouseMoveEvent(self, event):
        """Track mouse for tooltip position"""
        self.mouse_pos = QCursor.pos()
        super().mouseMoveEvent(event)
    
    def show_custom_tooltip(self):
        """Show tooltip at mouse position"""
        if hasattr(self, 'mouse_pos'):
            QToolTip.showText(self.mouse_pos, self.display_name)
    
    def mousePressEvent(self, event):
        """Start drag operation"""
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.device_type)
            drag.setMimeData(mime_data)
            drag.exec_(Qt.CopyAction)


class DeviceCategoryWidget(QWidget):
    """Widget containing devices for a category"""
    
    def __init__(self, devices):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Add device buttons
        for display_name, device_type in devices:
            if device_type:  # Skip None entries
                button = DeviceButton(device_type, display_name)
                layout.addWidget(button)
        
        layout.addStretch()


class DeviceToolbar(QWidget):
    """Bottom toolbar with tabbed device categories"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the toolbar UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.South)
        self.tabs.setMovable(False)
        
        # Define device categories
        categories = {
            "End User": [
                ("PC", "pc"),
                ("Laptop", "laptop"),
                ("Smartphone", "smartphone"),
                ("Tablet", "tablet"),
                ("Printer", "printer"),
            ],
            "Network": [
                ("Router", "router"),
                ("Switch", "switch"),
                ("Hub", "hub"),
                ("Bridge", "bridge"),
                ("Access Point", "access_point"),
                ("Wireless Router", "wireless_router"),
            ],
            "Servers": [
                ("Server", "server"),
                ("Database Server", "database"),
                ("Web Server", "web_server"),
                ("Mail Server", "mail_server"),
                ("File Server", "file_server"),
                ("Game Server", "game_server"),
            ],
            "Security": [
                ("Firewall", "firewall"),
                ("VPN Gateway", "vpn"),
                ("IDS/IPS", "ids_ips"),
                ("Proxy Server", "proxy"),
                ("NAC Device", "nac"),
            ],
            "IoT": [
                ("Smart Home Hub", "smart_hub"),
                ("IP Camera", "ip_camera"),
                ("IoT Sensor", "iot_sensor"),
                ("Smart Light", "smart_light"),
                ("Smart Speaker", "smart_speaker"),
            ],
            "Special": [
                ("Cloud Service", "cloud"),
                ("Satellite Link", "satellite"),
                ("VoIP Phone", "voip"),
                ("Load Balancer", "load_balancer"),
                ("NAS Storage", "nas"),
                ("UPS", "ups")
            ]
        }
        
        # Create tabs for each category
        for category, devices in categories.items():
            widget = DeviceCategoryWidget(devices)
            self.tabs.addTab(widget, category)
        
        layout.addWidget(self.tabs)
        
        # Set fixed height
        self.setFixedHeight(120)