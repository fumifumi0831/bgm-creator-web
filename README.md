# BGM Creator Web

A web application for creating YouTube BGM videos with loop playback and frequency adjustment.

## Features

- Upload audio files and convert them to looped BGM videos
- Adjust frequency (Hz) of audio files
- Add fade-in and fade-out effects
- Add static images or GIF animations to videos
- Generate videos of custom length (up to 30 minutes)
- Simple and intuitive user interface for casual creators

## Tech Stack

- Frontend: Next.js
- Backend: Python with FastAPI
- Audio/Video Processing: FFmpeg
- Deployment: Vercel (Frontend) and Python backend service

## Project Structure

```
/
├── frontend/          # Next.js frontend application
├── backend/           # Python FastAPI backend
│   ├── app/           # Main application code
│   ├── processors/    # Audio/video processing modules
│   └── tests/         # Backend tests
└── docs/              # Documentation
```

## Development

### Prerequisites

- Node.js 18+
- Python 3.9+
- FFmpeg

### Getting Started

Instructions for setup and development will be added soon.

## License

MIT
