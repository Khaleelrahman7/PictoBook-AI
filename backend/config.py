"""Configuration settings for the personalization pipeline"""

import os

# Face detection settings
FACE_CROP_SIZE = 768  # Size for face crop (512, 768, or 1024)
FACE_DETECTION_CONFIDENCE = 0.9

# Stylization settings
STYLIZATION_PROMPT = "illustrative child portrait, flat colors, cute large eyes, soft shading, clean cartoon style, children's book illustration, vibrant colors, friendly expression"
NEGATIVE_PROMPT = "photorealistic, realistic, photo, photograph, blurry, distorted, ugly, bad anatomy"
STYLIZATION_STRENGTH = 0.75  # How much to stylize (0.0-1.0)
NUM_INFERENCE_STEPS = 30
GUIDANCE_SCALE = 7.5

# Model settings - Default to NVIDIA NIM API (fast and reliable)
USE_NVIDIA_NIM = os.getenv("USE_NVIDIA_NIM", "true").lower() == "true"  # Default to true
NVIDIA_NIM_API_KEY = os.getenv("NVIDIA_NIM_API_KEY", "")
NVIDIA_NIM_MODEL = os.getenv("NVIDIA_NIM_MODEL", "stabilityai/stable-diffusion-3-medium")  # SD3 Medium
NVIDIA_NIM_BASE_URL = os.getenv("NVIDIA_NIM_BASE_URL", "https://ai.api.nvidia.com/v1/genai")

# Alternative APIs
USE_REPLICATE = os.getenv("USE_REPLICATE", "false").lower() == "true"
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")
USE_HUGGINGFACE = os.getenv("USE_HUGGINGFACE", "false").lower() == "true"
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", "")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "ByteDance/SDXL-Lightning")
HUGGINGFACE_PROVIDER = os.getenv("HUGGINGFACE_PROVIDER", "fal-ai")
USE_LOCAL_SDXL = os.getenv("USE_LOCAL_SDXL", "false").lower() == "true"  # Only if explicitly enabled

# Face restoration settings
USE_FACE_RESTORATION = os.getenv("USE_FACE_RESTORATION", "true").lower() == "true"

# Template settings
TEMPLATE_DIR = "templates"
DEFAULT_TEMPLATE = "template1.png"

# Output settings
OUTPUT_FORMAT = "PNG"
OUTPUT_QUALITY = 95

