# Use official Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory inside container
WORKDIR /app

# Copy source code into container
COPY . /app

# Install dependencies
RUN pip install flask

# Expose port (must match app.py)
EXPOSE 8000

# Run the Flask app
CMD ["python", "myapp/app.py"]
