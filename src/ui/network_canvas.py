"""
Network canvas for visual network building
"""

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem
from PySide6.QtCore import Qt, QPointF, Signal, QMimeData
from PySide6.QtGui import QPen, QBrush, QColor, QPainter, QDrag, QWheelEvent, QMouseEvent

from src.devices.base_device import NetworkDevice

# Import all device categories
from src.devices.end_user_devices import PC, Laptop, Smartphone, Tablet, Printer
from src.devices.network_devices import Router, Switch, Hub, Bridge, AccessPoint, WirelessRouter
from src.devices.server_devices import Server, DatabaseServer, WebServer, MailServer, FileServer, GameServer
from src.devices.security_devices import Firewall, VPNGateway, IDSDevice, ProxyServer, NACDevice
from src.devices.iot_devices import SmartHub, IPCamera, IoTSensor, SmartLight, SmartSpeaker
from src.devices.specialized_devices import CloudService, SatelliteLink, VoIPPhone, LoadBalancer, NASStorage, UPSDevice


class NetworkCanvas(QGraphicsView):
    """Canvas for building network topology"""
    
    device_added = Signal(object)  # Emits device when added
    
    def __init__(self, simulator):
        super().__init__()
        self.simulator = simulator
        self.device_counter = 0
        self.main_window = None  # Will be set by main window
        self.connection_manager = None  # Will be set by main window
        
        # Create scene
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-2000, -2000, 4000, 4000)
        self.setScene(self.scene)
        
        # Configure view
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.NoDrag)
        self.setAcceptDrops(True)
        
        # Hide scrollbars
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Pan state
        self.panning = False
        self.pan_start_pos = None
        
        # Set background
        self.setBackgroundBrush(QBrush(QColor("#0a0a0a")))
        
        # Draw grid
        self.draw_grid()
    
    def draw_grid(self):
        """Draw background grid"""
        grid_size = 50
        pen = QPen(QColor(40, 40, 40), 1, Qt.DotLine)
        
        # Draw vertical lines
        for x in range(-2000, 2001, grid_size):
            self.scene.addLine(x, -2000, x, 2000, pen)
        
        # Draw horizontal lines
        for y in range(-2000, 2001, grid_size):
            self.scene.addLine(-2000, y, 2000, y, pen)
        
        # Draw origin marker
        origin_pen = QPen(QColor(80, 80, 80), 2)
        self.scene.addLine(-20, 0, 20, 0, origin_pen)
        self.scene.addLine(0, -20, 0, 20, origin_pen)
    
    def dragEnterEvent(self, event):
        """Handle drag enter event"""
        if event.mimeData().hasText():
            # Check if it's a valid device type (not a category header)
            device_type = event.mimeData().text()
            if device_type and device_type != "None":
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        """Handle drag move event"""
        if event.mimeData().hasText():
            device_type = event.mimeData().text()
            if device_type and device_type != "None":
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        """Handle drop event"""
        if event.mimeData().hasText():
            device_type = event.mimeData().text()
            
            if device_type and device_type != "None":
                # Convert to scene coordinates
                pos = self.mapToScene(event.pos())
                
                # Create device
                self.add_device(device_type, pos)
                
                event.acceptProposedAction()
            else:
                event.ignore()
    
    def add_device(self, device_type: str, position: QPointF):
        """Add a device to the canvas"""
        self.device_counter += 1
        device_id = f"{device_type}_{self.device_counter}"
        
        # Create device based on type
        device_map = {
            # End User Devices
            "pc": PC,
            "laptop": Laptop,
            "smartphone": Smartphone,
            "tablet": Tablet,
            "printer": Printer,
            
            # Network Infrastructure
            "router": Router,
            "switch": Switch,
            "hub": Hub,
            "bridge": Bridge,
            "access_point": AccessPoint,
            "wireless_router": WirelessRouter,
            
            # Servers
            "server": Server,
            "database": DatabaseServer,
            "web_server": WebServer,
            "mail_server": MailServer,
            "file_server": FileServer,
            "game_server": GameServer,
            
            # Security
            "firewall": Firewall,
            "vpn": VPNGateway,
            "ids_ips": IDSDevice,
            "proxy": ProxyServer,
            "nac": NACDevice,
            
            # IoT
            "smart_hub": SmartHub,
            "ip_camera": IPCamera,
            "iot_sensor": IoTSensor,
            "smart_light": SmartLight,
            "smart_speaker": SmartSpeaker,
            
            # Specialized
            "cloud": CloudService,
            "satellite": SatelliteLink,
            "voip": VoIPPhone,
            "load_balancer": LoadBalancer,
            "nas": NASStorage,
            "ups": UPSDevice
        }
        
        # Create device instance
        DeviceClass = device_map.get(device_type, PC)
        device = DeviceClass(device_id, position)
        
        # Add to scene
        self.scene.addItem(device)
        
        # Add to simulator
        self.simulator.add_device(device)
        
        # Emit signal
        self.device_added.emit(device)
    
    def wheelEvent(self, event: QWheelEvent):
        """Handle mouse wheel for zooming"""
        # Get the current scale factor
        current_scale = self.transform().m11()
        
        # Calculate zoom factor
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        
        # Set zoom limits
        min_scale = 0.1
        max_scale = 5.0
        
        # Determine zoom direction
        if event.angleDelta().y() > 0:
            # Zoom in
            scale_factor = zoom_in_factor
            new_scale = current_scale * scale_factor
        else:
            # Zoom out
            scale_factor = zoom_out_factor
            new_scale = current_scale * scale_factor
        
        # Apply limits
        if new_scale < min_scale:
            scale_factor = min_scale / current_scale
        elif new_scale > max_scale:
            scale_factor = max_scale / current_scale
        
        # Apply the scaling
        self.scale(scale_factor, scale_factor)
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press for panning and cable connections"""
        if event.button() == Qt.MiddleButton or \
           (event.button() == Qt.LeftButton and event.modifiers() == Qt.ControlModifier):
            # Start panning
            self.panning = True
            self.pan_start_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
        elif event.button() == Qt.LeftButton and self.main_window and self.main_window.current_tool == "cable":
            # Handle cable mode
            pos = self.mapToScene(event.pos())
            item = self.scene.itemAt(pos, self.transform())
            
            if isinstance(item, NetworkDevice):
                if self.connection_manager.connection_mode:
                    # Complete connection
                    self.connection_manager.complete_connection(item)
                else:
                    # Start connection
                    self.connection_manager.start_connection(item)
                event.accept()
            else:
                # Cancel connection if clicking empty space
                self.connection_manager.cancel_connection()
                event.accept()
        elif event.button() == Qt.LeftButton and self.main_window and self.main_window.current_tool == "ping":
            # Handle ping mode
            pos = self.mapToScene(event.pos())
            item = self.scene.itemAt(pos, self.transform())
            
            if isinstance(item, NetworkDevice):
                if hasattr(self.main_window, 'selected_device') and self.main_window.selected_device:
                    # Ping from selected device to clicked device
                    self.send_ping(self.main_window.selected_device, item)
                event.accept()
        else:
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move for panning and cable preview"""
        if self.panning and self.pan_start_pos:
            # Calculate pan delta
            delta = event.pos() - self.pan_start_pos
            self.pan_start_pos = event.pos()
            
            # Apply pan
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x()
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y()
            )
            event.accept()
        elif self.connection_manager and self.connection_manager.connection_mode:
            # Update temporary connection line
            pos = self.mapToScene(event.pos())
            self.connection_manager.update_temp_connection(pos)
            event.accept()
        else:
            super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release"""
        if event.button() == Qt.MiddleButton or \
           (event.button() == Qt.LeftButton and self.panning):
            # Stop panning
            self.panning = False
            self.pan_start_pos = None
            self.setCursor(Qt.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)
    
    def keyPressEvent(self, event):
        """Handle keyboard navigation"""
        # Pan with arrow keys
        step = 50
        if event.key() == Qt.Key_Left:
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - step
            )
        elif event.key() == Qt.Key_Right:
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() + step
            )
        elif event.key() == Qt.Key_Up:
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - step
            )
        elif event.key() == Qt.Key_Down:
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() + step
            )
        else:
            super().keyPressEvent(event)
    
    def send_ping(self, source_device, target_device):
        """Send ping from source to target device"""
        if source_device and target_device and source_device != target_device:
            # Create ping packet
            self.simulator.send_ping(source_device, target_device)