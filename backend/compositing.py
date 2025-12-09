"""Composite stylized face into template"""

import os
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
from config import TEMPLATE_DIR, DEFAULT_TEMPLATE

class TemplateCompositor:
    def __init__(self, template_path=None):
        """Initialize with template path"""
        if template_path is None:
            template_path = os.path.join(TEMPLATE_DIR, DEFAULT_TEMPLATE)
        self.template_path = template_path
    
    def composite(self, stylized_face, face_bbox=None, template_path=None):
        """
        Composite stylized face into template
        
        Args:
            stylized_face: PIL Image of stylized face
            face_bbox: Original bounding box (x1, y1, x2, y2) - optional for auto-detection
            template_path: Path to template (uses default if None)
            
        Returns:
            final_image: PIL Image of composited result
        """
        if template_path is None:
            template_path = self.template_path
        
        # Load template
        if not os.path.exists(template_path):
            # Create a simple template if none exists
            return self._create_simple_template(stylized_face)
        
        template = Image.open(template_path).convert("RGB")
        
        # Detect face area in template (simple approach: center region)
        # In production, you'd have predefined coordinates or use face detection
        face_region = self._detect_template_face_region(template)
        
        # Resize stylized face to match template face region
        target_width = face_region[2] - face_region[0]
        target_height = face_region[3] - face_region[1]
        
        # Maintain aspect ratio but ensure it fits
        face_aspect = stylized_face.width / stylized_face.height
        target_aspect = target_width / target_height
        
        if face_aspect > target_aspect:
            # Face is wider - fit to width
            new_width = target_width
            new_height = int(target_width / face_aspect)
        else:
            # Face is taller - fit to height
            new_height = target_height
            new_width = int(target_height * face_aspect)
        
        resized_face = stylized_face.resize((new_width, new_height), Image.LANCZOS)
        
        # Create mask for smooth blending
        mask = self._create_feathered_mask(new_width, new_height, feather_size=20)
        
        # Paste face into template
        result = template.copy()
        
        # Calculate paste position (center in face region)
        paste_x = face_region[0] + (target_width - new_width) // 2
        paste_y = face_region[1] + (target_height - new_height) // 2
        
        # Convert to RGBA for alpha blending
        if resized_face.mode != "RGBA":
            resized_face = resized_face.convert("RGBA")
        
        # Apply mask as alpha channel
        resized_face.putalpha(mask)
        
        # Paste with alpha blending
        result.paste(resized_face, (paste_x, paste_y), resized_face)
        
        # Optional: Color matching to template
        result = self._match_colors(result, template, face_region)
        
        return result
    
    def _detect_template_face_region(self, template):
        """
        Detect or estimate face region in template
        For now, uses center region. In production, use predefined coordinates.
        """
        width, height = template.size
        
        # Assume face is in center 30% of image
        face_width = int(width * 0.3)
        face_height = int(height * 0.3)
        
        x1 = (width - face_width) // 2
        y1 = int(height * 0.25)  # Slightly above center
        x2 = x1 + face_width
        y2 = y1 + face_height
        
        return (x1, y1, x2, y2)
    
    def _create_feathered_mask(self, width, height, feather_size=20):
        """Create a feathered mask for smooth blending"""
        # Create base mask
        mask = Image.new("L", (width, height), 255)
        
        # Create gradient edges
        mask_array = np.array(mask)
        
        # Feather edges
        for i in range(feather_size):
            alpha = int(255 * (i / feather_size))
            # Top edge
            mask_array[i, :] = np.minimum(mask_array[i, :], alpha)
            # Bottom edge
            mask_array[height - 1 - i, :] = np.minimum(mask_array[height - 1 - i, :], alpha)
            # Left edge
            mask_array[:, i] = np.minimum(mask_array[:, i], alpha)
            # Right edge
            mask_array[:, width - 1 - i] = np.minimum(mask_array[:, width - 1 - i], alpha)
        
        # Apply gaussian blur for smoother edges
        mask = Image.fromarray(mask_array)
        mask = mask.filter(ImageFilter.GaussianBlur(radius=feather_size // 4))
        
        return mask
    
    def _match_colors(self, result, template, face_region):
        """Match colors of pasted face to template style"""
        # Extract template colors around face region
        region = template.crop(face_region)
        
        # Simple color adjustment - can be enhanced
        # For now, just slight brightness/contrast matching
        enhancer = ImageEnhance.Brightness(result)
        result = enhancer.enhance(0.98)  # Slight darkening
        
        return result
    
    def _create_simple_template(self, face_image):
        """Create a simple template if none exists"""
        # Create a simple colored background
        width, height = 1024, 1024
        template = Image.new("RGB", (width, height), color=(240, 248, 255))  # Light blue
        
        # Add some decorative elements (simple circles)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(template)
        
        # Draw some decorative circles
        for i in range(5):
            x = width // 2 + (i - 2) * 150
            y = height // 4
            draw.ellipse([x - 30, y - 30, x + 30, y + 30], fill=(255, 200, 200), outline=None)
        
        # Composite face in center
        face_size = min(width, height) // 2
        face_resized = face_image.resize((face_size, face_size), Image.LANCZOS)
        
        paste_x = (width - face_size) // 2
        paste_y = (height - face_size) // 2
        
        if face_resized.mode != "RGBA":
            face_resized = face_resized.convert("RGBA")
        
        mask = self._create_feathered_mask(face_size, face_size)
        face_resized.putalpha(mask)
        
        template.paste(face_resized, (paste_x, paste_y), face_resized)
        
        return template

