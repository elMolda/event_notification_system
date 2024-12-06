# Use a lightweight Python image
FROM python:3.10-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Copy and install dependencies
COPY ../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code
COPY . /app

# Start the notification processor script
CMD ["python", "notification_processor.py"]
