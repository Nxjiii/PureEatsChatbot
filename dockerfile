FROM python:3.8.16-slim

WORKDIR /app

# System dependencies to build Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    pkg-config \
    libhdf5-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set pip global timeout
RUN pip config set global.timeout 100

# Upgrade pip
RUN python -m pip install --upgrade pip

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install -v --no-cache-dir -i https://pypi.org/simple -r requirements.txt

# Clean up
RUN apt-get clean && rm -rf /root/.cache

# Create entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Use entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
