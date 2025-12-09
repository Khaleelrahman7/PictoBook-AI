# Quick Start with NVIDIA NIM API

## Setup in 2 Steps

### 1. Set NVIDIA NIM API Key

**Windows PowerShell:**
```powershell
$env:NVIDIA_NIM_API_KEY="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"
```

**Windows CMD:**
```cmd
set NVIDIA_NIM_API_KEY=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
```

**Linux/Mac:**
```bash
export NVIDIA_NIM_API_KEY="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"
```

### 2. Run the Application

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Frontend (in another terminal):**
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 and upload a photo!

## API Details

- **Endpoint**: `https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium`
- **Model**: Stable Diffusion 3 Medium
- **Fast**: NVIDIA NIM provides fast inference
- **Reliable**: Enterprise-grade API

## Troubleshooting

**"NVIDIA_NIM_API_KEY not set" error:**
- Make sure you set the environment variable before running the backend
- Restart the backend after setting the variable

**API errors:**
- Check your API key is correct
- Verify you have API access/credits
- Check your internet connection

## Alternative APIs

If NVIDIA NIM doesn't work, you can use:
- **Hugging Face**: Set `USE_NVIDIA_NIM=false` and `HUGGINGFACE_API_TOKEN=your_token`
- **Replicate**: Set `USE_NVIDIA_NIM=false` and `REPLICATE_API_TOKEN=your_token`

