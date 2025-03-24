# BGM Creator Web

A web application for creating YouTube BGM videos with loop playback and frequency adjustment. This project aims to simplify the process of creating background music videos for YouTube content creators.

## Features

- Upload audio files and convert them to looped BGM videos
- Adjust frequency (Hz) of audio files
- Add fade-in and fade-out effects
- Add static images or GIF animations to videos
- Add motion effects to static images
- Generate videos of custom length (up to 30 minutes)
- Simple and intuitive user interface for casual creators

## Tech Stack

- Frontend: Next.js with TypeScript and Tailwind CSS
- Backend: Python with FastAPI
- Audio/Video Processing: FFmpeg
- Deployment: Docker containers for easy deployment

## Project Structure

```
/
├── frontend/          # Next.js frontend application
│   ├── components/    # Reusable UI components
│   ├── pages/         # Application pages
│   └── styles/        # Global styles
├── backend/           # Python FastAPI backend
│   ├── app/           # Main application code
│   ├── processors/    # Audio/video processing modules
│   └── assets/        # Default resources
└── docs/              # Documentation
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- FFmpeg
- Docker and Docker Compose (optional, for containerized setup)

### Development Setup

#### Option 1: Local Development

1. **Clone the repository**

```bash
git clone https://github.com/fumifumi0831/bgm-creator-web.git
cd bgm-creator-web
```

2. **Set up the frontend**

```bash
cd frontend
npm install
npm run dev
```

3. **Set up the backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. **Run the backend server**

```bash
uvicorn app.main:app --reload
```

5. **Access the application**

Open [http://localhost:3000](http://localhost:3000) in your web browser.

#### Option 2: Docker Setup

1. **Clone the repository**

```bash
git clone https://github.com/fumifumi0831/bgm-creator-web.git
cd bgm-creator-web
```

2. **Build and run with Docker Compose**

```bash
docker-compose up -d
```

3. **Access the application**

Open [http://localhost:3000](http://localhost:3000) in your web browser.

## Usage

1. **Create a BGM Video**
   - Upload an audio file (MP3, WAV, etc.)
   - Optionally upload an image or GIF
   - Set desired video length
   - Configure additional options (frequency adjustment, fade effects, motion)
   - Click "Create BGM Video"

2. **Download Your Video**
   - Once processing is complete, download your video
   - Upload to YouTube or use as needed

## Deployment

### Server Requirements

- 2 CPU cores minimum (4+ recommended for faster processing)
- 4GB RAM minimum (8GB+ recommended)
- FFmpeg installed
- Docker and Docker Compose (for containerized deployment)

### Production Deployment

1. **Clone the repository on your server**

```bash
git clone https://github.com/fumifumi0831/bgm-creator-web.git
cd bgm-creator-web
```

2. **Configure environment variables**

Create a `.env` file in the root directory:

```
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

3. **Deploy with Docker Compose**

```bash
docker-compose up -d
```

4. **Set up a reverse proxy (Nginx, etc.)**

Configure your reverse proxy to forward requests to the appropriate containers.

## License

MIT

## Acknowledgements

- FFmpeg for audio/video processing
- Next.js and FastAPI for the application framework
- All contributors and users of this project
