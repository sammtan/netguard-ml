"""
Main window for AI Network Simulator
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QDockWidget, QTabWidget, QSplitter,
    QPushButton, QLabel, QListWidgetItem,
    QSizePolicy, QGraphicsView, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QSize, QTimer, QPointF
from PySide6.QtGui import QAction, QIcon, QColor
from src.devices.base_device import NetworkDevice

from src.ui.network_canvas import NetworkCanvas
from src.ui.ai_monitor import AIMonitorWidget
from src.ui.packet_viewer import PacketViewerWidget
from src.ui.connections import ConnectionManager
from src.ui.device_list import DeviceListWidget
from src.ui.device_toolbar import DeviceToolbar
from src.ui.device_tree import DeviceTreePanel
from src.ui.icons import IconManager
from src.ui.theme import COLORS
from src.simulation.simulator import NetworkSimulator
from src.core.file_format import NetworkFileFormat


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.simulator = NetworkSimulator()
        self.current_tool = "select"
        self.selected_device = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("AI Network Simulator")
        self.setGeometry(100, 100, 1400, 800)
        
        # Create toolbar
        self.create_toolbar()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create vertical splitter for main content and bottom toolbar
        vertical_splitter = QSplitter(Qt.Vertical)
        
        # Create horizontal splitter for main content
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Device tree
        self.device_tree_panel = DeviceTreePanel()
        self.device_tree_panel.tree.device_selected.connect(self.on_tree_device_selected)
        main_splitter.addWidget(self.device_tree_panel)
        
        # Center - Network canvas
        self.network_canvas = NetworkCanvas(self.simulator)
        self.network_canvas.main_window = self  # Set reference to main window
        self.connection_manager = ConnectionManager(self.network_canvas.scene)
        self.network_canvas.connection_manager = self.connection_manager  # Set connection manager
        self.network_canvas.scene.selectionChanged.connect(self.on_selection_changed)
        self.network_canvas.device_added.connect(self.on_device_added)
        main_splitter.addWidget(self.network_canvas)
        
        # Right panel - Tabs
        right_tabs = QTabWidget()
        
        # AI Monitor tab
        self.ai_monitor = AIMonitorWidget()
        right_tabs.addTab(self.ai_monitor, "AI Monitor")
        
        # Packet viewer tab
        self.packet_viewer = PacketViewerWidget()
        right_tabs.addTab(self.packet_viewer, "Packets")
        
        main_splitter.addWidget(right_tabs)
        
        # Set splitter sizes
        main_splitter.setSizes([250, 700, 450])
        
        # Add main content to vertical splitter
        vertical_splitter.addWidget(main_splitter)
        
        # Bottom toolbar - Device palette
        self.device_toolbar = DeviceToolbar()
        vertical_splitter.addWidget(self.device_toolbar)
        
        # Set vertical splitter sizes
        vertical_splitter.setSizes([680, 120])
        vertical_splitter.setCollapsible(1, False)  # Don't allow bottom toolbar to collapse
        
        layout.addWidget(vertical_splitter)
        
        # Connect signals
        self.simulator.packet_sent.connect(self.packet_viewer.add_packet)
        self.simulator.traffic_update.connect(self.ai_monitor.update_traffic)
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")
    
    def create_toolbar(self):
        """Create main toolbar"""
        toolbar = self.addToolBar("Main")
        toolbar.setMovable(False)
        
        # Simulation controls
        self.start_action = QAction("Start", self)
        self.start_action.setIcon(QIcon(IconManager.get_toolbar_pixmap('start', 16, QColor(COLORS['success']))))
        self.start_action.setToolTip("Start simulation")
        self.start_action.triggered.connect(self.start_simulation)
        toolbar.addAction(self.start_action)
        
        self.stop_action = QAction("Stop", self)
        self.stop_action.setIcon(QIcon(IconManager.get_toolbar_pixmap('stop', 16, QColor(COLORS['error']))))
        self.stop_action.setToolTip("Stop simulation")
        self.stop_action.setEnabled(False)
        self.stop_action.triggered.connect(self.stop_simulation)
        toolbar.addAction(self.stop_action)
        
        toolbar.addSeparator()
        
        # Tools
        self.select_action = QAction("Select", self)
        self.select_action.setIcon(QIcon(IconManager.get_toolbar_pixmap('select', 16, QColor(COLORS['text_primary']))))
        self.select_action.setCheckable(True)
        self.select_action.setChecked(True)
        self.select_action.triggered.connect(lambda: self.set_tool("select"))
        toolbar.addAction(self.select_action)
        
        self.cable_action = QAction("Cable", self)
        self.cable_action.setIcon(QIcon(IconManager.get_toolbar_pixmap('cable', 16, QColor(COLORS['text_primary']))))
        self.cable_action.setCheckable(True)
        self.cable_action.triggered.connect(lambda: self.set_tool("cable"))
        toolbar.addAction(self.cable_action)
        
        self.delete_action = QAction("Delete", self)
        self.delete_action.setIcon(QIcon(IconManager.get_toolbar_pixmap('delete', 16, QColor(COLORS['error']))))
        self.delete_action.triggered.connect(self.delete_selected)
        toolbar.addAction(self.delete_action)
        
        toolbar.addSeparator()
        
        # Testing tools
        self.ping_action = QAction("Ping", self)
        self.ping_action.setIcon(QIcon(IconManager.get_toolbar_pixmap('ping', 16, QColor(COLORS['text_primary']))))
        self.ping_action.setCheckable(True)
        self.ping_action.triggered.connect(lambda: self.set_tool("ping"))
        toolbar.addAction(self.ping_action)
        
        # Spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)
        
        # Reset view button
        reset_view_action = QAction("Reset View", self)
        reset_view_action.setIcon(QIcon(IconManager.get_toolbar_pixmap('reset_view', 16, QColor(COLORS['text_primary']))))
        reset_view_action.setToolTip("Reset to center (0,0) at 100% zoom")
        reset_view_action.triggered.connect(self.reset_canvas_view)
        toolbar.addAction(reset_view_action)
        
        toolbar.addSeparator()
        
        # Save/Load
        save_action = QAction("Save", self)
        save_action.setIcon(QIcon(IconManager.get_toolbar_pixmap('save', 16, QColor(COLORS['text_primary']))))
        save_action.triggered.connect(self.save_network)
        toolbar.addAction(save_action)
        
        load_action = QAction("Load", self)
        load_action.setIcon(QIcon(IconManager.get_toolbar_pixmap('load', 16, QColor(COLORS['text_primary']))))
        load_action.triggered.connect(self.load_network)
        toolbar.addAction(load_action)
    
    
    def start_simulation(self):
        """Start the network simulation"""
        self.simulator.start()
        self.start_action.setEnabled(False)
        self.stop_action.setEnabled(True)
        self.status_bar.showMessage("Simulation running...")
        
        # Start AI monitoring
        self.ai_monitor.start_monitoring()
    
    def stop_simulation(self):
        """Stop the network simulation"""
        self.simulator.stop()
        self.start_action.setEnabled(True)
        self.stop_action.setEnabled(False)
        self.status_bar.showMessage("Simulation stopped")
        
        # Stop AI monitoring
        self.ai_monitor.stop_monitoring()
    
    def reset_canvas_view(self):
        """Reset canvas to center at 100% zoom"""
        self.network_canvas.resetTransform()
        self.network_canvas.centerOn(0, 0)
    
    def set_tool(self, tool_name):
        """Set the current tool"""
        self.current_tool = tool_name
        
        # Update button states
        self.select_action.setChecked(tool_name == "select")
        self.cable_action.setChecked(tool_name == "cable")
        self.ping_action.setChecked(tool_name == "ping")
        
        # Update canvas mode
        if tool_name == "cable":
            self.network_canvas.setDragMode(QGraphicsView.NoDrag)
        else:
            self.network_canvas.setDragMode(QGraphicsView.RubberBandDrag)
    
    def delete_selected(self):
        """Delete selected items"""
        selected_items = self.network_canvas.scene.selectedItems()
        for item in selected_items:
            if isinstance(item, NetworkDevice):
                # Remove from simulator
                self.simulator.remove_device(item)
                # Remove from scene
                self.network_canvas.scene.removeItem(item)
        
        # Update device tree
        self.update_device_tree()
    
    def on_selection_changed(self):
        """Handle selection changes"""
        selected_items = self.network_canvas.scene.selectedItems()
        if selected_items and isinstance(selected_items[0], NetworkDevice):
            self.selected_device = selected_items[0]
            # Highlight in tree
            self.device_tree_panel.tree.highlight_device(self.selected_device)
        else:
            self.selected_device = None
    
    def on_device_added(self, device):
        """Handle device added to canvas"""
        self.update_device_tree()
    
    def update_device_tree(self):
        """Update the device hierarchy tree"""
        devices = self.simulator.devices
        connections = self.connection_manager.connections
        self.device_tree_panel.update_topology(devices, connections)
    
    def on_tree_device_selected(self, device):
        """Handle device selection from tree"""
        # Clear current selection
        self.network_canvas.scene.clearSelection()
        # Select the device
        device.setSelected(True)
        # Center view on device
        self.network_canvas.centerOn(device)
    
    def save_network(self):
        """Save network topology to file"""
        # Get file path
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Network Topology",
            "",
            "Network Simulation Files (*.netsim);;All Files (*.*)"
        )
        
        if file_path:
            # Get devices and connections
            devices = self.simulator.devices
            connections = self.connection_manager.connections
            
            # Save to file
            if NetworkFileFormat.save_to_file(file_path, devices, connections):
                QMessageBox.information(self, "Success", "Network topology saved successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to save network topology!")
    
    def load_network(self):
        """Load network topology from file"""
        # Get file path
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Network Topology", 
            "",
            "Network Simulation Files (*.netsim);;All Files (*.*)"
        )
        
        if file_path:
            # Load file data
            file_data = NetworkFileFormat.load_from_file(file_path)
            
            if file_data and NetworkFileFormat.validate_file_data(file_data):
                # Clear current network
                self.clear_network()
                
                # Load devices
                self.load_devices_from_data(file_data['network']['devices'])
                
                # Load connections
                self.load_connections_from_data(file_data['network']['connections'])
                
                # Update tree
                self.update_device_tree()
                
                QMessageBox.information(self, "Success", "Network topology loaded successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to load network topology!")
    
    def clear_network(self):
        """Clear all devices and connections"""
        # Stop simulation if running
        if self.simulator.running:
            self.stop_simulation()
        
        # Clear devices
        for device in list(self.simulator.devices):
            self.simulator.remove_device(device)
            self.network_canvas.scene.removeItem(device)
        
        # Clear connections
        for conn in list(self.connection_manager.connections):
            self.connection_manager.remove_connection(conn['device1'], conn['device2'])
        
        # Clear scene
        self.network_canvas.scene.clear()
        self.network_canvas.draw_grid()
    
    def load_devices_from_data(self, devices_data):
        """Load devices from file data"""
        device_map = {}  # Map device IDs to device objects
        
        for device_data in devices_data:
            # Get position
            pos = QPointF(device_data['position']['x'], device_data['position']['y'])
            
            # Create device
            device_type = device_data['type']
            self.network_canvas.add_device(device_type, pos)
            
            # Get the newly created device (last one added)
            if self.simulator.devices:
                device = self.simulator.devices[-1]
                
                # Set properties
                device.device_id = device_data['hostname']
                device.identity.hostname = device_data['hostname']
                device.ip_address = device_data.get('ip_address', device.ip_address)
                device.identity.ip_address = device.ip_address
                
                # Set identity properties if available
                if 'identity' in device_data:
                    identity = device_data['identity']
                    device.identity.mac_address = identity.get('mac_address', device.identity.mac_address)
                    device.identity.manufacturer = identity.get('manufacturer', device.identity.manufacturer)
                    device.identity.model = identity.get('model', device.identity.model)
                    device.identity.serial_number = identity.get('serial_number', device.identity.serial_number)
                    device.identity.firmware_version = identity.get('firmware_version', device.identity.firmware_version)
                
                # Set running state
                if device_data.get('is_running', False):
                    device.start()
                
                # Store in map
                device_map[device_data['id']] = device
        
        return device_map
    
    def load_connections_from_data(self, connections_data):
        """Load connections from file data"""
        # Build device ID map
        device_id_map = {}
        for idx, device in enumerate(self.simulator.devices):
            device_id_map[f"device_{idx}"] = device
        
        # Create connections
        for conn_data in connections_data:
            device1 = device_id_map.get(conn_data['device1'])
            device2 = device_id_map.get(conn_data['device2'])
            
            if device1 and device2:
                # Complete connection
                self.connection_manager.start_device = device1
                self.connection_manager.complete_connection(device2)