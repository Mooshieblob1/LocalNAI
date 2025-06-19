from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QByteArray
from PIL import Image
import io
import base64

class ImageHandler:
    @staticmethod
    def bytes_to_pixmap(image_bytes: bytes) -> QPixmap:
        """Convert image bytes to QPixmap"""
        byte_array = QByteArray(image_bytes)
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array)
        return pixmap
    
    @staticmethod
    def save_image(image_bytes: bytes, filepath: str):
        """Save image bytes to file"""
        image = Image.open(io.BytesIO(image_bytes))
        image.save(filepath)
    
    @staticmethod
    def resize_image(image_bytes: bytes, width: int, height: int) -> bytes:
        """Resize image and return as bytes"""
        image = Image.open(io.BytesIO(image_bytes))
        resized = image.resize((width, height), Image.Resampling.LANCZOS)
        
        output = io.BytesIO()
        resized.save(output, format='PNG')
        return output.getvalue()
    
    @staticmethod
    def image_to_base64(image_bytes: bytes) -> str:
        """Convert image bytes to base64 string"""
        return base64.b64encode(image_bytes).decode('utf-8')
    
    @staticmethod
    def calculate_resolution(pixel_limit: int, original_size: tuple) -> tuple:
        """Calculate resolution that fits within pixel limit while maintaining aspect ratio"""
        width, height = original_size
        total_pixels = width * height
        
        if total_pixels <= pixel_limit:
            return width, height
        
        # Calculate scaling factor
        scale = (pixel_limit / total_pixels) ** 0.5
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Round to nearest 64 (NovelAI requirement)
        new_width = ((new_width + 31) // 64) * 64
        new_height = ((new_height + 31) // 64) * 64
        
        return new_width, new_height