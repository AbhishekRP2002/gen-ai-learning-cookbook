# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .


# If you don't have a requirements.txt, you can directly install packages like this:
RUN pip install --no-cache-dir llama-index pandas 'crewai[tools]'

# Run app.py when the container launches
CMD ["python3", "csv-rag-agent/test.py"]
