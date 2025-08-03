"""
Specialized network devices
"""

import random
from PySide6.QtGui import QColor
from src.devices.base_device import NetworkDevice


class CloudService(NetworkDevice):
    """Cloud service endpoint"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "cloud")
        self.color = QColor(135, 206, 235)  # Sky blue
        self.icon = "☁️"
        self.services = ['SaaS', 'PaaS', 'IaaS']
        self.api_calls = 0
        self.storage_used = 0
    
    def receive_packet(self, packet: dict):
        """Handle cloud API requests"""
        if packet['protocol'] in ['HTTPS', 'REST']:
            self.api_calls += 1
            # Simulate API response
            self.send_packet(packet['source'], 'HTTPS', f'{{\"status\": \"ok\", \"data\": {random.randint(1, 100)}}}')


class SatelliteLink(NetworkDevice):
    """Satellite communication link"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "satellite")
        self.color = QColor(64, 64, 64)  # Dark gray
        self.icon = "📡"
        self.latency_ms = random.randint(500, 800)
        self.signal_strength = random.randint(60, 100)
    
    def receive_packet(self, packet: dict):
        """Handle satellite communication with high latency"""
        # Add latency simulation
        super().receive_packet(packet)


class VoIPPhone(NetworkDevice):
    """VoIP telephone"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "voip")
        self.color = QColor(0, 128, 0)  # Green
        self.icon = "📞"
        self.extension = f"{random.randint(1000, 9999)}"
        self.in_call = False
        self.codec = "G.711"
    
    def generate_traffic(self):
        """Generate VoIP traffic when in call"""
        if self.in_call and self.simulator:
            # Simulate RTP voice packets
            target = self.simulator.get_random_device()
            if target and target != self:
                for _ in range(50):  # 50 packets/sec for voice
                    self.send_packet(target.ip_address, 'RTP', f'voice_packet_{random.randint(1, 1000)}')


class LoadBalancer(NetworkDevice):
    """Load balancer"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "load_balancer")
        self.color = QColor(255, 165, 0)  # Orange
        self.icon = "🎛️"
        self.backend_servers = []
        self.algorithm = "round_robin"
        self.current_index = 0
    
    def receive_packet(self, packet: dict):
        """Distribute load across backend servers"""
        if packet['protocol'] in ['HTTP', 'HTTPS']:
            if self.backend_servers:
                # Round-robin distribution
                target = self.backend_servers[self.current_index % len(self.backend_servers)]
                self.current_index += 1
                # Forward to backend
                self.send_packet(target, packet['protocol'], packet.get('data', ''))


class NASStorage(NetworkDevice):
    """Network Attached Storage"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "nas")
        self.color = QColor(70, 70, 70)  # Dark gray
        self.icon = "💾"
        self.capacity_tb = random.randint(1, 20)
        self.used_tb = random.uniform(0, self.capacity_tb)
        self.raid_level = random.choice(['RAID0', 'RAID1', 'RAID5', 'RAID10'])
    
    def receive_packet(self, packet: dict):
        """Handle storage requests"""
        if packet['protocol'] in ['SMB', 'NFS', 'iSCSI']:
            # Simulate file operation
            operation = random.choice(['read', 'write'])
            self.send_packet(packet['source'], packet['protocol'], f'{operation}_complete')


class UPSDevice(NetworkDevice):
    """Uninterruptible Power Supply"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "ups")
        self.color = QColor(50, 50, 50)  # Very dark gray
        self.icon = "🔋"
        self.battery_level = random.randint(80, 100)
        self.load_percentage = random.randint(20, 80)
        self.on_battery = False
        self.runtime_minutes = random.randint(10, 60)
    
    def generate_traffic(self):
        """Send UPS status updates"""
        if self.simulator:
            # Send SNMP traps for power events
            if self.on_battery or self.battery_level < 20:
                target = self.simulator.find_device_by_type('server')
                if target:
                    self.send_packet(target.ip_address, 'SNMP', f'ups_alert:battery_{self.battery_level}%')