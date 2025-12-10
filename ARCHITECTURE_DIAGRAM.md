# PictoBook AI - Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                              │
│                    (Netlify - Frontend)                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Next.js React App                                       │   │
│  │  - Upload Photo UI                                       │   │
│  │  - Preview & Download                                    │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────────┘
                        │ HTTPS POST /personalize
                        │ (multipart/form-data)
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RENDER.COM (Backend)                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  FastAPI Application                                     │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │  1. Face Detection (MTCNN)                        │   │   │
│  │  │     - Detect face in uploaded image               │   │   │
│  │  │     - Align eyes                                  │   │   │
│  │  │     - Crop face region (768x768)                  │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │  2. Face Stylization (NVIDIA NIM API)            │   │   │
│  │  │     - Call NVIDIA NIM API                        │   │   │
│  │  │     - Model: Stable Diffusion 3 Medium           │   │   │
│  │  │     - Transform to illustration style            │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │  3. Template Compositing (Pillow)                 │   │   │
│  │  │     - Load book template                         │   │   │
│  │  │     - Blend stylized face into template          │   │   │
│  │  │     - Apply feathered edges                      │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │  4. Return Result                                 │   │   │
│  │  │     - Encode as base64                           │   │   │
│  │  │     - Return JSON response                        │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        │ API Call
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              NVIDIA NIM API (External Service)                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Stable Diffusion 3 Medium                               │   │
│  │  - Text-to-Image Generation                              │   │
│  │  - Illustration Style Transformation                     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

Data Flow:
1. User uploads photo → Frontend (Netlify)
2. Frontend sends to → Backend (Render)
3. Backend processes:
   a. Face Detection (MTCNN)
   b. Face Stylization (NVIDIA NIM API)
   c. Template Compositing
4. Backend returns base64 image → Frontend
5. Frontend displays result → User downloads
```

## Component Details

### Frontend (Next.js on Netlify)
- **Technology**: Next.js 14 (App Router), React 18
- **Hosting**: Netlify (static hosting with serverless functions)
- **Features**: File upload, preview, result display, download

### Backend (FastAPI on Render)
- **Technology**: FastAPI, Python 3.12
- **Hosting**: Render.com (web service)
- **Components**:
  - Face Detection: MTCNN (facenet-pytorch)
  - Stylization: NVIDIA NIM API (SD3 Medium)
  - Compositing: Pillow, OpenCV

### External Services
- **NVIDIA NIM API**: Stable Diffusion 3 Medium for image stylization
- **Alternative APIs**: Hugging Face, Replicate (configurable)

## Request/Response Flow

```
POST /personalize
Content-Type: multipart/form-data
Body: { photo: <image file> }

Response:
{
  "status": "success",
  "image_base64": "<base64 encoded PNG>",
  "format": "png"
}
```

## Deployment Architecture

```
GitHub Repository
    │
    ├─── Frontend (Netlify)
    │    └─── Auto-deploy on push
    │
    └─── Backend (Render)
         └─── Auto-deploy on push
```

