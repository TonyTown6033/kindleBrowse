# Kindle Online Book Server

This is a simple web application to upload books from your computer and download them on your Kindle.

## Features
- **Backend**: FastAPI (Python)
- **Frontend**: Vue 3
- **Storage**: Local `uploads/` directory
- **Design**: E-ink friendly (High contrast, simple layout)

## Setup

### 1. Backend
Install dependencies:
```bash
pip install -r requirements.txt
```

Run the server:
```bash
python main.py
```
The server will run on `http://0.0.0.0:8000`.

### 2. Frontend (Development)
In a new terminal:
```bash
cd vue-project
npm install
npm run dev
```
Access at `http://localhost:5173`.

### 3. Build for Production (Recommended for Kindle)
Build the frontend so the Python server can serve it directly:

```bash
cd vue-project
npm install
npm run build
```

After building, restart the Python server. You can now access the app at `http://<YOUR_COMPUTER_IP>:8000` from your Kindle.

## How to use on Kindle
1. Find your computer's local IP address (e.g., `192.168.1.5`).
2. Run the backend server (`python main.py`).
3. Open the Experimental Browser on your Kindle.
4. Type `http://192.168.1.5:8000` in the address bar.
5. Download your uploaded books.

