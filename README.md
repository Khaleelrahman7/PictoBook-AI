# PictoBook AI - Photo Personalization System

A complete working implementation that personalizes children's book illustrations by replacing template faces with stylized versions of uploaded photos.

## Architecture

```
[ Next.js UI ]  <--->  [ FastAPI Backend ]  <--->  [ ML Pipeline ]
     |                           |                               |
     |                           |---> Face detection (MTCNN)
     |                           |---> Face alignment & crop
     |                           |---> Stylization (SDXL/img2img)
     |                           |---> Composite into template
     |                           |---> Optional: Face restoration
     |                           |---> Return image
```

## Tech Stack

- **Frontend**: Next.js 14 (App Router), React
- **Backend**: FastAPI (Python)
- **Face Detection**: MTCNN (facenet-pytorch)
- **Stylization**: Stable Diffusion XL (img2img) via diffusers or Replicate API
- **Image Processing**: Pillow, OpenCV
- **Face Restoration**: GFPGAN (optional)

## Setup Instructions

### Prerequisites

- Python 3.9+ (Python 3.12+ recommended - uses updated package versions)
- Node.js 18+
- CUDA-capable GPU (recommended for local SDXL) or Replicate API key

**Note**: If using Python 3.12+, the requirements.txt has been updated with compatible package versions. For Python 3.11 or earlier, you may need to adjust version constraints.

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. **Configure API (Recommended - No huge downloads)**:
   - **NVIDIA NIM API (Default - Fast and reliable)**:
     - Set environment variable with your API key:
       ```bash
       # Windows PowerShell
       $env:NVIDIA_NIM_API_KEY="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"
       
       # Windows CMD
       set NVIDIA_NIM_API_KEY=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
       
       # Linux/Mac
       export NVIDIA_NIM_API_KEY="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"
       ```
   - **Alternative: Hugging Face API**:
     - Get token from https://huggingface.co/settings/tokens
     - Set: `USE_NVIDIA_NIM=false` and `HUGGINGFACE_API_TOKEN=your_token`
   - **Alternative: Replicate API**:
     - Get token from https://replicate.com/account/api-tokens
     - Set: `USE_NVIDIA_NIM=false` and `REPLICATE_API_TOKEN=your_token`
   - The system defaults to using NVIDIA NIM API (no local models needed)

5. **Optional: Local Models (Only if you want offline processing)**:
   - Requires GPU and ~10GB download
   - Install local dependencies: `pip install -r requirements-local.txt`
   - Set environment variable: `USE_LOCAL_SDXL=true`
   - Not recommended for most users

6. Run the backend:
```bash
python main.py
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Update backend URL in `frontend/app/page.jsx` if needed (default: `http://localhost:8000`)

4. Run development server:
```bash
npm run dev
```

Frontend will run on `http://localhost:3000`

## Usage

1. Start backend server
2. Start frontend server
3. Open browser to `http://localhost:3000`
4. Upload a photo with a clear face
5. Click "Personalize" and wait for processing
6. Download the result

## Project Structure

```
.
├── frontend/          # Next.js application
│   ├── app/
│   ├── public/
│   └── package.json
├── backend/           # FastAPI application
│   ├── main.py
│   ├── face_detection.py
│   ├── stylization.py
│   ├── compositing.py
│   ├── requirements.txt
│   └── templates/     # Book templates
└── README.md
```

## API Endpoints

- `POST /personalize` - Upload photo and get personalized result
  - Body: multipart/form-data with `photo` field
  - Response: JSON with `image_base64` field

## Configuration

Edit `backend/config.py` to adjust:
- Face crop size
- Stylization prompt
- Template selection
- Model settings

## Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel deploy
```

### Backend (GPU Server)
- Deploy to AWS EC2 (GPU instance), GCP, or Azure
- Or use serverless with Replicate API

## Quick Start (API-Based - No Huge Downloads!)

1. **Get NVIDIA NIM API Key** (Recommended - Fast and reliable):
   - Get your API key from NVIDIA (provided: `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`)
   - Set environment variable: `NVIDIA_NIM_API_KEY=your_key`
   
2. **Alternative: Hugging Face API**:
   - Get token from https://huggingface.co/settings/tokens (free tier available)
   - Set: `USE_NVIDIA_NIM=false` and `HUGGINGFACE_API_TOKEN=your_token`

3. Install backend: `cd backend && pip install -r requirements.txt && python main.py`

4. Install frontend: `cd frontend && npm install && npm run dev`

5. Open http://localhost:3000

**Note**: The system now defaults to using NVIDIA NIM API - no local model downloads needed!

See `SETUP.md` for detailed instructions.

## Notes

- First run downloads models (~7GB for SDXL locally) - only if using local SDXL
- Processing time: ~10-30 seconds per image (depends on GPU/API)
- Replicate API: ~$0.01-0.05 per image (check current pricing)
- For production, consider adding:
  - S3 storage for results
  - Queue system for async processing
  - Rate limiting
  - Authentication
  - Error handling and retries

