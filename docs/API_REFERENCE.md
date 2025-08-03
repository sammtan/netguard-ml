# NetGuard ML - API Reference

## Core APIs

### NetworkDevice

Base class for all network devices.

```python
class NetworkDevice(QGraphicsItem):
    """Base class for network devices"""
    
    def __init__(self, device_id: str, position: QPointF, device_type: str)
    def start() -> None
    def stop() -> None
    def send_packet(destination: str, protocol: str, info: str = "") -> None
    def receive_packet(packet: Dict) -> None
    def process_packet(packet: Dict) -> None  # Override in subclasses
```

### NetworkSimulator

Main simulation engine.

```python
class NetworkSimulator(QObject):
    # Signals
    packet_sent = Signal(dict)
    traffic_update = Signal(dict)
    
    def __init__(self)
    def add_device(device: NetworkDevice) -> None
    def remove_device(device: NetworkDevice) -> None
    def start() -> None
    def stop() -> None
    def send_packet(packet: Dict) -> None
```

### NetworkAI

AI analysis engine.

```python
class NetworkAI:
    def __init__(self)
    def analyze_packet(packet: Dict) -> Dict
    def train_ml_models(labeled_data: List[Dict] = None) -> bool
    def add_threat_label(packet: Dict, threat_type: str) -> None
    def calculate_network_health() -> float
    def save_ml_models(directory: str) -> None
    def load_ml_models(directory: str) -> None
```

## Packet Format

Standard packet structure used throughout the system:

```python
packet = {
    'source': str,           # Source device ID
    'destination': str,      # Destination device ID  
    'protocol': str,         # Protocol name (TCP, UDP, ICMP, etc.)
    'port': int,            # Destination port (optional)
    'size': int,            # Packet size in bytes (optional)
    'info': str,            # Human-readable description (optional)
    'timestamp': datetime,   # Packet timestamp (auto-added)
    'source_type': str,     # Source device type (auto-added)
    'destination_type': str # Destination device type (auto-added)
}
```

## ML Model APIs

### NetworkAnomalyDetector

```python
class NetworkAnomalyDetector:
    def __init__(self)
    def extract_features(packet: Dict) -> np.ndarray
    def train(training_data: List[Dict] = None) -> bool
    def predict(packet: Dict) -> Dict
    def add_labeled_threat(packet: Dict, threat_label: str) -> None
    def save_model(path: str) -> None
    def load_model(path: str) -> bool
```

### Prediction Format

```python
prediction = {
    'is_anomaly': bool,        # True if anomaly detected
    'anomaly_score': float,    # 0-100 anomaly score
    'threat_type': str,        # Classified threat type
    'confidence': float,       # Classification confidence (0-1)
    'cluster': int            # Assigned cluster ID
}
```

## UI Component APIs

### AIMonitorWidget

```python
class AIMonitorWidget(QWidget):
    # Signals
    alert_generated = Signal(str, str)  # severity, message
    
    def __init__(self)
    def start_monitoring() -> None
    def stop_monitoring() -> None
    def update_traffic(packet_data: Dict) -> None
    def add_insight(message: str, severity: str = "info") -> None
```

### NetworkCanvas

```python
class NetworkCanvas(QGraphicsView):
    # Signals
    device_added = Signal(NetworkDevice)
    connection_made = Signal(NetworkDevice, NetworkDevice)
    
    def __init__(self, simulator: NetworkSimulator)
    def add_device(device_type: str, position: QPointF) -> NetworkDevice
    def handle_cable_connection(device1: NetworkDevice, device2: NetworkDevice) -> None
```

## File Format APIs

### NetworkFileFormat

```python
class NetworkFileFormat:
    @staticmethod
    def save_to_file(file_path: str, devices: List, connections: List) -> bool
    
    @staticmethod
    def load_from_file(file_path: str) -> Dict[str, Any]
    
    @staticmethod
    def validate_file_data(file_data: Dict[str, Any]) -> bool
```

### File Structure

```json
{
    "metadata": {
        "version": "1.0",
        "created": "ISO-8601 timestamp",
        "application": "NetGuard ML",
        "description": "Optional description"
    },
    "network": {
        "devices": [
            {
                "id": "device_0",
                "type": "router|switch|server|...",
                "hostname": "device_name",
                "ip_address": "192.168.1.1",
                "position": {"x": 0, "y": 0},
                "identity": {
                    "mac_address": "AA:BB:CC:DD:EE:FF",
                    "manufacturer": "Vendor",
                    "model": "Model",
                    "serial_number": "SN123",
                    "firmware_version": "1.0"
                },
                "is_running": true
            }
        ],
        "connections": [
            {
                "device1": "device_0",
                "device2": "device_1",
                "type": "ethernet|wireless"
            }
        ]
    }
}
```

## Report Generation APIs

### NetworkReportGenerator

```python
class NetworkReportGenerator:
    def __init__(self)
    
    def generate_full_report(
        scenario_name: str, 
        simulation_data: Dict
    ) -> Dict
    
    def generate_graphical_pdf(
        scenario_name: str,
        data: Dict,
        image_path: str
    ) -> str
    
    def generate_narrative_pdf(
        scenario_name: str,
        data: Dict
    ) -> str
```

### Report Data Format

```python
simulation_data = {
    'scenario_name': str,
    'total_packets': int,
    'total_threats': int,
    'duration': float,  # minutes
    'accuracy': float,  # 0-1
    'mttd': float,      # seconds
    'events': List[Dict],
    'anomaly_scores': List[Dict],
    'attack_phases': List[Dict],
    'ml_metrics': Dict[str, Dict],
    'threat_types': Dict[str, int],
    'affected_devices': List[str],
    'attack_vectors': List[str],
    'ml_insights': List[str],
    'final_recommendations': List[str]
}
```

## Event System

### Common Signals

```python
# Device events
device.state_changed = Signal(bool)  # running state
device.packet_received = Signal(dict)
device.packet_sent = Signal(dict)

# Simulator events  
simulator.simulation_started = Signal()
simulator.simulation_stopped = Signal()
simulator.packet_sent = Signal(dict)
simulator.traffic_update = Signal(dict)

# AI events
ai_monitor.alert_generated = Signal(str, str)
ai_monitor.anomaly_detected = Signal(dict)
```

### Connecting to Signals

```python
# Example: Monitor all packets
def on_packet(packet_data):
    print(f"Packet from {packet_data['source']} to {packet_data['destination']}")

simulator.packet_sent.connect(on_packet)
```

## Extension Points

### Custom Device Types

```python
from src.devices.base_device import NetworkDevice

class CustomDevice(NetworkDevice):
    def __init__(self):
        super().__init__("custom_device")
        
    def process_packet(self, packet: Dict) -> None:
        # Custom packet processing logic
        if packet['protocol'] == 'CUSTOM':
            self.send_packet(packet['source'], 'CUSTOM_REPLY')
```

### Custom ML Models

```python
from src.ai.ml_models import BaseDetector

class CustomDetector(BaseDetector):
    def train(self, data: List[Dict]) -> bool:
        # Custom training logic
        return True
        
    def predict(self, packet: Dict) -> Dict:
        # Custom prediction logic
        return {
            'is_anomaly': False,
            'confidence': 0.95
        }
```

### Custom Reports

```python
def generate_custom_report(data: Dict) -> str:
    # Process simulation data
    # Generate custom visualizations
    # Return report path
    pass

# Register with report generator
report_gen.custom_reports['my_report'] = generate_custom_report
```

## Usage Examples

### Basic Network Setup

```python
# Create simulator
sim = NetworkSimulator()

# Add devices
router = Router()
router.setPos(0, 0)
sim.add_device(router)

switch = Switch()
switch.setPos(200, 0)
sim.add_device(switch)

# Create connection
connection_mgr = ConnectionManager(scene)
connection_mgr.create_connection(router, switch)

# Start simulation
sim.start()
```

### ML Training

```python
# Generate training data
generator = TrainingDataGenerator()
normal_traffic = generator.generate_normal_traffic(1000)
attack_traffic = generator.generate_attack_traffic('ddos', 200)

# Train models
ai = NetworkAI()
ai.train_ml_models(normal_traffic + attack_traffic)

# Save trained models
ai.save_ml_models('models/')
```

### Packet Analysis

```python
# Analyze single packet
packet = {
    'source': 'workstation_1',
    'destination': 'server_1',
    'protocol': 'HTTP',
    'port': 80,
    'info': 'GET /index.html'
}

result = ai.analyze_packet(packet)
print(f"Threat Level: {result['threat_level']}")
print(f"Anomaly Score: {result['anomaly_score']}")
```