from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os
import uuid
import shutil
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import asyncio

# Import processors
from processors.audio_processor import AudioProcessor
from processors.video_processor import VideoProcessor

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

# Create directories
os.makedirs("./temp/uploads", exist_ok=True)
os.makedirs("./temp/outputs", exist_ok=True)
os.makedirs("./temp/jobs", exist_ok=True)

# In-memory job storage (in production, use a database or Redis)
jobs = {}

@app.get("/")
def read_root():
    return {"message": "BGM Creator API is running"}

async def process_job(job_id: str, audio_path: str, image_path: Optional[str], 
               duration: int, frequency: Optional[float], 
               fade_in: int, fade_out: int, add_motion: bool,
               audio_profile: str, apply_frequency_optimization: bool):
    """
    Background task to process audio and video
    """
    try:
        # Update job status
        update_job_status(job_id, "processing", 10, "Processing audio...")
        
        # Step 1: Process audio
        output_dir = "./temp/outputs"
        processed_audio = AudioProcessor.process_audio(
            audio_path, output_dir, duration, frequency, fade_in, fade_out,
            profile=audio_profile, apply_frequency_optimization=apply_frequency_optimization
        )
        
        update_job_status(job_id, "processing", 50, "Creating video...")
        
        # Step 2: Create video
        motion_type = "zoom"
        if image_path:
            video_file = VideoProcessor.process_video(
                processed_audio, image_path, output_dir, duration, add_motion, motion_type
            )
        else:
            # If no image provided, use a default image or create a placeholder
            default_image = "./assets/default_background.jpg"
            video_file = VideoProcessor.process_video(
                processed_audio, default_image, output_dir, duration, add_motion, motion_type
            )
        
        # Step 3: Finalize job
        file_id = os.path.basename(video_file).split('.')[0]
        update_job_status(job_id, "completed", 100, "Video ready", file_id=file_id)
        
        # Clean up the processed audio file
        if os.path.exists(processed_audio):
            os.remove(processed_audio)
            
    except Exception as e:
        # Update job status with error
        update_job_status(job_id, "failed", 0, f"Error: {str(e)}")
        
        # Clean up files on error
        for file_path in [audio_path, image_path, processed_audio]:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

def update_job_status(job_id: str, status: str, progress: int, message: str, file_id: str = None):
    """
    Update job status in memory and on disk
    """
    job_info = {
        "status": status,
        "progress": progress,
        "message": message,
        "updated_at": datetime.now().isoformat(),
        "file_id": file_id
    }
    
    # Update in-memory job status
    jobs[job_id] = job_info
    
    # Write to disk for persistence
    job_file = os.path.join("./temp/jobs", f"{job_id}.json")
    with open(job_file, 'w') as f:
        json.dump(job_info, f)

@app.post("/api/process")
async def process_files(background_tasks: BackgroundTasks,
                       audio_file: UploadFile = File(...),
                       image_file: Optional[UploadFile] = File(None),
                       duration: int = Form(...),  # Duration in seconds
                       frequency: Optional[float] = Form(None),  # Hz adjustment
                       fade_in: Optional[int] = Form(0),  # Fade in duration in seconds
                       fade_out: Optional[int] = Form(0),  # Fade out duration in seconds
                       add_motion: bool = Form(False),  # Whether to add motion to static images
                       audio_profile: str = Form("default"),  # Audio optimization profile
                       apply_frequency_optimization: bool = Form(True)  # Whether to apply frequency optimization
                       ):
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Save uploaded files
    upload_dir = "./temp/uploads"
    audio_path = os.path.join(upload_dir, f"{job_id}_{audio_file.filename}")
    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(audio_file.file, buffer)
    
    image_path = None
    if image_file:
        image_path = os.path.join(upload_dir, f"{job_id}_{image_file.filename}")
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)
    
    # Initialize job status
    update_job_status(job_id, "pending", 0, "Job queued, waiting to start...")
    
    # Start processing in background
    background_tasks.add_task(
        process_job, job_id, audio_path, image_path, duration, frequency, 
        fade_in, fade_out, add_motion, audio_profile, apply_frequency_optimization
    )
    
    return {"job_id": job_id, "message": "Processing started"}

@app.get("/api/status/{job_id}")
def get_job_status(job_id: str):
    # Check in-memory cache first
    if job_id in jobs:
        return jobs[job_id]
    
    # Try to read from disk
    job_file = os.path.join("./temp/jobs", f"{job_id}.json")
    if os.path.exists(job_file):
        with open(job_file, 'r') as f:
            try:
                return json.load(f)
            except:
                pass
    
    # Return not found if job doesn't exist
    raise HTTPException(status_code=404, detail="Job not found")

@app.get("/api/download/{file_id}")
def download_file(file_id: str):
    # Construct file path
    file_path = f"./temp/outputs/{file_id}.mp4"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
        
    return FileResponse(
        file_path,
        media_type="video/mp4",
        filename=f"bgm_{file_id}.mp4"
    )

@app.get("/api/profiles")
def get_audio_profiles():
    """
    Get available audio optimization profiles
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return {
                    "profiles": list(config.get("profiles", {}).keys())
                }
        except Exception as e:
            return {"profiles": ["default"]}
    
    return {"profiles": ["default"]}

# Cleanup task
@app.on_event("startup")
async def setup_periodic_cleanup():
    asyncio.create_task(periodic_cleanup())

async def periodic_cleanup():
    """
    Periodically clean up old files
    """
    while True:
        # Clean up files older than 24 hours
        cleanup_old_files("./temp/uploads", hours=24)
        cleanup_old_files("./temp/outputs", hours=24)
        cleanup_old_files("./temp/jobs", hours=24)
        
        # Wait for 1 hour
        await asyncio.sleep(3600)

def cleanup_old_files(directory: str, hours: int = 24):
    """
    Delete files older than specified hours
    """
    now = datetime.now()
    cutoff = now - timedelta(hours=hours)
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_modified < cutoff:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")
