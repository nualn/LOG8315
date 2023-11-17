# This Dockerfile is used to build a Docker image for the orchestrator service.

# Use the Python 3.8.12 base image
FROM python:3.8.12

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files to the working directory
COPY ./request_handler.py /app/
COPY ./requirements.txt /app/
COPY ./worker_status.json /app/

# Install the required Python packages
RUN pip install -r requirements.txt

# Set the command to run when the container starts
CMD ["sh", "-c", "python request_handler.py > output.log 2>&1"]