# Use the official Python image as the base image
FROM python:3.12-slim
# Create a working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the entire application into the container
COPY . .
RUN chmod +x start.sh
# Expose the port the app runs on
EXPOSE 8080
ENTRYPOINT ["./start.sh"]