# Deployment Guide

## Local Development

### Windows (PowerShell)

```powershell
# Install dependencies
pip install -r requirements.txt
npm install

# Terminal 1: Start Backend
python app.py

# Terminal 2: Start Frontend
npm start
```

### macOS/Linux (Bash)

```bash
# Install dependencies
pip install -r requirements.txt
npm install

# Terminal 1: Start Backend
python app.py

# Terminal 2: Start Frontend
npm start
```

## Docker Deployment (Optional)

Create a `Dockerfile` for containerized deployment:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js
RUN apt-get update && apt-get install -y nodejs npm
RUN npm install -g serve

# Copy project files
COPY . .

# Install frontend dependencies
RUN npm install
RUN npm run build

# Expose ports
EXPOSE 5000 3000

# Start both servers
CMD ["sh", "-c", "python app.py & serve -s build -l 3000"]
```

Build and run:
```bash
docker build -t bankruptcy-predictor .
docker run -p 5000:5000 -p 3000:3000 bankruptcy-predictor
```

## Environment Variables

Create a `.env` file (optional):

```env
FLASK_ENV=production
FLASK_DEBUG=0
REACT_APP_API_URL=http://localhost:5000
```

Update `App.js` to use:
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

## Production Checklist

- [ ] Model trained and `model.pkl` exists
- [ ] All dependencies installed
- [ ] CORS properly configured in `app.py`
- [ ] Environment variables set
- [ ] Frontend optimized build created (`npm run build`)
- [ ] Backend running with production server (Gunicorn)
- [ ] HTTPS enabled (if deploying online)
- [ ] Error logging configured
- [ ] Rate limiting added (optional)

## Performance Optimization

### Backend
```bash
pip install gunicorn gevent
gunicorn --worker-class gevent --workers 4 app:app
```

### Frontend
```bash
npm run build
# Serve the build/ folder with a CDN or static server
```

## Monitoring & Maintenance

### Check Backend Health
```bash
curl http://localhost:5000/api/health
```

### Monitor Logs
```bash
# Flask logs will show in terminal
# React dev server shows compile status
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
npm update
```
