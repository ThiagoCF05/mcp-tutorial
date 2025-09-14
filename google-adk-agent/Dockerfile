# Use the official Python image as the base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src and .env to the working directory
COPY fundamental_analyst/ ./fundamental_analyst

# Expose the port that the app will be running on
EXPOSE 8080

# Set the command to run when the container starts
CMD ["adk", "web", "--port", "7000", "--host", "0.0.0.0"]