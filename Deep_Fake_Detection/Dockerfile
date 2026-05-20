# ==========================================================================
# 🐳 Production-Grade Docker Configuration for DFD_SYS
# Engineered by Darshan Naidu
# ==========================================================================

# Pull Python 3.10 slim-buster image for lightweight build
FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system-level build tools and requirements for dlib/face-recognition/OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up the working directory inside the container
WORKDIR /app

# Upgrade pip and install standard build wrappers
RUN python -m pip install --upgrade pip setuptools wheel

# Copy requirements list first to leverage Docker build cache layers
COPY requirements.txt /app/requirements.txt

# Install PyTorch, torchvision, dlib, and all app dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn server for production environment WSGI hosting
RUN pip install --no-cache-dir gunicorn

# Copy all project code assets to app folder
COPY . /app

# Create static directories and pre-set video/image uploads folder
RUN mkdir -p /home/app/staticfiles/app/uploaded_videos/ \
    && mkdir -p /app/uploaded_videos/app/uploaded_videos/ \
    && mkdir -p /app/run/

# Compile production-ready Django static files
RUN python manage.py collectstatic --noinput

# Set execution permission on the deployment script
RUN chmod +x /app/bin/gunicorn_start.sh

# Mount socket storage volume
VOLUME /app/run/

# Run the deployment container Gunicorn entry point
ENTRYPOINT ["/app/bin/gunicorn_start.sh"]