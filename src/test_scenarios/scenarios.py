"""
Sophisticated test scenarios for AI Network Simulator
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import random


class NetworkTestScenarios:
    """Define sophisticated attack scenarios for testing"""
    
    @staticmethod
    def create_corporate_data_breach() -> Dict:
        """
        Scenario 1: Corporate Data Breach
        A multi-stage attack targeting a corporate network to steal sensitive data
        """
        return {
            'name': 'Corporate_Data_Breach',
            'description': 'Sophisticated multi-stage attack targeting corporate intellectual property',
            'duration': 120,  # 2 hours
            'network_topology': {
                'devices': [
                    {'type': 'firewall', 'id': 'fw_main', 'position': (0, 0)},
                    {'type': 'router', 'id': 'router_dmz', 'position': (200, 0)},
                    {'type': 'switch', 'id': 'switch_internal', 'position': (400, 0)},
                    {'type': 'web_server', 'id': 'web_server_1', 'position': (200, 150)},
                    {'type': 'database', 'id': 'db_customer', 'position': (600, 100)},
                    {'type': 'file_server', 'id': 'fs_confidential', 'position': (600, -100)},
                    {'type': 'workstation', 'id': 'ws_ceo', 'position': (400, 200)},
                    {'type': 'workstation', 'id': 'ws_finance_1', 'position': (500, 200)},
                    {'type': 'workstation', 'id': 'ws_finance_2', 'position': (600, 200)},
                    {'type': 'mail_server', 'id': 'mail_exchange', 'position': (300, -150)}
                ],
                'connections': [
                    ('fw_main', 'router_dmz'),
                    ('router_dmz', 'switch_internal'),
                    ('router_dmz', 'web_server_1'),
                    ('switch_internal', 'db_customer'),
                    ('switch_internal', 'fs_confidential'),
                    ('switch_internal', 'ws_ceo'),
                    ('switch_internal', 'ws_finance_1'),
                    ('switch_internal', 'ws_finance_2'),
                    ('router_dmz', 'mail_exchange')
                ]
            },
            'attack_phases': [
                {
                    'id': 1,
                    'name': 'Initial Reconnaissance',
                    'duration': 15,
                    'description': 'Attackers perform comprehensive network scanning to identify vulnerable services',
                    'packets': NetworkTestScenarios._generate_recon_packets(),
                    'expected_detections': ['port_scan', 'service_enumeration']
                },
                {
                    'id': 2,
                    'name': 'Spear Phishing Campaign',
                    'duration': 20,
                    'description': 'Targeted phishing emails sent to finance department with malicious attachments',
                    'packets': NetworkTestScenarios._generate_phishing_packets(),
                    'expected_detections': ['suspicious_email', 'malware_download']
                },
                {
                    'id': 3,
                    'name': 'Lateral Movement',
                    'duration': 30,
                    'description': 'Compromised workstation used to access internal systems using stolen credentials',
                    'packets': NetworkTestScenarios._generate_lateral_movement_packets(),
                    'expected_detections': ['credential_theft', 'privilege_escalation', 'unusual_access_pattern']
                },
                {
                    'id': 4,
                    'name': 'Data Staging',
                    'duration': 25,
                    'description': 'Sensitive files collected and compressed in preparation for exfiltration',
                    'packets': NetworkTestScenarios._generate_data_staging_packets(),
                    'expected_detections': ['file_access_anomaly', 'data_aggregation']
                },
                {
                    'id': 5,
                    'name': 'Data Exfiltration',
                    'duration': 30,
                    'description': 'Large volumes of data transmitted to external command & control server',
                    'packets': NetworkTestScenarios._generate_exfiltration_packets(),
                    'expected_detections': ['large_data_transfer', 'suspicious_destination', 'data_exfiltration']
                }
            ]
        }
    
    @staticmethod
    def create_iot_botnet_attack() -> Dict:
        """
        Scenario 2: IoT Botnet Attack
        Massive IoT device compromise leading to DDoS attack on critical infrastructure
        """
        return {
            'name': 'IoT_Botnet_DDoS',
            'description': 'Large-scale IoT botnet formation and subsequent DDoS attack',
            'duration': 90,  # 1.5 hours
            'network_topology': {
                'devices': [
                    {'type': 'router', 'id': 'isp_router', 'position': (0, 0)},
                    {'type': 'firewall', 'id': 'corp_firewall', 'position': (200, 0)},
                    {'type': 'smart_hub', 'id': 'iot_hub_1', 'position': (400, 100)},
                    {'type': 'ip_camera', 'id': 'camera_1', 'position': (600, 150)},
                    {'type': 'ip_camera', 'id': 'camera_2', 'position': (600, 100)},
                    {'type': 'ip_camera', 'id': 'camera_3', 'position': (600, 50)},
                    {'type': 'iot_sensor', 'id': 'temp_sensor_1', 'position': (500, 200)},
                    {'type': 'iot_sensor', 'id': 'temp_sensor_2', 'position': (550, 200)},
                    {'type': 'smart_light', 'id': 'light_1', 'position': (600, -50)},
                    {'type': 'smart_light', 'id': 'light_2', 'position': (600, -100)},
                    {'type': 'smart_speaker', 'id': 'speaker_1', 'position': (500, -150)},
                    {'type': 'web_server', 'id': 'target_server', 'position': (200, -200)}
                ],
                'connections': [
                    ('isp_router', 'corp_firewall'),
                    ('corp_firewall', 'iot_hub_1'),
                    ('iot_hub_1', 'camera_1'),
                    ('iot_hub_1', 'camera_2'),
                    ('iot_hub_1', 'camera_3'),
                    ('iot_hub_1', 'temp_sensor_1'),
                    ('iot_hub_1', 'temp_sensor_2'),
                    ('iot_hub_1', 'light_1'),
                    ('iot_hub_1', 'light_2'),
                    ('iot_hub_1', 'speaker_1'),
                    ('corp_firewall', 'target_server')
                ]
            },
            'attack_phases': [
                {
                    'id': 1,
                    'name': 'IoT Device Discovery',
                    'duration': 10,
                    'description': 'Automated scanning for vulnerable IoT devices with default credentials',
                    'packets': NetworkTestScenarios._generate_iot_discovery_packets(),
                    'expected_detections': ['iot_scan', 'default_credential_attempt']
                },
                {
                    'id': 2,
                    'name': 'Mass Device Compromise',
                    'duration': 20,
                    'description': 'Exploitation of IoT devices using known vulnerabilities and default passwords',
                    'packets': NetworkTestScenarios._generate_iot_compromise_packets(),
                    'expected_detections': ['mass_login_attempt', 'iot_malware_infection']
                },
                {
                    'id': 3,
                    'name': 'Botnet Formation',
                    'duration': 15,
                    'description': 'Infected devices connect to command & control server and await instructions',
                    'packets': NetworkTestScenarios._generate_botnet_c2_packets(),
                    'expected_detections': ['c2_communication', 'botnet_behavior']
                },
                {
                    'id': 4,
                    'name': 'DDoS Attack Launch',
                    'duration': 30,
                    'description': 'Coordinated DDoS attack from thousands of compromised IoT devices',
                    'packets': NetworkTestScenarios._generate_ddos_packets(),
                    'expected_detections': ['ddos_attack', 'traffic_flood', 'service_degradation']
                },
                {
                    'id': 5,
                    'name': 'Attack Persistence',
                    'duration': 15,
                    'description': 'Botnet maintains attack while evading detection and mitigation attempts',
                    'packets': NetworkTestScenarios._generate_persistence_packets(),
                    'expected_detections': ['sustained_attack', 'evasion_technique']
                }
            ]
        }
    
    @staticmethod
    def create_apt_scenario() -> Dict:
        """
        Scenario 3: Advanced Persistent Threat (APT)
        Nation-state level attack with long-term persistence and stealth
        """
        return {
            'name': 'Advanced_Persistent_Threat',
            'description': 'Sophisticated nation-state APT campaign targeting critical infrastructure',
            'duration': 180,  # 3 hours (simulating weeks of activity)
            'network_topology': {
                'devices': [
                    {'type': 'firewall', 'id': 'perimeter_fw', 'position': (0, 0)},
                    {'type': 'router', 'id': 'core_router', 'position': (200, 0)},
                    {'type': 'switch', 'id': 'datacenter_switch', 'position': (400, 0)},
                    {'type': 'scada_server', 'id': 'scada_master', 'position': (600, 0)},
                    {'type': 'database', 'id': 'scada_historian', 'position': (600, 100)},
                    {'type': 'hmi_panel', 'id': 'hmi_control', 'position': (800, 0)},
                    {'type': 'plc_controller', 'id': 'plc_1', 'position': (800, 100)},
                    {'type': 'plc_controller', 'id': 'plc_2', 'position': (800, -100)},
                    {'type': 'workstation', 'id': 'engineer_ws', 'position': (400, 150)},
                    {'type': 'server', 'id': 'domain_controller', 'position': (400, -150)},
                    {'type': 'server', 'id': 'backup_server', 'position': (600, -150)}
                ],
                'connections': [
                    ('perimeter_fw', 'core_router'),
                    ('core_router', 'datacenter_switch'),
                    ('datacenter_switch', 'scada_master'),
                    ('datacenter_switch', 'scada_historian'),
                    ('datacenter_switch', 'engineer_ws'),
                    ('datacenter_switch', 'domain_controller'),
                    ('datacenter_switch', 'backup_server'),
                    ('scada_master', 'hmi_control'),
                    ('scada_master', 'plc_1'),
                    ('scada_master', 'plc_2')
                ]
            },
            'attack_phases': [
                {
                    'id': 1,
                    'name': 'Initial Compromise',
                    'duration': 25,
                    'description': 'Zero-day exploit used to compromise engineer workstation via watering hole attack',
                    'packets': NetworkTestScenarios._generate_zero_day_packets(),
                    'expected_detections': ['zero_day_exploit', 'unusual_process_behavior']
                },
                {
                    'id': 2,
                    'name': 'Establish Foothold',
                    'duration': 30,
                    'description': 'Custom implant installed with kernel-level rootkit for persistence',
                    'packets': NetworkTestScenarios._generate_rootkit_packets(),
                    'expected_detections': ['rootkit_installation', 'kernel_modification']
                },
                {
                    'id': 3,
                    'name': 'Network Mapping',
                    'duration': 40,
                    'description': 'Slow and stealthy reconnaissance of critical infrastructure components',
                    'packets': NetworkTestScenarios._generate_stealth_recon_packets(),
                    'expected_detections': ['slow_scan', 'scada_enumeration']
                },
                {
                    'id': 4,
                    'name': 'Credential Harvesting',
                    'duration': 35,
                    'description': 'Advanced techniques to steal SCADA engineer and admin credentials',
                    'packets': NetworkTestScenarios._generate_credential_harvest_packets(),
                    'expected_detections': ['memory_scraping', 'credential_dumping']
                },
                {
                    'id': 5,
                    'name': 'SCADA Manipulation',
                    'duration': 30,
                    'description': 'Subtle modifications to PLC logic and SCADA configurations',
                    'packets': NetworkTestScenarios._generate_scada_attack_packets(),
                    'expected_detections': ['plc_modification', 'scada_anomaly', 'process_deviation']
                },
                {
                    'id': 6,
                    'name': 'Cover Tracks',
                    'duration': 20,
                    'description': 'Log deletion, timestamp manipulation, and false flag operations',
                    'packets': NetworkTestScenarios._generate_antiforensics_packets(),
                    'expected_detections': ['log_tampering', 'antiforensics_activity']
                }
            ]
        }
    
    # Packet generation methods
    @staticmethod
    def _generate_recon_packets() -> List[Dict]:
        """Generate reconnaissance packets"""
        packets = []
        target_ips = ['192.168.1.10', '192.168.1.20', '192.168.1.30']
        
        for target in target_ips:
            for port in range(1, 1000, 10):  # Sample ports
                packets.append({
                    'source': 'external_scanner',
                    'destination': target,
                    'protocol': 'TCP',
                    'port': port,
                    'info': f'SYN scan port {port}',
                    'threat_indicators': ['port_scan', 'reconnaissance']
                })
        
        return packets
    
    @staticmethod
    def _generate_phishing_packets() -> List[Dict]:
        """Generate phishing email packets"""
        packets = []
        targets = ['ws_finance_1', 'ws_finance_2', 'ws_ceo']
        
        for target in targets:
            packets.append({
                'source': 'external_mail',
                'destination': target,
                'protocol': 'SMTP',
                'port': 25,
                'info': 'Phishing email: "Urgent Invoice Review"',
                'threat_indicators': ['phishing', 'social_engineering']
            })
            
            # Malware download
            packets.append({
                'source': target,
                'destination': 'malicious_site',
                'protocol': 'HTTPS',
                'port': 443,
                'info': 'Download malware.exe',
                'threat_indicators': ['malware_download', 'trojan']
            })
        
        return packets
    
    @staticmethod
    def _generate_lateral_movement_packets() -> List[Dict]:
        """Generate lateral movement packets"""
        packets = []
        compromised = 'ws_finance_1'
        targets = ['db_customer', 'fs_confidential', 'domain_controller']
        
        for target in targets:
            # Credential theft
            packets.append({
                'source': compromised,
                'destination': target,
                'protocol': 'SMB',
                'port': 445,
                'info': 'Pass-the-hash attack',
                'threat_indicators': ['credential_theft', 'lateral_movement']
            })
            
            # Remote execution
            packets.append({
                'source': compromised,
                'destination': target,
                'protocol': 'RPC',
                'port': 135,
                'info': 'Remote command execution',
                'threat_indicators': ['remote_execution', 'privilege_escalation']
            })
        
        return packets
    
    @staticmethod
    def _generate_data_staging_packets() -> List[Dict]:
        """Generate data staging packets"""
        packets = []
        staging_server = 'compromised_server'
        
        # File access
        for i in range(50):
            packets.append({
                'source': staging_server,
                'destination': 'fs_confidential',
                'protocol': 'SMB',
                'port': 445,
                'info': f'Access confidential_file_{i}.doc',
                'threat_indicators': ['data_access', 'file_aggregation']
            })
        
        # Compression
        packets.append({
            'source': staging_server,
            'destination': staging_server,
            'protocol': 'LOCAL',
            'port': 0,
            'info': 'Create archive: stolen_data.zip (2.5GB)',
            'threat_indicators': ['data_compression', 'exfiltration_prep']
        })
        
        return packets
    
    @staticmethod
    def _generate_exfiltration_packets() -> List[Dict]:
        """Generate data exfiltration packets"""
        packets = []
        
        # Large data transfer
        for i in range(100):
            packets.append({
                'source': 'compromised_server',
                'destination': 'c2_server',
                'protocol': 'HTTPS',
                'port': 443,
                'size': 1500,  # Max packet size
                'info': f'Encrypted data chunk {i}/100',
                'threat_indicators': ['data_exfiltration', 'large_transfer']
            })
        
        return packets
    
    @staticmethod
    def _generate_iot_discovery_packets() -> List[Dict]:
        """Generate IoT discovery packets"""
        packets = []
        iot_devices = ['camera_1', 'camera_2', 'camera_3', 'temp_sensor_1', 
                      'temp_sensor_2', 'light_1', 'light_2', 'speaker_1']
        
        for device in iot_devices:
            packets.append({
                'source': 'iot_scanner',
                'destination': device,
                'protocol': 'Telnet',
                'port': 23,
                'info': 'Login attempt: admin/admin',
                'threat_indicators': ['iot_scan', 'default_creds']
            })
        
        return packets
    
    @staticmethod
    def _generate_iot_compromise_packets() -> List[Dict]:
        """Generate IoT compromise packets"""
        packets = []
        
        for i in range(8):
            packets.append({
                'source': 'malware_server',
                'destination': f'iot_device_{i}',
                'protocol': 'HTTP',
                'port': 80,
                'info': 'Download Mirai variant',
                'threat_indicators': ['iot_malware', 'botnet_infection']
            })
        
        return packets
    
    @staticmethod
    def _generate_botnet_c2_packets() -> List[Dict]:
        """Generate botnet C2 packets"""
        packets = []
        
        for i in range(8):
            packets.append({
                'source': f'infected_iot_{i}',
                'destination': 'c2_server',
                'protocol': 'IRC',
                'port': 6667,
                'info': 'Join botnet channel #ddos',
                'threat_indicators': ['c2_communication', 'botnet_checkin']
            })
        
        return packets
    
    @staticmethod
    def _generate_ddos_packets() -> List[Dict]:
        """Generate DDoS attack packets"""
        packets = []
        
        # Massive traffic from botnet
        for i in range(1000):
            packets.append({
                'source': f'bot_{i % 100}',
                'destination': 'target_server',
                'protocol': random.choice(['TCP', 'UDP', 'ICMP']),
                'port': random.choice([80, 443]),
                'size': 1500,
                'info': 'DDoS flood packet',
                'threat_indicators': ['ddos', 'traffic_flood']
            })
        
        return packets
    
    @staticmethod
    def _generate_persistence_packets() -> List[Dict]:
        """Generate persistence packets"""
        packets = []
        
        for i in range(50):
            packets.append({
                'source': f'bot_{i}',
                'destination': 'target_server',
                'protocol': 'TCP',
                'port': 80,
                'info': 'Persistent DDoS with evasion',
                'threat_indicators': ['sustained_ddos', 'evasion']
            })
        
        return packets
    
    @staticmethod
    def _generate_zero_day_packets() -> List[Dict]:
        """Generate zero-day exploit packets"""
        packets = []
        
        packets.append({
            'source': 'watering_hole_site',
            'destination': 'engineer_ws',
            'protocol': 'HTTPS',
            'port': 443,
            'info': 'Deliver zero-day exploit (CVE-2025-XXXX)',
            'threat_indicators': ['zero_day', 'targeted_attack']
        })
        
        return packets
    
    @staticmethod
    def _generate_rootkit_packets() -> List[Dict]:
        """Generate rootkit installation packets"""
        packets = []
        
        packets.append({
            'source': 'engineer_ws',
            'destination': 'apt_c2',
            'protocol': 'HTTPS',
            'port': 443,
            'info': 'Download kernel rootkit module',
            'threat_indicators': ['rootkit', 'kernel_exploit']
        })
        
        return packets
    
    @staticmethod
    def _generate_stealth_recon_packets() -> List[Dict]:
        """Generate stealthy reconnaissance packets"""
        packets = []
        
        targets = ['scada_master', 'plc_1', 'plc_2', 'hmi_control']
        for target in targets:
            packets.append({
                'source': 'engineer_ws',
                'destination': target,
                'protocol': 'Modbus',
                'port': 502,
                'info': 'Read SCADA registers',
                'threat_indicators': ['scada_recon', 'slow_scan']
            })
        
        return packets
    
    @staticmethod
    def _generate_credential_harvest_packets() -> List[Dict]:
        """Generate credential harvesting packets"""
        packets = []
        
        packets.append({
            'source': 'engineer_ws',
            'destination': 'domain_controller',
            'protocol': 'LDAP',
            'port': 389,
            'info': 'Dump Active Directory credentials',
            'threat_indicators': ['credential_dump', 'mimikatz']
        })
        
        return packets
    
    @staticmethod
    def _generate_scada_attack_packets() -> List[Dict]:
        """Generate SCADA attack packets"""
        packets = []
        
        # PLC logic modification
        packets.append({
            'source': 'engineer_ws',
            'destination': 'plc_1',
            'protocol': 'S7',
            'port': 102,
            'info': 'Modify ladder logic: pressure_threshold',
            'threat_indicators': ['plc_modification', 'sabotage']
        })
        
        return packets
    
    @staticmethod
    def _generate_antiforensics_packets() -> List[Dict]:
        """Generate anti-forensics packets"""
        packets = []
        
        packets.append({
            'source': 'engineer_ws',
            'destination': 'domain_controller',
            'protocol': 'RPC',
            'port': 445,
            'info': 'Clear security event logs',
            'threat_indicators': ['log_deletion', 'antiforensics']
        })
        
        return packets