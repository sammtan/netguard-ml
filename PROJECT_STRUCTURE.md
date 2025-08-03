# Project Structure

```
ai-network-simulator/
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
├── README.md                   # Project documentation
└── PROJECT_STRUCTURE.md        # This file
```

## Key Components

### AI/ML System
- Ensemble machine learning approach
- Real-time anomaly detection
- Threat classification
- Sequential pattern analysis

### Device System
- Modular device architecture
- 20+ device types
- Realistic network behaviors
- Protocol simulation

### UI System
- Qt-based graphical interface
- Drag-and-drop network building
- Real-time visualization
- AI insights panel

### Reporting System
- Comprehensive PDF generation
- Graphical analysis charts
- Narrative security reports
- Export capabilities