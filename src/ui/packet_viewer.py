"""
Packet viewer widget for real-time packet display
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class PacketViewerWidget(QWidget):
    """Widget for viewing network packets"""
    
    def __init__(self):
        super().__init__()
        self.packet_count = 0
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        
        # Title and controls
        header_layout = QHBoxLayout()
        
        title = QLabel("Packet Capture")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 8px;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Clear button
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_packets)
        header_layout.addWidget(clear_btn)
        
        layout.addLayout(header_layout)
        
        # Packet table
        self.packet_table = QTableWidget()
        self.packet_table.setColumnCount(6)
        self.packet_table.setHorizontalHeaderLabels([
            "No.", "Time", "Source", "Destination", "Protocol", "Info"
        ])
        
        # Set column widths
        self.packet_table.setColumnWidth(0, 50)
        self.packet_table.setColumnWidth(1, 80)
        self.packet_table.setColumnWidth(2, 120)
        self.packet_table.setColumnWidth(3, 120)
        self.packet_table.setColumnWidth(4, 80)
        self.packet_table.setColumnWidth(5, 200)
        
        # Style
        self.packet_table.setAlternatingRowColors(True)
        self.packet_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.packet_table)
        
        # Status
        self.status_label = QLabel("Packets: 0")
        layout.addWidget(self.status_label)
    
    def add_packet(self, packet_data: dict):
        """Add a packet to the viewer"""
        self.packet_count += 1
        
        # Insert new row at top
        self.packet_table.insertRow(0)
        
        # Packet number
        self.packet_table.setItem(0, 0, QTableWidgetItem(str(self.packet_count)))
        
        # Time (simplified)
        time_str = f"{(self.packet_count * 0.1):.2f}s"
        self.packet_table.setItem(0, 1, QTableWidgetItem(time_str))
        
        # Source
        source = packet_data.get('source', 'Unknown')
        self.packet_table.setItem(0, 2, QTableWidgetItem(source))
        
        # Destination
        dest = packet_data.get('destination', 'Unknown')
        self.packet_table.setItem(0, 3, QTableWidgetItem(dest))
        
        # Protocol
        protocol = packet_data.get('protocol', 'Unknown')
        protocol_item = QTableWidgetItem(protocol)
        
        # Color code by protocol
        protocol_colors = {
            'ARP': QColor(255, 200, 100),
            'ICMP': QColor(100, 200, 255),
            'TCP': QColor(100, 255, 100),
            'UDP': QColor(255, 100, 255),
            'HTTP': QColor(200, 255, 200)
        }
        
        if protocol in protocol_colors:
            protocol_item.setBackground(protocol_colors[protocol])
        
        self.packet_table.setItem(0, 4, protocol_item)
        
        # Info
        info = packet_data.get('info', '')
        self.packet_table.setItem(0, 5, QTableWidgetItem(info))
        
        # Limit rows to prevent memory issues
        if self.packet_table.rowCount() > 100:
            self.packet_table.removeRow(self.packet_table.rowCount() - 1)
        
        # Update status
        self.status_label.setText(f"Packets: {self.packet_count}")
    
    def clear_packets(self):
        """Clear all packets"""
        self.packet_table.setRowCount(0)
        self.packet_count = 0
        self.status_label.setText("Packets: 0")