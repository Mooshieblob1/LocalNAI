from PyQt6.QtWidgets import (QTextEdit, QListWidget, QListWidgetItem, QVBoxLayout, 
                             QWidget, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QTextCursor, QKeyEvent, QColor
from utils.tag_manager import TagManager
import re
import math

class TagCompleteWidget(QWidget):
    """Widget that contains both text edit and embedded suggestions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tag_manager = TagManager()
        self.setup_ui()
        
        # Timer to delay search while typing
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.update_suggestions)
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        # Text edit with weighting support
        self.text_edit = WeightedTextEdit()
        self.text_edit.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.text_edit)
        
        # Suggestions list (embedded below text edit)
        self.suggestions_list = QListWidget()
        self.suggestions_list.setMaximumHeight(120)
        self.suggestions_list.setFrameStyle(QFrame.Shape.Box)
        self.suggestions_list.itemClicked.connect(self.insert_completion)
        self.suggestions_list.hide()  # Hidden initially
        layout.addWidget(self.suggestions_list)
        
    def on_text_changed(self):
        """Called when text changes - start search timer"""
        self.search_timer.stop()
        self.search_timer.start(200)  # 200ms delay
        
    def update_suggestions(self):
        """Update tag suggestions based on current word being typed"""
        cursor = self.text_edit.textCursor()
        current_word = self.get_current_word(cursor)
        
        if len(current_word) < 1:
            self.suggestions_list.hide()
            return
            
        # Search for matching tags
        matches = self.tag_manager.search_tags(current_word, limit=8)
        
        if not matches:
            self.suggestions_list.hide()
            return
            
        # Populate suggestions
        self.suggestions_list.clear()
        for tag_name, category, count in matches:
            category_name = self.tag_manager.get_category_name(category)
            
            # Format tag for display - keep original for display
            display_tag = self.format_tag_for_insertion(tag_name)
            item_text = f"{display_tag} ({category_name}, {count:,})"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, tag_name)  # Store original tag name
            
            # Color code by category
            if category == 4:  # Character
                item.setBackground(QColor(173, 216, 230))  # Light blue
            elif category == 1:  # Artist
                item.setBackground(QColor(144, 238, 144))  # Light green
            elif category == 3:  # Copyright
                item.setBackground(QColor(255, 255, 224))  # Light yellow
                
            self.suggestions_list.addItem(item)
        
        # Show the suggestions
        self.suggestions_list.show()
        
    def format_tag_for_insertion(self, tag_name):
        """Format tag by removing underscores and escaping parentheses"""
        # Remove underscores
        formatted = tag_name.replace('_', ' ')
        
        # Escape parentheses (but not weight parentheses)
        formatted = formatted.replace('(', r'\(')
        formatted = formatted.replace(')', r'\)')
        
        return formatted
        
    def get_current_word(self, cursor):
        """Get the word currently being typed at cursor position"""
        text = self.text_edit.toPlainText()
        pos = cursor.position()
        
        # Find start of current word (after comma or beginning)
        start = pos
        while start > 0 and text[start-1] not in [',', '\n']:
            start -= 1
            
        # Skip whitespace at start
        while start < len(text) and text[start] in [' ', '\t']:
            start += 1
            
        # Get text from start to cursor position
        current_word = text[start:pos].strip()
        return current_word
        
    def insert_completion(self, item):
        """Insert the selected completion"""
        original_tag = item.data(Qt.ItemDataRole.UserRole)
        formatted_tag = self.format_tag_for_insertion(original_tag)
        
        cursor = self.text_edit.textCursor()
        
        # Get current word to replace
        current_word = self.get_current_word(cursor)
        
        # Find the start position of the current word
        text = self.text_edit.toPlainText()
        pos = cursor.position()
        start = pos
        
        while start > 0 and text[start-1] not in [',', '\n']:
            start -= 1
        
        # Skip whitespace
        while start < len(text) and text[start] in [' ', '\t']:
            start += 1
            
        # Select current word and replace
        cursor.setPosition(start)
        cursor.setPosition(pos, QTextCursor.MoveMode.KeepAnchor)
        cursor.insertText(formatted_tag)  # Insert formatted tag
        
        # Add comma and space if we're not at the end
        current_text = self.text_edit.toPlainText()
        if cursor.position() < len(current_text) or not current_text.endswith(formatted_tag):
            cursor.insertText(', ')
        
        self.suggestions_list.hide()
        self.text_edit.setFocus()
        
    def keyPressEvent(self, event):
        """Handle key presses for suggestions navigation"""
        if self.suggestions_list.isVisible():
            if event.key() == Qt.Key.Key_Down:
                current_row = self.suggestions_list.currentRow()
                if current_row < self.suggestions_list.count() - 1:
                    self.suggestions_list.setCurrentRow(current_row + 1)
                else:
                    self.suggestions_list.setCurrentRow(0)
                return
                
            elif event.key() == Qt.Key.Key_Up:
                current_row = self.suggestions_list.currentRow()
                if current_row > 0:
                    self.suggestions_list.setCurrentRow(current_row - 1)
                else:
                    self.suggestions_list.setCurrentRow(self.suggestions_list.count() - 1)
                return
                
            elif event.key() in [Qt.Key.Key_Return, Qt.Key.Key_Enter]:
                current_item = self.suggestions_list.currentItem()
                if current_item:
                    self.insert_completion(current_item)
                return
                
            elif event.key() == Qt.Key.Key_Escape:
                self.suggestions_list.hide()
                return
                
        # Pass to text edit
        self.text_edit.keyPressEvent(event)
        
    # Proxy methods to make it work like a QTextEdit
    def toPlainText(self):
        return self.text_edit.toPlainText()
        
    def setPlainText(self, text):
        return self.text_edit.setPlainText(text)
        
    def setMinimumHeight(self, height):
        return self.text_edit.setMinimumHeight(height)
        
    def setMaximumHeight(self, height):
        return self.text_edit.setMaximumHeight(height)


class WeightedTextEdit(QTextEdit):
    """QTextEdit with tag weighting support via Ctrl+Up/Down using weight::tag:: format"""
    
    def keyPressEvent(self, event):
        # Check for Ctrl+Up/Down for weighting
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_Up:
                self.adjust_weight(0.1)  # Increase weight
                return
            elif event.key() == Qt.Key.Key_Down:
                self.adjust_weight(-0.1)  # Decrease weight
                return
                
        # Default handling
        super().keyPressEvent(event)
        
    def adjust_weight(self, delta):
        """Adjust weight of selected text or current tag"""
        cursor = self.textCursor()
        
        if cursor.hasSelection():
            # Check if selection is within a weighted tag
            selection_start = cursor.selectionStart()
            selection_end = cursor.selectionEnd()
            
            # Find the full weighted tag that contains this selection
            tag_start, tag_end = self.find_weighted_tag_boundaries(selection_start, selection_end)
            
            if tag_start != tag_end:
                # Select the entire weighted tag
                cursor.setPosition(tag_start)
                cursor.setPosition(tag_end, QTextCursor.MoveMode.KeepAnchor)
                tag_text = cursor.selectedText().strip()
                
                # Adjust weight and replace
                new_text = self.modify_tag_weight(tag_text, delta)
                cursor.insertText(new_text)
                return
            
            # Fallback to selected text if no weighted tag found
            selected_text = cursor.selectedText().strip()
            if not selected_text:
                return
                
            # Adjust weight and replace selection
            new_text = self.modify_tag_weight(selected_text, delta)
            cursor.insertText(new_text)
        else:
            # Find current tag at cursor position
            tag_start, tag_end = self.find_tag_boundaries(cursor.position())
            if tag_start == tag_end:
                return
                
            # Select the tag
            cursor.setPosition(tag_start)
            cursor.setPosition(tag_end, QTextCursor.MoveMode.KeepAnchor)
            
            tag_text = cursor.selectedText().strip()
            if not tag_text:
                return
                
            # Adjust weight and replace
            new_text = self.modify_tag_weight(tag_text, delta)
            cursor.insertText(new_text)
    
    def find_weighted_tag_boundaries(self, selection_start, selection_end):
        """Find boundaries of a weighted tag that contains the selection"""
        text = self.toPlainText()
        
        # Look for weight::tag:: pattern that contains the selection
        # Search backwards from selection_start to find potential start
        search_start = max(0, selection_start - 50)  # Look back up to 50 chars
        search_end = min(len(text), selection_end + 50)  # Look forward up to 50 chars
        
        search_text = text[search_start:search_end]
        
        # Find all weighted tag patterns in the search area
        weighted_pattern = r'([0-9.]+)::([^:,]+)::'
        
        for match in re.finditer(weighted_pattern, search_text):
            match_start = search_start + match.start()
            match_end = search_start + match.end()
            
            # Check if this weighted tag contains our selection
            if match_start <= selection_start and match_end >= selection_end:
                return match_start, match_end
        
        # No weighted tag found containing the selection
        return selection_start, selection_start
            
    def find_tag_boundaries(self, position):
        """Find the start and end of the current tag (weighted or unweighted)"""
        text = self.toPlainText()
        
        # First check if we're inside a weighted tag
        weighted_start, weighted_end = self.find_weighted_tag_boundaries(position, position)
        if weighted_start != weighted_end:
            return weighted_start, weighted_end
        
        # Fallback to regular tag boundaries
        # Find start (after comma or beginning)
        start = position
        while start > 0 and text[start-1] not in [',', '\n']:
            start -= 1
        while start < len(text) and text[start] in [' ', '\t']:
            start += 1
            
        # Find end (before comma or end)
        end = position
        while end < len(text) and text[end] not in [',', '\n']:
            end += 1
        while end > start and text[end-1] in [' ', '\t']:
            end -= 1
            
        return start, end
        
    def modify_tag_weight(self, tag_text, delta):
        """Modify the weight of a tag using weight::tag:: format"""
        tag_text = tag_text.strip()
        
        # Parse current weight
        current_weight, clean_tag = self.parse_tag_weight(tag_text)
        
        # Calculate new weight
        new_weight = current_weight + delta
        new_weight = max(0.1, min(2.0, new_weight))  # Clamp between 0.1 and 2.0
        
        # Format in weight::tag:: format
        return self.format_nai_weight(clean_tag, new_weight)
        
    def parse_tag_weight(self, tag_text):
        """Parse weight from tag in either SD or NAI weight::tag:: format"""
        tag_text = tag_text.strip()
        
        # Check for NAI weight::tag:: format
        nai_match = re.match(r'^([0-9.]+)::([^:]+)::$', tag_text)
        if nai_match:
            weight = float(nai_match.group(1))
            tag = nai_match.group(2).strip()
            return weight, tag
        
        # Check for SD format: (tag:weight) - for backwards compatibility
        sd_match = re.match(r'\(([^:]+):([0-9.]+)\)', tag_text)
        if sd_match:
            tag = sd_match.group(1).strip()
            weight = float(sd_match.group(2))
            return weight, tag
                
        # No weight found, assume 1.0
        return 1.0, tag_text
        
    def format_nai_weight(self, tag, weight):
        """Format tag with weight in NAI weight::tag:: format"""
        if abs(weight - 1.0) < 0.05:  # Close to 1.0, no weighting needed
            return tag
        
        # Use NAI weight::tag:: format with 1 decimal place
        weight_str = f"{weight:.1f}"
        return f"{weight_str}::{tag}::"