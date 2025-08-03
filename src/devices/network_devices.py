"""
Network infrastructure devices
"""

from PySide6.QtGui import QColor
from src.devices.base_device import NetworkDevice
from src.ui.theme import COLORS


class Router(NetworkDevice):
    """Router device"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "router")
        self.routing_table = {}
        self.interfaces = []
    
    def update_visual_properties(self):
        """Update visual properties"""
        self.color = QColor(COLORS['device_router'])
        self.icon = "📡"
        self.size = 70
    
    def receive_packet(self, packet: dict):
        """Route packets based on destination"""
        if packet['protocol'] == 'ICMP':
            # Respond to ping if we're the target
            if packet['destination'] == self.ip_address:
                self.send_packet(packet['source'], 'ICMP', 'ping_reply')
        else:
            # Route to next hop
            pass


class Switch(NetworkDevice):
    """Layer 2 switch device"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "switch")
        self.mac_table = {}
    
    def update_visual_properties(self):
        """Update visual properties"""
        self.color = QColor(COLORS['device_switch'])
        self.icon = "🔀"
        self.size = 65
    
    def receive_packet(self, packet: dict):
        """Forward packets based on MAC address"""
        # Simplified switching logic
        pass


class Hub(NetworkDevice):
    """Network hub (broadcasts to all)"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "hub")
    
    def update_visual_properties(self):
        """Update visual properties"""
        self.color = QColor(150, 100, 50)  # Brown
        self.icon = "🔁"
        self.size = 60
    
    def receive_packet(self, packet: dict):
        """Broadcast to all connected devices"""
        pass


class Bridge(NetworkDevice):
    """Network bridge"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "bridge")
    
    def update_visual_properties(self):
        """Update visual properties"""
        self.color = QColor(100, 100, 150)  # Light purple
        self.icon = "🌉"
        self.size = 60


class AccessPoint(NetworkDevice):
    """Wireless access point"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "access_point")
        self.ssid = f"AP_{self.identity.hostname}"
        self.channel = 6
    
    def update_visual_properties(self):
        """Update visual properties"""
        self.color = QColor(100, 150, 200)  # Light blue
        self.icon = "📶"
        self.size = 65


class WirelessRouter(Router):
    """Wireless router (router + AP)"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position)
        self.device_type = "wireless_router"
        self.ssid = f"WiFi_{self.identity.hostname}"
        self.channel = 11
    
    def update_visual_properties(self):
        """Update visual properties"""
        super().update_visual_properties()
        self.icon = "📡"