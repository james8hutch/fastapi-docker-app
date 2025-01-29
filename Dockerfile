# Stage 1: Base setup for application
FROM python:3.9-slim AS base

# Install curl and system updates
RUN apt-get update && apt-get install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Alembic configurations
COPY alembic.ini .
COPY alembic ./alembic

# Copy the application code
COPY app ./app

# Expose the application port and debugging port
EXPOSE 8000 5678

# Add a HEALTHCHECK instruction
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 2: Test environment setup
FROM base AS test

# Copy the test requirements file and install test dependencies
COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt

# Copy the tests
COPY tests ./tests

# Ensure the app directory is accessible in PYTHONPATH
ENV PYTHONPATH=/app

# Set the entry point to run tests
ENTRYPOINT ["pytest", "-s"]
