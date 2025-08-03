"""
Lights-out theme with red and blue accents
"""

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor, QFont

# Color palette
COLORS = {
    # Base colors
    'background': '#0a0a0a',
    'surface': '#141414',
    'surface_light': '#1a1a1a',
    'border': '#2a2a2a',
    
    # Text colors
    'text_primary': '#ffffff',
    'text_secondary': '#a0a0a0',
    'text_disabled': '#606060',
    
    # Accent colors
    'accent_red': '#ff3b3b',
    'accent_red_dark': '#cc2020',
    'accent_red_light': '#ff6666',
    
    'accent_blue': '#3b8fff',
    'accent_blue_dark': '#2070cc',
    'accent_blue_light': '#66a8ff',
    
    # Status colors
    'success': '#00ff88',
    'warning': '#ffaa00',
    'error': '#ff3b3b',
    'info': '#3b8fff',
    
    # Device type colors
    'device_pc': '#4a90e2',
    'device_server': '#9b59b6',
    'device_router': '#3498db',
    'device_switch': '#27ae60',
    'device_firewall': '#e74c3c',
    'device_iot': '#f39c12',
    'device_cloud': '#87ceeb',
}

def apply_dark_theme(app: QApplication):
    """Apply lights-out theme to the application"""
    
    # Set application font
    app.setFont(QFont("Inter", 10))
    
    # Create dark palette
    dark_palette = QPalette()
    
    # Window colors
    dark_palette.setColor(QPalette.Window, QColor(COLORS['background']))
    dark_palette.setColor(QPalette.WindowText, QColor(COLORS['text_primary']))
    
    # Base colors
    dark_palette.setColor(QPalette.Base, QColor(COLORS['surface']))
    dark_palette.setColor(QPalette.AlternateBase, QColor(COLORS['surface_light']))
    
    # Text colors
    dark_palette.setColor(QPalette.Text, QColor(COLORS['text_primary']))
    dark_palette.setColor(QPalette.BrightText, QColor(COLORS['text_primary']))
    dark_palette.setColor(QPalette.PlaceholderText, QColor(COLORS['text_disabled']))
    
    # Button colors
    dark_palette.setColor(QPalette.Button, QColor(COLORS['surface_light']))
    dark_palette.setColor(QPalette.ButtonText, QColor(COLORS['text_primary']))
    
    # Highlight colors
    dark_palette.setColor(QPalette.Highlight, QColor(COLORS['accent_blue']))
    dark_palette.setColor(QPalette.HighlightedText, QColor(COLORS['text_primary']))
    
    # Link colors
    dark_palette.setColor(QPalette.Link, QColor(COLORS['accent_blue']))
    dark_palette.setColor(QPalette.LinkVisited, QColor(COLORS['accent_blue_dark']))
    
    # Apply palette
    app.setPalette(dark_palette)
    
    # Global stylesheet
    app.setStyleSheet(f"""
        QMainWindow {{
            background-color: {COLORS['background']};
        }}
        
        QWidget {{
            font-family: 'Inter', sans-serif;
            color: {COLORS['text_primary']};
        }}
        
        /* Toolbar */
        QToolBar {{
            background-color: {COLORS['surface']};
            border: none;
            border-bottom: 1px solid {COLORS['border']};
            spacing: 8px;
            padding: 4px;
        }}
        
        QToolBar QToolButton {{
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 4px;
            padding: 6px 12px;
            margin: 2px;
            font-weight: 500;
        }}
        
        QToolBar QToolButton:hover {{
            background-color: {COLORS['surface_light']};
            border-color: {COLORS['border']};
        }}
        
        QToolBar QToolButton:pressed {{
            background-color: {COLORS['border']};
        }}
        
        QToolBar QToolButton:checked {{
            background-color: {COLORS['accent_blue']};
            color: white;
        }}
        
        /* List Widget */
        QListWidget {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            padding: 4px;
            outline: none;
        }}
        
        QListWidget::item {{
            padding: 10px;
            border-radius: 4px;
            margin: 2px 0;
        }}
        
        QListWidget::item:hover {{
            background-color: {COLORS['surface_light']};
        }}
        
        QListWidget::item:selected {{
            background-color: {COLORS['accent_blue']};
            color: white;
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
        }}
        
        QTabBar::tab {{
            background-color: {COLORS['surface']};
            color: {COLORS['text_secondary']};
            padding: 8px 16px;
            margin-right: 4px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            font-weight: 500;
        }}
        
        QTabBar::tab:selected {{
            background-color: {COLORS['surface_light']};
            color: {COLORS['text_primary']};
            border-bottom: 2px solid {COLORS['accent_blue']};
        }}
        
        QTabBar::tab:hover {{
            background-color: {COLORS['surface_light']};
        }}
        
        /* Progress Bar */
        QProgressBar {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            text-align: center;
            height: 20px;
        }}
        
        QProgressBar::chunk {{
            background-color: {COLORS['accent_blue']};
            border-radius: 3px;
        }}
        
        /* Labels */
        QLabel {{
            color: {COLORS['text_primary']};
        }}
        
        /* Text Edit */
        QTextEdit, QPlainTextEdit {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 8px;
            font-family: 'JetBrains Mono', 'Consolas', monospace;
            font-size: 11px;
        }}
        
        /* Scroll Bar */
        QScrollBar:vertical {{
            background-color: {COLORS['surface']};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {COLORS['border']};
            border-radius: 6px;
            min-height: 30px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {COLORS['text_disabled']};
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {COLORS['surface']};
            border-top: 1px solid {COLORS['border']};
            color: {COLORS['text_secondary']};
        }}
        
        /* Splitter */
        QSplitter::handle {{
            background-color: {COLORS['border']};
        }}
        
        QSplitter::handle:hover {{
            background-color: {COLORS['accent_blue']};
        }}
        
        /* Graphics View */
        QGraphicsView {{
            background-color: {COLORS['background']};
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
        }}
        
        /* Push Button */
        QPushButton {{
            background-color: {COLORS['surface_light']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 6px 16px;
            font-weight: 500;
        }}
        
        QPushButton:hover {{
            background-color: {COLORS['border']};
            border-color: {COLORS['accent_blue']};
        }}
        
        QPushButton:pressed {{
            background-color: {COLORS['accent_blue']};
        }}
        
        QPushButton:checked {{
            background-color: {COLORS['accent_blue']};
            color: white;
        }}
        
        /* Line Edit */
        QLineEdit {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 6px 8px;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        QLineEdit:focus {{
            border-color: {COLORS['accent_blue']};
        }}
        
        /* Combo Box */
        QComboBox {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 6px 8px;
        }}
        
        QComboBox:hover {{
            border-color: {COLORS['accent_blue']};
        }}
        
        QComboBox::drop-down {{
            border: none;
        }}
        
        /* Spin Box */
        QSpinBox {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 4px 8px;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        QSpinBox:focus {{
            border-color: {COLORS['accent_blue']};
        }}
    """)