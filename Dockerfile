# Base Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

# Copy app code
COPY remote_server.py .

# Expose Port
EXPOSE 8080

# Run app

CMD ["python","remote_server.py"]