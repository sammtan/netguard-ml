"""
Device Identity System - Each device has unique properties
"""

import random
import string
import uuid
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class DeviceIdentity:
    """Unique identity for each device"""
    device_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    hostname: str = ""
    mac_address: str = ""
    ip_address: str = ""
    manufacturer: str = ""
    model: str = ""
    serial_number: str = ""
    firmware_version: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.mac_address:
            self.mac_address = self.generate_mac()
        if not self.serial_number:
            self.serial_number = self.generate_serial()


    @staticmethod
    def generate_mac() -> str:
        """Generate random MAC address"""
        mac = [random.randint(0x00, 0xff) for _ in range(6)]
        mac[0] = (mac[0] & 0xfc) | 0x02  # Locally administered
        return ':'.join(f'{byte:02x}' for byte in mac)
    
    @staticmethod
    def generate_serial() -> str:
        """Generate random serial number"""
        prefix = random.choice(['SN', 'S/N', 'SER'])
        numbers = ''.join(random.choices(string.digits, k=8))
        return f"{prefix}-{numbers}"


class DeviceIdentityFactory:
    """Factory for creating device identities based on type"""
    
    # Manufacturer pools for different device types
    MANUFACTURERS = {
        'pc': ['Dell', 'HP', 'Lenovo', 'ASUS', 'Acer', 'MSI'],
        'laptop': ['Apple', 'Dell', 'HP', 'Lenovo', 'ASUS', 'Microsoft'],
        'smartphone': ['Apple', 'Samsung', 'Google', 'OnePlus', 'Xiaomi'],
        'router': ['Cisco', 'Juniper', 'Ubiquiti', 'MikroTik', 'TP-Link', 'Netgear'],
        'switch': ['Cisco', 'Aruba', 'Juniper', 'Dell', 'HP'],
        'firewall': ['Palo Alto', 'Fortinet', 'Check Point', 'SonicWall', 'pfSense'],
        'server': ['Dell', 'HP', 'IBM', 'Supermicro', 'Lenovo'],
        'iot_sensor': ['Honeywell', 'Siemens', 'Bosch', 'Philips', 'Xiaomi'],
        'ip_camera': ['Hikvision', 'Dahua', 'Axis', 'Ubiquiti', 'Nest'],
    }
    
    # Model templates
    MODELS = {
        'pc': {
            'Dell': ['OptiPlex 7090', 'Precision 5820', 'XPS 8940'],
            'HP': ['EliteDesk 800 G8', 'ProDesk 600 G6', 'Z2 Tower G8'],
            'Lenovo': ['ThinkCentre M720', 'IdeaCentre 5i', 'Legion T7'],
        },
        'laptop': {
            'Apple': ['MacBook Pro 16"', 'MacBook Air M2', 'MacBook Pro 14"'],
            'Dell': ['XPS 15', 'Latitude 7420', 'Precision 5560'],
            'HP': ['Spectre x360', 'EliteBook 840 G8', 'ZBook Studio G8'],
        },
        'router': {
            'Cisco': ['ISR 4451', 'ASR 1001-X', 'Catalyst 8200'],
            'Juniper': ['MX204', 'SRX300', 'MX80'],
            'Ubiquiti': ['Dream Machine Pro', 'EdgeRouter 12', 'UDM-SE'],
        },
        'switch': {
            'Cisco': ['Catalyst 9300', 'Nexus 9000', 'Catalyst 2960-X'],
            'Aruba': ['6300M', '5400R', 'CX 8360'],
            'Juniper': ['EX4300', 'QFX5100', 'EX2300'],
        },
        'firewall': {
            'Palo Alto': ['PA-850', 'PA-3260', 'PA-5450'],
            'Fortinet': ['FortiGate 100F', 'FortiGate 600E', 'FortiGate 3000F'],
            'Check Point': ['3200', '6000', '16000'],
        },
        'server': {
            'Dell': ['PowerEdge R750', 'PowerEdge R640', 'PowerEdge T550'],
            'HP': ['ProLiant DL380 Gen10', 'ProLiant ML350', 'Apollo 4200'],
            'IBM': ['Power System S922', 'LinuxONE III', 'Power E1080'],
        },
    }
    
    @classmethod
    def create_identity(cls, device_type: str, custom_name: Optional[str] = None) -> DeviceIdentity:
        """Create a unique device identity"""
        identity = DeviceIdentity()
        
        # Set hostname
        if custom_name:
            identity.hostname = custom_name
        else:
            identity.hostname = cls._generate_hostname(device_type)
        
        # Set manufacturer and model
        identity.manufacturer = cls._get_manufacturer(device_type)
        identity.model = cls._get_model(device_type, identity.manufacturer)
        
        # Set firmware version
        identity.firmware_version = cls._generate_firmware_version(device_type)
        
        # Set device-specific properties
        identity.properties = cls._get_device_properties(device_type)
        
        return identity
    
    @staticmethod
    def _generate_hostname(device_type: str) -> str:
        """Generate appropriate hostname"""
        prefixes = {
            'pc': ['DESKTOP', 'WORKSTATION', 'PC'],
            'laptop': ['LAPTOP', 'NOTEBOOK', 'MOBILE'],
            'smartphone': ['PHONE', 'MOBILE', 'DEVICE'],
            'tablet': ['TABLET', 'PAD', 'SLATE'],
            'printer': ['PRINTER', 'PRN', 'PRINT'],
            'router': ['ROUTER', 'RTR', 'GW'],
            'switch': ['SWITCH', 'SW', 'CORE-SW'],
            'hub': ['HUB', 'CONCENTRATOR'],
            'firewall': ['FW', 'FIREWALL', 'SECURITY'],
            'vpn': ['VPN', 'VPNGW', 'TUNNEL'],
            'server': ['SERVER', 'SRV', 'HOST'],
            'web_server': ['WEB', 'WWW', 'HTTPD'],
            'database': ['DB', 'DATABASE', 'SQL'],
            'mail_server': ['MAIL', 'SMTP', 'EXCHANGE'],
            'file_server': ['FILE', 'NAS', 'STORAGE'],
            'game_server': ['GAME', 'GAMING', 'PLAY'],
            'cloud': ['CLOUD', 'AWS', 'AZURE'],
            'iot_sensor': ['SENSOR', 'IOT', 'DEVICE'],
            'ip_camera': ['CAM', 'CAMERA', 'IPCAM'],
            'smart_hub': ['HUB', 'SMARTHUB', 'HOME'],
            'smart_light': ['LIGHT', 'BULB', 'LAMP'],
            'smart_speaker': ['SPEAKER', 'ALEXA', 'ASSISTANT'],
            'voip': ['VOIP', 'PHONE', 'IP-PHONE'],
            'load_balancer': ['LB', 'LOADBAL', 'BALANCE'],
            'nas': ['NAS', 'STORAGE', 'FILESTORE'],
            'ups': ['UPS', 'POWER', 'BATTERY'],
        }
        
        prefix = random.choice(prefixes.get(device_type, ['DEVICE']))
        suffix = ''.join(random.choices(string.digits, k=4))
        return f"{prefix}-{suffix}"
    
    @classmethod
    def _get_manufacturer(cls, device_type: str) -> str:
        """Get appropriate manufacturer"""
        manufacturers = cls.MANUFACTURERS.get(device_type, ['Generic'])
        return random.choice(manufacturers)
    
    @classmethod
    def _get_model(cls, device_type: str, manufacturer: str) -> str:
        """Get appropriate model"""
        if device_type in cls.MODELS and manufacturer in cls.MODELS[device_type]:
            return random.choice(cls.MODELS[device_type][manufacturer])
        
        # Generic model naming
        type_abbr = device_type[:3].upper()
        return f"{manufacturer} {type_abbr}-{random.randint(1000, 9999)}"
    
    @staticmethod
    def _generate_firmware_version(device_type: str) -> str:
        """Generate firmware version"""
        if device_type in ['router', 'switch', 'firewall']:
            # Network devices often use specific versioning
            major = random.randint(12, 17)
            minor = random.randint(0, 9)
            patch = random.randint(0, 99)
            return f"{major}.{minor}.{patch}"
        elif device_type in ['pc', 'laptop', 'server']:
            # OS versions
            os_versions = ['Windows 11 Pro', 'Windows 10 Enterprise', 'Ubuntu 22.04', 'RHEL 8.5']
            return random.choice(os_versions)
        elif device_type in ['smartphone', 'tablet']:
            # Mobile OS
            ios_ver = f"iOS {random.randint(14, 17)}.{random.randint(0, 6)}"
            android_ver = f"Android {random.randint(11, 14)}"
            return random.choice([ios_ver, android_ver])
        else:
            # Generic versioning
            return f"v{random.randint(1, 9)}.{random.randint(0, 99)}.{random.randint(0, 999)}"
    
    @staticmethod
    def _get_device_properties(device_type: str) -> Dict[str, Any]:
        """Get device-specific properties"""
        properties = {}
        
        if device_type == 'pc' or device_type == 'laptop':
            properties['cpu'] = random.choice(['Intel i7-12700K', 'AMD Ryzen 9 5900X', 'Intel i5-11400'])
            properties['ram_gb'] = random.choice([8, 16, 32, 64])
            properties['storage_gb'] = random.choice([256, 512, 1024, 2048])
            
        elif device_type == 'router':
            properties['interfaces'] = random.randint(4, 48)
            properties['throughput_gbps'] = random.choice([1, 10, 40, 100])
            properties['routing_protocols'] = ['BGP', 'OSPF', 'EIGRP']
            
        elif device_type == 'switch':
            properties['ports'] = random.choice([24, 48, 96])
            properties['port_speed'] = random.choice(['1G', '10G', '25G', '100G'])
            properties['vlans_supported'] = 4096
            
        elif device_type == 'firewall':
            properties['throughput_gbps'] = random.choice([1, 5, 10, 20])
            properties['concurrent_sessions'] = random.randint(100000, 10000000)
            properties['vpn_tunnels'] = random.randint(100, 5000)
            
        elif device_type == 'server':
            properties['cpu_cores'] = random.choice([8, 16, 32, 64, 128])
            properties['ram_gb'] = random.choice([32, 64, 128, 256, 512])
            properties['storage_tb'] = random.choice([2, 4, 8, 16, 32])
            properties['raid_level'] = random.choice(['RAID 0', 'RAID 1', 'RAID 5', 'RAID 10'])
            
        elif device_type == 'iot_sensor':
            properties['sensor_type'] = random.choice(['temperature', 'humidity', 'motion', 'pressure'])
            properties['battery_powered'] = random.choice([True, False])
            properties['wireless_protocol'] = random.choice(['WiFi', 'Zigbee', 'LoRaWAN', 'BLE'])
            
        elif device_type == 'ip_camera':
            properties['resolution'] = random.choice(['720p', '1080p', '4K', '8K'])
            properties['fps'] = random.choice([15, 30, 60])
            properties['night_vision'] = True
            properties['ptz'] = random.choice([True, False])
            
        elif device_type == 'ups':
            properties['capacity_va'] = random.choice([1000, 1500, 3000, 6000, 10000])
            properties['battery_runtime_min'] = random.randint(5, 120)
            properties['outlets'] = random.randint(6, 16)
            
        return properties