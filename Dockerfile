FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    gcc \
    libpq-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . /app
WORKDIR /app

# Copy entrypoint script
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
