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
COPY mcp-tutorial.pub.pem /app/
ENV PUBLIC_KEY=/app/mcp-tutorial.pub.pem

# Copy the database path to the working directory Set the environment variable it
COPY fundamental_analysis.db /app/
ENV DATABASE_PATH=/app/fundamental_analysis.db

# Expose the port that the app will be running on
EXPOSE 8080

# Set the command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]