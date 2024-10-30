# Use an official Python image as the base image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install dependencies with pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the application code into the container
COPY . .

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# Set the entrypoint script to be executed
ENTRYPOINT ["/app/entrypoint.sh"]
