"""
Icon management for the network simulator using Phosphor icons
"""

from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon
from PySide6.QtCore import Qt, QRect, QByteArray
from PySide6.QtSvg import QSvgRenderer
import os
import sys


class IconManager:
    """Manages icons for the application using Phosphor SVG icons"""
    
    # Map device types to Phosphor icon names
    DEVICE_ICONS = {
        # End User Devices
        'pc': 'desktop-bold',
        'laptop': 'laptop-bold',
        'smartphone': 'device-mobile-bold',
        'tablet': 'device-tablet-bold',
        'printer': 'printer-bold',
        
        # Network Infrastructure
        'router': 'share-network-bold',
        'switch': 'git-branch-bold',
        'hub': 'circle-notch-bold',
        'bridge': 'bridge-bold',
        'access_point': 'wifi-high-bold',
        'wireless_router': 'wifi-high-bold',
        
        # Servers
        'server': 'hard-drives-bold',
        'database': 'database-bold',
        'web_server': 'globe-bold',
        'mail_server': 'envelope-bold',
        'file_server': 'folder-bold',
        'game_server': 'game-controller-bold',
        
        # Security
        'firewall': 'shield-bold',
        'vpn': 'lock-bold',
        'ids_ips': 'shield-check-bold',
        'proxy': 'funnel-bold',
        'nac': 'key-bold',
        
        # IoT
        'smart_hub': 'house-bold',
        'ip_camera': 'camera-bold',
        'iot_sensor': 'cpu-bold',
        'smart_light': 'lightbulb-bold',
        'smart_speaker': 'speaker-high-bold',
        
        # Specialized
        'cloud': 'cloud-bold',
        'satellite': 'broadcast-bold',
        'voip': 'phone-bold',
        'load_balancer': 'scales-bold',
        'nas': 'hard-drive-bold',
        'ups': 'battery-charging-bold',
        
        # Default
        'generic': 'cube-bold'
    }
    
    # Toolbar icons
    TOOLBAR_ICONS = {
        'start': 'play-bold',
        'stop': 'stop-bold',
        'select': 'cursor-bold',
        'cable': 'plug-bold',
        'delete': 'trash-bold',
        'ping': 'wifi-high-bold',
        'save': 'floppy-disk-bold',
        'load': 'folder-open-bold',
        'reset_view': 'house-bold'
    }
    
    _icon_cache = {}
    
    @staticmethod
    def get_svg_path(icon_name: str) -> str:
        """Get the full path to an SVG icon"""
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Try different paths
        base_paths = [
            # Relative to current script
            os.path.join(current_dir, "..", "..", "resources", "phosphor-svgs", "bold"),
            # From working directory
            os.path.join("resources", "phosphor-svgs", "bold"),
            # Absolute path on Windows
            os.path.join(os.path.dirname(sys.executable), "resources", "phosphor-svgs", "bold"),
        ]
        
        for base_path in base_paths:
            svg_path = os.path.join(base_path, f"{icon_name}.svg")
            if os.path.exists(svg_path):
                return os.path.abspath(svg_path)
        
        # Debug print
        print(f"Warning: Icon not found: {icon_name}")
        print(f"Searched paths: {base_paths}")
        
        # Fallback to text if icon not found
        return None
    
    @staticmethod
    def get_icon_char(device_type: str) -> str:
        """Get icon character for device type (fallback for painting)"""
        # Simple text fallback
        fallbacks = {
            'pc': 'PC', 'laptop': 'LT', 'smartphone': 'SP', 'tablet': 'TB', 'printer': 'PR',
            'router': 'RT', 'switch': 'SW', 'hub': 'HB', 'bridge': 'BR', 'access_point': 'AP', 
            'wireless_router': 'WR', 'server': 'SV', 'database': 'DB', 'web_server': 'WS',
            'mail_server': 'MS', 'file_server': 'FS', 'game_server': 'GS', 'firewall': 'FW',
            'vpn': 'VP', 'ids_ips': 'ID', 'proxy': 'PX', 'nac': 'NC', 'smart_hub': 'SH',
            'ip_camera': 'CM', 'iot_sensor': 'SN', 'smart_light': 'LI', 'smart_speaker': 'SK',
            'cloud': 'CL', 'satellite': 'ST', 'voip': 'VO', 'load_balancer': 'LB',
            'nas': 'NS', 'ups': 'UP', 'generic': 'DV'
        }
        return fallbacks.get(device_type, 'DV')
    
    @staticmethod
    def get_svg_pixmap(icon_name: str, size: int = 24, color: QColor = None) -> QPixmap:
        """Create a pixmap from an SVG icon with the specified color"""
        if color is None:
            color = QColor(255, 255, 255)
        
        # Check cache
        cache_key = f"{icon_name}_{size}_{color.name()}"
        if cache_key in IconManager._icon_cache:
            return IconManager._icon_cache[cache_key]
        
        svg_path = IconManager.get_svg_path(icon_name)
        if not svg_path:
            # Return empty pixmap if SVG not found
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            return pixmap
        
        # Load SVG
        try:
            with open(svg_path, 'r') as f:
                svg_content = f.read()
            
            # Replace currentColor with our color
            svg_content = svg_content.replace('currentColor', color.name())
            
            # Create pixmap
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            # Render SVG to pixmap
            svg_renderer = QSvgRenderer(QByteArray(svg_content.encode()))
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            svg_renderer.render(painter)
            painter.end()
            
            # Cache the pixmap
            IconManager._icon_cache[cache_key] = pixmap
            return pixmap
            
        except Exception as e:
            print(f"Error loading SVG {svg_path}: {e}")
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            return pixmap
    
    @staticmethod
    def get_device_pixmap(device_type: str, size: int = 24, color: QColor = None) -> QPixmap:
        """Get pixmap for a device type"""
        icon_name = IconManager.DEVICE_ICONS.get(device_type, IconManager.DEVICE_ICONS['generic'])
        return IconManager.get_svg_pixmap(icon_name, size, color)
    
    @staticmethod
    def get_toolbar_pixmap(action: str, size: int = 24, color: QColor = None) -> QPixmap:
        """Get pixmap for a toolbar action"""
        icon_name = IconManager.TOOLBAR_ICONS.get(action, 'question-bold')
        return IconManager.get_svg_pixmap(icon_name, size, color)
    
    @staticmethod
    def create_pixmap_icon(icon_char: str, size: int = 24, color: QColor = None) -> QPixmap:
        """Legacy method for compatibility - now uses SVG icons"""
        # This is used by toolbar, redirect to get_toolbar_pixmap
        for action, icon in IconManager.TOOLBAR_ICONS.items():
            if icon_char in icon:
                return IconManager.get_toolbar_pixmap(action, size, color)
        return QPixmap(size, size)  # Empty pixmap
    
    @staticmethod
    def get_toolbar_icon_char(action: str) -> str:
        """Legacy method - returns action name for compatibility"""
        return action
    
    @staticmethod
    def load_font():
        """Legacy method - no longer needed for SVG icons"""
        pass