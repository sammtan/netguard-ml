"""
Server devices
"""

import random
from PySide6.QtGui import QColor
from src.devices.base_device import NetworkDevice
from src.ui.theme import COLORS


class Server(NetworkDevice):
    """Generic server"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "server")
        self.services = []
    
    def update_visual_properties(self):
        """Update visual properties"""
        self.color = QColor(COLORS['device_server'])
        self.icon = "🖧"
        self.size = 70
    
    def receive_packet(self, packet: dict):
        """Handle server requests"""
        if packet['protocol'] == 'ICMP' and packet['destination'] == self.ip_address:
            self.send_packet(packet['source'], 'ICMP', 'ping_reply')


class DatabaseServer(Server):
    """Database server"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position)
        self.device_type = "database"
        self.icon = "🗄️"
        self.services = ['MySQL', 'PostgreSQL']
        self.queries_per_second = 0
    
    def receive_packet(self, packet: dict):
        """Handle database queries"""
        super().receive_packet(packet)
        if packet['protocol'] == 'TCP' and packet.get('port') in [3306, 5432]:
            self.queries_per_second += 1
            # Simulate query response
            self.send_packet(packet['source'], 'TCP', f'query_result_{random.randint(1, 100)}')


class WebServer(Server):
    """Web server"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position)
        self.device_type = "web_server"
        self.icon = "🌐"
        self.services = ['HTTP', 'HTTPS']
        self.requests_per_second = 0
    
    def receive_packet(self, packet: dict):
        """Handle HTTP requests"""
        super().receive_packet(packet)
        if packet['protocol'] == 'TCP' and packet.get('port') in [80, 443]:
            self.requests_per_second += 1
            # Simulate HTTP response
            self.send_packet(packet['source'], 'HTTP', '<html>200 OK</html>')


class MailServer(Server):
    """Email server"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position)
        self.device_type = "mail_server"
        self.icon = "📧"
        self.services = ['SMTP', 'IMAP', 'POP3']
        self.mail_queue = []
    
    def receive_packet(self, packet: dict):
        """Handle email traffic"""
        super().receive_packet(packet)
        if packet['protocol'] == 'TCP' and packet.get('port') in [25, 143, 110]:
            self.mail_queue.append(packet['data'])


class FileServer(Server):
    """File server"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position)
        self.device_type = "file_server"
        self.icon = "📁"
        self.services = ['SMB', 'NFS', 'FTP']
        self.storage_used = random.randint(100, 1000)  # GB


class GameServer(Server):
    """Game server"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position)
        self.device_type = "game_server"
        self.icon = "🎮"
        self.services = ['Game Protocol']
        self.players_online = 0
        self.ping_times = {}