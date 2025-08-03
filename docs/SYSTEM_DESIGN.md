# NetGuard ML - System Design & Architecture

## Design Philosophy

NetGuard ML embodies three core principles:

1. **Intelligence First**: ML isn't bolted on; it's woven into the fabric of packet processing
2. **Visual Clarity**: Complex network behavior should be immediately understandable
3. **Extensible Architecture**: Adding new capabilities shouldn't require architectural changes

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                  │
│  ┌─────────────┐ ┌──────────────┐ ┌─────────────────┐ │
│  │   Canvas    │ │  AI Monitor  │ │ Device Controls │ │
│  └─────────────┘ └──────────────┘ └─────────────────┘ │
├─────────────────────────────────────────────────────────┤
│                  Business Logic Layer                    │
│  ┌─────────────┐ ┌──────────────┐ ┌─────────────────┐ │
│  │  Simulator  │ │   AI Engine  │ │ Report Generator│ │
│  └─────────────┘ └──────────────┘ └─────────────────┘ │
├─────────────────────────────────────────────────────────┤
│                     Data Layer                          │
│  ┌─────────────┐ ┌──────────────┐ ┌─────────────────┐ │
│  │   Devices   │ │   ML Models  │ │   File System   │ │
│  └─────────────┘ └──────────────┘ └─────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Network Simulation Engine

The simulation engine operates on a discrete event model:

```python
Event Queue → Process Event → Update State → Trigger Side Effects → Next Event
```

**Key Design Decisions:**

- **Deterministic Timing**: Uses Qt timers for reproducible simulations
- **Packet Queue**: Prevents blocking on heavy traffic
- **Device Autonomy**: Each device manages its own state and behavior

### 2. AI/ML Pipeline

```
Packet → Feature Extraction → Model Ensemble → Prediction → Insight Generation
   ↓                                               ↓
Historical Data ←────────────────────────── Update Profiles
```

**Model Ensemble Strategy:**

```python
Ensemble Score = w1*IsolationForest + w2*LSTM + w3*RandomForest + w4*DBSCAN
```

Where weights are dynamically adjusted based on:
- Recent prediction accuracy
- Traffic patterns
- Time of day

### 3. Device System Architecture

```
NetworkDevice (Abstract Base)
    ├── NetworkInfrastructure
    │   ├── Router
    │   ├── Switch
    │   └── AccessPoint
    ├── SecurityDevices
    │   ├── Firewall
    │   └── VPNGateway
    ├── EndUserDevices
    │   ├── Workstation
    │   ├── Laptop
    │   └── Smartphone
    └── SpecializedDevices
        ├── IoTSensor
        ├── IPCamera
        └── SCADAController
```

Each device implements:
- Identity management
- Packet processing logic
- Visual representation
- State persistence

### 4. UI Component Hierarchy

```
QMainWindow
    ├── QToolBar (Actions)
    ├── QSplitter
    │   ├── DeviceTree (Left)
    │   ├── NetworkCanvas (Center)
    │   └── QTabWidget (Right)
    │       ├── AIMonitor
    │       └── PacketViewer
    └── DeviceToolbar (Bottom)
```

## Data Flow Architecture

### Packet Lifecycle

1. **Generation**: User action or simulation triggers packet creation
2. **Queuing**: Packet enters simulator queue with timestamp
3. **Processing**: Simulator dequeues and routes to destination
4. **Analysis**: AI engine analyzes packet in parallel
5. **Visualization**: UI updates to show packet movement
6. **Insight**: AI insights appear in monitor panel

### ML Data Pipeline

```
Raw Packets → Feature Engineering → Model Input
                    ↓
              [15 Features]
              - Temporal (3)
              - Protocol (4)  
              - Device (2)
              - Traffic (6)
                    ↓
            Ensemble Prediction
                    ↓
        Anomaly Score + Threat Class
```

## Performance Architecture

### Threading Model

```
Main Thread (UI)
    ├── Simulation Timer (10ms intervals)
    ├── AI Analysis (Async via QThread)
    └── Report Generation (Separate Process)
```

### Memory Management

- **Packet History**: Circular buffer (last 1000 packets)
- **Device Profiles**: LRU cache with 100 device limit
- **ML Models**: Lazy loading, shared across instances

### Optimization Strategies

1. **Batch Processing**: Group packets for ML inference
2. **Dirty Rectangle**: Only redraw changed canvas areas
3. **Feature Caching**: Reuse computed features for similar packets

## Security Architecture

### Threat Detection Layers

```
Layer 1: Statistical Anomaly (Unsupervised)
    ↓ Suspicious
Layer 2: Pattern Matching (Rules)
    ↓ Likely Threat
Layer 3: ML Classification (Supervised)
    ↓ Confirmed Threat
Layer 4: Behavioral Analysis (Contextual)
    ↓ Threat Intelligence
```

### Defense in Depth

- **Input Validation**: All packet data sanitized
- **Resource Limits**: Prevent DoS via packet flooding
- **Secure Defaults**: Devices start in minimal privilege mode

## Scalability Considerations

### Horizontal Scaling

```
Load Balancer
    ├── Simulator Instance 1 (Subnet A)
    ├── Simulator Instance 2 (Subnet B)
    └── Simulator Instance N (Subnet N)
         ↓
    Aggregated AI Analysis
```

### Vertical Scaling

- **GPU Acceleration**: LSTM/Deep models on CUDA
- **Multiprocessing**: Separate processes for simulation/AI
- **Distributed Training**: Federated learning across instances

## Integration Architecture

### Plugin System

```python
# Plugin Interface
class NetworkPlugin:
    def on_packet(self, packet: Dict) -> Optional[Dict]
    def on_device_add(self, device: NetworkDevice) -> None
    def get_menu_actions(self) -> List[QAction]
```

### External APIs

```
NetGuard ML
    ├── PCAP Import/Export
    ├── Threat Intelligence Feeds
    ├── SIEM Integration (Syslog)
    └── Cloud ML Model Updates
```

## Deployment Architecture

### Desktop Application

```
Installer Package
    ├── Python Runtime
    ├── Qt Libraries
    ├── ML Models
    └── Assets
```

### Docker Container

```dockerfile
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ /app/src/
CMD ["python", "/app/src/main.py"]
```

### Cloud Deployment

```
User → Load Balancer → Web Gateway → Container Cluster
                                         ├── UI Service
                                         ├── Simulation Service
                                         └── AI Service
```

## Future Architecture Evolution

### Phase 1: Real-Time Enhancement
- WebSocket for live updates
- Streaming ML inference
- Real device integration via SNMP

### Phase 2: Distributed Simulation
- Kubernetes orchestration
- Inter-simulator communication
- Global threat correlation

### Phase 3: Advanced AI
- Reinforcement learning for defense
- GAN for attack generation
- Explainable AI dashboard

## Design Patterns Used

1. **Observer Pattern**: Event system for loose coupling
2. **Strategy Pattern**: Swappable ML models
3. **Factory Pattern**: Device creation
4. **Template Method**: Base device behavior
5. **Singleton**: Simulator and AI engine instances
6. **Command Pattern**: User actions as commands

## Architectural Decisions Record (ADR)

### ADR-001: Qt for UI Framework
- **Status**: Accepted
- **Context**: Need cross-platform UI with good performance
- **Decision**: Use Qt (PySide6) for native performance
- **Consequences**: Larger binary size but better UX

### ADR-002: Ensemble ML Approach
- **Status**: Accepted  
- **Context**: Single models insufficient for all attack types
- **Decision**: Ensemble of specialized models
- **Consequences**: Higher complexity but better detection

### ADR-003: JSON File Format
- **Status**: Accepted
- **Context**: Need human-readable persistence format
- **Decision**: JSON over binary formats
- **Consequences**: Larger files but easier debugging

## System Constraints

1. **Performance**: Must handle 1000 packets/second
2. **Memory**: Stay under 500MB RAM usage
3. **Latency**: ML inference < 100ms per packet
4. **Accuracy**: > 90% threat detection rate
5. **Usability**: No more than 3 clicks for any action

---

*"Architecture is about the important stuff. Whatever that is."* - Ralph Johnson