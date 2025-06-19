"""Convert between SD and NAI prompt formats"""
import re

def sd_to_nai_format(prompt_text):
    """Convert SD format weights to NAI format for API submission"""
    if not prompt_text:
        return prompt_text
    
    def convert_weight(match):
        tag = match.group(1).strip()
        weight = float(match.group(2))
        
        # Use NAI's weight::tag:: format
        return f"{weight:.1f}::{tag}::"
    
    # Convert all SD format weights (tag:weight) to NAI weight::tag:: format
    converted = re.sub(r'\(([^:]+):([0-9.]+)\)', convert_weight, prompt_text)
    return converted

def nai_to_sd_format(prompt_text):
    """Convert NAI format weights to SD format for display"""
    if not prompt_text:
        return prompt_text
    
    def convert_nai_weight(match):
        weight = float(match.group(1))
        tag = match.group(2).strip()
        return f"({tag}:{weight:.1f})"
    
    # Convert NAI weight::tag:: format to SD format
    converted = re.sub(r'([0-9.]+)::([^:]+)::', convert_nai_weight, prompt_text)
    
    return converted