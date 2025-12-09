# Quick Start Guide

## Get Started in 3 Steps

### 1. Get Hugging Face API Token (Free!)

1. Go to https://huggingface.co and sign up (free account)
2. Go to https://huggingface.co/settings/tokens
3. Click "New token"
4. Name it (e.g., "pictobook-ai")
5. Select "Read" permissions
6. Click "Generate token"
7. Copy the token (starts with `hf_...`)

### 2. Set Environment Variable

**Windows PowerShell:**
```powershell
$env:HUGGINGFACE_API_TOKEN="hf_your_token_here"
```

**Windows CMD:**
```cmd
set HUGGINGFACE_API_TOKEN=hf_your_token_here
```

**Linux/Mac:**
```bash
export HUGGINGFACE_API_TOKEN="hf_your_token_here"
```

### 3. Run the Application

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

## Troubleshooting

**"No API configured" error:**
- Make sure you set `HUGGINGFACE_API_TOKEN` environment variable
- Restart the backend after setting the variable

**"Model is loading" message:**
- Hugging Face models load on first use
- Wait 10-20 seconds and try again
- This only happens the first time

**API errors:**
- Check your token is correct
- Make sure token has "Read" permissions
- Check your internet connection

## Alternative: Use Replicate

If you prefer Replicate:
```bash
export USE_REPLICATE="true"
export USE_HUGGINGFACE="false"
export REPLICATE_API_TOKEN="your_replicate_token"
```

