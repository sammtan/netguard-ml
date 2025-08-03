"""
Base network device class
"""

from PySide6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsTextItem
from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtGui import QPen, QBrush, QColor, QPainter, QFont, QRadialGradient, QPixmap
import random
from src.core.device_identity import DeviceIdentity, DeviceIdentityFactory
from src.ui.theme import COLORS
from src.ui.icons import IconManager


class NetworkDevice(QGraphicsItem):
    """Base class for all network devices"""
    
    def __init__(self, device_id: str, position: QPointF, device_type: str = "generic"):
        super().__init__()
        self.device_type = device_type
        self.simulator = None
        
        # Create unique identity
        self.identity = DeviceIdentityFactory.create_identity(device_type, device_id)
        self.device_id = self.identity.hostname
        
        # Generate unique IP
        subnet = random.randint(1, 254)
        host = random.randint(1, 254)
        self.identity.ip_address = f"192.168.{subnet}.{host}"
        self.ip_address = self.identity.ip_address
        
        # Graphics
        self.setPos(position)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        
        # Device state
        self.is_running = False
        self.connections = []
        
        # Visual properties
        self.size = 60
        self.update_visual_properties()
        self.selected = False
    
    def boundingRect(self):
        """Return bounding rectangle"""
        return QRectF(-self.size/2, -self.size/2, self.size, self.size)
    
    def paint(self, painter, option, widget):
        """Paint the device"""
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Determine state colors
        if self.isSelected():
            self.selected = True
            pen_color = QColor(COLORS['accent_blue'])
            pen_width = 3
            glow_color = QColor(COLORS['accent_blue'])
            glow_color.setAlpha(30)
        else:
            self.selected = False
            pen_color = self.color.darker(150)
            pen_width = 2
            glow_color = None
        
        # Draw glow effect when selected
        if glow_color:
            painter.setPen(QPen(Qt.transparent))
            painter.setBrush(QBrush(glow_color))
            painter.drawEllipse(-self.size/2 - 10, -self.size/2 - 10, 
                              self.size + 20, self.size + 20)
        
        # Draw main circle
        painter.setPen(QPen(pen_color, pen_width))
        
        # Gradient fill
        gradient = QRadialGradient(0, -self.size/4, self.size/2)
        gradient.setColorAt(0, self.color.lighter(120))
        gradient.setColorAt(1, self.color)
        painter.setBrush(QBrush(gradient))
        
        painter.drawEllipse(-self.size/2, -self.size/2, self.size, self.size)
        
        # Draw icon using SVG or fallback to text
        icon_size = int(self.size * 0.6)
        icon_pixmap = IconManager.get_device_pixmap(self.device_type, icon_size, QColor(Qt.white))
        
        if not icon_pixmap.isNull():
            # Draw SVG icon
            icon_offset = icon_size / 2
            painter.drawPixmap(-icon_offset, -icon_offset, icon_pixmap)
        else:
            # Fallback to text icon
            painter.setPen(QPen(Qt.white))
            font = QFont("Inter", int(self.size * 0.25), QFont.Bold)
            painter.setFont(font)
            icon_rect = QRectF(-self.size/2, -self.size/2, self.size, self.size)
            icon_text = IconManager.get_icon_char(self.device_type)
            painter.drawText(icon_rect, Qt.AlignCenter, icon_text)
        
        # Draw hostname
        painter.setPen(QPen(QColor(COLORS['text_primary'])))
        font = QFont("Inter", 10, QFont.Medium)
        painter.setFont(font)
        label_rect = QRectF(-50, self.size/2 + 5, 100, 20)
        painter.drawText(label_rect, Qt.AlignCenter, self.device_id)
        
        # Draw IP address
        painter.setPen(QPen(QColor(COLORS['text_secondary'])))
        font = QFont("JetBrains Mono", 8)
        painter.setFont(font)
        ip_rect = QRectF(-50, self.size/2 + 22, 100, 16)
        painter.drawText(ip_rect, Qt.AlignCenter, self.ip_address)
        
        # Draw manufacturer/model on hover or selection
        if self.selected:
            painter.setPen(QPen(QColor(COLORS['text_secondary'])))
            font = QFont("Inter", 7)
            painter.setFont(font)
            info_rect = QRectF(-60, self.size/2 + 38, 120, 14)
            info_text = f"{self.identity.manufacturer} {self.identity.model}"
            painter.drawText(info_rect, Qt.AlignCenter, info_text)
    
    def start(self):
        """Start the device"""
        self.is_running = True
    
    def stop(self):
        """Stop the device"""
        self.is_running = False
    
    def receive_packet(self, packet: dict):
        """Receive a packet"""
        # Override in subclasses
        pass
    
    def update_visual_properties(self):
        """Update visual properties based on device type"""
        # Default values
        self.color = QColor(100, 100, 100)
        
    def send_packet(self, destination, protocol: str, data: str):
        """Send a packet to destination"""
        if self.simulator:
            self.simulator.send_packet(self, destination, protocol, data)
    
    def mouseDoubleClickEvent(self, event):
        """Handle double-click to open device control panel"""
        from src.ui.device_controls import create_control_panel
        if hasattr(self, 'scene') and self.scene():
            # Find the main window
            views = self.scene().views()
            if views:
                main_window = views[0].window()
                if main_window:
                    # Open device control panel
                    control_panel = create_control_panel(self, main_window)
                    control_panel.show()
        super().mouseDoubleClickEvent(event)
    
    def get_status_info(self) -> dict:
        """Get device status information"""
        return {
            'hostname': self.identity.hostname,
            'ip_address': self.identity.ip_address,
            'mac_address': self.identity.mac_address,
            'manufacturer': self.identity.manufacturer,
            'model': self.identity.model,
            'serial': self.identity.serial_number,
            'firmware': self.identity.firmware_version,
            'is_running': self.is_running,
            'properties': self.identity.properties
        }
    
    def itemChange(self, change, value):
        """Handle item changes"""
        if change == QGraphicsItem.ItemPositionHasChanged and self.scene():
            # Update connections when device moves
            if hasattr(self.scene(), 'views') and self.scene().views():
                view = self.scene().views()[0]
                if hasattr(view, 'connection_manager') and view.connection_manager:
                    # Update all connections involving this device
                    for conn_data in view.connection_manager.connections:
                        if conn_data['device1'] == self or conn_data['device2'] == self:
                            connection = conn_data['connection']
                            if hasattr(connection, 'update_cable'):
                                connection.update_cable()
                            elif hasattr(connection, 'update_signal'):
                                connection.update_signal()
            
            # Force scene update to prevent trails
            self.scene().update()
        
        return super().itemChange(change, value)