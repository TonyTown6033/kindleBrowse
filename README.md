# Kindle Online Book Server

This is a simple web application to upload books from your computer and download them on your Kindle.

## Features
- **Backend**: FastAPI (Python)
- **Frontend**: Vue 3 (Clean, E-ink friendly design)
- **Storage**: Local `uploads/` directory
- **Design**: Optimized for Kindle browser

## Deployment with Docker (Recommended)

1. **Install Docker and Docker Compose** on your server.
2. **Clone or copy this project** to your server.
3. **Run the container**:
   ```bash
   docker-compose up -d
   ```
4. **Access the app**:
   Open `http://<YOUR_SERVER_IP>:8000` on your Kindle or browser.

   Uploaded books will be persisted in the local `uploads/` directory.

## Local Development (Without Docker)

### 1. Backend
```bash
pip install -r requirements.txt
python main.py
```

### 2. Frontend
```bash
cd vue-project
npm install
npm run dev
```

## How to use on Kindle
1. Ensure your Kindle is connected to the internet.
2. Open the Experimental Browser on your Kindle.
3. Type `http://<YOUR_SERVER_IP>:8000` in the address bar.
4. Tap "Tap to Upload New Book" or click "Download" on existing books.
