# Use the slim base as requested
#Stage : 1
FROM python:3.11-slim AS builder 
# added As Builder for multi-stage

# Set the working directory
WORKDIR /app

#install build dependencies if needed.
RUN mkdir -p /install

# Copy requirements first for cache optimization
COPY requirements.txt .

# Install dependencies into the /install prefix
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


#Stage 2
FROM python:3.11-slim 
# added for second stage

WORKDIR /app

#copy only the installed dependencies from the builder
COPY --from=builder /install /usr/local

# Copy the rest of the source code
COPY . .

EXPOSE 5000


# Create a non-root user for security
RUN useradd -m myuser
USER myuser

# Start the application
CMD ["python", "app.py"]

