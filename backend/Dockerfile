# Use the official Python image from the Docker Hub
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/local/bin/python3.10

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gfortran \
    build-essential \
    libffi-dev \
    libopenblas-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install poetry and scipy
RUN pip install --upgrade pip \
    && pip install -U poetry

# Set working directory
WORKDIR /workdir/backend

# Copy pyproject.toml and install dependencies
COPY pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction 

# Copy the rest of the application code
COPY . .

# Ensure poetry is executable and update shebang line
RUN chmod +x /usr/local/bin/poetry \
    && sed -i '1s|^.*$|#!/usr/local/bin/python3.10|' /usr/local/bin/poetry

# List poetry to verify
RUN ls -l /usr/local/bin/poetry

# Command to run the application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
