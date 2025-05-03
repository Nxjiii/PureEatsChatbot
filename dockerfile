FROM python:3.8.16-slim

# Set the working directory inside the container
WORKDIR /app

# system dependencies required to build some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    pkg-config \
    libhdf5-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# pip global timeout to help with slow downloads
RUN pip config set global.timeout 100

# Upgrade pip
RUN python -m pip install --upgrade pip

# Copy the project files into the container
COPY . /app

# Install Python dependencies 
RUN pip install -v --no-cache-dir -i https://pypi.org/simple -r requirements.txt

# Expose port for the Rasa model server
EXPOSE 5005

# exec form of CMD to ensure proper signal handling
CMD ["rasa", "run", "--model", "/app/models", "--enable-api", "--cors", "*", "--port", "5005"]
