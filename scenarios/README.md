# Network Topology Scenarios

This folder contains pre-configured network topologies based on the test scenarios used in the AI analysis reports.

## Available Scenarios

### 1. Corporate Data Breach (`corporate_breach.netsim`)
A sophisticated corporate network topology designed to simulate a multi-stage data breach attack:
- **Devices**: 10 (Firewall, Router, Switch, Servers, Workstations)
- **Target**: Finance department workstations and confidential file server
- **Attack Path**: External → DMZ → Internal Network → Data Exfiltration

### 2. IoT Botnet Attack (`iot_botnet.netsim`)
A smart home/office environment with multiple IoT devices vulnerable to botnet compromise:
- **Devices**: 12 (Router, Firewall, Smart Hub, IP Cameras, Sensors, Smart Devices)
- **Target**: External web server (DDoS victim)
- **Attack Path**: IoT Compromise → Botnet Formation → DDoS Launch

### 3. Advanced Persistent Threat (`apt_scada.netsim`)
Critical infrastructure SCADA network targeted by nation-state level threat:
- **Devices**: 11 (Firewall, Router, SCADA Master, PLCs, HMI, Domain Controller)
- **Target**: Industrial control systems
- **Attack Path**: Engineer Workstation → SCADA Network → PLC Manipulation

## How to Use

1. Open the AI Network Simulator application
2. Click **File → Load** in the menu
3. Navigate to the `scenarios` folder
4. Select the desired `.netsim` file
5. The network topology will be loaded automatically
6. Start the simulation to see the network in action

## Topology Features

Each topology includes:
- Realistic device configurations with proper IP addresses
- Manufacturer and model information
- Strategic device placement for visual clarity
- Appropriate connection types (Ethernet/Wireless)
- Pre-configured running states

## Testing Attack Scenarios

After loading a topology:
1. Enable AI monitoring from the toolbar
2. Use the ping tool to test connectivity
3. Observe the AI insights panel for anomaly detection
4. Generate traffic between devices to trigger ML analysis

These topologies provide a foundation for testing the AI-powered security monitoring capabilities of the simulator.