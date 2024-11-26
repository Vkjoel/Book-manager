
FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y libzbar0 && pip install flask flask-cors pyzbar pillow

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
