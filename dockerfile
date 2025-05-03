# Use an official Python 3.8.16 image as the base
FROM python:3.8.16-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required to build some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    pkg-config \
    libhdf5-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set pip global timeout to help with slow downloads
RUN pip config set global.timeout 100

# Upgrade pip
RUN python -m pip install --upgrade pip

# Copy the project files into the container
COPY . /app

# Install Python dependencies with verbosity and fallback mirror
RUN pip install -v --no-cache-dir -i https://pypi.org/simple -r requirements.txt

# Expose the ports for both Rasa model and actions server
EXPOSE 5005 5055

# Use exec form of CMD to ensure proper signal handling
CMD ["sh", "-c", "rasa run --model /app/models --enable-api --cors '*' --port 5005 & rasa run actions --port 5055"]
