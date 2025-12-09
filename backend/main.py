"""FastAPI backend for photo personalization"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from PIL import Image
import io
import base64
import os
import traceback

from face_detection import FaceDetector
from stylization import FaceStylizer
from compositing import TemplateCompositor
from face_restoration import FaceRestorer
from config import OUTPUT_FORMAT, OUTPUT_QUALITY

app = FastAPI(title="PictoBook AI Personalization API")

# CORS middleware - Allow production frontend domains
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://pictobook-ai.netlify.app",  # Update with your Netlify domain
]

# Add environment variable for custom frontend URL
if os.getenv("FRONTEND_URL"):
    allowed_origins.append(os.getenv("FRONTEND_URL"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
face_detector = FaceDetector()
stylizer = FaceStylizer()
compositor = TemplateCompositor()
restorer = FaceRestorer()

@app.get("/")
async def root():
    return {"message": "PictoBook AI Personalization API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/personalize")
async def personalize(photo: UploadFile = File(...)):
    """
    Personalize a photo by detecting face, stylizing, and compositing into template
    
    Args:
        photo: Uploaded image file
        
    Returns:
        JSON with base64 encoded result image
    """
    try:
        # Read uploaded image
        contents = await photo.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
        
        print(f"Processing image: {photo.filename}, size: {img.size}")
        
        # Step 1: Detect and align face
        print("Step 1: Detecting face...")
        face_img, bbox, landmarks = face_detector.detect_and_align(img)
        print(f"Face detected at: {bbox}")
        
        # Step 2: Stylize face
        print("Step 2: Stylizing face...")
        stylized_face = stylizer.stylize_face(face_img)
        print("Stylization complete")
        
        # Step 3: Optional face restoration
        if restorer.use_restoration:
            print("Step 3: Restoring face...")
            stylized_face = restorer.restore(stylized_face)
            print("Face restoration complete")
        
        # Step 4: Composite into template
        print("Step 4: Compositing into template...")
        final_image = compositor.composite(stylized_face, bbox)
        print("Compositing complete")
        
        # Step 5: Convert to base64
        buf = io.BytesIO()
        if OUTPUT_FORMAT == "PNG":
            final_image.save(buf, format="PNG")
        else:
            final_image.save(buf, format="JPEG", quality=OUTPUT_QUALITY)
        
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        
        print("Processing complete!")
        
        return JSONResponse({
            "status": "success",
            "image_base64": b64,
            "format": OUTPUT_FORMAT.lower()
        })
        
    except ValueError as e:
        # Face detection error
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Other errors
        error_msg = str(e)
        print(f"Error: {error_msg}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Processing error: {error_msg}")

if __name__ == "__main__":
    # Create templates directory if it doesn't exist
    os.makedirs("templates", exist_ok=True)
    
    # Get port from environment (Render sets this automatically)
    port = int(os.getenv("PORT", 8000))
    
    print("Starting PictoBook AI Backend...")
    print("=" * 50)
    print(f"Backend will be available at: http://0.0.0.0:{port}")
    print(f"API docs at: http://0.0.0.0:{port}/docs")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

