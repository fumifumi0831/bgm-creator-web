FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p ./temp/uploads ./temp/outputs ./temp/jobs ./assets

# Create default background image if it doesn't exist
RUN echo "Creating default background" && \
    mkdir -p ./assets && \
    convert -size 1280x720 gradient:blue-black ./assets/default_background.jpg || \
    echo "ImageMagick not available, skipping default background creation"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
