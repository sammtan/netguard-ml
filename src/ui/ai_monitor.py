"""
AI Monitor widget for real-time traffic analysis
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QLabel,
    QProgressBar, QHBoxLayout, QGroupBox,
    QGridLayout
)
from PySide6.QtCore import QTimer, Signal
from PySide6.QtGui import QTextCursor
from src.ai.network_ai import NetworkAI
from src.ui.theme import COLORS

import random


class AIMonitorWidget(QWidget):
    """AI monitoring and analysis panel"""
    
    alert_generated = Signal(str, str)  # severity, message
    
    def __init__(self):
        super().__init__()
        self.monitoring = False
        self.packet_count = 0
        self.anomaly_score = 0
        
        # Initialize AI engine
        self.ai_engine = NetworkAI()
        
        # Threat tracking
        self.current_threats = []
        self.threat_history = []
        
        self.init_ui()
        
        # Analysis timer
        self.analysis_timer = QTimer()
        self.analysis_timer.timeout.connect(self.analyze_traffic)
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Title and Status
        header_layout = QHBoxLayout()
        
        title = QLabel("🧠 AI Traffic Monitor")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.status_label = QLabel("Status: Idle")
        self.status_label.setStyleSheet(f"padding: 4px 8px; background-color: {COLORS['surface_light']}; border-radius: 4px;")
        header_layout.addWidget(self.status_label)
        
        layout.addLayout(header_layout)
        
        # Metrics Dashboard
        metrics_group = QGroupBox("Network Metrics")
        metrics_layout = QGridLayout()
        
        # Packet rate
        self.packet_rate_label = QLabel("0")
        self.packet_rate_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        metrics_layout.addWidget(QLabel("Packets/s:"), 0, 0)
        metrics_layout.addWidget(self.packet_rate_label, 0, 1)
        
        # Network health
        self.health_label = QLabel("100%")
        self.health_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #00ff00;")
        metrics_layout.addWidget(QLabel("Health:"), 0, 2)
        metrics_layout.addWidget(self.health_label, 0, 3)
        
        # Threat level
        self.threat_label = QLabel("Low")
        self.threat_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #00ff00;")
        metrics_layout.addWidget(QLabel("Threat Level:"), 1, 0)
        metrics_layout.addWidget(self.threat_label, 1, 1)
        
        # Active threats
        self.active_threats_label = QLabel("0")
        self.active_threats_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        metrics_layout.addWidget(QLabel("Active Threats:"), 1, 2)
        metrics_layout.addWidget(self.active_threats_label, 1, 3)
        
        metrics_group.setLayout(metrics_layout)
        layout.addWidget(metrics_group)
        
        # Anomaly Detection
        anomaly_group = QGroupBox("Anomaly Detection")
        anomaly_layout = QVBoxLayout()
        
        # Anomaly score
        anomaly_header = QHBoxLayout()
        anomaly_header.addWidget(QLabel("Anomaly Score:"))
        self.anomaly_label = QLabel("0%")
        self.anomaly_label.setStyleSheet("font-weight: bold;")
        anomaly_header.addWidget(self.anomaly_label)
        anomaly_header.addStretch()
        anomaly_layout.addLayout(anomaly_header)
        
        # Anomaly bar
        self.anomaly_bar = QProgressBar()
        self.anomaly_bar.setRange(0, 100)
        self.anomaly_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                text-align: center;
                height: 20px;
            }}
            QProgressBar::chunk {{
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #00ff00, stop: 0.5 #ffff00, stop: 1 #ff0000);
                border-radius: 3px;
            }}
        """)
        anomaly_layout.addWidget(self.anomaly_bar)
        
        anomaly_group.setLayout(anomaly_layout)
        layout.addWidget(anomaly_group)
        
        # AI Insights
        insights_group = QGroupBox("AI Insights & Recommendations")
        insights_layout = QVBoxLayout()
        
        self.insights_text = QTextEdit()
        self.insights_text.setReadOnly(True)
        self.insights_text.setMaximumHeight(150)
        insights_layout.addWidget(self.insights_text)
        
        insights_group.setLayout(insights_layout)
        layout.addWidget(insights_group)
        
        # Recommendations
        recommendations_group = QGroupBox("Security Recommendations")
        recommendations_layout = QVBoxLayout()
        
        self.recommendations_text = QTextEdit()
        self.recommendations_text.setReadOnly(True)
        self.recommendations_text.setMaximumHeight(100)
        recommendations_layout.addWidget(self.recommendations_text)
        
        recommendations_group.setLayout(recommendations_layout)
        layout.addWidget(recommendations_group)
        
        # Add initial message
        self.add_insight("🤖 AI Monitor ready. Start simulation to begin analysis.", "info")
        
        layout.addStretch()
    
    def start_monitoring(self):
        """Start AI monitoring"""
        self.monitoring = True
        self.status_label.setText("Status: 🟢 Active")
        self.status_label.setStyleSheet(f"padding: 4px 8px; background-color: {COLORS['success']}; color: black; border-radius: 4px; font-weight: bold;")
        self.analysis_timer.start(2000)  # Analyze every 2 seconds
        self.add_insight("✅ AI monitoring started - Analyzing network patterns...", "success")
    
    def stop_monitoring(self):
        """Stop AI monitoring"""
        self.monitoring = False
        self.status_label.setText("Status: 🔴 Stopped")
        self.status_label.setStyleSheet(f"padding: 4px 8px; background-color: {COLORS['error']}; color: white; border-radius: 4px; font-weight: bold;")
        self.analysis_timer.stop()
        self.add_insight("⏹️ AI monitoring stopped", "info")
    
    def update_traffic(self, packet_data):
        """Update traffic data and analyze with AI"""
        self.packet_count += 1
        
        # Add device type information to packet
        packet_data['source_type'] = self.get_device_type(packet_data.get('source'))
        packet_data['destination_type'] = self.get_device_type(packet_data.get('destination'))
        
        # Analyze packet with AI
        analysis = self.ai_engine.analyze_packet(packet_data)
        
        # Update UI with analysis results
        self.update_ui_with_analysis(analysis)
        
        # Update packet rate
        self.packet_rate_label.setText(f"{self.packet_count % 10 + 5}")
    
    def analyze_traffic(self):
        """Perform periodic AI analysis"""
        if not self.monitoring:
            return
        
        # Get comprehensive network analysis
        network_health = self.ai_engine.calculate_network_health()
        
        # Update health display
        health_percent = int(network_health * 100)
        self.health_label.setText(f"{health_percent}%")
        if health_percent > 80:
            self.health_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #00ff00;")
        elif health_percent > 60:
            self.health_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffaa00;")
        else:
            self.health_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ff0000;")
        
        # Generate periodic insights
        if random.random() < 0.5:  # 50% chance for new insight
            # Create a dummy packet for periodic analysis
            analysis = self.ai_engine.analyze_packet({
                'source': 'periodic_check',
                'destination': 'network',
                'protocol': 'MONITOR'
            })
            
            # Add insights
            for insight in analysis.get('insights', []):
                self.add_insight(insight, "info")
            
            # Update recommendations
            self.update_recommendations(analysis.get('recommendations', []))
    
    def update_ui_with_analysis(self, analysis):
        """Update UI with AI analysis results"""
        # Update anomaly score
        anomaly_score = analysis.get('anomaly_score', 0)
        self.anomaly_score = anomaly_score
        self.anomaly_bar.setValue(int(anomaly_score))
        self.anomaly_label.setText(f"{int(anomaly_score)}%")
        
        # Update threat level
        threat_level = analysis.get('threat_level', 'low')
        self.update_threat_level(threat_level)
        
        # Count active threats
        if threat_level in ['high', 'critical']:
            self.current_threats.append(analysis)
        
        self.active_threats_label.setText(str(len(self.current_threats)))
        
        # Add insights
        for insight in analysis.get('insights', [])[:2]:  # Limit insights per packet
            self.add_insight(insight, "info")
    
    def update_threat_level(self, level):
        """Update threat level display"""
        self.threat_label.setText(level.capitalize())
        
        if level == 'low':
            self.threat_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #00ff00;")
        elif level == 'medium':
            self.threat_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffaa00;")
        elif level == 'high':
            self.threat_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ff6600;")
        elif level == 'critical':
            self.threat_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ff0000;")
    
    def update_recommendations(self, recommendations):
        """Update recommendations display"""
        if recommendations:
            cursor = self.recommendations_text.textCursor()
            cursor.movePosition(QTextCursor.End)
            
            # Clear old recommendations
            self.recommendations_text.clear()
            
            # Add new recommendations
            for rec in recommendations:
                cursor.insertHtml(f'<span style="color: {COLORS["text_primary"]};">• {rec}</span><br>')
            
            # Auto-scroll
            self.recommendations_text.verticalScrollBar().setValue(
                self.recommendations_text.verticalScrollBar().maximum()
            )
    
    def get_device_type(self, device_id):
        """Get device type from device ID"""
        # Extract type from device ID (e.g., "router_1" -> "router")
        if device_id:
            parts = device_id.split('_')
            if parts:
                return parts[0]
        return "unknown"
    
    def add_insight(self, message: str, severity: str = "info"):
        """Add an insight to the display"""
        cursor = self.insights_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        # Color based on severity
        colors = {
            "info": "#00a2e8",
            "success": "#00ff00",
            "warning": "#ffaa00",
            "critical": "#ff0000"
        }
        
        color = colors.get(severity, "#ffffff")
        
        # Insert formatted text with proper line break
        cursor.insertHtml(
            f'<span style="color: {color};">{message}</span><br>'
        )
        
        # Auto-scroll
        self.insights_text.verticalScrollBar().setValue(
            self.insights_text.verticalScrollBar().maximum()
        )