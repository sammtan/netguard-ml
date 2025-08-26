# NetGuard ML ⚠️ NOT READY TO USE

An AI-powered network security simulator that combines visual network building with machine learning-based threat detection. NetGuard ML provides real-time analysis of network traffic patterns, anomaly detection, and intelligent security insights through an ensemble of ML models.

## Core Features

### 1. Visual Network Builder
- Drag-and-drop network devices (routers, switches, PCs, servers)
- Connect devices with different cable types
- Configure device properties visually
- Save/load network topologies

### 2. Network Simulation Engine
- Packet-level simulation
- Support for key protocols (ARP, ICMP, TCP, UDP, HTTP)
- Routing table simulation
- VLAN support
- Real-time packet flow visualization

### 3. AI Monitoring & Analysis
- Live traffic pattern analysis
- Anomaly detection (DDoS, port scans, unusual traffic)
- Performance predictions
- Network optimization suggestions
- Natural language insights

### 4. Device Types
- **Routers**: Static/dynamic routing, NAT
- **Switches**: VLANs, STP, port security  
- **PCs/Laptops**: Generate traffic, run services
- **Servers**: Web, DNS, DHCP simulation
- **Firewalls**: Rule-based filtering

## Technology Stack

- **Frontend**: PySide6 for GUI
- **Simulation**: Custom Python engine
- **Visualization**: NetworkX + Qt Graphics
- **AI/ML**: TensorFlow/scikit-learn for analysis
- **Database**: SQLite for configs

## Key Differences from Packet Tracer

1. **AI Integration**: Real-time ML analysis of traffic
2. **Modern UI**: Clean, dark theme interface
3. **Python-based**: Fully extensible and scriptable
4. **Open Source**: Free and customizable
5. **Focus**: Educational with AI insights

## Installation

```bash
pip install -r requirements.txt
python src/main.py
```

## Usage

1. **Build Network**: Drag devices from palette, connect with cables
2. **Configure**: Right-click devices to set IPs, routes, etc.
3. **Simulate**: Click "Start Simulation" to begin packet flow
4. **Monitor**: Watch AI insights panel for analysis
5. **Test**: Use ping, traceroute tools between devices

## Architecture

```
┌─────────────────────────────────────┐
│         GUI Layer (PySide6)         │
├─────────────────────────────────────┤
│    Simulation Engine (Python)        │
│  ┌─────────┐ ┌──────────┐ ┌──────┐ │
│  │ Devices │ │ Protocols│ │ AI   │ │
│  │ Layer   │ │  Stack   │ │Engine│ │
│  └─────────┘ └──────────┘ └──────┘ │
├─────────────────────────────────────┤
│        Event System (Qt)            │
└─────────────────────────────────────┘
```

## AI Model Architecture

The simulator uses an ensemble machine learning approach combining multiple models:

- **Isolation Forest**: Unsupervised anomaly detection for identifying unusual network patterns
- **Random Forest Classifier**: Supervised learning for threat classification (DDoS, malware, etc.)
- **LSTM Network**: Sequential pattern analysis for time-series network behavior
- **DBSCAN Clustering**: Pattern recognition and traffic categorization

The models are trained on network packet features including:
- Temporal patterns (time of day, day of week)
- Protocol and port analysis
- Device type behaviors
- Traffic volume and patterns
- Packet size distributions

## Test Scenarios & Results

The test runner has been executed and generated comprehensive reports for each scenario. All reports are available in PDF format in the `reports/` directory.

### Test Execution

```bash
python test_runner_standalone.py
```

**Execution Output:**
- Successfully trained ML models with 2000 synthetic packets
- Executed all three attack scenarios
- Generated both graphical and narrative PDF reports for each scenario

### Scenario 1: Corporate Data Breach

**Attack Overview**: A sophisticated multi-stage attack targeting corporate intellectual property through spear phishing, lateral movement, and data exfiltration.

![Corporate Data Breach Analysis](reports/Corporate_Data_Breach_analysis.png)

**Simulated Attack Details**:
- **Total Packets**: 463
- **Attack Duration**: 120 minutes (simulated)
- **Phases**: 5 (Reconnaissance → Phishing → Lateral Movement → Data Staging → Exfiltration)

**Attack Timeline**:
1. **Initial Reconnaissance** (15 min): 300 packets - Comprehensive port scanning across multiple targets
2. **Spear Phishing** (20 min): 6 packets - Targeted emails to finance department
3. **Lateral Movement** (30 min): 6 packets - Pass-the-hash attacks, remote execution
4. **Data Staging** (25 min): 51 packets - File aggregation and compression
5. **Data Exfiltration** (30 min): 100 packets - Large encrypted data transfers

**Generated Reports**:
- [Graphical PDF Report](reports/Corporate_Data_Breach_graphical_report.pdf)
- [Narrative PDF Report](reports/Corporate_Data_Breach_narrative_report.pdf)

### Scenario 2: IoT Botnet Attack

**Attack Overview**: Mass compromise of IoT devices leading to a coordinated DDoS attack against critical infrastructure.

![IoT Botnet DDoS Analysis](reports/IoT_Botnet_DDoS_analysis.png)

**Simulated Attack Details**:
- **Total Packets**: 1074
- **Attack Duration**: 90 minutes (simulated)  
- **Compromised Devices**: 8 IoT devices (cameras, sensors, smart lights)

**Attack Progression**:
1. **IoT Discovery** (10 min): 8 packets - Telnet scans with default credentials
2. **Mass Compromise** (20 min): 8 packets - Mirai variant malware deployment
3. **Botnet Formation** (15 min): 8 packets - IRC C2 channel connections
4. **DDoS Launch** (30 min): 1000 packets - Massive traffic flood to target
5. **Attack Persistence** (15 min): 50 packets - Sustained attack with evasion

**Generated Reports**:
- [Graphical PDF Report](reports/IoT_Botnet_DDoS_graphical_report.pdf)
- [Narrative PDF Report](reports/IoT_Botnet_DDoS_narrative_report.pdf)

### Scenario 3: Advanced Persistent Threat (APT)

**Attack Overview**: Nation-state level attack with long-term persistence targeting critical SCADA infrastructure.

![Advanced Persistent Threat Analysis](reports/Advanced_Persistent_Threat_analysis.png)

**Simulated Attack Details**:
- **Total Packets**: 187
- **Attack Duration**: 180 minutes (simulated)
- **Target Systems**: SCADA, PLCs, Domain Controller

**Attack Phases**:
1. **Zero-Day Exploit** (25 min): 1 packet - Watering hole with CVE-2025-XXXX
2. **Rootkit Installation** (30 min): 1 packet - Kernel module download
3. **Network Mapping** (40 min): 4 packets - Stealthy SCADA enumeration
4. **Credential Harvesting** (35 min): 1 packet - AD credential dumping
5. **SCADA Manipulation** (30 min): 1 packet - PLC logic modification
6. **Anti-Forensics** (20 min): 1 packet - Log deletion and timestomping

**Generated Reports**:
- [Graphical PDF Report](reports/Advanced_Persistent_Threat_graphical_report.pdf)
- [Narrative PDF Report](reports/Advanced_Persistent_Threat_narrative_report.pdf)

## Report Types

### 1. Graphical PDF Reports
Each scenario generates a comprehensive graphical report containing:
- **Threat Timeline**: Visual representation of threat levels over time
- **Anomaly Heatmap**: Device-based anomaly scores across time slots
- **Attack Phase Progression**: Duration and packet volume per phase
- **Network Impact Analysis**: Security metrics before/after attack
- **ML Model Performance**: Precision, recall, and F1-scores
- **Threat Distribution**: Pie chart of detected threat types
- **Real-time Detection Rate**: True/false positive trends

### 2. Narrative PDF Reports
Detailed narrative reports include:
- **Executive Summary**: High-level overview with key metrics
- **Phase-by-Phase Analysis**: Detailed breakdown of each attack phase
- **AI Detection Response**: How the system responded to each phase
- **Machine Learning Insights**: Key insights from ML models
- **Critical Findings**: Most affected devices and attack vectors
- **Response Effectiveness**: MTTD, detection rates, accuracy metrics
- **Security Recommendations**: Actionable remediation steps

## ML Model Architecture Details

The system employs an ensemble approach combining:
- **Isolation Forest**: Detects outliers in network traffic patterns
- **Random Forest Classifier**: Classifies known threat types
- **LSTM Network**: Analyzes sequential patterns in packet flows
- **DBSCAN Clustering**: Groups similar traffic patterns

### Feature Engineering
The ML models analyze 15 key features:
- Temporal patterns (time-of-day, day-of-week)
- Protocol and port characteristics
- Device type relationships
- Packet size distributions
- Traffic pattern anomalies

## Running Test Scenarios

To run the comprehensive test suite:

```bash
python test_runner_standalone.py
```

This will:
1. Train the ML models with 2000+ synthetic packets
2. Execute all three attack scenarios
3. Generate graphical and narrative PDF reports
4. Save all results in the `reports/` directory

### Note on Current Implementation

The current test implementation demonstrates the full pipeline of:
- ML model training with synthetic data
- Attack scenario simulation
- Real-time packet analysis
- Comprehensive report generation

In a production environment, the ML models would require:
- Extended training on real network traffic data
- Fine-tuning of detection thresholds
- Continuous learning from labeled security incidents
- Integration with threat intelligence feeds

## Future Enhancements

- Integration with real network traffic (PCAP import)
- Distributed training for larger networks
- Real-time model updates with online learning
- Quantum-resistant encryption simulation
- 5G network topology support

## Project Structure

```
netguard-ml/
├── src/                        # Main application source code
│   ├── ai/                     # AI and ML components
│   │   ├── ml_models.py        # Machine learning models (Isolation Forest, LSTM, etc.)
│   │   ├── network_ai.py       # Main AI engine for network analysis
│   │   └── training_data.py    # Synthetic data generation for ML training
│   │
│   ├── core/                   # Core functionality
│   │   ├── device_identity.py  # Device identification system
│   │   └── file_format.py      # .netsim file format handler
│   │
│   ├── devices/                # Network device implementations
│   │   ├── base_device.py      # Base class for all devices
│   │   ├── network_devices.py  # Routers, switches
│   │   ├── security_devices.py # Firewalls, VPN gateways
│   │   ├── server_devices.py   # Various server types
│   │   ├── end_user_devices.py # Workstations, laptops
│   │   ├── iot_devices.py      # IoT sensors, cameras, smart devices
│   │   └── specialized_devices.py # SCADA, industrial devices
│   │
│   ├── reporting/              # Report generation system
│   │   └── report_generator.py # PDF and graphical report creation
│   │
│   ├── simulation/             # Network simulation engine
│   │   └── simulator.py        # Core simulation logic
│   │
│   ├── test_scenarios/         # Test scenario definitions
│   │   └── scenarios.py        # Attack scenario generators
│   │
│   ├── ui/                     # User interface components
│   │   ├── ai_monitor.py       # AI monitoring panel
│   │   ├── connections.py      # Cable connection management
│   │   ├── device_controls.py  # Device configuration dialogs
│   │   ├── device_list.py      # Device palette widget
│   │   ├── device_toolbar.py   # Bottom device toolbar
│   │   ├── device_tree.py      # Network topology tree view
│   │   ├── icons.py            # Icon management system
│   │   ├── main_window.py      # Main application window
│   │   ├── network_canvas.py   # Network visualization canvas
│   │   ├── packet_viewer.py    # Packet inspection panel
│   │   └── theme.py            # UI theme and colors
│   │
│   └── main.py                 # Application entry point
│
├── scenarios/                  # Pre-built network topologies
│   ├── corporate_breach.netsim # Corporate network scenario
│   ├── iot_botnet.netsim       # IoT botnet scenario
│   ├── apt_scada.netsim        # APT SCADA attack scenario
│   └── README.md               # Scenario documentation
│
├── reports/                    # Generated analysis reports
│   ├── *.png                   # Graphical visualizations
│   ├── *_graphical_report.pdf  # Graphical PDF reports
│   ├── *_narrative_report.pdf  # Narrative PDF reports
│   └── test_results.json       # Test execution results
│
├── assets/                     # Application assets
│   └── icons/                  # Phosphor icon library
│       └── phosphor-icons/     # SVG icon files
│
├── test_runner.py              # Standalone test scenario runner
├── test_runner_standalone.py   # Qt-independent test runner
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Author

Sam Tan - Network Security & AI
