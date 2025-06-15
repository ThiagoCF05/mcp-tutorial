FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (adjust if your app uses a different port)
EXPOSE 8080

# Set default command to run the server
CMD ["fastmcp", "run", "server.py", "--transport", "streamable-http", "--port", "8080"]
