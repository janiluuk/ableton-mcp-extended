FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask

# Copy application code
COPY app.py /app/

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
