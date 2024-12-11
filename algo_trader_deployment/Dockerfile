# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any Python dependencies listed in requirements.txt
# If you don't have a requirements.txt, skip this line
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
# Uncomment the next line if your script uses networking
# EXPOSE 80

# Define the command to run your script
CMD ["python", "app.py"]
