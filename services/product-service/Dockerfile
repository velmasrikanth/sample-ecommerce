# Use official Python runtime as a parent image (lightweight slim variant)
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file first (leverages Docker cache)
COPY requirements.txt ./

# Install Python dependencies without caching wheels
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5001

# Default command to run the Flask app
CMD ["python", "app.py"]
