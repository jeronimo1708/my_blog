# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

ARG PYTHON_VERSION=3.13.3
# Use a specific minor version for consistency between builder and final stages.
# PYTHON_VERSION will be '3.13.3'
# This allows us to dynamically construct the site-packages path later.

# --- Stage 1: Builder Stage ---
# This stage installs Python dependencies and OS dependencies for compilation
FROM python:${PYTHON_VERSION}-slim AS builder

# Set environment variables for the build stage (mostly for pip and compilation)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

# Install OS-level dependencies required for building Python packages.
# For a Django app, you almost certainly need libpq-dev (for psycopg2 if using PostgreSQL).
# gcc is also needed for compiling some Python packages.
# Add other build-time OS dependencies here if needed, e.g., libjpeg-dev zlib1g-dev for Pillow,
# or imagemagick for image processing.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    # Optional: If you use Pillow for image processing:
    # libjpeg-dev \
    # zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to the latest version
# This needs to be done *before* installing other requirements
RUN pip install --upgrade pip

# Copy the requirements file first for better Docker caching.
# If requirements.txt doesn't change, this layer and subsequent layers
# (up to where the code is copied) can be reused.
COPY requirements.txt /app/

# Install Python dependencies.
# --no-cache-dir reduces the size of this layer, which is important
# because this layer will be copied to the final image.
RUN pip install --no-cache-dir -r requirements.txt


# --- Stage 2: Production / Runtime Stage ---
# This stage is minimal and only contains what's needed to run the app.
FROM python:${PYTHON_VERSION}-slim

# Set environment variables for the runtime stage (essential for production)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-privileged user consistent with the original Dockerfile template.
# This ensures the app runs with minimal permissions.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

WORKDIR /app

# Copy only the Python site-packages and binaries from the builder stage.
# We dynamically get the Python minor version for the site-packages path.
# PYTHON_VERSION is '3.13.3', so PYTHON_VERSION%.* will be '3.13'
COPY --from=builder /usr/local/lib/python${PYTHON_VERSION%.*}/site-packages/ /usr/local/lib/python${PYTHON_VERSION%.*}/site-packages/
# Copy executables like 'gunicorn', 'django-admin' from the builder stage
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy your application code into the container.
# This should be the last step to take advantage of Docker's caching,
# as code changes are frequent.
# --chown ensures the files are owned by the non-privileged appuser.
COPY --chown=appuser:appuser . .

# Switch to the non-privileged user for running the application.
USER appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Start the application using Gunicorn.
# Ensure 'blog_project.wsgi:application' matches your actual Django project's WSGI path.
# It was 'blog_project.wsgi' in your original, so I've kept it consistent.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "blog_project.wsgi:application"]