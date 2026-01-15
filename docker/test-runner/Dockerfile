FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY pyproject.toml /app/

# Install Python dependencies
RUN pip install --no-cache-dir -e ".[dev]"

# Copy application code
COPY . /app/

# Run tests by default
CMD ["pytest", "tests/", "-v"]
