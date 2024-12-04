# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies from the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask runs on (default is 5000)
EXPOSE 5000

# Install Waitress for running the application in production
RUN pip install waitress

# Command to run the Flask application using Waitress
CMD ["python", "-c", "from waitress import serve; from restaurant import app; serve(app, host='0.0.0.0', port=5000)"]
