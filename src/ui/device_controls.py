"""
Device Control Panels - Unique interface for each device type
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QWidget, QGridLayout, QLineEdit, QTextEdit,
    QComboBox, QSpinBox, QCheckBox, QGroupBox, QSlider,
    QProgressBar, QTableWidget, QTableWidgetItem, QHeaderView,
    QFrame, QScrollArea
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QIcon
from src.ui.theme import COLORS
import random


class DeviceControlPanel(QDialog):
    """Base control panel for devices"""
    
    device_updated = Signal(object)
    
    def __init__(self, device, parent=None):
        super().__init__(parent)
        self.device = device
        self.setWindowTitle(f"{device.identity.hostname} - Control Panel")
        self.setModal(False)
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        # Set window flags to stay on top
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Main content
        content = self.create_content()
        layout.addWidget(content, 1)
        
        # Footer
        footer = self.create_footer()
        layout.addWidget(footer)
        
    def create_header(self):
        """Create header with device info"""
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border-bottom: 2px solid {COLORS['accent_blue']};
                padding: 16px;
            }}
        """)
        
        layout = QVBoxLayout(header)
        
        # Device icon and name
        title_layout = QHBoxLayout()
        
        icon_label = QLabel(self.device.icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 32))
        title_layout.addWidget(icon_label)
        
        info_layout = QVBoxLayout()
        
        hostname_label = QLabel(self.device.identity.hostname)
        hostname_label.setFont(QFont("Inter", 16, QFont.Bold))
        info_layout.addWidget(hostname_label)
        
        model_label = QLabel(f"{self.device.identity.manufacturer} {self.device.identity.model}")
        model_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        info_layout.addWidget(model_label)
        
        title_layout.addLayout(info_layout)
        title_layout.addStretch()
        
        # Status indicator
        status_layout = QVBoxLayout()
        status_label = QLabel("Status")
        status_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px;")
        status_layout.addWidget(status_label)
        
        self.status_indicator = QLabel("● Online" if self.device.is_running else "● Offline")
        self.status_indicator.setStyleSheet(
            f"color: {COLORS['success'] if self.device.is_running else COLORS['error']}; font-size: 14px; font-weight: bold;"
        )
        status_layout.addWidget(self.status_indicator)
        
        title_layout.addLayout(status_layout)
        
        layout.addLayout(title_layout)
        
        return header
    
    def create_content(self):
        """Create main content area"""
        # Override in subclasses
        content = QTabWidget()
        content.setStyleSheet(f"""
            QTabWidget::pane {{
                background-color: {COLORS['background']};
                border: none;
            }}
        """)
        
        # General tab
        general_tab = self.create_general_tab()
        content.addTab(general_tab, "General")
        
        # Device-specific tabs
        self.add_device_specific_tabs(content)
        
        return content
    
    def create_general_tab(self):
        """Create general information tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Identity section
        identity_group = QGroupBox("Identity")
        identity_layout = QGridLayout()
        
        fields = [
            ("Hostname:", self.device.identity.hostname),
            ("IP Address:", self.device.identity.ip_address),
            ("MAC Address:", self.device.identity.mac_address),
            ("Serial Number:", self.device.identity.serial_number),
            ("Firmware:", self.device.identity.firmware_version),
        ]
        
        for i, (label, value) in enumerate(fields):
            label_widget = QLabel(label)
            label_widget.setStyleSheet(f"color: {COLORS['text_secondary']};")
            value_widget = QLineEdit(value)
            value_widget.setReadOnly(True)
            value_widget.setFont(QFont("JetBrains Mono", 10))
            
            identity_layout.addWidget(label_widget, i, 0)
            identity_layout.addWidget(value_widget, i, 1)
        
        identity_group.setLayout(identity_layout)
        layout.addWidget(identity_group)
        
        # Properties section
        if self.device.identity.properties:
            props_group = QGroupBox("Device Properties")
            props_layout = QGridLayout()
            
            for i, (key, value) in enumerate(self.device.identity.properties.items()):
                label_widget = QLabel(f"{key.replace('_', ' ').title()}:")
                label_widget.setStyleSheet(f"color: {COLORS['text_secondary']};")
                value_widget = QLabel(str(value))
                value_widget.setFont(QFont("JetBrains Mono", 10))
                
                props_layout.addWidget(label_widget, i, 0)
                props_layout.addWidget(value_widget, i, 1)
            
            props_group.setLayout(props_layout)
            layout.addWidget(props_group)
        
        layout.addStretch()
        return widget
    
    def add_device_specific_tabs(self, tab_widget):
        """Add device-specific tabs based on device type"""
        # Override in subclasses
        pass
    
    def create_footer(self):
        """Create footer with action buttons"""
        footer = QFrame()
        footer.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border-top: 1px solid {COLORS['border']};
                padding: 8px;
            }}
        """)
        
        layout = QHBoxLayout(footer)
        
        # Power button
        self.power_btn = QPushButton("Power On" if not self.device.is_running else "Power Off")
        self.power_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_red'] if self.device.is_running else COLORS['accent_blue']};
                color: white;
                font-weight: bold;
                padding: 8px 16px;
            }}
        """)
        self.power_btn.clicked.connect(self.toggle_power)
        layout.addWidget(self.power_btn)
        
        layout.addStretch()
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        return footer
    
    def toggle_power(self):
        """Toggle device power state"""
        if self.device.is_running:
            self.device.stop()
            self.power_btn.setText("Power On")
            self.power_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['accent_blue']};
                    color: white;
                    font-weight: bold;
                    padding: 8px 16px;
                }}
            """)
            self.status_indicator.setText("● Offline")
            self.status_indicator.setStyleSheet(f"color: {COLORS['error']}; font-size: 14px; font-weight: bold;")
        else:
            self.device.start()
            self.power_btn.setText("Power Off")
            self.power_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['accent_red']};
                    color: white;
                    font-weight: bold;
                    padding: 8px 16px;
                }}
            """)
            self.status_indicator.setText("● Online")
            self.status_indicator.setStyleSheet(f"color: {COLORS['success']}; font-size: 14px; font-weight: bold;")
        
        self.device_updated.emit(self.device)


class RouterControlPanel(DeviceControlPanel):
    """Control panel for routers"""
    
    def add_device_specific_tabs(self, tab_widget):
        """Add router-specific tabs"""
        # Routing tab
        routing_tab = self.create_routing_tab()
        tab_widget.addTab(routing_tab, "Routing")
        
        # Interfaces tab
        interfaces_tab = self.create_interfaces_tab()
        tab_widget.addTab(interfaces_tab, "Interfaces")
        
        # Security tab
        security_tab = self.create_security_tab()
        tab_widget.addTab(security_tab, "Security")
    
    def create_routing_tab(self):
        """Create routing configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Routing table
        routing_group = QGroupBox("Routing Table")
        routing_layout = QVBoxLayout()
        
        # Table widget
        self.routing_table = QTableWidget()
        self.routing_table.setColumnCount(4)
        self.routing_table.setHorizontalHeaderLabels(["Destination", "Gateway", "Interface", "Metric"])
        self.routing_table.horizontalHeader().setStretchLastSection(True)
        
        # Add sample routes
        routes = [
            ("0.0.0.0/0", "192.168.1.1", "eth0", "1"),
            ("192.168.1.0/24", "0.0.0.0", "eth1", "0"),
            ("10.0.0.0/8", "192.168.1.254", "eth0", "10"),
        ]
        
        self.routing_table.setRowCount(len(routes))
        for i, route in enumerate(routes):
            for j, value in enumerate(route):
                item = QTableWidgetItem(value)
                item.setFont(QFont("JetBrains Mono", 9))
                self.routing_table.setItem(i, j, item)
        
        routing_layout.addWidget(self.routing_table)
        
        # Route actions
        route_actions = QHBoxLayout()
        add_route_btn = QPushButton("Add Route")
        add_route_btn.setIcon(QIcon("➕"))
        route_actions.addWidget(add_route_btn)
        
        del_route_btn = QPushButton("Delete Route")
        del_route_btn.setIcon(QIcon("➖"))
        route_actions.addWidget(del_route_btn)
        
        route_actions.addStretch()
        routing_layout.addLayout(route_actions)
        
        routing_group.setLayout(routing_layout)
        layout.addWidget(routing_group)
        
        # Routing protocols
        protocols_group = QGroupBox("Routing Protocols")
        protocols_layout = QVBoxLayout()
        
        bgp_check = QCheckBox("BGP (Border Gateway Protocol)")
        bgp_check.setChecked(True)
        protocols_layout.addWidget(bgp_check)
        
        ospf_check = QCheckBox("OSPF (Open Shortest Path First)")
        ospf_check.setChecked(True)
        protocols_layout.addWidget(ospf_check)
        
        eigrp_check = QCheckBox("EIGRP (Enhanced Interior Gateway Routing Protocol)")
        protocols_layout.addWidget(eigrp_check)
        
        rip_check = QCheckBox("RIP (Routing Information Protocol)")
        protocols_layout.addWidget(rip_check)
        
        protocols_group.setLayout(protocols_layout)
        layout.addWidget(protocols_group)
        
        layout.addStretch()
        return widget
    
    def create_interfaces_tab(self):
        """Create interfaces configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Interfaces list
        interfaces_group = QGroupBox("Network Interfaces")
        interfaces_layout = QVBoxLayout()
        
        # Create interface widgets
        for i in range(min(4, self.device.identity.properties.get('interfaces', 4))):
            interface_frame = QFrame()
            interface_frame.setFrameStyle(QFrame.Box)
            interface_frame.setStyleSheet(f"QFrame {{ border: 1px solid {COLORS['border']}; border-radius: 4px; padding: 8px; }}")
            
            interface_layout = QHBoxLayout(interface_frame)
            
            # Interface name
            name_label = QLabel(f"eth{i}")
            name_label.setFont(QFont("JetBrains Mono", 12, QFont.Bold))
            interface_layout.addWidget(name_label)
            
            # Status LED
            status_led = QLabel("●")
            status_led.setStyleSheet(f"color: {COLORS['success'] if random.random() > 0.3 else COLORS['error']};")
            interface_layout.addWidget(status_led)
            
            # IP configuration
            ip_layout = QVBoxLayout()
            ip_label = QLabel(f"IP: 192.168.{i+1}.1/24")
            ip_label.setFont(QFont("JetBrains Mono", 9))
            ip_layout.addWidget(ip_label)
            
            speed_label = QLabel(f"Speed: {self.device.identity.properties.get('throughput_gbps', 1)}Gbps")
            speed_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
            ip_layout.addWidget(speed_label)
            
            interface_layout.addLayout(ip_layout)
            interface_layout.addStretch()
            
            # Configure button
            config_btn = QPushButton("Configure")
            interface_layout.addWidget(config_btn)
            
            interfaces_layout.addWidget(interface_frame)
        
        interfaces_group.setLayout(interfaces_layout)
        
        # Create scroll area for interfaces
        scroll = QScrollArea()
        scroll.setWidget(interfaces_group)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        return widget
    
    def create_security_tab(self):
        """Create security configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Access Control Lists
        acl_group = QGroupBox("Access Control Lists (ACL)")
        acl_layout = QVBoxLayout()
        
        self.acl_table = QTableWidget()
        self.acl_table.setColumnCount(5)
        self.acl_table.setHorizontalHeaderLabels(["Action", "Protocol", "Source", "Destination", "Port"])
        
        # Sample ACL rules
        acl_rules = [
            ("Permit", "TCP", "192.168.1.0/24", "Any", "80"),
            ("Permit", "TCP", "192.168.1.0/24", "Any", "443"),
            ("Deny", "ICMP", "0.0.0.0/0", "192.168.1.0/24", "Any"),
        ]
        
        self.acl_table.setRowCount(len(acl_rules))
        for i, rule in enumerate(acl_rules):
            for j, value in enumerate(rule):
                item = QTableWidgetItem(value)
                item.setFont(QFont("JetBrains Mono", 9))
                self.acl_table.setItem(i, j, item)
        
        acl_layout.addWidget(self.acl_table)
        acl_group.setLayout(acl_layout)
        layout.addWidget(acl_group)
        
        # Security features
        features_group = QGroupBox("Security Features")
        features_layout = QVBoxLayout()
        
        firewall_check = QCheckBox("Enable Stateful Firewall")
        firewall_check.setChecked(True)
        features_layout.addWidget(firewall_check)
        
        ddos_check = QCheckBox("DDoS Protection")
        ddos_check.setChecked(True)
        features_layout.addWidget(ddos_check)
        
        ipsec_check = QCheckBox("IPSec VPN Support")
        ipsec_check.setChecked(True)
        features_layout.addWidget(ipsec_check)
        
        features_group.setLayout(features_layout)
        layout.addWidget(features_group)
        
        layout.addStretch()
        return widget


class ServerControlPanel(DeviceControlPanel):
    """Control panel for servers"""
    
    def __init__(self, device, parent=None):
        super().__init__(device, parent)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_metrics)
        self.update_timer.start(2000)  # Update every 2 seconds
    
    def add_device_specific_tabs(self, tab_widget):
        """Add server-specific tabs"""
        # Performance tab
        performance_tab = self.create_performance_tab()
        tab_widget.addTab(performance_tab, "Performance")
        
        # Services tab
        services_tab = self.create_services_tab()
        tab_widget.addTab(services_tab, "Services")
        
        # Storage tab
        storage_tab = self.create_storage_tab()
        tab_widget.addTab(storage_tab, "Storage")
    
    def create_performance_tab(self):
        """Create performance monitoring tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # CPU metrics
        cpu_group = QGroupBox("CPU Performance")
        cpu_layout = QVBoxLayout()
        
        # CPU usage
        cpu_label = QLabel("CPU Usage")
        cpu_layout.addWidget(cpu_label)
        
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setRange(0, 100)
        self.cpu_progress.setValue(random.randint(20, 80))
        self.cpu_progress.setStyleSheet(f"""
            QProgressBar::chunk {{
                background-color: {COLORS['accent_blue']};
            }}
        """)
        cpu_layout.addWidget(self.cpu_progress)
        
        # CPU cores info
        cores_info = QLabel(f"Cores: {self.device.identity.properties.get('cpu_cores', 8)} | Load Average: {random.uniform(0.5, 2.5):.2f}")
        cores_info.setStyleSheet(f"color: {COLORS['text_secondary']};")
        cpu_layout.addWidget(cores_info)
        
        cpu_group.setLayout(cpu_layout)
        layout.addWidget(cpu_group)
        
        # Memory metrics
        mem_group = QGroupBox("Memory Usage")
        mem_layout = QVBoxLayout()
        
        mem_label = QLabel("RAM Usage")
        mem_layout.addWidget(mem_label)
        
        self.mem_progress = QProgressBar()
        self.mem_progress.setRange(0, 100)
        self.mem_progress.setValue(random.randint(40, 90))
        self.mem_progress.setStyleSheet(f"""
            QProgressBar::chunk {{
                background-color: {COLORS['accent_red'] if self.mem_progress.value() > 80 else COLORS['accent_blue']};
            }}
        """)
        mem_layout.addWidget(self.mem_progress)
        
        # Memory info
        total_ram = self.device.identity.properties.get('ram_gb', 32)
        used_ram = (self.mem_progress.value() / 100) * total_ram
        mem_info = QLabel(f"Used: {used_ram:.1f}GB / {total_ram}GB")
        mem_info.setStyleSheet(f"color: {COLORS['text_secondary']};")
        mem_layout.addWidget(mem_info)
        
        mem_group.setLayout(mem_layout)
        layout.addWidget(mem_group)
        
        # Network metrics
        net_group = QGroupBox("Network Activity")
        net_layout = QHBoxLayout()
        
        # Upload
        upload_layout = QVBoxLayout()
        upload_label = QLabel("Upload")
        upload_layout.addWidget(upload_label)
        self.upload_rate = QLabel(f"{random.randint(10, 100)} Mbps")
        self.upload_rate.setFont(QFont("JetBrains Mono", 14, QFont.Bold))
        self.upload_rate.setStyleSheet(f"color: {COLORS['accent_blue']};")
        upload_layout.addWidget(self.upload_rate)
        net_layout.addLayout(upload_layout)
        
        # Download
        download_layout = QVBoxLayout()
        download_label = QLabel("Download")
        download_layout.addWidget(download_label)
        self.download_rate = QLabel(f"{random.randint(50, 200)} Mbps")
        self.download_rate.setFont(QFont("JetBrains Mono", 14, QFont.Bold))
        self.download_rate.setStyleSheet(f"color: {COLORS['success']};")
        download_layout.addWidget(self.download_rate)
        net_layout.addLayout(download_layout)
        
        net_group.setLayout(net_layout)
        layout.addWidget(net_group)
        
        layout.addStretch()
        return widget
    
    def create_services_tab(self):
        """Create services management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Services list
        services_group = QGroupBox("Running Services")
        services_layout = QVBoxLayout()
        
        self.services_table = QTableWidget()
        self.services_table.setColumnCount(4)
        self.services_table.setHorizontalHeaderLabels(["Service", "Status", "Port", "Memory"])
        self.services_table.horizontalHeader().setStretchLastSection(True)
        
        # Define services based on server type
        services = self._get_server_services()
        
        self.services_table.setRowCount(len(services))
        for i, service in enumerate(services):
            for j, value in enumerate(service):
                item = QTableWidgetItem(str(value))
                if j == 1:  # Status column
                    if value == "Running":
                        item.setForeground(QColor(COLORS['success']))
                    else:
                        item.setForeground(QColor(COLORS['error']))
                item.setFont(QFont("JetBrains Mono", 9))
                self.services_table.setItem(i, j, item)
        
        services_layout.addWidget(self.services_table)
        
        # Service actions
        actions_layout = QHBoxLayout()
        start_btn = QPushButton("Start")
        stop_btn = QPushButton("Stop")
        restart_btn = QPushButton("Restart")
        
        actions_layout.addWidget(start_btn)
        actions_layout.addWidget(stop_btn)
        actions_layout.addWidget(restart_btn)
        actions_layout.addStretch()
        
        services_layout.addLayout(actions_layout)
        services_group.setLayout(services_layout)
        layout.addWidget(services_group)
        
        layout.addStretch()
        return widget
    
    def create_storage_tab(self):
        """Create storage management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Storage overview
        storage_group = QGroupBox("Storage Overview")
        storage_layout = QVBoxLayout()
        
        # Total storage
        total_storage = self.device.identity.properties.get('storage_tb', 2) * 1024  # Convert to GB
        used_storage = random.randint(100, int(total_storage * 0.8))
        
        storage_progress = QProgressBar()
        storage_progress.setRange(0, 100)
        storage_progress.setValue(int((used_storage / total_storage) * 100))
        storage_layout.addWidget(storage_progress)
        
        storage_info = QLabel(f"Used: {used_storage}GB / {total_storage}GB ({storage_progress.value()}%)")
        storage_info.setStyleSheet(f"color: {COLORS['text_secondary']};")
        storage_layout.addWidget(storage_info)
        
        storage_group.setLayout(storage_layout)
        layout.addWidget(storage_group)
        
        # RAID configuration
        raid_group = QGroupBox("RAID Configuration")
        raid_layout = QVBoxLayout()
        
        raid_level = self.device.identity.properties.get('raid_level', 'RAID 1')
        raid_info = QLabel(f"Current Configuration: {raid_level}")
        raid_info.setFont(QFont("Inter", 11, QFont.Bold))
        raid_layout.addWidget(raid_info)
        
        # Disk status
        disk_table = QTableWidget()
        disk_table.setColumnCount(4)
        disk_table.setHorizontalHeaderLabels(["Disk", "Size", "Status", "Health"])
        
        num_disks = 4 if 'RAID 5' in raid_level else 2
        disk_table.setRowCount(num_disks)
        
        for i in range(num_disks):
            disk_table.setItem(i, 0, QTableWidgetItem(f"/dev/sd{chr(97+i)}"))
            disk_table.setItem(i, 1, QTableWidgetItem(f"{total_storage // num_disks}GB"))
            
            status_item = QTableWidgetItem("Active")
            status_item.setForeground(QColor(COLORS['success']))
            disk_table.setItem(i, 2, status_item)
            
            health = random.choice(["Healthy", "Healthy", "Healthy", "Warning"])
            health_item = QTableWidgetItem(health)
            health_item.setForeground(QColor(COLORS['success'] if health == "Healthy" else COLORS['warning']))
            disk_table.setItem(i, 3, health_item)
        
        raid_layout.addWidget(disk_table)
        raid_group.setLayout(raid_layout)
        layout.addWidget(raid_group)
        
        layout.addStretch()
        return widget
    
    def _get_server_services(self):
        """Get services based on server type"""
        device_type = self.device.device_type
        
        if device_type == 'web_server':
            return [
                ("nginx", "Running", 80, "125MB"),
                ("php-fpm", "Running", 9000, "256MB"),
                ("mysql", "Running", 3306, "512MB"),
                ("redis", "Running", 6379, "64MB"),
            ]
        elif device_type == 'database':
            return [
                ("postgresql", "Running", 5432, "2GB"),
                ("pgbouncer", "Running", 6432, "32MB"),
                ("pg_backup", "Running", "-", "16MB"),
            ]
        elif device_type == 'mail_server':
            return [
                ("postfix", "Running", 25, "64MB"),
                ("dovecot", "Running", 143, "128MB"),
                ("spamassassin", "Running", 783, "256MB"),
                ("clamav", "Running", 3310, "512MB"),
            ]
        else:  # Generic server
            return [
                ("sshd", "Running", 22, "16MB"),
                ("systemd", "Running", "-", "64MB"),
                ("docker", "Running", 2375, "256MB"),
                ("monitoring", "Running", 9090, "128MB"),
            ]
    
    def update_metrics(self):
        """Update performance metrics"""
        if hasattr(self, 'cpu_progress'):
            # Update CPU
            current_cpu = self.cpu_progress.value()
            new_cpu = max(0, min(100, current_cpu + random.randint(-10, 10)))
            self.cpu_progress.setValue(new_cpu)
            
            # Update Memory
            current_mem = self.mem_progress.value()
            new_mem = max(0, min(100, current_mem + random.randint(-5, 5)))
            self.mem_progress.setValue(new_mem)
            self.mem_progress.setStyleSheet(f"""
                QProgressBar::chunk {{
                    background-color: {COLORS['accent_red'] if new_mem > 80 else COLORS['accent_blue']};
                }}
            """)
            
            # Update network rates
            self.upload_rate.setText(f"{random.randint(10, 100)} Mbps")
            self.download_rate.setText(f"{random.randint(50, 200)} Mbps")


class FirewallControlPanel(DeviceControlPanel):
    """Control panel for firewall devices"""
    
    def add_device_specific_tabs(self, tab_widget):
        """Add firewall-specific tabs"""
        # Rules tab
        rules_tab = self.create_rules_tab()
        tab_widget.addTab(rules_tab, "Firewall Rules")
        
        # Monitoring tab
        monitoring_tab = self.create_monitoring_tab()
        tab_widget.addTab(monitoring_tab, "Monitoring")
        
        # Threats tab
        threats_tab = self.create_threats_tab()
        tab_widget.addTab(threats_tab, "Threat Detection")
    
    def create_rules_tab(self):
        """Create firewall rules tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Rules table
        rules_group = QGroupBox("Firewall Rules")
        rules_layout = QVBoxLayout()
        
        self.rules_table = QTableWidget()
        self.rules_table.setColumnCount(6)
        self.rules_table.setHorizontalHeaderLabels(["Priority", "Action", "Source", "Destination", "Service", "Log"])
        
        # Sample firewall rules
        rules = [
            ("1", "Allow", "192.168.1.0/24", "Any", "HTTP/HTTPS", "Yes"),
            ("2", "Allow", "192.168.1.0/24", "8.8.8.8", "DNS", "No"),
            ("3", "Block", "0.0.0.0/0", "192.168.1.0/24", "Telnet", "Yes"),
            ("4", "Allow", "10.0.0.0/8", "192.168.1.0/24", "SSH", "Yes"),
            ("5", "Block", "Any", "Any", "Any", "Yes"),
        ]
        
        self.rules_table.setRowCount(len(rules))
        for i, rule in enumerate(rules):
            for j, value in enumerate(rule):
                item = QTableWidgetItem(value)
                if j == 1:  # Action column
                    if value == "Allow":
                        item.setForeground(QColor(COLORS['success']))
                    else:
                        item.setForeground(QColor(COLORS['error']))
                item.setFont(QFont("JetBrains Mono", 9))
                self.rules_table.setItem(i, j, item)
        
        rules_layout.addWidget(self.rules_table)
        
        # Rule actions
        actions_layout = QHBoxLayout()
        add_rule_btn = QPushButton("Add Rule")
        edit_rule_btn = QPushButton("Edit Rule")
        delete_rule_btn = QPushButton("Delete Rule")
        
        actions_layout.addWidget(add_rule_btn)
        actions_layout.addWidget(edit_rule_btn)
        actions_layout.addWidget(delete_rule_btn)
        actions_layout.addStretch()
        
        rules_layout.addLayout(actions_layout)
        rules_group.setLayout(rules_layout)
        layout.addWidget(rules_group)
        
        layout.addStretch()
        return widget
    
    def create_monitoring_tab(self):
        """Create monitoring tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Traffic statistics
        stats_group = QGroupBox("Traffic Statistics")
        stats_layout = QGridLayout()
        
        stats = [
            ("Total Sessions:", f"{random.randint(1000, 50000):,}"),
            ("Active Connections:", f"{random.randint(100, 5000):,}"),
            ("Blocked Attempts:", f"{random.randint(10, 500):,}"),
            ("Throughput:", f"{random.randint(100, 1000)} Mbps"),
            ("CPU Usage:", f"{random.randint(20, 80)}%"),
            ("Memory Usage:", f"{random.randint(40, 90)}%"),
        ]
        
        for i, (label, value) in enumerate(stats):
            label_widget = QLabel(label)
            label_widget.setStyleSheet(f"color: {COLORS['text_secondary']};")
            value_widget = QLabel(value)
            value_widget.setFont(QFont("JetBrains Mono", 12, QFont.Bold))
            
            stats_layout.addWidget(label_widget, i // 2, (i % 2) * 2)
            stats_layout.addWidget(value_widget, i // 2, (i % 2) * 2 + 1)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Real-time log
        log_group = QGroupBox("Real-time Activity Log")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        
        # Add sample log entries
        log_entries = [
            "[ALLOW] 192.168.1.100 -> 8.8.8.8:53 (DNS)",
            "[BLOCK] 203.0.113.45 -> 192.168.1.10:22 (SSH brute force attempt)",
            "[ALLOW] 192.168.1.50 -> 172.217.16.142:443 (HTTPS)",
            "[BLOCK] 198.51.100.78 -> 192.168.1.1:23 (Telnet blocked)",
            "[ALLOW] 192.168.1.25 -> 93.184.216.34:80 (HTTP)",
        ]
        
        for entry in log_entries:
            self.log_text.append(entry)
        
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        layout.addStretch()
        return widget
    
    def create_threats_tab(self):
        """Create threat detection tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Threat level indicator
        threat_group = QGroupBox("Current Threat Level")
        threat_layout = QVBoxLayout()
        
        threat_level = random.choice(["Low", "Medium", "High", "Critical"])
        threat_color = {
            "Low": COLORS['success'],
            "Medium": COLORS['warning'],
            "High": COLORS['accent_red'],
            "Critical": COLORS['error']
        }[threat_level]
        
        threat_label = QLabel(threat_level)
        threat_label.setAlignment(Qt.AlignCenter)
        threat_label.setFont(QFont("Inter", 24, QFont.Bold))
        threat_label.setStyleSheet(f"color: {threat_color};")
        threat_layout.addWidget(threat_label)
        
        threat_group.setLayout(threat_layout)
        layout.addWidget(threat_group)
        
        # Recent threats
        threats_group = QGroupBox("Recent Threat Detections")
        threats_layout = QVBoxLayout()
        
        self.threats_table = QTableWidget()
        self.threats_table.setColumnCount(4)
        self.threats_table.setHorizontalHeaderLabels(["Time", "Type", "Source", "Action"])
        
        threats = [
            ("14:32:15", "DDoS Attack", "203.0.113.0/24", "Blocked"),
            ("14:28:43", "Port Scan", "198.51.100.15", "Blocked"),
            ("14:15:22", "SQL Injection", "192.0.2.45", "Blocked"),
            ("13:45:10", "Malware C&C", "10.0.0.50", "Quarantined"),
        ]
        
        self.threats_table.setRowCount(len(threats))
        for i, threat in enumerate(threats):
            for j, value in enumerate(threat):
                item = QTableWidgetItem(value)
                if j == 3:  # Action column
                    item.setForeground(QColor(COLORS['accent_red']))
                item.setFont(QFont("JetBrains Mono", 9))
                self.threats_table.setItem(i, j, item)
        
        threats_layout.addWidget(self.threats_table)
        threats_group.setLayout(threats_layout)
        layout.addWidget(threats_group)
        
        layout.addStretch()
        return widget


# Device control panel factory
def create_control_panel(device, parent=None):
    """Create appropriate control panel based on device type"""
    device_type = device.device_type
    
    # Map device types to control panels
    control_panels = {
        'router': RouterControlPanel,
        'wireless_router': RouterControlPanel,
        'server': ServerControlPanel,
        'web_server': ServerControlPanel,
        'database': ServerControlPanel,
        'mail_server': ServerControlPanel,
        'file_server': ServerControlPanel,
        'game_server': ServerControlPanel,
        'firewall': FirewallControlPanel,
    }
    
    # Get appropriate control panel class
    panel_class = control_panels.get(device_type, DeviceControlPanel)
    return panel_class(device, parent)