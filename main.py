import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

# CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/api/books")
async def list_books():
    books = []
    # Ensure uploads directory exists
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
        
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.isfile(file_path) and not filename.startswith('.'):
            size = os.path.getsize(file_path)
            books.append({
                "name": filename,
                "size": size,
                "url": f"/api/download/{filename}"
            })
    return books

@app.post("/api/upload")
async def upload_book(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"filename": file.filename, "message": "Upload successful"}

@app.get("/api/download/{filename}")
async def download_book(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

# Serve frontend if built
dist_path = os.path.join(os.path.dirname(__file__), "vue-project/dist")
if os.path.exists(dist_path):
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
