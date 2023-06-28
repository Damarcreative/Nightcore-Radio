# Use a base image that matches the programming language used in your project.
FROM python:3.9

# Copy the requirements.txt file into the image
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy the main.py file into the image
COPY main.py .

# Copy the "nightcore" folder into the image
COPY nightcore /nightcore

# Specify the command to run your application
CMD ["python", "main.py"]
