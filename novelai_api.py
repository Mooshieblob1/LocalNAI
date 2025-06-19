import requests
import base64
import io
import zipfile
import random
from typing import Optional, Dict, Any
from config import Config

class NovelAIClient:
    def __init__(self):
        Config.validate()
        self.api_key = Config.API_KEY
        self.image_base_url = "https://image.novelai.net"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def generate_image(self, prompt: str, **kwargs) -> Optional[tuple]:
        """Generate image using NovelAI API - returns (image_bytes, actual_seed)"""
        
        model = kwargs.get('model', 'nai-diffusion-3')
        action = "generate"
        
        # Handle seed - always use the seed passed in (GUI handles -1 conversion)
        seed = kwargs.get('seed', 0)
        
        # Build parameters
        params = {
            "params_version": 1,
            "width": kwargs.get('width', 832),
            "height": kwargs.get('height', 1216),
            "scale": kwargs.get('scale', 5.0),
            "sampler": kwargs.get('sampler', 'k_euler'),
            "steps": kwargs.get('steps', 28),
            "seed": seed,
            "n_samples": 1,
            "ucPreset": 3,
            "qualityToggle": False,
            "sm": False,
            "sm_dyn": False,
            "dynamic_thresholding": False,
            "skip_cfg_above_sigma": None,
            "controlnet_strength": 1.0,
            "legacy": False,
            "add_original_image": False,
            "cfg_rescale": 0.0,
            "noise_schedule": kwargs.get('scheduler', 'native'),
            "legacy_v3_extend": False,
            "uncond_scale": 1.0,
            "negative_prompt": kwargs.get('negative_prompt', 'lowres'),
            "prompt": prompt,
            "reference_image_multiple": [],
            "reference_information_extracted_multiple": [],
            "reference_strength_multiple": [],
            "extra_noise_seed": seed,
            "v4_prompt": {
                "use_coords": False,
                "use_order": False,
                "caption": {
                    "base_caption": prompt,
                    "char_captions": []
                }
            },
            "v4_negative_prompt": {
                "use_coords": False,
                "use_order": False,
                "caption": {
                    "base_caption": kwargs.get('negative_prompt', 'lowres'),
                    "char_captions": []
                }
            }
        }
        
        request_data = {
            "input": prompt,
            "model": model,
            "action": action,
            "parameters": params
        }
        
        try:
            response = requests.post(
                f'{self.image_base_url}/ai/generate-image',
                headers=self.headers,
                json=request_data,
                timeout=120
            )
            
            if response.status_code == 200:
                # Success! Extract the image
                zip_content = response.content
                with zipfile.ZipFile(io.BytesIO(zip_content)) as zip_file:
                    image_files = zip_file.namelist()
                    if image_files:
                        print(f"✓ Image generated successfully (seed: {seed})")
                        return zip_file.read(image_files[0]), seed
            
            elif response.status_code == 400:
                print(f"Bad request: {response.text}")
            elif response.status_code == 401:
                print("Authentication failed - check your API key")
            elif response.status_code == 402:
                print("Payment required - check your subscription")
            elif response.status_code == 500:
                print(f"Server error: {response.text}")
            
            return None, None
            
        except Exception as e:
            print(f"Error generating image: {e}")
            return None, None