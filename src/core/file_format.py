"""
Network topology file format (.netsim)
A human-readable format for saving network simulations
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any


class NetworkFileFormat:
    """
    Handles saving and loading of network topology files
    
    File format (.netsim):
    - JSON-based for human readability
    - Contains metadata, devices, and connections
    - Extensible for future features
    """
    
    VERSION = "1.0"
    FILE_EXTENSION = ".netsim"
    
    @staticmethod
    def create_file_data(devices: List, connections: List) -> Dict[str, Any]:
        """Create file data structure from network topology"""
        # Metadata
        metadata = {
            "version": NetworkFileFormat.VERSION,
            "created": datetime.now().isoformat(),
            "application": "AI Network Simulator",
            "description": "Network topology simulation"
        }
        
        # Devices data
        devices_data = []
        device_id_map = {}  # Map device objects to IDs for connections
        
        for idx, device in enumerate(devices):
            device_id = f"device_{idx}"
            device_id_map[device] = device_id
            
            device_data = {
                "id": device_id,
                "type": device.device_type,
                "hostname": device.device_id,
                "ip_address": device.ip_address,
                "position": {
                    "x": device.pos().x(),
                    "y": device.pos().y()
                },
                "identity": {
                    "mac_address": device.identity.mac_address,
                    "manufacturer": device.identity.manufacturer,
                    "model": device.identity.model,
                    "serial_number": device.identity.serial_number,
                    "firmware_version": device.identity.firmware_version,
                },
                "is_running": device.is_running
            }
            devices_data.append(device_data)
        
        # Connections data
        connections_data = []
        for conn in connections:
            # Determine connection type
            connection_obj = conn['connection']
            conn_type = "ethernet"
            
            if hasattr(connection_obj, 'connection_type'):
                conn_type = connection_obj.connection_type
            elif connection_obj.__class__.__name__ == 'WirelessSignal':
                conn_type = "wireless"
            
            connection_data = {
                "device1": device_id_map.get(conn['device1'], "unknown"),
                "device2": device_id_map.get(conn['device2'], "unknown"),
                "type": conn_type
            }
            connections_data.append(connection_data)
        
        # Complete file structure
        file_data = {
            "metadata": metadata,
            "network": {
                "devices": devices_data,
                "connections": connections_data
            }
        }
        
        return file_data
    
    @staticmethod
    def save_to_file(file_path: str, devices: List, connections: List) -> bool:
        """Save network topology to file"""
        try:
            # Ensure .netsim extension
            if not file_path.endswith(NetworkFileFormat.FILE_EXTENSION):
                file_path += NetworkFileFormat.FILE_EXTENSION
            
            # Create file data
            file_data = NetworkFileFormat.create_file_data(devices, connections)
            
            # Write to file with pretty formatting
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(file_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    @staticmethod
    def load_from_file(file_path: str) -> Dict[str, Any]:
        """Load network topology from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
            
            # Validate version
            version = file_data.get('metadata', {}).get('version', '0.0')
            if not NetworkFileFormat.is_compatible_version(version):
                raise ValueError(f"Incompatible file version: {version}")
            
            return file_data
            
        except Exception as e:
            print(f"Error loading file: {e}")
            return None
    
    @staticmethod
    def is_compatible_version(version: str) -> bool:
        """Check if file version is compatible"""
        # For now, only support exact version match
        # In future, add backward compatibility
        return version == NetworkFileFormat.VERSION
    
    @staticmethod
    def validate_file_data(file_data: Dict[str, Any]) -> bool:
        """Validate file data structure"""
        try:
            # Check required sections
            if 'metadata' not in file_data:
                return False
            if 'network' not in file_data:
                return False
            if 'devices' not in file_data['network']:
                return False
            if 'connections' not in file_data['network']:
                return False
            
            # Validate devices
            for device in file_data['network']['devices']:
                required_fields = ['id', 'type', 'hostname', 'position']
                if not all(field in device for field in required_fields):
                    return False
            
            return True
            
        except Exception:
            return False


class NetworkFileExample:
    """
    Example of the .netsim file format
    """
    
    EXAMPLE = """
{
  "metadata": {
    "version": "1.0",
    "created": "2025-01-03T15:30:00",
    "application": "AI Network Simulator",
    "description": "Example corporate network topology"
  },
  "network": {
    "devices": [
      {
        "id": "device_0",
        "type": "router",
        "hostname": "MainRouter",
        "ip_address": "192.168.1.1",
        "position": {"x": 0, "y": 0},
        "identity": {
          "mac_address": "AA:BB:CC:DD:EE:01",
          "manufacturer": "Cisco",
          "model": "ISR 4321",
          "serial_number": "FCZ1234567",
          "firmware_version": "16.9.1"
        },
        "is_running": true
      },
      {
        "id": "device_1",
        "type": "switch",
        "hostname": "CoreSwitch",
        "ip_address": "192.168.1.2",
        "position": {"x": 150, "y": 0},
        "identity": {
          "mac_address": "AA:BB:CC:DD:EE:02",
          "manufacturer": "Cisco",
          "model": "Catalyst 2960",
          "serial_number": "FCZ2345678",
          "firmware_version": "15.2"
        },
        "is_running": true
      }
    ],
    "connections": [
      {
        "device1": "device_0",
        "device2": "device_1",
        "type": "ethernet"
      }
    ]
  }
}
"""