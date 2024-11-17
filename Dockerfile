# Use the Python 3 official image
# https://hub.docker.com/_/python
FROM python:3.12

# Run in unbuffered mode
ENV PYTHONUNBUFFERED=1 

# Create and change to the app directory.
WORKDIR /app

# Copy only necessary files first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# (but .dockerignore will prevent .env from being copied)
COPY . .

# Run the web service on container startup.
CMD ["gunicorn", "app:app"]