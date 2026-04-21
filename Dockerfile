# Use the slim base as requested
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements first for cache optimization
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code
COPY . .

# Create a non-root user for security
RUN useradd -m myuser
USER myuser

# Start the application
CMD ["python", "app.py"]

