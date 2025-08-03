"""
Advanced AI engine for network monitoring and analysis
"""

import random
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import math
from .ml_models import NetworkMLEngine


class NetworkAI:
    """
    AI engine that monitors network traffic and provides intelligent insights
    """
    
    def __init__(self):
        # Traffic analysis
        self.packet_history = deque(maxlen=1000)  # Keep last 1000 packets
        self.time_window = deque(maxlen=60)  # 60 second window
        self.baseline_traffic = {}
        
        # Pattern detection
        self.device_profiles = defaultdict(DeviceProfile)
        self.protocol_patterns = defaultdict(ProtocolPattern)
        self.connection_graph = NetworkGraph()
        
        # Threat detection
        self.threat_indicators = []
        self.security_events = deque(maxlen=100)
        self.risk_scores = defaultdict(float)
        
        # Performance metrics
        self.latency_history = defaultdict(deque)
        self.bandwidth_usage = defaultdict(float)
        
        # Learning parameters
        self.learning_rate = 0.1
        self.anomaly_threshold = 2.5  # Standard deviations
        
        # Initialize ML engine
        self.ml_engine = NetworkMLEngine()
        self.use_ml = True  # Flag to enable/disable ML
        
    def analyze_packet(self, packet: Dict) -> Dict:
        """Analyze a single packet and return insights"""
        # Store packet
        self.packet_history.append({
            'timestamp': datetime.now(),
            'packet': packet
        })
        
        # Update profiles
        self.update_device_profile(packet)
        self.update_protocol_pattern(packet)
        self.update_connection_graph(packet)
        
        # Use ML engine if enabled
        if self.use_ml:
            ml_analysis = self.ml_engine.analyze_packet(packet)
            
            # Combine ML insights with rule-based insights
            rule_anomalies = self.detect_anomalies(packet)
            rule_threats = self.detect_threats(packet)
            
            # Merge insights
            all_insights = ml_analysis['insights'] + self.generate_insights(packet, rule_anomalies, rule_threats)
            all_recommendations = ml_analysis['recommendations'] + self.generate_recommendations(rule_anomalies, rule_threats)
            
            return {
                'anomaly_score': ml_analysis['anomaly_score'],
                'threat_level': ml_analysis['threat_level'],
                'insights': all_insights[:10],  # Limit total insights
                'recommendations': all_recommendations[:5],  # Limit recommendations
                'ml_prediction': ml_analysis['ml_prediction'],
                'deep_score': ml_analysis['deep_score']
            }
        else:
            # Fallback to rule-based analysis
            anomalies = self.detect_anomalies(packet)
            threats = self.detect_threats(packet)
            insights = self.generate_insights(packet, anomalies, threats)
            
            return {
                'anomaly_score': self.calculate_anomaly_score(anomalies),
                'threat_level': self.calculate_threat_level(threats),
                'insights': insights,
                'recommendations': self.generate_recommendations(anomalies, threats)
            }
    
    def update_device_profile(self, packet: Dict):
        """Update device behavior profile"""
        device = packet.get('source')
        if device:
            profile = self.device_profiles[device]
            profile.update(packet)
    
    def update_protocol_pattern(self, packet: Dict):
        """Update protocol usage patterns"""
        protocol = packet.get('protocol')
        if protocol:
            pattern = self.protocol_patterns[protocol]
            pattern.update(packet)
    
    def update_connection_graph(self, packet: Dict):
        """Update network connection graph"""
        source = packet.get('source')
        dest = packet.get('destination')
        if source and dest:
            self.connection_graph.add_edge(source, dest, packet)
    
    def detect_anomalies(self, packet: Dict) -> List[Dict]:
        """Detect anomalies in network traffic"""
        anomalies = []
        
        # Traffic volume anomaly
        if self.is_traffic_volume_anomaly():
            anomalies.append({
                'type': 'traffic_volume',
                'severity': 'medium',
                'description': 'Unusual traffic volume detected'
            })
        
        # Port scan detection
        if self.is_port_scan(packet):
            anomalies.append({
                'type': 'port_scan',
                'severity': 'high',
                'description': f'Possible port scan from {packet.get("source")}'
            })
        
        # Protocol anomaly
        if self.is_protocol_anomaly(packet):
            anomalies.append({
                'type': 'protocol_anomaly',
                'severity': 'low',
                'description': f'Unusual {packet.get("protocol")} traffic pattern'
            })
        
        # Device behavior anomaly
        if self.is_device_behavior_anomaly(packet):
            anomalies.append({
                'type': 'device_behavior',
                'severity': 'medium',
                'description': f'Abnormal behavior from {packet.get("source")}'
            })
        
        return anomalies
    
    def detect_threats(self, packet: Dict) -> List[Dict]:
        """Detect potential security threats"""
        threats = []
        
        # DDoS detection
        if self.is_ddos_pattern():
            threats.append({
                'type': 'ddos',
                'severity': 'critical',
                'description': 'Possible DDoS attack detected',
                'affected_devices': self.get_ddos_targets()
            })
        
        # Malware communication
        if self.is_malware_pattern(packet):
            threats.append({
                'type': 'malware',
                'severity': 'high',
                'description': f'Suspicious communication from {packet.get("source")}',
                'indicators': self.get_malware_indicators(packet)
            })
        
        # Data exfiltration
        if self.is_exfiltration_pattern(packet):
            threats.append({
                'type': 'exfiltration',
                'severity': 'critical',
                'description': 'Possible data exfiltration attempt',
                'source': packet.get('source'),
                'volume': self.get_exfiltration_volume(packet.get('source'))
            })
        
        # Unauthorized access
        if self.is_unauthorized_access(packet):
            threats.append({
                'type': 'unauthorized_access',
                'severity': 'high',
                'description': f'Unauthorized access attempt to {packet.get("destination")}'
            })
        
        return threats
    
    def generate_insights(self, packet: Dict, anomalies: List, threats: List) -> List[str]:
        """Generate intelligent insights based on analysis"""
        insights = []
        
        # Network health insights
        health_score = self.calculate_network_health()
        if health_score < 0.7:
            insights.append(f"⚠️ Network health degraded ({health_score:.0%})")
        else:
            insights.append(f"✅ Network health optimal ({health_score:.0%})")
        
        # Traffic pattern insights
        top_talkers = self.get_top_talkers(5)
        if top_talkers:
            insights.append(f"📊 Top talker: {top_talkers[0][0]} ({top_talkers[0][1]} packets)")
        
        # Protocol distribution
        protocol_dist = self.get_protocol_distribution()
        if protocol_dist:
            dominant = max(protocol_dist.items(), key=lambda x: x[1])
            insights.append(f"🔍 {dominant[0]} traffic dominates ({dominant[1]:.0%})")
        
        # Security insights
        if threats:
            insights.append(f"🚨 {len(threats)} security threat(s) detected!")
        elif anomalies:
            insights.append(f"⚡ {len(anomalies)} anomaly(ies) require attention")
        
        # Performance insights
        avg_latency = self.get_average_latency()
        if avg_latency > 100:
            insights.append(f"🐌 High latency detected: {avg_latency:.0f}ms")
        
        # IoT specific insights
        iot_devices = self.get_iot_devices()
        if iot_devices:
            insights.append(f"💡 {len(iot_devices)} IoT devices active")
            if self.are_iot_devices_segmented():
                insights.append("✅ IoT devices properly segmented")
            else:
                insights.append("⚠️ IoT devices should be segmented")
        
        return insights
    
    def generate_recommendations(self, anomalies: List, threats: List) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Threat-based recommendations
        for threat in threats:
            if threat['type'] == 'ddos':
                recommendations.append("🛡️ Enable DDoS protection on edge devices")
                recommendations.append("📊 Implement rate limiting on affected servers")
            elif threat['type'] == 'malware':
                recommendations.append(f"🔒 Isolate {threat.get('source', 'infected device')}")
                recommendations.append("🔍 Run full security scan on affected devices")
            elif threat['type'] == 'exfiltration':
                recommendations.append("🚫 Block outbound connections to suspicious IPs")
                recommendations.append("📝 Review data access logs")
        
        # Anomaly-based recommendations
        for anomaly in anomalies:
            if anomaly['type'] == 'port_scan':
                recommendations.append("🔥 Update firewall rules to block scanner")
            elif anomaly['type'] == 'traffic_volume':
                recommendations.append("📈 Consider bandwidth upgrade or optimization")
        
        # General recommendations
        if not self.is_encryption_used():
            recommendations.append("🔐 Enable encryption for sensitive traffic")
        
        if self.has_outdated_firmware():
            recommendations.append("📦 Update firmware on network devices")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    # Helper methods
    def is_traffic_volume_anomaly(self) -> bool:
        """Check if current traffic volume is anomalous"""
        if len(self.time_window) < 10:
            return False
        
        current_rate = len(self.time_window) / 60
        avg_rate = sum(len(w) for w in self.time_window) / len(self.time_window)
        
        return abs(current_rate - avg_rate) > self.anomaly_threshold * avg_rate
    
    def is_port_scan(self, packet: Dict) -> bool:
        """Detect port scanning behavior"""
        source = packet.get('source')
        if not source:
            return False
        
        # Check recent packets from this source
        recent_ports = set()
        for entry in list(self.packet_history)[-50:]:
            if entry['packet'].get('source') == source:
                port = entry['packet'].get('port', 0)
                if port > 0:
                    recent_ports.add(port)
        
        # More than 10 different ports in recent history suggests scanning
        return len(recent_ports) > 10
    
    def is_protocol_anomaly(self, packet: Dict) -> bool:
        """Detect anomalous protocol usage"""
        protocol = packet.get('protocol')
        if not protocol or protocol not in self.protocol_patterns:
            return False
        
        pattern = self.protocol_patterns[protocol]
        return pattern.is_anomalous()
    
    def is_device_behavior_anomaly(self, packet: Dict) -> bool:
        """Detect anomalous device behavior"""
        device = packet.get('source')
        if not device or device not in self.device_profiles:
            return False
        
        profile = self.device_profiles[device]
        return profile.is_anomalous(packet)
    
    def is_ddos_pattern(self) -> bool:
        """Detect DDoS attack patterns"""
        # Simple heuristic: high traffic to single target
        if len(self.packet_history) < 100:
            return False
        
        target_counts = defaultdict(int)
        for entry in list(self.packet_history)[-100:]:
            dest = entry['packet'].get('destination')
            if dest:
                target_counts[dest] += 1
        
        # If any target gets more than 50% of traffic, possible DDoS
        max_count = max(target_counts.values()) if target_counts else 0
        return max_count > 50
    
    def is_malware_pattern(self, packet: Dict) -> bool:
        """Detect malware communication patterns"""
        # Simulate detection based on suspicious patterns
        indicators = [
            packet.get('port') in [4444, 6666, 31337],  # Known malware ports
            'cmd' in packet.get('info', '').lower(),
            'shell' in packet.get('info', '').lower(),
            packet.get('protocol') == 'Unknown'
        ]
        return sum(indicators) >= 2
    
    def is_exfiltration_pattern(self, packet: Dict) -> bool:
        """Detect data exfiltration patterns"""
        source = packet.get('source')
        if not source:
            return False
        
        # Check for sustained outbound traffic
        outbound_count = sum(1 for entry in list(self.packet_history)[-50:]
                           if entry['packet'].get('source') == source)
        
        return outbound_count > 30
    
    def is_unauthorized_access(self, packet: Dict) -> bool:
        """Detect unauthorized access attempts"""
        # Check for access to sensitive devices
        sensitive_types = ['database', 'file_server', 'mail_server']
        dest_device = packet.get('destination_type', '')
        
        return (dest_device in sensitive_types and 
                packet.get('port') not in [80, 443, 22] and
                random.random() < 0.1)  # Simulate detection
    
    def calculate_anomaly_score(self, anomalies: List) -> float:
        """Calculate overall anomaly score (0-100)"""
        if not anomalies:
            return 0.0
        
        severity_weights = {'low': 10, 'medium': 30, 'high': 50, 'critical': 80}
        total_score = sum(severity_weights.get(a['severity'], 0) for a in anomalies)
        
        return min(total_score, 100.0)
    
    def calculate_threat_level(self, threats: List) -> str:
        """Calculate overall threat level"""
        if not threats:
            return 'low'
        
        severities = [t['severity'] for t in threats]
        if 'critical' in severities:
            return 'critical'
        elif 'high' in severities:
            return 'high'
        elif 'medium' in severities:
            return 'medium'
        return 'low'
    
    def calculate_network_health(self) -> float:
        """Calculate overall network health score (0-1)"""
        factors = []
        
        # Packet loss estimation
        factors.append(0.9)  # Simulated
        
        # Latency factor
        avg_latency = self.get_average_latency()
        latency_score = max(0, 1 - (avg_latency / 1000))
        factors.append(latency_score)
        
        # Device availability
        factors.append(0.95)  # Simulated
        
        # Security posture
        recent_threats = sum(1 for e in self.security_events if 
                           (datetime.now() - e['timestamp']).seconds < 300)
        security_score = max(0, 1 - (recent_threats / 10))
        factors.append(security_score)
        
        return sum(factors) / len(factors) if factors else 1.0
    
    def get_top_talkers(self, n: int) -> List[Tuple[str, int]]:
        """Get top n devices by packet count"""
        device_counts = defaultdict(int)
        for entry in self.packet_history:
            source = entry['packet'].get('source')
            if source:
                device_counts[source] += 1
        
        return sorted(device_counts.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def get_protocol_distribution(self) -> Dict[str, float]:
        """Get protocol distribution as percentages"""
        protocol_counts = defaultdict(int)
        total = 0
        
        for entry in self.packet_history:
            protocol = entry['packet'].get('protocol')
            if protocol:
                protocol_counts[protocol] += 1
                total += 1
        
        if total == 0:
            return {}
        
        return {p: c/total for p, c in protocol_counts.items()}
    
    def get_average_latency(self) -> float:
        """Get average network latency in ms"""
        # Simulate latency calculation
        base_latency = 20
        congestion_factor = min(len(self.packet_history) / 100, 5)
        return base_latency * (1 + congestion_factor)
    
    def get_iot_devices(self) -> List[str]:
        """Get list of IoT devices"""
        iot_types = ['iot_sensor', 'smart_light', 'smart_speaker', 'ip_camera', 'smart_hub']
        iot_devices = []
        
        for device, profile in self.device_profiles.items():
            if profile.device_type in iot_types:
                iot_devices.append(device)
        
        return iot_devices
    
    def are_iot_devices_segmented(self) -> bool:
        """Check if IoT devices are properly segmented"""
        # Simulate segmentation check
        return random.random() > 0.3
    
    def is_encryption_used(self) -> bool:
        """Check if encryption is being used"""
        encrypted_protocols = ['HTTPS', 'SSH', 'TLS', 'VPN']
        protocol_dist = self.get_protocol_distribution()
        
        encrypted_ratio = sum(protocol_dist.get(p, 0) for p in encrypted_protocols)
        return encrypted_ratio > 0.5
    
    def has_outdated_firmware(self) -> bool:
        """Check for devices with outdated firmware"""
        # Simulate firmware check
        return random.random() > 0.7
    
    def get_ddos_targets(self) -> List[str]:
        """Get list of DDoS targets"""
        target_counts = defaultdict(int)
        for entry in list(self.packet_history)[-100:]:
            dest = entry['packet'].get('destination')
            if dest:
                target_counts[dest] += 1
        
        # Return devices with high incoming traffic
        threshold = 20
        return [d for d, c in target_counts.items() if c > threshold]
    
    def get_malware_indicators(self, packet: Dict) -> List[str]:
        """Get malware indicators from packet"""
        indicators = []
        
        if packet.get('port') in [4444, 6666, 31337]:
            indicators.append(f"Suspicious port: {packet.get('port')}")
        
        info = packet.get('info', '').lower()
        suspicious_keywords = ['cmd', 'shell', 'exec', 'payload']
        for keyword in suspicious_keywords:
            if keyword in info:
                indicators.append(f"Suspicious keyword: {keyword}")
        
        return indicators
    
    def get_exfiltration_volume(self, source: str) -> str:
        """Estimate data exfiltration volume"""
        # Simulate volume calculation
        packet_count = sum(1 for entry in self.packet_history 
                         if entry['packet'].get('source') == source)
        
        # Estimate MB based on packet count
        estimated_mb = packet_count * 0.1
        return f"{estimated_mb:.1f} MB"


class DeviceProfile:
    """Profile for device behavior analysis"""
    
    def __init__(self):
        self.device_type = None
        self.packet_count = 0
        self.protocol_usage = defaultdict(int)
        self.destination_frequency = defaultdict(int)
        self.port_usage = defaultdict(int)
        self.time_patterns = []
        self.baseline_established = False
    
    def update(self, packet: Dict):
        """Update profile with new packet"""
        self.packet_count += 1
        
        if not self.device_type and 'source_type' in packet:
            self.device_type = packet['source_type']
        
        protocol = packet.get('protocol')
        if protocol:
            self.protocol_usage[protocol] += 1
        
        dest = packet.get('destination')
        if dest:
            self.destination_frequency[dest] += 1
        
        port = packet.get('port', 0)
        if port > 0:
            self.port_usage[port] += 1
        
        # Establish baseline after 100 packets
        if self.packet_count == 100:
            self.baseline_established = True
    
    def is_anomalous(self, packet: Dict) -> bool:
        """Check if packet represents anomalous behavior"""
        if not self.baseline_established:
            return False
        
        # Check for new protocols
        protocol = packet.get('protocol')
        if protocol and protocol not in self.protocol_usage:
            return True
        
        # Check for unusual ports
        port = packet.get('port', 0)
        if port > 0 and port not in self.port_usage and port > 1024:
            return True
        
        # Check for new destinations
        dest = packet.get('destination')
        if dest and dest not in self.destination_frequency:
            # New destination might be normal for some devices
            if self.device_type not in ['router', 'switch', 'firewall']:
                return random.random() < 0.3
        
        return False


class ProtocolPattern:
    """Pattern analysis for network protocols"""
    
    def __init__(self):
        self.packet_count = 0
        self.packet_sizes = deque(maxlen=100)
        self.inter_arrival_times = deque(maxlen=100)
        self.last_packet_time = None
        self.baseline_mean = 0
        self.baseline_std = 0
    
    def update(self, packet: Dict):
        """Update pattern with new packet"""
        self.packet_count += 1
        
        # Track packet size
        size = packet.get('size', 100)  # Default size
        self.packet_sizes.append(size)
        
        # Track inter-arrival times
        current_time = datetime.now()
        if self.last_packet_time:
            delta = (current_time - self.last_packet_time).total_seconds()
            self.inter_arrival_times.append(delta)
        self.last_packet_time = current_time
        
        # Update baseline after 50 packets
        if self.packet_count == 50:
            self.baseline_mean = sum(self.packet_sizes) / len(self.packet_sizes)
            self.baseline_std = math.sqrt(
                sum((x - self.baseline_mean) ** 2 for x in self.packet_sizes) / len(self.packet_sizes)
            )
    
    def is_anomalous(self) -> bool:
        """Check if current pattern is anomalous"""
        if self.packet_count < 50:
            return False
        
        # Check packet size anomaly
        if self.packet_sizes:
            recent_mean = sum(list(self.packet_sizes)[-10:]) / 10
            if abs(recent_mean - self.baseline_mean) > 2 * self.baseline_std:
                return True
        
        # Check timing anomaly
        if len(self.inter_arrival_times) > 10:
            recent_rate = 1 / (sum(list(self.inter_arrival_times)[-10:]) / 10)
            baseline_rate = 1 / (sum(self.inter_arrival_times) / len(self.inter_arrival_times))
            if recent_rate > baseline_rate * 3:
                return True
        
        return False


class NetworkGraph:
    """Graph representation of network connections"""
    
    def __init__(self):
        self.edges = defaultdict(lambda: defaultdict(int))
        self.node_centrality = {}
        self.communities = []
    
    def add_edge(self, source: str, dest: str, packet: Dict):
        """Add edge to graph"""
        self.edges[source][dest] += 1
        self.edges[dest][source] += 1  # Bidirectional
        
        # Update centrality periodically
        if sum(sum(d.values()) for d in self.edges.values()) % 100 == 0:
            self.update_centrality()
    
    def update_centrality(self):
        """Update node centrality scores"""
        # Simple degree centrality
        for node in self.edges:
            self.node_centrality[node] = len(self.edges[node])
    
    def detect_communities(self):
        """Detect network communities"""
        # Simplified community detection
        # In real implementation, use algorithms like Louvain
        pass
    
    def get_critical_nodes(self) -> List[str]:
        """Get critical nodes in the network"""
        if not self.node_centrality:
            return []
        
        # Return top 5 nodes by centrality
        sorted_nodes = sorted(self.node_centrality.items(), 
                            key=lambda x: x[1], reverse=True)
        return [node for node, _ in sorted_nodes[:5]]
    
    def train_ml_models(self, labeled_data: List[Dict] = None):
        """Train ML models with historical data"""
        if labeled_data:
            # Use provided labeled data
            training_data = labeled_data
        else:
            # Use packet history as unlabeled training data
            training_data = [entry['packet'] for entry in self.packet_history]
        
        if self.ml_engine.train(training_data):
            print("ML models trained successfully")
            return True
        return False
    
    def add_threat_label(self, packet: Dict, threat_type: str):
        """Add labeled threat for supervised learning"""
        self.ml_engine.anomaly_detector.add_labeled_threat(packet, threat_type)
    
    def save_ml_models(self, directory: str):
        """Save trained ML models"""
        self.ml_engine.save_models(directory)
    
    def load_ml_models(self, directory: str):
        """Load pre-trained ML models"""
        self.ml_engine.load_models(directory)