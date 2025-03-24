# BGM Creator Web - Backend

This is the backend service for the BGM Creator Web application, handling audio processing and video generation.

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000
