# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage cache
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose gateway port
EXPOSE 5000

# Run the uvicorn server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
