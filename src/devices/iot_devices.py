"""
IoT and smart devices
"""

import random
from PySide6.QtGui import QColor
from src.devices.base_device import NetworkDevice


class SmartHub(NetworkDevice):
    """Smart home hub"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "smart_hub")
        self.color = QColor(50, 150, 150)  # Turquoise
        self.icon = "🏠"
        self.connected_devices = []
        self.automations = []
    
    def receive_packet(self, packet: dict):
        """Handle IoT device commands"""
        if packet['protocol'] == 'MQTT':
            # Route to appropriate device
            pass


class IPCamera(NetworkDevice):
    """IP security camera"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "ip_camera")
        self.color = QColor(100, 100, 150)
        self.icon = "📹"
        self.streaming = True
        self.resolution = "1080p"
        self.fps = 30
    
    def generate_traffic(self):
        """Generate video stream traffic"""
        if self.streaming and self.simulator:
            # Simulate video stream
            for _ in range(self.fps // 10):  # Send packets
                target = self.simulator.get_random_device()
                if target and target != self:
                    self.send_packet(target.ip_address, 'RTP', f'video_frame_{random.randint(1, 1000)}')


class IoTSensor(NetworkDevice):
    """Generic IoT sensor"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "iot_sensor")
        self.color = QColor(150, 150, 50)
        self.icon = "🌡️"
        self.sensor_type = random.choice(['temperature', 'humidity', 'motion', 'door'])
        self.value = random.randint(20, 30)
    
    def generate_traffic(self):
        """Send sensor data periodically"""
        if self.simulator:
            # Update sensor value
            self.value += random.randint(-2, 2)
            # Send to hub
            hub = self.simulator.find_device_by_type('smart_hub')
            if hub:
                self.send_packet(hub.ip_address, 'MQTT', f'{self.sensor_type}:{self.value}')


class SmartLight(NetworkDevice):
    """Smart light bulb"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "smart_light")
        self.color = QColor(255, 255, 100)  # Light yellow
        self.icon = "💡"
        self.is_on = True
        self.brightness = 100
        self.color_temp = 3000
    
    def receive_packet(self, packet: dict):
        """Handle light commands"""
        if packet['protocol'] == 'MQTT':
            cmd = packet.get('data', '')
            if cmd == 'turn_on':
                self.is_on = True
            elif cmd == 'turn_off':
                self.is_on = False


class SmartSpeaker(NetworkDevice):
    """Smart speaker/assistant"""
    
    def __init__(self, device_id: str, position):
        super().__init__(device_id, position, "smart_speaker")
        self.color = QColor(80, 80, 200)  # Blue
        self.icon = "🔊"
        self.is_listening = False
        self.volume = 50
    
    def generate_traffic(self):
        """Generate voice assistant traffic"""
        if self.is_listening and self.simulator:
            # Simulate voice queries
            cloud = self.simulator.find_device_by_type('cloud')
            if cloud:
                self.send_packet(cloud.ip_address, 'HTTPS', 'voice_query_data')