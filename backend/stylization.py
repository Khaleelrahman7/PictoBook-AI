"""Face stylization using APIs (Replicate/HuggingFace) - no local models needed"""

import os
import io
import base64
from PIL import Image
import requests
import json
from config import (
    STYLIZATION_PROMPT,
    NEGATIVE_PROMPT,
    STYLIZATION_STRENGTH,
    NUM_INFERENCE_STEPS,
    GUIDANCE_SCALE,
    USE_NVIDIA_NIM,
    NVIDIA_NIM_API_KEY,
    NVIDIA_NIM_MODEL,
    NVIDIA_NIM_BASE_URL,
    USE_REPLICATE,
    REPLICATE_API_TOKEN,
    USE_HUGGINGFACE,
    HUGGINGFACE_API_TOKEN,
    HUGGINGFACE_MODEL,
    HUGGINGFACE_PROVIDER,
    USE_LOCAL_SDXL
)

# Optional imports for local models (only if USE_LOCAL_SDXL is True)
try:
    import replicate
    REPLICATE_AVAILABLE = True
except ImportError:
    REPLICATE_AVAILABLE = False

# Check if diffusers is available (only import if needed)
DIFFUSERS_AVAILABLE = False
try:
    import torch
    from diffusers import StableDiffusionXLImg2ImgPipeline
    DIFFUSERS_AVAILABLE = True
except ImportError:
    # diffusers not installed - that's fine, we'll use API
    pass

# Import HuggingFace InferenceClient
try:
    from huggingface_hub import InferenceClient
    HF_CLIENT_AVAILABLE = True
except ImportError:
    HF_CLIENT_AVAILABLE = False
    InferenceClient = None
    print("Warning: huggingface_hub not installed. Install with: pip install huggingface_hub")

class FaceStylizer:
    def __init__(self):
        """Initialize stylization pipeline - defaults to NVIDIA NIM API"""
        # Priority: NVIDIA NIM > HuggingFace API > Replicate API > Local (if enabled) > Basic enhancement
        # Check NVIDIA NIM first (default and preferred)
        self.use_nvidia_nim = USE_NVIDIA_NIM and NVIDIA_NIM_API_KEY
        
        # Check Hugging Face if NVIDIA NIM is not available
        self.use_huggingface = False
        if not self.use_nvidia_nim and USE_HUGGINGFACE and HUGGINGFACE_API_TOKEN:
            self.use_huggingface = True
        
        # Only use Replicate if other APIs are not available AND Replicate is explicitly enabled
        self.use_replicate = False
        if not self.use_nvidia_nim and not self.use_huggingface and USE_REPLICATE and REPLICATE_AVAILABLE and REPLICATE_API_TOKEN:
            self.use_replicate = True
        
        self.pipeline = None
        
        # Only load local models if explicitly enabled AND no API is available
        if USE_LOCAL_SDXL and not self.use_nvidia_nim and not self.use_huggingface and not self.use_replicate:
            if DIFFUSERS_AVAILABLE:
                self._load_local_pipeline()
            else:
                print("Warning: Local SDXL requested but diffusers not available. Using API or basic enhancement.")
        
        # Print status
        if self.use_nvidia_nim:
            print(f"✓ Using NVIDIA NIM API for stylization (model: {NVIDIA_NIM_MODEL})")
        elif self.use_huggingface:
            print(f"✓ Using HuggingFace API for stylization (model: {HUGGINGFACE_MODEL})")
        elif self.use_replicate:
            print("✓ Using Replicate API for stylization (no local models needed)")
        elif self.pipeline is not None:
            print("✓ Using local SDXL model (large download required)")
        else:
            print("⚠ No API configured. Using basic enhancement.")
            if not NVIDIA_NIM_API_KEY:
                print("  Set NVIDIA_NIM_API_KEY for AI stylization (recommended)")
            if not HUGGINGFACE_API_TOKEN:
                print("  Or set HUGGINGFACE_API_TOKEN as alternative")
            if not REPLICATE_API_TOKEN:
                print("  Or set REPLICATE_API_TOKEN as alternative")
    
    def _load_local_pipeline(self):
        """Load local SDXL img2img pipeline"""
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            dtype = torch.float16 if device == "cuda" else torch.float32
            
            print(f"Loading SDXL pipeline on {device}...")
            self.pipeline = StableDiffusionXLImg2ImgPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=dtype,
                variant="fp16" if dtype == torch.float16 else None
            )
            self.pipeline = self.pipeline.to(device)
            self.pipeline.enable_attention_slicing()  # Reduce memory usage
            
            if device == "cpu":
                print("Warning: Running on CPU. This will be very slow. Consider using Replicate API.")
            
            print("SDXL pipeline loaded successfully")
        except Exception as e:
            print(f"Failed to load local SDXL: {e}")
            print("Falling back to Replicate API or basic stylization")
            self.use_replicate = True
    
    def stylize_face(self, face_image, prompt=None, negative_prompt=None):
        """
        Stylize a face image using API (preferred) or local model
        
        Args:
            face_image: PIL Image of face
            prompt: Custom prompt (uses default if None)
            negative_prompt: Custom negative prompt (uses default if None)
            
        Returns:
            stylized_face: PIL Image
        """
        if prompt is None:
            prompt = STYLIZATION_PROMPT
        if negative_prompt is None:
            negative_prompt = NEGATIVE_PROMPT
        
        # Try APIs first (no local models needed) - NVIDIA NIM has priority
        if self.use_nvidia_nim:
            return self._stylize_with_nvidia_nim(face_image, prompt, negative_prompt)
        elif self.use_huggingface:
            return self._stylize_with_huggingface(face_image, prompt, negative_prompt)
        elif self.use_replicate:
            return self._stylize_with_replicate(face_image, prompt, negative_prompt)
        elif self.pipeline is not None:
            return self._stylize_local(face_image, prompt, negative_prompt)
        else:
            # Fallback: basic enhancement (no actual AI stylization)
            print("Warning: No stylization API/model available. Using basic enhancement.")
            print("To enable AI stylization, set NVIDIA_NIM_API_KEY environment variable.")
            return self._basic_enhancement(face_image)
    
    def _stylize_local(self, face_image, prompt, negative_prompt):
        """Stylize using local SDXL pipeline (only if explicitly enabled)"""
        if not DIFFUSERS_AVAILABLE or self.pipeline is None:
            raise ValueError("Local SDXL not available. Use API instead.")
        
        try:
            # Ensure image is RGB and right size
            if face_image.mode != "RGB":
                face_image = face_image.convert("RGB")
            
            # Resize to 1024x1024 for SDXL (optimal size)
            face_image = face_image.resize((1024, 1024), Image.LANCZOS)
            
            # Generate
            result = self.pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt,
                image=face_image,
                strength=STYLIZATION_STRENGTH,
                num_inference_steps=NUM_INFERENCE_STEPS,
                guidance_scale=GUIDANCE_SCALE,
            )
            
            stylized = result.images[0]
            return stylized
            
        except Exception as e:
            print(f"Error in local stylization: {e}")
            raise
    
    def _stylize_with_nvidia_nim(self, face_image, prompt, negative_prompt):
        """Stylize using NVIDIA NIM API"""
        try:
            if not NVIDIA_NIM_API_KEY:
                raise ValueError("NVIDIA_NIM_API_KEY not set")
            
            # Construct the API URL
            invoke_url = f"{NVIDIA_NIM_BASE_URL}/{NVIDIA_NIM_MODEL}"
            
            headers = {
                "Authorization": f"Bearer {NVIDIA_NIM_API_KEY}",
                "Accept": "application/json",
            }
            
            # Prepare payload based on user's example
            payload = {
                "prompt": prompt,
                "cfg_scale": int(GUIDANCE_SCALE),
                "seed": 0,  # Can be randomized for variety
                "steps": NUM_INFERENCE_STEPS,
                "negative_prompt": negative_prompt if negative_prompt else ""
            }
            
            # Make API request
            print(f"Calling NVIDIA NIM API: {invoke_url}")
            print(f"Prompt: {prompt[:80]}...")
            
            response = requests.post(
                invoke_url,
                headers=headers,
                json=payload,
                timeout=120
            )
            
            response.raise_for_status()
            response_body = response.json()
            
            # Extract image from response
            # NVIDIA NIM API typically returns base64 encoded image
            if "image" in response_body:
                image_b64 = response_body["image"]
            elif "b64_json" in response_body:
                image_b64 = response_body["b64_json"]
            elif "data" in response_body and len(response_body["data"]) > 0:
                # Some formats return array with image data
                image_data = response_body["data"][0]
                if "b64_json" in image_data:
                    image_b64 = image_data["b64_json"]
                elif "image" in image_data:
                    image_b64 = image_data["image"]
                else:
                    raise ValueError(f"Unexpected response format: {response_body.keys()}")
            else:
                # Try to find base64 string in response
                raise ValueError(f"Could not find image in response. Response keys: {response_body.keys()}")
            
            # Decode base64 image
            # Handle data URL format if present
            if image_b64.startswith("data:image"):
                image_b64 = image_b64.split(",")[1]
            
            image_bytes = base64.b64decode(image_b64)
            stylized = Image.open(io.BytesIO(image_bytes))
            
            # Resize to match input face size for compositing
            stylized = stylized.resize(face_image.size, Image.LANCZOS)
            
            return stylized
            
        except requests.exceptions.RequestException as e:
            print(f"Error in NVIDIA NIM API request: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"API response: {error_detail}")
                except:
                    print(f"API response: {e.response.text}")
            import traceback
            traceback.print_exc()
            return self._basic_enhancement(face_image)
        except Exception as e:
            print(f"Error in NVIDIA NIM stylization: {e}")
            import traceback
            traceback.print_exc()
            return self._basic_enhancement(face_image)
    
    def _stylize_with_huggingface(self, face_image, prompt, negative_prompt):
        """Stylize using HuggingFace InferenceClient"""
        try:
            if not HUGGINGFACE_API_TOKEN:
                raise ValueError("HUGGINGFACE_API_TOKEN not set")
            
            if not HF_CLIENT_AVAILABLE:
                raise ValueError("huggingface_hub not installed. Install with: pip install huggingface_hub")
            
            # Initialize InferenceClient
            # Using provider from config (default: fal-ai for better performance)
            try:
                if HUGGINGFACE_PROVIDER and HUGGINGFACE_PROVIDER.lower() != "none":
                    client = InferenceClient(
                        provider=HUGGINGFACE_PROVIDER,
                        api_key=HUGGINGFACE_API_TOKEN,
                    )
                    print(f"Using {HUGGINGFACE_PROVIDER} provider for faster inference")
                else:
                    client = InferenceClient(
                        token=HUGGINGFACE_API_TOKEN,
                    )
                    print("Using standard HF inference")
            except Exception as e:
                # Fallback to standard HF inference if provider fails
                print(f"Note: Using standard HF inference (provider failed: {e})")
                client = InferenceClient(
                    token=HUGGINGFACE_API_TOKEN,
                )
            
            # For face stylization, we'll use text_to_image with a detailed prompt
            # The prompt describes the desired illustration style
            # Note: This generates a stylized image based on the prompt
            # The face features will be approximated based on the style description
            enhanced_prompt = f"{prompt}"
            
            print(f"Generating stylized image with model: {HUGGINGFACE_MODEL}")
            print(f"Prompt: {enhanced_prompt[:80]}...")
            
            # Generate stylized image using text_to_image
            stylized = client.text_to_image(
                prompt=enhanced_prompt,
                model=HUGGINGFACE_MODEL,
            )
            
            # Handle different return types
            if isinstance(stylized, Image.Image):
                # Resize to match input face size for compositing
                stylized = stylized.resize(face_image.size, Image.LANCZOS)
                return stylized
            elif isinstance(stylized, bytes):
                # If it's bytes, convert to PIL Image
                stylized = Image.open(io.BytesIO(stylized))
                stylized = stylized.resize(face_image.size, Image.LANCZOS)
                return stylized
            else:
                raise ValueError(f"Unexpected return type from InferenceClient: {type(stylized)}")
                    
        except Exception as e:
            print(f"Error in HuggingFace stylization: {e}")
            import traceback
            traceback.print_exc()
            return self._basic_enhancement(face_image)
    
    def _stylize_with_replicate(self, face_image, prompt, negative_prompt):
        """Stylize using Replicate API"""
        try:
            if not REPLICATE_API_TOKEN:
                raise ValueError("REPLICATE_API_TOKEN not set")
            
            # Set API token
            os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
            
            # Save image to temporary file (Replicate works better with file paths)
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
                face_image.save(tmp_file.name, format="PNG")
                tmp_path = tmp_file.name
            
            try:
                # Use Replicate's SDXL img2img model
                # Note: Using a more recent/stable model version
                output = replicate.run(
                    "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                    input={
                        "prompt": prompt,
                        "negative_prompt": negative_prompt,
                        "image": open(tmp_path, "rb"),
                        "strength": STYLIZATION_STRENGTH,
                        "num_inference_steps": NUM_INFERENCE_STEPS,
                        "guidance_scale": GUIDANCE_SCALE,
                    }
                )
                
                # Download result
                if isinstance(output, list):
                    output_url = output[0]
                else:
                    output_url = output
                
                response = requests.get(output_url, timeout=120)
                response.raise_for_status()
                stylized = Image.open(io.BytesIO(response.content))
                return stylized
            finally:
                # Clean up temp file
                try:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                except:
                    pass
            
        except Exception as e:
            print(f"Error in Replicate stylization: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to basic enhancement
            return self._basic_enhancement(face_image)
    
    def _basic_enhancement(self, face_image):
        """Basic image enhancement as fallback"""
        from PIL import ImageEnhance
        
        # Simple enhancement - increase saturation and contrast slightly
        enhancer = ImageEnhance.Color(face_image)
        face_image = enhancer.enhance(1.2)
        
        enhancer = ImageEnhance.Contrast(face_image)
        face_image = enhancer.enhance(1.1)
        
        return face_image

