"""
Training data generator for ML models
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict
import numpy as np


class TrainingDataGenerator:
    """Generate synthetic training data for network anomaly detection"""
    
    def __init__(self):
        self.device_types = ['router', 'switch', 'firewall', 'server', 'workstation', 
                            'laptop', 'smartphone', 'iot_sensor', 'printer', 'ip_camera']
        self.protocols = ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS', 'SSH', 'FTP', 'DNS', 'DHCP']
        self.threat_types = ['ddos', 'malware', 'exfiltration', 'intrusion', 'port_scan']
        
    def generate_normal_traffic(self, count: int) -> List[Dict]:
        """Generate normal network traffic patterns"""
        packets = []
        
        for i in range(count):
            # Normal traffic characteristics
            hour = random.randint(8, 18)  # Business hours
            protocol = random.choice(['HTTP', 'HTTPS', 'DNS', 'DHCP'])
            
            packet = {
                'timestamp': datetime.now() - timedelta(seconds=random.randint(0, 3600)),
                'source': f'device_{random.randint(1, 20)}',
                'destination': f'device_{random.randint(1, 20)}',
                'source_type': random.choice(['workstation', 'laptop', 'server']),
                'destination_type': random.choice(['server', 'router', 'switch']),
                'protocol': protocol,
                'port': self._get_normal_port(protocol),
                'size': random.randint(40, 1500),
                'info': self._get_normal_info(protocol),
                'label': 'normal'
            }
            packets.append(packet)
        
        return packets
    
    def generate_attack_traffic(self, attack_type: str, count: int) -> List[Dict]:
        """Generate attack traffic patterns"""
        packets = []
        
        generators = {
            'ddos': self._generate_ddos_packets,
            'malware': self._generate_malware_packets,
            'exfiltration': self._generate_exfiltration_packets,
            'intrusion': self._generate_intrusion_packets,
            'port_scan': self._generate_port_scan_packets
        }
        
        generator = generators.get(attack_type, self._generate_ddos_packets)
        return generator(count)
    
    def _generate_ddos_packets(self, count: int) -> List[Dict]:
        """Generate DDoS attack packets"""
        packets = []
        target = f'server_{random.randint(1, 5)}'
        
        for i in range(count):
            packet = {
                'timestamp': datetime.now() - timedelta(seconds=i * 0.01),  # Rapid fire
                'source': f'bot_{random.randint(1, 100)}',
                'destination': target,
                'source_type': random.choice(['workstation', 'iot_sensor', 'smartphone']),
                'destination_type': 'server',
                'protocol': random.choice(['TCP', 'UDP', 'ICMP']),
                'port': random.choice([80, 443, 22]),
                'size': random.randint(1000, 1500),  # Large packets
                'info': 'SYN flood',
                'label': 'ddos'
            }
            packets.append(packet)
        
        return packets
    
    def _generate_malware_packets(self, count: int) -> List[Dict]:
        """Generate malware communication packets"""
        packets = []
        infected_device = f'workstation_{random.randint(1, 10)}'
        c2_server = 'external_server_666'
        
        for i in range(count):
            packet = {
                'timestamp': datetime.now() - timedelta(seconds=random.randint(0, 3600)),
                'source': infected_device,
                'destination': c2_server,
                'source_type': 'workstation',
                'destination_type': 'unknown',
                'protocol': random.choice(['TCP', 'HTTP', 'Unknown']),
                'port': random.choice([4444, 6666, 31337, random.randint(40000, 60000)]),
                'size': random.randint(100, 500),
                'info': random.choice(['cmd.exe', 'shell', 'beacon', 'encrypted_payload']),
                'label': 'malware'
            }
            packets.append(packet)
        
        return packets
    
    def _generate_exfiltration_packets(self, count: int) -> List[Dict]:
        """Generate data exfiltration packets"""
        packets = []
        source = f'server_{random.randint(1, 5)}'
        
        for i in range(count):
            packet = {
                'timestamp': datetime.now() - timedelta(seconds=i * 2),
                'source': source,
                'destination': 'external_server',
                'source_type': 'server',
                'destination_type': 'unknown',
                'protocol': random.choice(['HTTPS', 'FTP', 'SSH']),
                'port': random.choice([443, 21, 22, 8443]),
                'size': random.randint(1200, 1500),  # Large data transfers
                'info': 'large_data_transfer',
                'label': 'exfiltration'
            }
            packets.append(packet)
        
        return packets
    
    def _generate_intrusion_packets(self, count: int) -> List[Dict]:
        """Generate intrusion attempt packets"""
        packets = []
        attacker = 'external_attacker'
        
        for i in range(count):
            target_type = random.choice(['database', 'file_server', 'mail_server'])
            packet = {
                'timestamp': datetime.now() - timedelta(seconds=random.randint(0, 600)),
                'source': attacker,
                'destination': f'{target_type}_1',
                'source_type': 'unknown',
                'destination_type': target_type,
                'protocol': random.choice(['SSH', 'RDP', 'SQL']),
                'port': random.choice([22, 3389, 1433, 3306]),
                'size': random.randint(50, 200),
                'info': random.choice(['brute_force', 'sql_injection', 'exploit_attempt']),
                'label': 'intrusion'
            }
            packets.append(packet)
        
        return packets
    
    def _generate_port_scan_packets(self, count: int) -> List[Dict]:
        """Generate port scanning packets"""
        packets = []
        scanner = f'scanner_{random.randint(1, 5)}'
        target = f'server_{random.randint(1, 10)}'
        
        ports = list(range(1, min(count + 1, 65536)))
        random.shuffle(ports)
        
        for i, port in enumerate(ports[:count]):
            packet = {
                'timestamp': datetime.now() - timedelta(seconds=i * 0.1),
                'source': scanner,
                'destination': target,
                'source_type': 'unknown',
                'destination_type': 'server',
                'protocol': 'TCP',
                'port': port,
                'size': 40,  # Small SYN packets
                'info': 'SYN scan',
                'label': 'port_scan'
            }
            packets.append(packet)
        
        return packets
    
    def _get_normal_port(self, protocol: str) -> int:
        """Get normal port for protocol"""
        port_map = {
            'HTTP': 80,
            'HTTPS': 443,
            'SSH': 22,
            'FTP': 21,
            'DNS': 53,
            'DHCP': random.choice([67, 68])
        }
        return port_map.get(protocol, random.randint(1024, 49151))
    
    def _get_normal_info(self, protocol: str) -> str:
        """Get normal packet info"""
        info_map = {
            'HTTP': 'GET /index.html',
            'HTTPS': 'TLS handshake',
            'DNS': 'Query A record',
            'DHCP': 'DHCP Request'
        }
        return info_map.get(protocol, 'Normal traffic')
    
    def generate_mixed_dataset(self, total_size: int, anomaly_ratio: float = 0.1) -> List[Dict]:
        """Generate mixed dataset with normal and anomalous traffic"""
        normal_count = int(total_size * (1 - anomaly_ratio))
        anomaly_count = total_size - normal_count
        
        # Generate normal traffic
        dataset = self.generate_normal_traffic(normal_count)
        
        # Generate various attack types
        attacks_per_type = anomaly_count // len(self.threat_types)
        remainder = anomaly_count % len(self.threat_types)
        
        for i, threat_type in enumerate(self.threat_types):
            count = attacks_per_type + (1 if i < remainder else 0)
            dataset.extend(self.generate_attack_traffic(threat_type, count))
        
        # Shuffle dataset
        random.shuffle(dataset)
        
        return dataset
    
    def generate_sequential_attack(self, attack_scenario: str) -> List[Dict]:
        """Generate sequential attack scenarios for testing"""
        scenarios = {
            'corporate_breach': self._generate_corporate_breach_scenario,
            'iot_botnet': self._generate_iot_botnet_scenario,
            'apt': self._generate_apt_scenario
        }
        
        generator = scenarios.get(attack_scenario, self._generate_corporate_breach_scenario)
        return generator()
    
    def _generate_corporate_breach_scenario(self) -> List[Dict]:
        """Generate corporate data breach scenario"""
        packets = []
        
        # Phase 1: Reconnaissance (port scanning)
        packets.extend(self.generate_attack_traffic('port_scan', 50))
        
        # Phase 2: Initial compromise (malware)
        packets.extend(self.generate_attack_traffic('malware', 20))
        
        # Phase 3: Lateral movement (intrusion)
        packets.extend(self.generate_attack_traffic('intrusion', 30))
        
        # Phase 4: Data exfiltration
        packets.extend(self.generate_attack_traffic('exfiltration', 100))
        
        return packets
    
    def _generate_iot_botnet_scenario(self) -> List[Dict]:
        """Generate IoT botnet attack scenario"""
        packets = []
        
        # Phase 1: IoT device compromise
        for i in range(20):
            packet = {
                'timestamp': datetime.now() - timedelta(seconds=3600 - i*60),
                'source': 'botnet_controller',
                'destination': f'iot_sensor_{i}',
                'source_type': 'unknown',
                'destination_type': 'iot_sensor',
                'protocol': 'Telnet',
                'port': 23,
                'size': 100,
                'info': 'default_password_attempt',
                'label': 'malware'
            }
            packets.append(packet)
        
        # Phase 2: Botnet formation
        packets.extend(self.generate_attack_traffic('malware', 50))
        
        # Phase 3: DDoS attack
        packets.extend(self.generate_attack_traffic('ddos', 200))
        
        return packets
    
    def _generate_apt_scenario(self) -> List[Dict]:
        """Generate Advanced Persistent Threat scenario"""
        packets = []
        
        # Phase 1: Spear phishing (initial access)
        for i in range(5):
            packet = {
                'timestamp': datetime.now() - timedelta(days=7, seconds=i*3600),
                'source': 'external_mail',
                'destination': f'workstation_{i}',
                'source_type': 'unknown',
                'destination_type': 'workstation',
                'protocol': 'SMTP',
                'port': 25,
                'size': 2000,
                'info': 'phishing_email_with_attachment',
                'label': 'intrusion'
            }
            packets.append(packet)
        
        # Phase 2: Establish foothold
        packets.extend(self.generate_attack_traffic('malware', 10))
        
        # Phase 3: Privilege escalation
        packets.extend(self.generate_attack_traffic('intrusion', 20))
        
        # Phase 4: Long-term monitoring (stealthy exfiltration)
        for day in range(30):
            for hour in [2, 3, 4]:  # Late night hours
                packet = {
                    'timestamp': datetime.now() - timedelta(days=30-day, hours=hour),
                    'source': 'compromised_server',
                    'destination': 'apt_c2_server',
                    'source_type': 'server',
                    'destination_type': 'unknown',
                    'protocol': 'HTTPS',
                    'port': 443,
                    'size': random.randint(500, 1000),
                    'info': 'encrypted_data',
                    'label': 'exfiltration'
                }
                packets.append(packet)
        
        return packets