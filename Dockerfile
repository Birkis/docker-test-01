# Use the Python 3 official image
# https://hub.docker.com/_/python
FROM python:3.12

# Run in unbuffered mode
ENV PYTHONUNBUFFERED=1 

# Add build dependencies before pip install
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    rust \
    cargo

# Create and change to the app directory.
WORKDIR /app

# Copy local code to the container image.
COPY . ./

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup.
CMD ["gunicorn", "app:app"]