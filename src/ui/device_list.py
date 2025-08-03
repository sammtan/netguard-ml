"""
Custom device list widget with proper drag and drop support
"""

from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, QMimeData, QByteArray
from PySide6.QtGui import QDrag


class DeviceListWidget(QListWidget):
    """Custom list widget that properly handles drag and drop of devices"""
    
    def startDrag(self, supportedActions):
        """Start drag operation with proper mime data"""
        item = self.currentItem()
        if item:
            # Get the device type from user data
            device_type = item.data(Qt.UserRole)
            
            if device_type:  # Only create drag for actual devices, not headers
                drag = QDrag(self)
                mime_data = QMimeData()
                
                # Set the device type as text
                mime_data.setText(device_type)
                
                drag.setMimeData(mime_data)
                drag.exec_(Qt.CopyAction)