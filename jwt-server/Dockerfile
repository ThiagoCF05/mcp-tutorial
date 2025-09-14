# Use the official Python image as the base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src and .env to the working directory
COPY src/ .
COPY .env .

# Copy the PEM key file to the working directory Set the environment variable it
COPY ../mcp-tutorial.pem /app/
ENV PRIVATE_KEY=/app/mcp-tutorial.pem

# Expose the port that the app will be running on
EXPOSE 8000

# Set the command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]