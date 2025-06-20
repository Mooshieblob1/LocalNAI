from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTextEdit, QPushButton, QLabel, QSpinBox, 
                             QComboBox, QProgressBar, QScrollArea, QGridLayout,
                             QMessageBox, QFileDialog, QDoubleSpinBox, QLineEdit,
                             QCheckBox, QFrame, QSplitter, QGroupBox)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QPixmap, QFont
import io
from datetime import datetime
from novelai_api import NovelAIClient
from utils.image_handler import ImageHandler
from gui.tag_autocomplete import TagCompleteWidget
from gui.image_viewer import ImageViewer
from gui.styles import MAIN_STYLE
from gui.custom_widgets import ModernCheckBox
from utils.prompt_converter import sd_to_nai_format, nai_to_sd_format

class ImageGenerationThread(QThread):
    finished = pyqtSignal(bytes, int)
    error = pyqtSignal(str)
    
    def __init__(self, client, prompt, params):
        super().__init__()
        self.client = client
        self.prompt = prompt
        self.params = params
    
    def run(self):
        try:
            result = self.client.generate_image(self.prompt, **self.params)
            if result and len(result) == 2:
                image_data, actual_seed = result
                if image_data:
                    self.finished.emit(image_data, actual_seed)
                else:
                    self.error.emit("Failed to generate image")
            else:
                self.error.emit("Invalid response from API")
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.client = NovelAIClient()
        self.image_handler = ImageHandler()
        self.current_image_data = None
        self.generation_thread = None
        
        self.setWindowTitle("NovelAI Local - Modern Interface")
        self.setMinimumSize(1440, 840)  # 20% bigger than 1200x700
        self.resize(1680, 960)  # 20% bigger than 1400x800
        
        # Apply modern styling with more compact spacing
        self.setStyleSheet(MAIN_STYLE + """
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
        """)
        
        self.setup_ui()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with splitter for responsive design
        splitter = QSplitter(Qt.Orientation.Horizontal)
        central_widget.setLayout(QHBoxLayout())
        central_widget.layout().addWidget(splitter)
        central_widget.layout().setContentsMargins(8, 8, 8, 8)  # Reduced margins
        
        # Left panel (controls) - give it more room
        left_panel = self.create_control_panel()
        left_panel.setMaximumWidth(500)  # Increased from 420
        left_panel.setMinimumWidth(450)  # Increased from 380
        
        # Right panel (image display)
        right_panel = self.create_image_panel()
        
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        
    def create_control_panel(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(8)  # Reduced spacing
        layout.setContentsMargins(12, 12, 12, 12)  # Reduced margins
        
        # Title - more compact
        title = QLabel("✨ AI Generation")
        title.setStyleSheet("font-weight: 700; font-size: 16px; margin-bottom: 4px; text-align: center;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Prompt section - compact
        prompt_group = self.create_prompt_section()
        layout.addWidget(prompt_group)
        
        # Parameters section - compact
        params_group = self.create_parameters_section()
        layout.addWidget(params_group)
        
        # Generation controls
        controls_layout = self.create_generation_controls()
        layout.addLayout(controls_layout)
        
        layout.addStretch(0)  # Minimal stretch
        
        return container
        
    def create_prompt_section(self):
        group = QGroupBox("🎨 Prompts")
        layout = QVBoxLayout(group)
        layout.setSpacing(6)  # Compact spacing
        layout.setContentsMargins(8, 12, 8, 8)
        
        # Prompt input - REMOVED height constraints to allow dynamic sizing
        self.prompt_input = TagCompleteWidget()
        # Remove these lines to allow dynamic height:
        # self.prompt_input.setMinimumHeight(60)  
        # self.prompt_input.setMaximumHeight(80)
        layout.addWidget(self.prompt_input)
        
        # Quality toggle - inline with custom checkbox
        self.positive_quality_check = ModernCheckBox("✨ Enhanced Quality")
        self.positive_quality_check.setChecked(True)
        self.positive_quality_check.setStyleSheet("margin: 2px;")
        layout.addWidget(self.positive_quality_check)
        
        # Weighting hint
        hint_label = QLabel("💡 Highlight text + Ctrl+↑/↓ to adjust weights (weight::tag::)")
        hint_label.setStyleSheet("""
            font-size: 11px; 
            color: #a0a0a0; 
            margin: 2px; 
            padding: 2px;
        """)
        layout.addWidget(hint_label)
        
        # Negative prompt - compact
        neg_label = QLabel("Negative:")
        neg_label.setStyleSheet("font-size: 12px; margin: 4px 0 2px 0;")
        layout.addWidget(neg_label)
        
        self.negative_prompt_input = TagCompleteWidget()
        # Remove these lines to allow dynamic height:
        # self.negative_prompt_input.setMinimumHeight(40)  
        # self.negative_prompt_input.setMaximumHeight(60)
        layout.addWidget(self.negative_prompt_input)
        
        # Negative quality toggle with custom checkbox
        self.negative_quality_check = ModernCheckBox("🛡️ Quality Filtering")
        self.negative_quality_check.setChecked(True)
        self.negative_quality_check.setStyleSheet("margin: 2px;")
        layout.addWidget(self.negative_quality_check)
        
        return group
        
    def create_parameters_section(self):
        group = QGroupBox("⚙️ Parameters")
        layout = QVBoxLayout(group)
        layout.setSpacing(4)  # Very compact
        layout.setContentsMargins(8, 12, 8, 8)
        
        # Create a more compact grid
        grid = QGridLayout()
        grid.setSpacing(6)
        grid.setVerticalSpacing(4)  # Tighter vertical spacing
        
        # Row 1: Model and Opus Limit (separate sections)
        grid.addWidget(QLabel("Model:"), 0, 0)
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            'nai-diffusion-4-5-full',
            'nai-diffusion-4-5-curated', 
            'nai-diffusion-4-full',
            'nai-diffusion-4-curated-preview',
            'nai-diffusion-3',
            'nai-diffusion-furry-3'
        ])
        grid.addWidget(self.model_combo, 0, 1)
        
        # Opus limit section - separate from model
        opus_label = QLabel("Limits:")
        opus_label.setStyleSheet("margin-left: 12px;")  # Add some spacing
        grid.addWidget(opus_label, 0, 2)
        
        self.opus_limit_checkbox = ModernCheckBox("Opus Limit")
        self.opus_limit_checkbox.setChecked(True)
        self.opus_limit_checkbox.stateChanged.connect(self.on_opus_limit_changed)
        grid.addWidget(self.opus_limit_checkbox, 0, 3)
        
        # Row 2: Dimensions side by side
        grid.addWidget(QLabel("Size:"), 1, 0)
        size_layout = QHBoxLayout()
        self.width_spin = QSpinBox()
        self.width_spin.setRange(64, 1600)
        self.width_spin.setValue(832)
        self.width_spin.setSingleStep(64)
        self.width_spin.valueChanged.connect(self.enforce_opus_limit)
        size_layout.addWidget(self.width_spin)
        
        size_layout.addWidget(QLabel("×"))
        
        self.height_spin = QSpinBox()
        self.height_spin.setRange(64, 1600)
        self.height_spin.setValue(1216)
        self.height_spin.setSingleStep(64)
        self.height_spin.valueChanged.connect(self.enforce_opus_limit)
        size_layout.addWidget(self.height_spin)
        
        size_widget = QWidget()
        size_widget.setLayout(size_layout)
        grid.addWidget(size_widget, 1, 1, 1, 3)  # Span across remaining columns
        
        # Row 3: Steps and CFG
        grid.addWidget(QLabel("Steps:"), 2, 0)
        self.steps_spin = QSpinBox()
        self.steps_spin.setRange(1, 50)
        self.steps_spin.setValue(23)
        grid.addWidget(self.steps_spin, 2, 1)
        
        grid.addWidget(QLabel("CFG:"), 2, 2)
        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(0.0, 10.0)
        self.scale_spin.setValue(5.0)
        self.scale_spin.setSingleStep(0.1)
        self.scale_spin.setMaximumWidth(80)
        grid.addWidget(self.scale_spin, 2, 3)
        
        # Row 4: Sampler
        grid.addWidget(QLabel("Sampler:"), 3, 0)
        self.sampler_combo = QComboBox()
        self.sampler_combo.addItems([
            'k_euler_ancestral', 'k_euler', 'k_dpmpp_2s_ancestral', 
            'k_dpmpp_2m_sde', 'k_dpmpp_2m', 'k_dpmpp_sde', 'ddim'
        ])
        self.sampler_combo.setCurrentText('k_euler_ancestral')
        grid.addWidget(self.sampler_combo, 3, 1, 1, 3)
        
        # Row 5: Scheduler
        grid.addWidget(QLabel("Schedule:"), 4, 0)
        self.scheduler_combo = QComboBox()
        self.scheduler_combo.addItems(['karras', 'native', 'exponential', 'polyexponential'])
        self.scheduler_combo.setCurrentText('karras')
        grid.addWidget(self.scheduler_combo, 4, 1, 1, 3)
        
        # Row 6: Seed
        grid.addWidget(QLabel("Seed:"), 5, 0)
        seed_layout = QHBoxLayout()
        seed_layout.setSpacing(4)
        
        self.seed_input = QLineEdit()
        self.seed_input.setText("-1")
        self.seed_input.setPlaceholderText("Random")
        seed_layout.addWidget(self.seed_input)
        
        reset_seed_btn = QPushButton("⟲")  # Try this circular arrow
        reset_seed_btn.setMaximumWidth(32)
        reset_seed_btn.setMaximumHeight(32)
        reset_seed_btn.setToolTip("Reset to random (-1)")
        reset_seed_btn.setStyleSheet("""
            QPushButton {
                background-color: #3d3d3d;
                border: 1px solid #5d5d5d;
                border-radius: 4px;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
                border: 1px solid #0078d4;
            }
            QPushButton:pressed {
                background-color: #0078d4;
            }
        """)
        reset_seed_btn.clicked.connect(self.reset_seed)
        seed_layout.addWidget(reset_seed_btn)
        
        seed_widget = QWidget()
        seed_widget.setLayout(seed_layout)
        grid.addWidget(seed_widget, 5, 1, 1, 3)
        
        layout.addLayout(grid)
        
        # Apply initial opus limit
        self.enforce_opus_limit()
        
        return group
        
    def create_generation_controls(self):
        layout = QVBoxLayout()
        layout.setSpacing(6)
        
        # Generate button
        self.generate_btn = QPushButton("🚀 Generate Image")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                font-size: 14px;
                font-weight: 700;
                padding: 10px 20px;
                border-radius: 6px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:pressed {
                background-color: #047857;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #6d6d6d;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_image)
        layout.addWidget(self.generate_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumHeight(6)  # Thinner progress bar
        layout.addWidget(self.progress_bar)
        
        return layout
        
    def create_image_panel(self):
        widget = QFrame()
        widget.setObjectName("glassPanel")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)  # Reduced spacing
        
        # Title - much more compact
        title = QLabel("🖼️ Generated Image")
        title.setStyleSheet("""
            font-weight: 600; 
            font-size: 14px; 
            margin: 0px; 
            padding: 4px 0px;
            color: #ffffff;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setMaximumHeight(24)  # Limit height
        layout.addWidget(title)
        
        # Image display
        self.image_viewer = ImageViewer()
        self.image_viewer.setStyleSheet("""
            QLabel {
                border: 2px dashed #3d3d3d;
                border-radius: 12px;
                background-color: #252525;
                min-height: 300px;
            }
        """)
        layout.addWidget(self.image_viewer)
        
        # Bottom controls - horizontal layout
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(8)
        
        # Seed display - now selectable
        self.seed_display = QLabel("Seed: Not generated yet")
        self.seed_display.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)
        self.seed_display.setStyleSheet("""
            background-color: #252525;
            border: 1px solid #3d3d3d;
            border-radius: 4px;
            font-family: 'SF Mono', 'Monaco', 'Cascadia Code', monospace;
            font-size: 11px;
            color: #a0a0a0;
            padding: 4px 8px;
            margin: 0px;
        """)
        self.seed_display.setMaximumHeight(24)  # Limit height
        bottom_layout.addWidget(self.seed_display)
        
        # Save button
        self.save_btn = QPushButton("💾 Save")
        self.save_btn.clicked.connect(self.save_image)
        self.save_btn.setEnabled(False)
        self.save_btn.setMaximumWidth(80)
        self.save_btn.setMaximumHeight(28)  # Limit height
        bottom_layout.addWidget(self.save_btn)
        
        layout.addLayout(bottom_layout)
        
        return widget

    def on_opus_limit_changed(self):
        """Called when Opus Limit checkbox is toggled"""
        self.enforce_opus_limit()
    
    def enforce_opus_limit(self):
        """Enforce Opus limits on resolution if checkbox is enabled"""
        if not self.opus_limit_checkbox.isChecked():
            return
        
        current_width = self.width_spin.value()
        current_height = self.height_spin.value()
        pixel_limit = 1024 * 1024
        
        if current_width * current_height > pixel_limit:
            new_width, new_height = self.calculate_resolution_within_limit(current_width, current_height, pixel_limit)
            
            self.width_spin.valueChanged.disconnect(self.enforce_opus_limit)
            self.height_spin.valueChanged.disconnect(self.enforce_opus_limit)
            
            self.width_spin.setValue(new_width)
            self.height_spin.setValue(new_height)
            
            self.width_spin.valueChanged.connect(self.enforce_opus_limit)
            self.height_spin.valueChanged.connect(self.enforce_opus_limit)

    def calculate_resolution_within_limit(self, width, height, pixel_limit=1024*1024):
        """Calculate resolution that maintains aspect ratio but fits exactly within pixel limit"""
        aspect_ratio = width / height
        new_width = int((pixel_limit * aspect_ratio) ** 0.5)
        new_height = int((pixel_limit / aspect_ratio) ** 0.5)
        
        new_width = ((new_width + 31) // 64) * 64
        new_height = ((new_height + 31) // 64) * 64
        
        while new_width * new_height > pixel_limit:
            if new_width > new_height:
                new_width -= 64
            else:
                new_height -= 64
        
        new_width = max(64, new_width)
        new_height = max(64, new_height)
        
        return new_width, new_height

    def randomize_seed(self):
        """Set a random seed value"""
        import random
        random_seed = random.randint(0, 2147483647)
        self.seed_input.setText(str(random_seed))
    
    def get_full_prompt(self):
        """Get the complete prompt including quality tags, converted to NAI format"""
        prompt = self.prompt_input.toPlainText().strip()
        
        if self.positive_quality_check.isChecked():
            positive_quality_tags = "best quality, very aesthetic, absurdres"
            if prompt:
                prompt = f"{prompt}, {positive_quality_tags}"
            else:
                prompt = positive_quality_tags
        
        # Convert SD format to NAI format for API
        return sd_to_nai_format(prompt)
    
    def get_full_negative_prompt(self):
        """Get the complete negative prompt including quality tags, converted to NAI format"""
        negative_prompt = self.negative_prompt_input.toPlainText().strip()
        
        if self.negative_quality_check.isChecked():
            negative_quality_tags = "blurry, lowres, error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, multiple views, logo, too many watermarks, white blank page, blank page"
            if negative_prompt:
                negative_prompt = f"{negative_prompt}, {negative_quality_tags}"
            else:
                negative_prompt = negative_quality_tags
        
        # Convert SD format to NAI format for API
        return sd_to_nai_format(negative_prompt)
    
    def get_display_prompt(self):
        """Get the prompt as displayed (SD format) for metadata"""
        prompt = self.prompt_input.toPlainText().strip()
        
        if self.positive_quality_check.isChecked():
            positive_quality_tags = "best quality, very aesthetic, absurdres"
            if prompt:
                prompt = f"{prompt}, {positive_quality_tags}"
            else:
                prompt = positive_quality_tags
                
        return prompt
    
    def get_display_negative_prompt(self):
        """Get the negative prompt as displayed (SD format) for metadata"""
        negative_prompt = self.negative_prompt_input.toPlainText().strip()
        
        if self.negative_quality_check.isChecked():
            negative_quality_tags = "blurry, lowres, error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, multiple views, logo, too many watermarks, white blank page, blank page"
            if negative_prompt:
                negative_prompt = f"{negative_prompt}, {negative_quality_tags}"
            else:
                negative_prompt = negative_quality_tags
                
        return negative_prompt
    
    def generate_image(self):
        # Get NAI-formatted prompts for API
        prompt = self.get_full_prompt()  # This now returns NAI format
        negative_prompt = self.get_full_negative_prompt()  # This now returns NAI format
        
        if not prompt:
            QMessageBox.warning(self, "Warning", "Please enter a prompt or enable positive quality tags")
            return
        
        try:
            seed_text = self.seed_input.text().strip()
            if seed_text == "-1" or seed_text == "":
                import random
                seed_value = random.randint(0, 2147483647)
            else:
                seed_value = int(seed_text)
                if seed_value < 0:
                    import random
                    seed_value = random.randint(0, 2147483647)
        except ValueError:
            import random
            seed_value = random.randint(0, 2147483647)
        
        params = {
            'model': self.model_combo.currentText(),
            'width': self.width_spin.value(),
            'height': self.height_spin.value(),
            'steps': self.steps_spin.value(),
            'scale': self.scale_spin.value(),
            'sampler': self.sampler_combo.currentText(),
            'scheduler': self.scheduler_combo.currentText(),
            'seed': seed_value,
            'negative_prompt': negative_prompt  # NAI format
        }
        
        print(f"Sending to API - Prompt: {prompt}")  # Debug - shows NAI format
        print(f"Sending to API - Negative: {negative_prompt}")  # Debug - shows NAI format
        
        self.generate_btn.setEnabled(False)
        self.generate_btn.setText("🔄 Generating...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        self.generation_thread = ImageGenerationThread(self.client, prompt, params)
        self.generation_thread.finished.connect(self.on_image_generated)
        self.generation_thread.error.connect(self.on_generation_error)
        self.generation_thread.start()
    
    def on_image_generated(self, image_data, actual_seed):
        self.current_image_data = image_data
        
        self.seed_display.setText(f"Seed: {actual_seed}")
        
        # Store metadata in NAI format to verify conversion is working
        metadata = {
            'prompt': self.get_full_prompt(),  # NAI format for verification
            'negative_prompt': self.get_full_negative_prompt(),  # NAI format for verification
            'model': self.model_combo.currentText(),
            'width': self.width_spin.value(),
            'height': self.height_spin.value(),
            'steps': self.steps_spin.value(),
            'scale': self.scale_spin.value(),
            'sampler': self.sampler_combo.currentText(),
            'scheduler': self.scheduler_combo.currentText(),
            'seed': actual_seed
        }
        
        self.image_viewer.set_image(image_data, metadata)
        
        self.save_btn.setEnabled(True)
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("🚀 Generate Image")
        self.progress_bar.setVisible(False)
    
    def on_generation_error(self, error_message):
        QMessageBox.critical(self, "Generation Error", f"Failed to generate image: {error_message}")
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("🚀 Generate Image")
        self.progress_bar.setVisible(False)
    
    def save_image(self):
        if self.current_image_data is None:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_image_{timestamp}.png"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save Image", 
            filename, 
            "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)"
        )
        
        if file_path:
            self.image_handler.save_image(self.current_image_data, file_path)

    def reset_seed(self):
        """Reset seed to -1 (random)"""
        self.seed_input.setText("-1")