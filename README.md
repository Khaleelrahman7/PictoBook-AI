# PictoBook AI - Photo Personalization System

Transform your photos into personalized children's book illustrations using AI.

🌐 **Live Demo**: [https://pictobookai.netlify.app](https://pictobookai.netlify.app)

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Deployment](#deployment)
- [Model Choice & Limitations](#model-choice--limitations)
- [Future Improvements](#future-improvements)

## 🎯 Overview

PictoBook AI is a full-stack application that:
1. Detects faces in uploaded photos
2. Transforms them into illustrated/cartoon style using AI
3. Composites the stylized face into a book template
4. Returns a personalized children's book page

## 🏗️ Architecture

See [ARCHITECTURE_DIAGRAM.md](./ARCHITECTURE_DIAGRAM.md) for detailed architecture diagram.

**High-Level Flow:**
```
User Upload → Frontend (Netlify) → Backend (Render) → Face Detection → 
AI Stylization (NVIDIA NIM) → Template Compositing → Return Result
```

## ✨ Features

- ✅ Face detection and alignment (MTCNN)
- ✅ AI-powered face stylization (Stable Diffusion 3)
- ✅ Template compositing with smooth blending
- ✅ Real-time processing feedback
- ✅ Download personalized results
- ✅ Responsive web interface

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** (App Router)
- **React 18**
- **Hosted on**: Netlify

### Backend
- **FastAPI** (Python)
- **Face Detection**: MTCNN (facenet-pytorch)
- **Stylization**: NVIDIA NIM API (Stable Diffusion 3 Medium)
- **Image Processing**: Pillow, OpenCV
- **Hosted on**: Render.com

### External Services
- **NVIDIA NIM API**: AI image generation
- **Alternatives**: Hugging Face API, Replicate API (configurable)

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- NVIDIA NIM API key (or alternative)

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
export NVIDIA_NIM_API_KEY="your_key_here"
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
export NEXT_PUBLIC_API_URL="http://localhost:8000"
npm run dev
```

Visit `http://localhost:3000`

## 📦 Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

**Quick Deploy:**
1. **Backend (Render)**: Connect GitHub repo, set env vars, deploy
2. **Frontend (Netlify)**: Connect GitHub repo, set `NEXT_PUBLIC_API_URL`, deploy

## 🎨 Model Choice & Limitations

See [MODEL_CHOICE_AND_LIMITATIONS.md](./MODEL_CHOICE_AND_LIMITATIONS.md) for detailed explanation.

### Model Choice: NVIDIA NIM API (SD3 Medium)

**Why:**
- Fast inference (~10-15 seconds)
- No infrastructure burden (no local models)
- High-quality results
- Simple API integration

**Limitations:**
- Uses text-to-image (not true img2img) - identity preservation varies
- Processing time: 15-30 seconds end-to-end
- API dependency (requires internet)
- Face detection may fail on edge cases (side profiles, poor lighting)

## 🔮 Future Improvements (v2)

See [MODEL_CHOICE_AND_LIMITATIONS.md](./MODEL_CHOICE_AND_LIMITATIONS.md#what-wed-improve-in-v2) for full roadmap.

**Priority Features:**
1. **True img2img** with ControlNet/Instant-ID for better identity preservation
2. **Async processing** with job queue (Celery + Redis)
3. **Multiple templates** with template selection UI
4. **Result storage** in S3 with shareable links
5. **Batch processing** for multiple photos
6. **Style presets** (cartoon, watercolor, sketch, etc.)

## 📁 Project Structure

```
.
├── frontend/          # Next.js application
│   ├── app/          # App Router pages
│   └── package.json
├── backend/           # FastAPI application
│   ├── main.py       # API endpoints
│   ├── face_detection.py
│   ├── stylization.py
│   ├── compositing.py
│   └── requirements.txt
├── ARCHITECTURE_DIAGRAM.md
├── MODEL_CHOICE_AND_LIMITATIONS.md
└── DEPLOYMENT.md
```

## 🔧 Configuration

### Environment Variables

**Backend (Render):**
```
NVIDIA_NIM_API_KEY=your_key
USE_NVIDIA_NIM=true
FRONTEND_URL=https://pictobookai.netlify.app
```

**Frontend (Netlify):**
```
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

## 📚 Documentation

- [Architecture Diagram](./ARCHITECTURE_DIAGRAM.md)
- [Model Choice & Limitations](./MODEL_CHOICE_AND_LIMITATIONS.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Quick Deployment](./DEPLOYMENT_QUICK.md)
- [Setup Guide](./SETUP.md)

## 🤝 Contributing

Contributions welcome! Please open an issue or pull request.

## 📄 License

MIT License

## 🙏 Acknowledgments

- NVIDIA for NIM API
- Stability AI for Stable Diffusion models
- FastAPI and Next.js communities

---

**Built with ❤️ for personalized storytelling**
