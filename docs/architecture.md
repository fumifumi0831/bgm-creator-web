# BGM Creator Web - Architecture

## System Overview

The BGM Creator Web application consists of two main components:

1. **Frontend**: A Next.js application that provides the user interface for uploading audio, configuring settings, and downloading the final video.

2. **Backend**: A Python FastAPI service that handles the processing of audio files, including:
   - Audio looping and extension
   - Frequency (Hz) adjustment
   - Fade effects
   - Combining with images/GIFs
   - Video generation

## Data Flow

1. User uploads audio file and image(s) via the frontend
2. Files are sent to the backend for processing
3. Backend processes the files using FFmpeg and returns a video file
4. User can preview and download the final video

## API Endpoints

- `POST /api/process`: Process audio and image files to create a video
- `GET /api/status/{job_id}`: Check the status of a processing job
- `GET /api/download/{file_id}`: Download a processed video file

## Infrastructure

- Frontend: Deployed on Vercel
- Backend: Python service with FFmpeg, deployed on a suitable server/cloud service
- Storage: Temporary storage for processing, with automatic cleanup

## Security Considerations

- File validation to prevent malicious uploads
- Rate limiting to prevent abuse
- Authentication for paid tier features
