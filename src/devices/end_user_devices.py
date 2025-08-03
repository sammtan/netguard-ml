"""
End user devices
"""

import random
from PySide6.QtGui import QColor
from src.devices.base_device import NetworkDevice
from src.ui.theme import COLORS


class PC(NetworkDevice):
    """Personal computer"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "pc")
    
    def update_visual_properties(self):
        """Update visual properties"""
        self.color = QColor(COLORS['device_pc'])
        self.icon = "🖥️"
        self.size = 60
    
    def receive_packet(self, packet: dict):
        """Handle received packets"""
        if packet['protocol'] == 'ICMP' and packet['destination'] == self.ip_address:
            self.send_packet(packet['source'], 'ICMP', 'ping_reply')


class Laptop(NetworkDevice):
    """Laptop computer"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "laptop")
    
    def update_visual_properties(self):
        """Update visual properties"""
        self.color = QColor(COLORS['device_pc']).darker(120)
        self.icon = "💻"
        self.size = 55
    
    def receive_packet(self, packet: dict):
        """Handle received packets"""
        if packet['protocol'] == 'ICMP' and packet['destination'] == self.ip_address:
            self.send_packet(packet['source'], 'ICMP', 'ping_reply')


class Smartphone(NetworkDevice):
    """Smartphone device"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "smartphone")
        self.battery_level = random.randint(20, 100)
    
    def update_visual_properties(self):
        """Update visual properties"""
        self.color = QColor(50, 50, 50)
        self.icon = "📱"
        self.size = 50
    
    def receive_packet(self, packet: dict):
        """Handle received packets"""
        if packet['protocol'] == 'ICMP' and packet['destination'] == self.ip_address:
            self.send_packet(packet['source'], 'ICMP', 'ping_reply')


class Tablet(NetworkDevice):
    """Tablet device"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "tablet")
        self.battery_level = random.randint(30, 100)
    
    def update_visual_properties(self):
        """Update visual properties"""
        self.color = QColor(60, 60, 60)
        self.icon = "📱"
        self.size = 55


class Printer(NetworkDevice):
    """Network printer"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "printer")
        self.print_queue = []
    
    def update_visual_properties(self):
        """Update visual properties"""
        self.color = QColor(200, 200, 200)
        self.icon = "🖨️"
        self.size = 55
    
    def receive_packet(self, packet: dict):
        """Handle print jobs"""
        if packet['protocol'] == 'TCP' and packet.get('port') == 9100:
            self.print_queue.append(packet['data'])