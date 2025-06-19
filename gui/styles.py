"""Modern dark theme styles for the application"""

MAIN_STYLE = """
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}

QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
    font-family: 'Segoe UI', 'San Francisco', system-ui, sans-serif;
    font-size: 13px;
}

QLabel {
    color: #ffffff;
    font-weight: 500;
    padding: 4px;
}

QTextEdit {
    background-color: #2d2d2d;
    border: 2px solid #3d3d3d;
    border-radius: 8px;
    padding: 12px;
    color: #ffffff;
    selection-background-color: #0078d4;
    font-family: 'SF Mono', 'Monaco', 'Cascadia Code', monospace;
}

QTextEdit:focus {
    border: 2px solid #0078d4;
}

QLineEdit {
    background-color: #2d2d2d;
    border: 2px solid #3d3d3d;
    border-radius: 6px;
    padding: 8px 12px;
    color: #ffffff;
    font-size: 13px;
}

QLineEdit:focus {
    border: 2px solid #0078d4;
}

QPushButton {
    background-color: #0078d4;
    border: none;
    border-radius: 6px;
    color: white;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 13px;
    min-height: 16px;
}

QPushButton:hover {
    background-color: #106ebe;
}

QPushButton:pressed {
    background-color: #005a9e;
}

QPushButton:disabled {
    background-color: #3d3d3d;
    color: #6d6d6d;
}

QComboBox {
    background-color: #2d2d2d;
    border: 2px solid #3d3d3d;
    border-radius: 6px;
    padding: 8px 12px;
    color: #ffffff;
    min-width: 120px;
}

QComboBox:focus {
    border: 2px solid #0078d4;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #ffffff;
    margin-right: 5px;
}

QComboBox QAbstractItemView {
    background-color: #2d2d2d;
    border: 1px solid #3d3d3d;
    border-radius: 6px;
    selection-background-color: #0078d4;
    color: #ffffff;
    padding: 4px;
}

QSpinBox, QDoubleSpinBox {
    background-color: #2d2d2d;
    border: 2px solid #3d3d3d;
    border-radius: 6px;
    padding: 8px 12px;
    color: #ffffff;
    min-width: 60px;
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border: 2px solid #0078d4;
}

QSpinBox::up-button, QDoubleSpinBox::up-button {
    background-color: #3d3d3d;
    border: none;
    border-radius: 3px;
    width: 18px;
    height: 12px;
    subcontrol-origin: border;
    subcontrol-position: top right;
    margin-right: 2px;
    margin-top: 2px;
}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {
    background-color: #4d4d4d;
}

QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed {
    background-color: #0078d4;
}

QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 4px solid #ffffff;
    width: 0px;
    height: 0px;
}

QSpinBox::down-button, QDoubleSpinBox::down-button {
    background-color: #3d3d3d;
    border: none;
    border-radius: 3px;
    width: 18px;
    height: 12px;
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    margin-right: 2px;
    margin-bottom: 2px;
}

QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #4d4d4d;
}

QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {
    background-color: #0078d4;
}

QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 4px solid #ffffff;
    width: 0px;
    height: 0px;
}

QCheckBox {
    color: #ffffff;
    spacing: 8px;
    font-weight: 500;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #3d3d3d;
    background-color: #2d2d2d;
}

QCheckBox::indicator:hover {
    border: 2px solid #0078d4;
}

QCheckBox::indicator:checked {
    background-color: #10b981;
    border: 2px solid #10b981;
}

QListWidget {
    background-color: #2d2d2d;
    border: 1px solid #3d3d3d;
    border-radius: 8px;
    padding: 4px;
    alternate-background-color: #333333;
}

QListWidget::item {
    padding: 8px 12px;
    border-radius: 4px;
    margin: 1px;
}

QListWidget::item:hover {
    background-color: #3d3d3d;
}

QListWidget::item:selected {
    background-color: #0078d4;
}

QProgressBar {
    border: none;
    border-radius: 6px;
    background-color: #3d3d3d;
    height: 8px;
}

QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 6px;
}

QScrollBar:vertical {
    background-color: #2d2d2d;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #3d3d3d;
    border-radius: 6px;
    min-height: 20px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background-color: #4d4d4d;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QFrame#parameterFrame {
    background-color: #252525;
    border: 1px solid #3d3d3d;
    border-radius: 12px;
    padding: 16px;
    margin: 8px;
}

QFrame#qualityFrame {
    background-color: #252525;
    border: 1px solid #3d3d3d;
    border-radius: 8px;
    padding: 8px;
}

QLabel#sectionTitle {
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
    padding: 8px 0px;
}

QLabel#seedDisplay {
    background-color: #252525;
    border: 1px solid #3d3d3d;
    border-radius: 6px;
    font-family: 'SF Mono', 'Monaco', 'Cascadia Code', monospace;
    font-size: 12px;
    color: #a0a0a0;
}

QMenu {
    background-color: #2d2d2d;
    border: 1px solid #3d3d3d;
    border-radius: 8px;
    padding: 4px;
}

QMenu::item {
    padding: 8px 16px;
    border-radius: 4px;
}

QMenu::item:selected {
    background-color: #0078d4;
}

QGroupBox {
    font-weight: 600;
    font-size: 13px;
    padding-top: 12px;
    margin-top: 8px;
    border: 1px solid #3d3d3d;
    border-radius: 6px;
    background-color: #252525;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px 0 4px;
    color: #ffffff;
    background-color: #252525;
}
"""

GLASSMORPHISM_STYLE = """
QFrame#glassPanel {
    background-color: rgba(45, 45, 45, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
}
"""