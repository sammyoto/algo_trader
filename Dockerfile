# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy algo_trader_deployment into container
COPY /algo_trader_deployment /app

# Copy src into container
COPY /src /app

# Install any Python dependencies listed in requirements.txt
# If you don't have a requirements.txt, skip this line
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
# Uncomment the next line if your script uses networking
EXPOSE 8080

# Define the command to run your script
CMD ["python", "app.py"]
