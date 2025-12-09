"""Test script to verify installation and components"""

import sys
import traceback

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    try:
        import torch
        print(f"✓ PyTorch {torch.__version__}")
        print(f"  CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"  CUDA device: {torch.cuda.get_device_name(0)}")
    except ImportError as e:
        print(f"✗ PyTorch not installed: {e}")
        return False
    
    try:
        from facenet_pytorch import MTCNN
        print("✓ facenet-pytorch")
    except ImportError as e:
        print(f"✗ facenet-pytorch not installed: {e}")
        return False
    
    try:
        # diffusers is optional (only for local models)
        from diffusers import StableDiffusionXLImg2ImgPipeline
        print("✓ diffusers (optional - for local models)")
    except ImportError:
        print("⚠ diffusers not installed (optional - only needed for local SDXL)")
        print("  Using API is recommended - no diffusers needed")
    
    try:
        import replicate
        print("✓ replicate")
    except ImportError as e:
        print(f"✗ replicate not installed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✓ Pillow")
    except ImportError as e:
        print(f"✗ Pillow not installed: {e}")
        return False
    
    try:
        import cv2
        print(f"✓ OpenCV {cv2.__version__}")
    except ImportError as e:
        print(f"✗ OpenCV not installed: {e}")
        return False
    
    try:
        from fastapi import FastAPI
        print("✓ FastAPI")
    except ImportError as e:
        print(f"✗ FastAPI not installed: {e}")
        return False
    
    return True

def test_components():
    """Test if components can be initialized"""
    print("\nTesting component initialization...")
    
    try:
        from face_detection import FaceDetector
        detector = FaceDetector()
        print("✓ FaceDetector initialized")
    except Exception as e:
        print(f"✗ FaceDetector failed: {e}")
        traceback.print_exc()
        return False
    
    try:
        from stylization import FaceStylizer
        stylizer = FaceStylizer()
        print("✓ FaceStylizer initialized")
        if not stylizer.use_replicate and not stylizer.use_huggingface and stylizer.pipeline is None:
            print("  ⚠ No API configured - stylization will use basic enhancement")
            print("  Set REPLICATE_API_TOKEN for AI stylization")
    except Exception as e:
        print(f"✗ FaceStylizer failed: {e}")
        traceback.print_exc()
        return False
    
    try:
        from compositing import TemplateCompositor
        compositor = TemplateCompositor()
        print("✓ TemplateCompositor initialized")
    except Exception as e:
        print(f"✗ TemplateCompositor failed: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    try:
        from config import (
            FACE_CROP_SIZE,
            STYLIZATION_PROMPT,
            USE_REPLICATE,
            REPLICATE_API_TOKEN
        )
        print(f"✓ Config loaded")
        print(f"  Face crop size: {FACE_CROP_SIZE}")
        print(f"  Use Replicate: {USE_REPLICATE}")
        if REPLICATE_API_TOKEN:
            print(f"  Replicate token: {'*' * 20} (set)")
        else:
            print(f"  Replicate token: Not set")
    except Exception as e:
        print(f"✗ Config failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("PictoBook AI - Installation Test")
    print("=" * 50)
    
    all_passed = True
    
    if not test_imports():
        all_passed = False
        print("\n⚠ Some imports failed. Install missing packages with: pip install -r requirements.txt")
    
    if not test_config():
        all_passed = False
    
    if not test_components():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All tests passed! Installation looks good.")
    else:
        print("⚠ Some tests failed. Check errors above.")
    print("=" * 50)

