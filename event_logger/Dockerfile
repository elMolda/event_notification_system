# Use a lightweight Python image
FROM python:3.10-slim

WORKDIR /app

# Copy and install dependencies
COPY ../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code
COPY . /app

# Add the current directory to PYTHONPATH
ENV PYTHONPATH=/app

# Expose the port FastAPI will run on
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
