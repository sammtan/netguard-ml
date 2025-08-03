"""
Device hierarchy tree view
"""

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor
from src.ui.theme import COLORS
from src.ui.icons import IconManager


class DeviceTreeWidget(QTreeWidget):
    """Tree widget showing device hierarchy"""
    
    device_selected = Signal(object)
    
    def __init__(self):
        super().__init__()
        self.device_items = {}  # Map device to tree item
        self.init_ui()
    
    def init_ui(self):
        """Initialize the tree widget"""
        self.setHeaderLabel("Network Topology")
        self.setAlternatingRowColors(True)
        
        # Style
        self.setStyleSheet(f"""
            QTreeWidget {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                outline: none;
            }}
            QTreeWidget::item {{
                padding: 4px;
                margin: 2px;
            }}
            QTreeWidget::item:hover {{
                background-color: {COLORS['surface_light']};
            }}
            QTreeWidget::item:selected {{
                background-color: {COLORS['accent_blue']};
            }}
            QTreeWidget::branch {{
                background-color: {COLORS['surface']};
            }}
        """)
        
        # Connect signals
        self.itemClicked.connect(self.on_item_clicked)
    
    def update_topology(self, devices, connections):
        """Update the tree based on network topology"""
        self.clear()
        self.device_items.clear()
        
        # Build adjacency list
        adj_list = {}
        for device in devices:
            adj_list[device] = []
        
        for conn in connections:
            device1 = conn['device1']
            device2 = conn['device2']
            adj_list[device1].append(device2)
            adj_list[device2].append(device1)
        
        # Find root devices (routers, switches, or most connected)
        root_devices = []
        for device in devices:
            if device.device_type in ['router', 'switch', 'firewall']:
                root_devices.append(device)
            elif len(adj_list[device]) >= 3:  # Hub-like device
                root_devices.append(device)
        
        # If no obvious roots, use devices with most connections
        if not root_devices:
            root_devices = sorted(devices, key=lambda d: len(adj_list[d]), reverse=True)[:3]
        
        # Build trees from each root
        visited = set()
        
        # First add all root devices
        for root in root_devices:
            if root not in visited:
                self.build_tree(root, None, adj_list, visited)
        
        # Add any unconnected devices
        unconnected_item = None
        for device in devices:
            if device not in visited:
                if unconnected_item is None:
                    unconnected_item = QTreeWidgetItem(self)
                    unconnected_item.setText(0, "Unconnected Devices")
                    unconnected_item.setFont(0, QFont("Inter", 10, QFont.Bold))
                    unconnected_item.setForeground(0, QColor(COLORS['text_secondary']))
                
                item = QTreeWidgetItem(unconnected_item)
                self.setup_device_item(item, device)
                self.device_items[device] = item
                visited.add(device)
        
        # Expand all items
        self.expandAll()
    
    def build_tree(self, device, parent_item, adj_list, visited):
        """Build tree recursively from a device"""
        if device in visited:
            return
        
        visited.add(device)
        
        # Create tree item
        if parent_item is None:
            item = QTreeWidgetItem(self)
        else:
            item = QTreeWidgetItem(parent_item)
        
        self.setup_device_item(item, device)
        self.device_items[device] = item
        
        # Add connected devices
        for connected in adj_list[device]:
            if connected not in visited:
                self.build_tree(connected, item, adj_list, visited)
    
    def setup_device_item(self, item, device):
        """Set up a tree item for a device"""
        # Format: [Icon] DeviceName (IP)
        icon_text = IconManager.get_icon_char(device.device_type)
        text = f"[{icon_text}] {device.device_id} ({device.ip_address})"
        item.setText(0, text)
        item.setData(0, Qt.UserRole, device)
        
        # Different colors for different device types
        if device.device_type in ['router', 'switch', 'firewall']:
            item.setForeground(0, QColor(COLORS['accent_blue']))
        elif device.device_type in ['server', 'database', 'web_server']:
            item.setForeground(0, QColor(COLORS['accent_red']))
        else:
            item.setForeground(0, QColor(COLORS['text_primary']))
    
    def on_item_clicked(self, item, column):
        """Handle item click"""
        device = item.data(0, Qt.UserRole)
        if device:
            self.device_selected.emit(device)
    
    def highlight_device(self, device):
        """Highlight a device in the tree"""
        if device in self.device_items:
            item = self.device_items[device]
            self.setCurrentItem(item)
            self.scrollToItem(item)


class DeviceTreePanel(QWidget):
    """Panel containing the device tree"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the panel UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Title
        title = QLabel("Device Hierarchy")
        title.setStyleSheet("font-size: 14px; font-weight: bold; padding: 4px;")
        layout.addWidget(title)
        
        # Tree widget
        self.tree = DeviceTreeWidget()
        layout.addWidget(self.tree)
    
    def update_topology(self, devices, connections):
        """Update the device tree"""
        self.tree.update_topology(devices, connections)