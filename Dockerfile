# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /backend

# Copy requirements.txt and install dependencies
COPY backend/requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PYTHONPATH /backend

# Copy the rest of the backend code
COPY backend/ .  


# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
