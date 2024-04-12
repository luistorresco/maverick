# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Expose the port your app runs on
EXPOSE 8000

# Define the command to run your app
CMD ["uvicorn", "mi_api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
