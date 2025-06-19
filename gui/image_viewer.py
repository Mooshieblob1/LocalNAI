from PyQt6.QtWidgets import QLabel, QMenu, QMessageBox, QApplication
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QAction
import json
import io
from PIL import Image
from PIL.PngImagePlugin import PngInfo

class ImageViewer(QLabel):
    """Custom QLabel with right-click context menu for image operations"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_image_data = None
        self.current_metadata = None
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 1px solid gray; min-height: 400px;")
        self.setText("No image generated yet")
        
    def set_image(self, image_data: bytes, metadata: dict):
        """Set the image and its metadata"""
        self.current_image_data = image_data
        self.current_metadata = metadata
        
        # Convert to pixmap and display
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        
        # Scale to fit
        scaled_pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(scaled_pixmap)
        
    def contextMenuEvent(self, event):
        """Show context menu on right click"""
        if self.current_image_data is None:
            return
            
        menu = QMenu(self)
        
        # Copy image action
        copy_action = QAction("Copy Image", self)
        copy_action.triggered.connect(self.copy_image_to_clipboard)
        menu.addAction(copy_action)
        
        # Copy image with metadata action
        copy_with_metadata_action = QAction("Copy Image with Metadata", self)
        copy_with_metadata_action.triggered.connect(self.copy_image_with_metadata_to_clipboard)
        menu.addAction(copy_with_metadata_action)
        
        menu.addSeparator()
        
        # Copy metadata action
        copy_metadata_action = QAction("Copy Metadata Only", self)
        copy_metadata_action.triggered.connect(self.copy_metadata_to_clipboard)
        menu.addAction(copy_metadata_action)
        
        menu.exec(event.globalPos())
        
    def copy_image_to_clipboard(self):
        """Copy just the image to clipboard"""
        if self.current_image_data is None:
            return
            
        try:
            pixmap = QPixmap()
            pixmap.loadFromData(self.current_image_data)
            
            clipboard = QApplication.clipboard()
            clipboard.setPixmap(pixmap)
            
        except Exception as e:
            print(f"Failed to copy image: {e}")
            
    def copy_image_with_metadata_to_clipboard(self):
        """Copy image with embedded metadata to clipboard (PNG format)"""
        if self.current_image_data is None or self.current_metadata is None:
            return
            
        try:
            # Load the original image
            image = Image.open(io.BytesIO(self.current_image_data))
            
            # Create PNG metadata
            png_info = PngInfo()
            
            # Add NovelAI-style metadata
            # Convert metadata to the format NovelAI uses
            novelai_metadata = self.format_novelai_metadata(self.current_metadata)
            
            # Add metadata chunks
            png_info.add_text("Title", "AI generated image")
            png_info.add_text("Description", novelai_metadata["prompt"])
            png_info.add_text("Software", "NovelAI")
            png_info.add_text("Source", "Stable Diffusion")
            png_info.add_text("Comment", json.dumps(novelai_metadata))
            
            # Save to bytes with metadata
            output = io.BytesIO()
            image.save(output, format="PNG", pnginfo=png_info)
            image_with_metadata = output.getvalue()
            
            # Copy to clipboard
            pixmap = QPixmap()
            pixmap.loadFromData(image_with_metadata)
            
            clipboard = QApplication.clipboard()
            clipboard.setPixmap(pixmap)
            
        except Exception as e:
            print(f"Failed to copy image with metadata: {e}")
            
    def copy_metadata_to_clipboard(self):
        """Copy just the metadata as JSON to clipboard"""
        if self.current_metadata is None:
            return
            
        try:
            novelai_metadata = self.format_novelai_metadata(self.current_metadata)
            metadata_json = json.dumps(novelai_metadata, indent=2)
            
            clipboard = QApplication.clipboard()
            clipboard.setText(metadata_json)
            
        except Exception as e:
            print(f"Failed to copy metadata: {e}")
            
    def format_novelai_metadata(self, metadata: dict) -> dict:
        """Format metadata in NovelAI's standard format"""
        return {
            "prompt": metadata.get('prompt', ''),
            "steps": metadata.get('steps', 28),
            "height": metadata.get('height', 1216),
            "width": metadata.get('width', 832),
            "scale": metadata.get('scale', 5.0),
            "uncond_scale": 1.0,
            "cfg_rescale": 0.0,
            "seed": metadata.get('seed', 0),
            "n_samples": 1,
            "hide_debug_overlay": False,
            "noise_schedule": metadata.get('scheduler', 'karras'),
            "legacy_v3_extend": False,
            "reference_information_extracted": [],
            "reference_strength": 0.6,
            "sampler": metadata.get('sampler', 'k_euler_ancestral'),
            "controlnet_strength": 1.0,
            "dynamic_thresholding": False,
            "dynamic_thresholding_percentile": 0.999,
            "dynamic_thresholding_mimic_scale": 10.0,
            "sm": False,
            "sm_dyn": False,
            "skip_cfg_above_sigma": None,
            "lora_unet_weights": None,
            "lora_clip_weights": None,
            "uc": metadata.get('negative_prompt', ''),
            "request_type": "PromptGenerateRequest",
            "signed_hash": None
        }