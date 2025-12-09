"""Optional face restoration using GFPGAN"""

import os
from PIL import Image
import numpy as np
from config import USE_FACE_RESTORATION

class FaceRestorer:
    def __init__(self):
        """Initialize face restoration"""
        self.use_restoration = USE_FACE_RESTORATION
        self.restorer = None
        
        if self.use_restoration:
            try:
                self._load_restorer()
            except Exception as e:
                print(f"Could not initialize face restoration: {e}")
                self.use_restoration = False
    
    def _load_restorer(self):
        """Load GFPGAN model"""
        try:
            from gfpgan import GFPGANer
            
            # Try to load GFPGAN
            model_path = 'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth'
            self.restorer = GFPGANer(
                model_path=model_path,
                upscale=1,
                arch='clean',
                channel_multiplier=2,
                bg_upsampler=None
            )
            print("GFPGAN loaded successfully")
        except Exception as e:
            print(f"Could not load GFPGAN: {e}")
            print("Face restoration will be skipped")
            self.use_restoration = False
            self.restorer = None
    
    def restore(self, face_image):
        """
        Restore/enhance face image
        
        Args:
            face_image: PIL Image
            
        Returns:
            restored_face: PIL Image
        """
        if not self.use_restoration or self.restorer is None:
            return face_image
        
        try:
            # Convert to numpy array
            img_array = np.array(face_image.convert('RGB'))
            
            # Restore
            _, _, restored = self.restorer.enhance(
                img_array,
                has_aligned=False,
                only_center_face=False,
                paste_back=True,
                weight=0.5
            )
            
            # Convert back to PIL
            restored_pil = Image.fromarray(restored)
            return restored_pil
            
        except Exception as e:
            print(f"Error in face restoration: {e}")
            return face_image

