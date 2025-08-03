"""
Security devices
"""

from PySide6.QtGui import QColor
from src.devices.base_device import NetworkDevice
from src.ui.theme import COLORS


class Firewall(NetworkDevice):
    """Network firewall"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "firewall")
        self.rules = []
        self.blocked_ips = set()
        self.allowed_ports = {80, 443, 22, 21}
    
    def update_visual_properties(self):
        """Update visual properties"""
        self.color = QColor(COLORS['device_firewall'])
        self.icon = "🛡️"
        self.size = 65
    
    def receive_packet(self, packet: dict):
        """Filter packets based on rules"""
        # Check if source is blocked
        if packet.get('source') in self.blocked_ips:
            return  # Drop packet
        
        # Check port rules
        port = packet.get('port', 0)
        if port > 0 and port not in self.allowed_ports:
            return  # Drop packet
        
        # Forward allowed packets
        if packet['protocol'] == 'ICMP' and packet['destination'] == self.ip_address:
            self.send_packet(packet['source'], 'ICMP', 'ping_reply')


class VPNGateway(NetworkDevice):
    """VPN gateway device"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "vpn")
        self.color = QColor(0, 100, 100)  # Teal
        self.icon = "🔐"
        self.tunnels = []
        self.encryption_type = "AES-256"
    
    def receive_packet(self, packet: dict):
        """Handle VPN tunneling"""
        if packet.get('encrypted'):
            # Decrypt and forward
            pass
        else:
            # Encrypt and tunnel
            pass


class IDSDevice(NetworkDevice):
    """Intrusion Detection System"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "ids_ips")
        self.color = QColor(255, 140, 0)  # Dark orange
        self.icon = "🚨"
        self.signatures = []
        self.alerts = []
        self.threat_level = 0
    
    def receive_packet(self, packet: dict):
        """Analyze packets for threats"""
        # Simple threat detection
        if packet.get('data', '').lower() in ['attack', 'exploit', 'malware']:
            self.threat_level += 10
            self.alerts.append(f"Threat detected from {packet.get('source')}")


class ProxyServer(NetworkDevice):
    """Proxy server"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "proxy")
        self.color = QColor(128, 128, 0)  # Olive
        self.icon = "🔒"
        self.cache = {}
        self.blocked_sites = set()
    
    def receive_packet(self, packet: dict):
        """Handle proxy requests"""
        if packet['protocol'] == 'HTTP':
            url = packet.get('url', '')
            if url in self.cache:
                # Return cached response
                self.send_packet(packet['source'], 'HTTP', self.cache[url])
            else:
                # Forward request
                pass


class NACDevice(NetworkDevice):
    """Network Access Control device"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "nac")
        self.color = QColor(75, 0, 130)  # Indigo
        self.icon = "🗝️"
        self.authorized_devices = set()
        self.quarantine_vlan = 999