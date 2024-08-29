# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=main.py

# Expose the port that the app runs on
EXPOSE $PORT

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=$PORT"]