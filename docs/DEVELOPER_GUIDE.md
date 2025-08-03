# NetGuard ML - Developer Guide

## Development Philosophy

NetGuard ML was born from the observation that network security tools often treat AI as an afterthought - a checkbox feature rather than a core component. This project takes the opposite approach: AI-first design where every packet, every connection, and every device interaction feeds into a comprehensive machine learning pipeline.

## System Architecture Thinking

### The Three-Layer Approach

```
Presentation Layer (UI)
    ↕
Business Logic Layer (Simulation + AI)
    ↕
Data Layer (Devices + Network State)
```

**Key Design Decisions:**

1. **Separation of Concerns**: The UI knows nothing about ML models. The ML models know nothing about Qt. This allows us to swap implementations without cascading changes.

2. **Event-Driven Architecture**: Everything is an event - packet transmission, device state changes, AI insights. This makes the system naturally asynchronous and scalable.

3. **Modular Device System**: Each device type is self-contained with its own behavior, making it trivial to add new device types without touching core code.

## Core Components Deep Dive

### 1. The AI Engine (`src/ai/network_ai.py`)

The brain of NetGuard ML. It maintains multiple perspectives on network traffic:

```python
# Three-tier analysis approach
self.packet_history      # Raw data collection
self.device_profiles     # Behavioral modeling  
self.connection_graph    # Topology understanding
```

**Design Insight**: Rather than analyzing packets in isolation, we build a contextual understanding. A ping from a workstation is normal; a ping from a printer might be suspicious.

### 2. ML Model Ensemble (`src/ai/ml_models.py`)

We use an ensemble approach because no single model excels at all aspects of network security:

- **Isolation Forest**: Great for finding outliers in normal traffic
- **Random Forest**: Excellent for classifying known attack patterns
- **LSTM**: Captures temporal patterns (e.g., slow port scans)
- **DBSCAN**: Groups similar traffic for pattern discovery

**Key Innovation**: Feature engineering that preserves network semantics:
```python
# Cyclic encoding for time (sin/cos) preserves the circular nature of hours
# Port encoding reflects well-known vs dynamic port ranges
# Device type encoding maintains semantic relationships
```

### 3. Device Architecture (`src/devices/base_device.py`)

Every device inherits from `NetworkDevice`, providing:
- Unique identity management
- Visual representation
- Packet processing pipeline
- State management

**Design Pattern**: Template Method
```python
class NetworkDevice:
    def receive_packet(self, packet):
        # Common preprocessing
        self.process_packet(packet)  # Device-specific logic
        # Common postprocessing
```

### 4. Simulation Engine (`src/simulation/simulator.py`)

The heartbeat of the network. Uses Qt's timer system for deterministic packet processing:

```python
# Pseudo-realtime simulation with configurable speed
self.packet_timer = QTimer()
self.packet_timer.timeout.connect(self.process_packet_queue)
```

**Performance Consideration**: Packet processing is batched to prevent UI freezing while maintaining smooth visualization.

## Development Workflow

### Adding a New Device Type

1. Create device class in appropriate category file:
```python
class QuantumRouter(NetworkDevice):
    def __init__(self):
        super().__init__("quantum_router")
        self.quantum_state = "superposition"
    
    def process_packet(self, packet):
        # Quantum routing logic
        pass
```

2. Register in device toolbar (`src/ui/device_toolbar.py`)
3. Add icon in icon mappings
4. Test with existing scenarios

### Implementing New ML Models

1. Add model class in `ml_models.py`:
```python
class GraphNeuralNetwork:
    def __init__(self):
        # Initialize GNN for topology-aware detection
        pass
    
    def predict(self, packet, topology):
        # Leverage network structure in predictions
        pass
```

2. Integrate into `NetworkMLEngine`
3. Update ensemble weights based on validation performance

### Creating Test Scenarios

The test scenario system (`src/test_scenarios/scenarios.py`) uses a declarative approach:

```python
{
    'name': 'Scenario_Name',
    'network_topology': {
        'devices': [...],  # Device definitions
        'connections': [...]  # Network links
    },
    'attack_phases': [
        {
            'name': 'Phase_Name',
            'packets': generate_packets(),  # Attack traffic
            'expected_detections': [...]  # For validation
        }
    ]
}
```

## Performance Optimization

### Current Bottlenecks & Solutions

1. **Packet Processing**: 
   - Problem: UI freezes with high packet rates
   - Solution: Batch processing with priority queue

2. **ML Inference**:
   - Problem: LSTM is slow for real-time analysis
   - Solution: Sliding window with cached hidden states

3. **Visual Updates**:
   - Problem: Redrawing entire canvas is expensive
   - Solution: Dirty rectangle optimization in Qt

### Profiling Commands

```bash
# Profile the application
python -m cProfile -o profile.stats src/main.py

# Analyze results
python -m pstats profile.stats
```

## API Design Principles

### Packet Format

Packets are dictionaries for flexibility:
```python
packet = {
    'source': 'device_id',
    'destination': 'device_id', 
    'protocol': 'TCP|UDP|ICMP|...',
    'port': 80,
    'size': 1500,
    'info': 'Human-readable description',
    'timestamp': datetime.now()
}
```

### Event System

All components communicate through Qt signals:
```python
# Emitting events
self.packet_sent.emit(packet_data)

# Subscribing to events
simulator.packet_sent.connect(self.on_packet_sent)
```

### File Format

The `.netsim` format is JSON for human readability:
```json
{
    "metadata": {...},
    "network": {
        "devices": [...],
        "connections": [...]
    }
}
```

## Testing Strategy

### Unit Tests (TODO)
```python
def test_anomaly_detection():
    detector = NetworkAnomalyDetector()
    normal_packet = create_normal_packet()
    anomalous_packet = create_ddos_packet()
    
    assert detector.predict(normal_packet)['is_anomaly'] == False
    assert detector.predict(anomalous_packet)['is_anomaly'] == True
```

### Integration Tests
- Load each scenario file
- Run simulation for N seconds
- Verify expected detections occur

### Performance Tests
- Generate 10,000 packets/second
- Measure UI responsiveness
- Profile memory usage

## Future Architecture Considerations

### Distributed Simulation
Split simulation across multiple processes:
- UI Process (main)
- Simulation Process (packet processing)
- AI Process (ML inference)
- Communication via shared memory or ZeroMQ

### Real-time Learning
Implement online learning where models update during simulation:
- Incremental learning algorithms
- Concept drift detection
- Active learning for labeling

### Plugin System
Allow third-party device types and protocols:
```python
# plugins/custom_device.py
class CustomDevice(NetworkDevice):
    pass

# Auto-discovery at startup
load_plugins('plugins/')
```

## Debugging Tips

### Common Issues

1. **"Connection lines don't update"**
   - Check `itemChange` method in device
   - Verify connection manager reference

2. **"ML predictions always low"**
   - Check feature scaling
   - Verify training data distribution

3. **"Icons not loading"**
   - Use absolute paths
   - Check SVG file encoding

### Debug Mode

Enable verbose logging:
```python
# In main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Qt Designer Integration

For rapid UI prototyping:
```bash
pyside6-designer
# Create .ui file
pyside6-uic form.ui -o form_ui.py
```

## Contributing Guidelines

1. **Code Style**: PEP 8 with 100-char line limit
2. **Docstrings**: Google style for all public methods
3. **Type Hints**: Use wherever possible for better IDE support
4. **Testing**: Add tests for new features
5. **Performance**: Profile before and after changes

## The Road Ahead

NetGuard ML is designed to grow. The architecture supports:
- Real network hardware integration via SNMP
- Cloud deployment for distributed monitoring
- Mobile companion app for notifications
- VR visualization for 3D network exploration

Remember: The goal isn't just to detect threats, but to understand them. Every line of code should contribute to that understanding.

---

*"In network security, paranoia is just good planning."* - Ancient SysAdmin Proverb