from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import uuid
import shutil
from typing import Optional

app = FastAPI(title="BGM Creator API")

# Configure CORS
origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    # Add your production frontend URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temporary directories
os.makedirs("./temp/uploads", exist_ok=True)
os.makedirs("./temp/outputs", exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "BGM Creator API is running"}

@app.post("/api/process")
async def process_files(
    audio_file: UploadFile = File(...),
    image_file: Optional[UploadFile] = File(None),
    duration: int = Form(...),  # Duration in seconds
    frequency: Optional[float] = Form(None),  # Hz adjustment
    fade_in: Optional[int] = Form(0),  # Fade in duration in seconds
    fade_out: Optional[int] = Form(0),  # Fade out duration in seconds
):
    job_id = str(uuid.uuid4())
    
    # TODO: Save uploaded files
    # TODO: Process audio and create video
    # TODO: Return job ID for status checking
    
    return {"job_id": job_id, "message": "Processing started"}

@app.get("/api/status/{job_id}")
def get_job_status(job_id: str):
    # TODO: Implement job status checking
    return {"status": "pending", "progress": 0}

@app.get("/api/download/{file_id}")
def download_file(file_id: str):
    # TODO: Implement file download
    file_path = f"./temp/outputs/{file_id}.mp4"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
        
    return FileResponse(
        file_path,
        media_type="video/mp4",
        filename=f"bgm_{file_id}.mp4"
    )
