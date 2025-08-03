"""
Network simulation engine
"""

from PySide6.QtCore import QObject, QTimer, Signal
import random
from typing import List, Dict


class NetworkSimulator(QObject):
    """Core network simulation engine"""
    
    packet_sent = Signal(dict)  # Emitted when packet is sent
    traffic_update = Signal(dict)  # Emitted for traffic updates
    
    def __init__(self):
        super().__init__()
        self.devices = []
        self.connections = []
        self.running = False
        
        # Simulation timer
        self.sim_timer = QTimer()
        self.sim_timer.timeout.connect(self.simulate_step)
    
    def add_device(self, device):
        """Add a device to the simulation"""
        self.devices.append(device)
        device.simulator = self
    
    def add_connection(self, device1, device2):
        """Add a connection between devices"""
        self.connections.append((device1, device2))
    
    def start(self):
        """Start the simulation"""
        self.running = True
        self.sim_timer.start(1000)  # Run every second
        
        # Initialize devices
        for device in self.devices:
            device.start()
    
    def stop(self):
        """Stop the simulation"""
        self.running = False
        self.sim_timer.stop()
        
        # Stop devices
        for device in self.devices:
            device.stop()
    
    def simulate_step(self):
        """Perform one simulation step"""
        if not self.running:
            return
        
        # Let devices generate their own traffic
        for device in self.devices:
            if hasattr(device, 'generate_traffic') and random.random() < 0.3:
                device.generate_traffic()
        
        # Generate general network traffic
        if len(self.devices) >= 2 and random.random() < 0.7:
            # Pick random source and destination
            source = random.choice(self.devices)
            dest = random.choice([d for d in self.devices if d != source])
            
            # Generate device-specific packet types
            packet_types = self.get_packet_types_for_device(source)
            
            if packet_types:
                protocol, info_template, port = random.choice(packet_types)
                
                # Create packet
                packet = {
                    'source': source.device_id,
                    'source_ip': source.ip_address,
                    'destination': dest.device_id,
                    'destination_ip': dest.ip_address,
                    'protocol': protocol,
                    'port': port,
                    'info': info_template.format(
                        source=source.device_id,
                        dest=dest.device_id
                    )
                }
                
                # Emit packet
                self.packet_sent.emit(packet)
                
                # Update traffic stats
                self.traffic_update.emit({
                    'packet_count': 1,
                    'protocol': protocol
                })
                
                # Deliver to destination
                dest.receive_packet(packet)
    
    def get_packet_types_for_device(self, device):
        """Get appropriate packet types based on device type"""
        base_packets = [
            ('ARP', 'Who has {dest}? Tell {source}', 0),
            ('ICMP', 'Echo request', 0),
        ]
        
        device_specific = {
            'pc': [('HTTP', 'GET /page', 80), ('HTTPS', 'Secure request', 443), ('DNS', 'Query: google.com', 53)],
            'laptop': [('HTTP', 'GET /api/data', 80), ('SSH', 'Connection request', 22), ('RDP', 'Remote desktop', 3389)],
            'smartphone': [('HTTPS', 'Mobile app API call', 443), ('MQTT', 'IoT message', 1883)],
            'server': [('HTTP', '200 OK Response', 80), ('HTTPS', 'API Response', 443)],
            'web_server': [('HTTP', 'Serving index.html', 80), ('HTTPS', 'Serving secure content', 443)],
            'database': [('MySQL', 'Query response', 3306), ('PostgreSQL', 'Data returned', 5432)],
            'mail_server': [('SMTP', 'Mail delivery', 25), ('IMAP', 'Mail fetch', 143)],
            'firewall': [('LOG', 'Packet filtered', 0), ('ALERT', 'Threat detected', 0)],
            'router': [('BGP', 'Route update', 179), ('OSPF', 'Hello packet', 89)],
            'switch': [('STP', 'Spanning tree', 0), ('VLAN', 'Tagged frame', 0)],
            'ip_camera': [('RTP', 'Video stream', 5004), ('RTSP', 'Stream control', 554)],
            'iot_sensor': [('MQTT', 'Sensor data: temp=25°C', 1883), ('CoAP', 'Sensor update', 5683)],
            'voip': [('SIP', 'Call setup', 5060), ('RTP', 'Voice data', 5004)],
            'cloud': [('REST', 'API response: {"status": "ok"}', 443), ('WebSocket', 'Real-time update', 443)],
        }
        
        specific = device_specific.get(device.device_type, [])
        return base_packets + specific
    
    def send_packet(self, source, destination_ip, protocol, data):
        """Send a packet between devices"""
        # Find destination device by IP
        dest_device = None
        for device in self.devices:
            if device.ip_address == destination_ip:
                dest_device = device
                break
        
        if not dest_device:
            return
        
        packet = {
            'source': source.device_id,
            'source_ip': source.ip_address,
            'destination': dest_device.device_id,
            'destination_ip': destination_ip,
            'protocol': protocol,
            'info': data
        }
        
        self.packet_sent.emit(packet)
        
        # Deliver to destination
        dest_device.receive_packet(packet)
    
    def get_random_device(self):
        """Get a random device from the network"""
        if self.devices:
            return random.choice(self.devices)
        return None
    
    def find_device_by_type(self, device_type):
        """Find first device of given type"""
        for device in self.devices:
            if device.device_type == device_type:
                return device
        return None
    
    def remove_device(self, device):
        """Remove a device from the simulation"""
        if device in self.devices:
            self.devices.remove(device)
            # Remove any connections involving this device
            self.connections = [(d1, d2) for d1, d2 in self.connections 
                               if d1 != device and d2 != device]
    
    def send_ping(self, source_device, target_device):
        """Send a ping from source to target device"""
        # Create ping packet
        packet = {
            'source': source_device.device_id,
            'source_ip': source_device.ip_address,
            'destination': target_device.device_id,
            'destination_ip': target_device.ip_address,
            'protocol': 'ICMP',
            'port': 0,
            'info': f'Echo (ping) request from {source_device.device_id} to {target_device.device_id}'
        }
        
        # Emit the packet
        self.packet_sent.emit(packet)
        
        # Simulate ping response after a short delay
        QTimer.singleShot(100, lambda: self.send_ping_reply(target_device, source_device))
    
    def send_ping_reply(self, source_device, target_device):
        """Send a ping reply"""
        # Create reply packet
        packet = {
            'source': source_device.device_id,
            'source_ip': source_device.ip_address,
            'destination': target_device.device_id,
            'destination_ip': target_device.ip_address,
            'protocol': 'ICMP',
            'port': 0,
            'info': f'Echo (ping) reply from {source_device.device_id} to {target_device.device_id}'
        }
        
        # Emit the packet
        self.packet_sent.emit(packet)