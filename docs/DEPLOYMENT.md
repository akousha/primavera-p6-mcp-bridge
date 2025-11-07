# Deployment Guide

## 🚀 Railway Deployment (Recommended)

### Option 1: Deploy from GitHub

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Clean P6 MCP Server"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy to Railway:**
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub account
   - Create new project → Deploy from GitHub repo
   - Select your repository
   - Railway will auto-detect and deploy

3. **Configure Environment Variables:**
   - In Railway dashboard → Variables tab
   - Add: `P6_BASE_URL=https://ca1.p6.oraclecloud.com/metrolinx/p6ws/restapi`

### Option 2: Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link  # Link to existing project or create new
railway up    # Deploy
```

## 🐳 Docker Deployment

### Build and Run Locally
```bash
docker build -f docker/Dockerfile -t p6-mcp-server .
docker run -p 8000:8000 -e P6_BASE_URL="https://ca1.p6.oraclecloud.com/metrolinx/p6ws/restapi" p6-mcp-server
```

### Docker Compose
```bash
cd docker/
docker-compose up --build
```

## ☁️ Other Cloud Platforms

### Heroku
```bash
# Install Heroku CLI and login
heroku create your-app-name
git push heroku main
heroku config:set P6_BASE_URL="https://ca1.p6.oraclecloud.com/metrolinx/p6ws/restapi"
```

### Google Cloud Run
```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/YOUR-PROJECT/p6-mcp-server
gcloud run deploy --image gcr.io/YOUR-PROJECT/p6-mcp-server --platform managed
```

### AWS Lambda (with Mangum)
Add to requirements.txt: `mangum`
Create `lambda_handler.py`:
```python
from mangum import Mangum
from src.main import app
handler = Mangum(app)
```

## 🔧 Environment Variables

Set these on your deployment platform:

| Variable | Value | Description |
|----------|-------|-------------|
| `P6_BASE_URL` | `https://ca1.p6.oraclecloud.com/metrolinx/p6ws/restapi` | P6 API base URL |
| `PORT` | `8000` | Server port (auto-set by most platforms) |

## ✅ Verify Deployment

After deployment, test these endpoints:

1. **Health Check:** `GET https://your-domain.com/health`
2. **MCP Manifest:** `GET https://your-domain.com/.well-known/mcp.json`
3. **Tool Schema:** `GET https://your-domain.com/tool_schema.json`

## 🧪 Testing Deployed Server

```bash
# Replace YOUR_DOMAIN with actual domain
curl https://YOUR_DOMAIN.com/health
curl https://YOUR_DOMAIN.com/.well-known/mcp.json
```

## 📱 MCP Client Configuration

Once deployed, use this URL in ChatGPT/Claude MCP settings:
```
https://YOUR_DOMAIN.com/.well-known/mcp.json
```