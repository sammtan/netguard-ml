"""
Network connections (cables, wireless signals)
"""

from PySide6.QtWidgets import QGraphicsItem, QGraphicsLineItem, QGraphicsPathItem
from PySide6.QtCore import Qt, QPointF, QLineF
from PySide6.QtGui import QPen, QBrush, QColor, QPainter, QPainterPath, QFont
from src.ui.theme import COLORS
import math


class NetworkCable(QGraphicsLineItem):
    """Visual representation of a network cable"""
    
    def __init__(self, device1, device2, cable_type="ethernet"):
        super().__init__()
        self.device1 = device1
        self.device2 = device2
        self.cable_type = cable_type
        
        # Visual properties
        self.setZValue(-1)  # Draw behind devices
        self.update_cable()
        
        # Set cable style based on type
        if cable_type == "ethernet":
            pen = QPen(QColor(COLORS['accent_blue']), 3)
            pen.setCapStyle(Qt.RoundCap)
            self.setPen(pen)
        elif cable_type == "fiber":
            pen = QPen(QColor(COLORS['accent_blue_light']), 3)
            pen.setCapStyle(Qt.RoundCap)
            pen.setStyle(Qt.DashLine)
            self.setPen(pen)
        elif cable_type == "serial":
            pen = QPen(QColor(COLORS['text_secondary']), 2)
            pen.setCapStyle(Qt.RoundCap)
            pen.setStyle(Qt.DotLine)
            self.setPen(pen)
    
    def update_cable(self):
        """Update cable position based on device positions"""
        # Get device centers
        pos1 = self.device1.scenePos()
        pos2 = self.device2.scenePos()
        
        # Calculate line
        line = QLineF(pos1, pos2)
        
        # Shorten line to not overlap with device circles
        # Calculate unit vector
        if line.length() > 0:
            dx = line.dx() / line.length()
            dy = line.dy() / line.length()
            
            # Offset by device radius
            offset1 = self.device1.size / 2 + 5
            offset2 = self.device2.size / 2 + 5
            
            # Adjust endpoints
            x1 = pos1.x() + dx * offset1
            y1 = pos1.y() + dy * offset1
            x2 = pos2.x() - dx * offset2
            y2 = pos2.y() - dy * offset2
            
            self.setLine(x1, y1, x2, y2)
    
    def paint(self, painter, option, widget):
        """Custom paint for cable"""
        super().paint(painter, option, widget)
        
        # Draw connection quality indicator at midpoint
        line = self.line()
        if line.length() > 0:
            mid_x = (line.x1() + line.x2()) / 2
            mid_y = (line.y1() + line.y2()) / 2
            
            # Draw small circle at midpoint
            painter.setPen(QPen(Qt.transparent))
            painter.setBrush(QBrush(QColor(COLORS['success'])))
            painter.drawEllipse(QPointF(mid_x, mid_y), 4, 4)


class WirelessSignal(QGraphicsPathItem):
    """Visual representation of wireless signal"""
    
    def __init__(self, device1, device2, connection_type='wifi'):
        super().__init__()
        self.device1 = device1
        self.device2 = device2
        self.connection_type = connection_type
        
        # Visual properties
        self.setZValue(-1)  # Draw behind devices
        self.update_signal()
        
        # Set signal style based on connection type
        if connection_type == 'wifi':
            pen = QPen(QColor(COLORS['accent_blue']), 2, Qt.DashDotLine)
        elif connection_type == 'bluetooth':
            pen = QPen(QColor("#2196F3"), 2, Qt.DashLine)  # Lighter blue
        elif connection_type == 'zigbee':
            pen = QPen(QColor("#4CAF50"), 2, Qt.DotLine)  # Green for IoT
        else:
            pen = QPen(QColor(COLORS['accent_blue']), 2, Qt.DashDotLine)
        
        pen.setCapStyle(Qt.RoundCap)
        self.setPen(pen)
        self.setBrush(Qt.NoBrush)
    
    def update_signal(self):
        """Update signal path based on device positions"""
        # Get device centers
        pos1 = self.device1.scenePos()
        pos2 = self.device2.scenePos()
        
        # Create wavy path to represent wireless
        path = QPainterPath()
        
        # Calculate direction
        dx = pos2.x() - pos1.x()
        dy = pos2.y() - pos1.y()
        length = math.sqrt(dx*dx + dy*dy)
        
        if length > 0:
            # Normalize direction
            dx /= length
            dy /= length
            
            # Perpendicular direction for wave
            perp_dx = -dy
            perp_dy = dx
            
            # Start from device1 edge
            offset1 = self.device1.size / 2 + 10
            start_x = pos1.x() + dx * offset1
            start_y = pos1.y() + dy * offset1
            
            path.moveTo(start_x, start_y)
            
            # Create wavy line
            segments = int(length / 30)
            wave_amplitude = 10
            
            for i in range(segments):
                t = (i + 1) / segments
                
                # Base position along line
                base_x = pos1.x() + dx * (offset1 + (length - offset1 - self.device2.size/2 - 10) * t)
                base_y = pos1.y() + dy * (offset1 + (length - offset1 - self.device2.size/2 - 10) * t)
                
                # Add wave offset
                wave_offset = wave_amplitude * math.sin(t * math.pi * 4)
                wave_x = base_x + perp_dx * wave_offset
                wave_y = base_y + perp_dy * wave_offset
                
                path.lineTo(wave_x, wave_y)
            
            self.setPath(path)


class ConnectionManager:
    """Manages connections between devices"""
    
    def __init__(self, scene):
        self.scene = scene
        self.connections = []
        self.connection_mode = False
        self.start_device = None
        self.temp_line = None
    
    def start_connection(self, device):
        """Start creating a connection from device"""
        self.connection_mode = True
        self.start_device = device
        
        # Create temporary line
        pos = device.scenePos()
        self.temp_line = QGraphicsLineItem(pos.x(), pos.y(), pos.x(), pos.y())
        pen = QPen(QColor(COLORS['accent_blue']), 2, Qt.DashLine)
        self.temp_line.setPen(pen)
        self.scene.addItem(self.temp_line)
    
    def update_temp_connection(self, pos):
        """Update temporary connection line"""
        if self.temp_line and self.start_device:
            start_pos = self.start_device.scenePos()
            self.temp_line.setLine(start_pos.x(), start_pos.y(), pos.x(), pos.y())
    
    def complete_connection(self, end_device):
        """Complete connection to end device"""
        if self.start_device and end_device and self.start_device != end_device:
            # Check if connection already exists
            existing = self.find_connection(self.start_device, end_device)
            if not existing:
                # Determine connection type
                connection_type = self.get_connection_type(self.start_device, end_device)
                
                if connection_type in ['wifi', 'bluetooth', 'zigbee']:
                    connection = WirelessSignal(self.start_device, end_device, connection_type)
                else:
                    # Check if it makes sense to connect these devices with cable
                    # Prevent laptop-to-laptop direct cable (unless it's for special purposes)
                    if (self.start_device.device_type == 'laptop' and end_device.device_type == 'laptop') or \
                       (self.start_device.device_type == 'smartphone' and end_device.device_type == 'smartphone'):
                        # These should typically be wireless
                        connection = WirelessSignal(self.start_device, end_device, 'bluetooth')
                    else:
                        connection = NetworkCable(self.start_device, end_device)
                
                # Add to scene and track
                self.scene.addItem(connection)
                self.connections.append({
                    'connection': connection,
                    'device1': self.start_device,
                    'device2': end_device
                })
                
                # Update simulator
                if hasattr(self.scene, 'parent') and hasattr(self.scene.parent(), 'simulator'):
                    self.scene.parent().simulator.add_connection(self.start_device, end_device)
                
                # Update device tree
                if hasattr(self.scene.views()[0], 'window'):
                    main_window = self.scene.views()[0].window()
                    if hasattr(main_window, 'update_device_tree'):
                        main_window.update_device_tree()
        
        self.cancel_connection()
    
    def cancel_connection(self):
        """Cancel current connection"""
        if self.temp_line:
            self.scene.removeItem(self.temp_line)
            self.temp_line = None
        
        self.connection_mode = False
        self.start_device = None
    
    def find_connection(self, device1, device2):
        """Find existing connection between devices"""
        for conn in self.connections:
            if (conn['device1'] == device1 and conn['device2'] == device2) or \
               (conn['device1'] == device2 and conn['device2'] == device1):
                return conn
        return None
    
    def remove_connection(self, device1, device2):
        """Remove connection between devices"""
        conn = self.find_connection(device1, device2)
        if conn:
            self.scene.removeItem(conn['connection'])
            self.connections.remove(conn)
            
            # Update device tree
            if hasattr(self.scene.views()[0], 'window'):
                main_window = self.scene.views()[0].window()
                if hasattr(main_window, 'update_device_tree'):
                    main_window.update_device_tree()
    
    def update_all_connections(self):
        """Update all connection positions"""
        for conn in self.connections:
            conn['connection'].update_cable() if hasattr(conn['connection'], 'update_cable') else conn['connection'].update_signal()
    
    def _is_wireless_device(self, device):
        """Check if device is wireless capable"""
        wireless_types = ['access_point', 'wireless_router', 'smartphone', 'tablet', 'laptop', 
                         'smart_speaker', 'smart_light', 'iot_sensor', 'ip_camera', 'smart_hub']
        return device.device_type in wireless_types
    
    def get_connection_type(self, device1, device2):
        """Determine the type of connection between two devices"""
        # If either is an access point or wireless router, it's WiFi
        if device1.device_type in ['access_point', 'wireless_router'] or \
           device2.device_type in ['access_point', 'wireless_router']:
            return 'wifi'
        
        # If both are wireless capable devices, determine by device types
        if self._is_wireless_device(device1) and self._is_wireless_device(device2):
            # IoT devices use different protocols
            iot_types = ['iot_sensor', 'smart_light', 'smart_speaker', 'smart_hub']
            if device1.device_type in iot_types or device2.device_type in iot_types:
                return 'zigbee'  # Could be Zigbee, Thread, or Bluetooth LE
            
            # Mobile devices might use Bluetooth
            mobile_types = ['smartphone', 'tablet', 'laptop']
            if device1.device_type in mobile_types and device2.device_type in mobile_types:
                return 'bluetooth'
            
            return 'wifi'
        
        # Default to ethernet for wired connections
        return 'ethernet'