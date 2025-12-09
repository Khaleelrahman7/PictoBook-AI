"""Face detection and alignment using MTCNN"""

import torch
from facenet_pytorch import MTCNN
from PIL import Image
import numpy as np
import cv2

class FaceDetector:
    def __init__(self, device=None):
        """Initialize MTCNN face detector"""
        if device is None:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device
        
        self.mtcnn = MTCNN(
            image_size=512,
            margin=40,
            min_face_size=40,
            thresholds=[0.6, 0.7, 0.7],
            factor=0.709,
            post_process=False,
            device=self.device
        )
    
    def detect_and_align(self, pil_image, target_size=768):
        """
        Detect face in image and return aligned, cropped face
        
        Args:
            pil_image: PIL Image
            target_size: Size to resize cropped face to
            
        Returns:
            face_image: PIL Image of cropped face
            bbox: (x1, y1, x2, y2) bounding box coordinates
            landmarks: Face landmarks (eyes, nose, mouth)
        """
        # Convert PIL to numpy array
        img_array = np.array(pil_image.convert('RGB'))
        
        # Detect faces and landmarks
        boxes, probs, landmarks = self.mtcnn.detect(img_array, landmarks=True)
        
        if boxes is None or len(boxes) == 0:
            raise ValueError("No face detected in the image. Please upload a photo with a clear face.")
        
        # Get the face with highest confidence
        best_idx = np.argmax(probs)
        box = boxes[best_idx]
        landmarks = landmarks[best_idx]
        
        # Extract bounding box
        x1, y1, x2, y2 = map(int, box)
        
        # Ensure coordinates are within image bounds
        width, height = pil_image.size
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(width, x2)
        y2 = min(height, y2)
        
        # Crop face with margin
        margin = 0.2  # 20% margin
        w = x2 - x1
        h = y2 - y1
        x1 = max(0, int(x1 - w * margin))
        y1 = max(0, int(y1 - h * margin))
        x2 = min(width, int(x2 + w * margin))
        y2 = min(height, int(y2 + h * margin))
        
        # Crop and resize
        face_crop = pil_image.crop((x1, y1, x2, y2))
        face_resized = face_crop.resize((target_size, target_size), Image.LANCZOS)
        
        return face_resized, (x1, y1, x2, y2), landmarks
    
    def align_face(self, pil_image, landmarks, target_size=768):
        """
        Align face using eye landmarks for better results
        
        Args:
            pil_image: PIL Image
            landmarks: Face landmarks from MTCNN
            target_size: Output size
            
        Returns:
            aligned_face: PIL Image
        """
        # Get eye coordinates
        left_eye = landmarks[0]
        right_eye = landmarks[1]
        
        # Calculate angle
        dy = right_eye[1] - left_eye[1]
        dx = right_eye[0] - left_eye[0]
        angle = np.degrees(np.arctan2(dy, dx))
        
        # Rotate to align eyes horizontally
        if abs(angle) > 1:  # Only rotate if misaligned
            img_array = np.array(pil_image)
            center = (img_array.shape[1] // 2, img_array.shape[0] // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(img_array, M, (img_array.shape[1], img_array.shape[0]))
            pil_image = Image.fromarray(rotated)
        
        return pil_image.resize((target_size, target_size), Image.LANCZOS)

