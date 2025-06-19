from PyQt6.QtWidgets import QCheckBox, QStyleOptionButton
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QPen, QColor

class ModernCheckBox(QCheckBox):
    """Custom checkbox with green checkmark"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
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
        """)
    
    def paintEvent(self, event):
        super().paintEvent(event)
        
        if self.isChecked():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Create style option
            option = QStyleOptionButton()
            self.initStyleOption(option)
            
            # Get checkbox rectangle
            checkbox_rect = self.style().subElementRect(
                self.style().SubElement.SE_CheckBoxIndicator, 
                option, 
                self
            )
            
            # Draw checkmark
            pen = QPen(QColor(255, 255, 255), 2)
            painter.setPen(pen)
            
            # Checkmark coordinates (convert to integers)
            x = checkbox_rect.x()
            y = checkbox_rect.y()
            w = checkbox_rect.width()
            h = checkbox_rect.height()
            
            # Draw the checkmark with integer coordinates
            x1 = int(x + w * 0.25)
            y1 = int(y + h * 0.5)
            x2 = int(x + w * 0.45)
            y2 = int(y + h * 0.7)
            x3 = int(x + w * 0.75)
            y3 = int(y + h * 0.3)
            
            painter.drawLine(x1, y1, x2, y2)
            painter.drawLine(x2, y2, x3, y3)