# Image
FROM python:3.7

# Send api service logs in real time
ENV PYTHONUNBUFFERED=1

# Create directory for the code
WORKDIR /code

# Copy over requirements to the code directory
COPY requirements.txt /code/

# Install dependencies
RUN pip install -r requirements.txt

# Copy full directory to the code directory
COPY . /code/

# Expose port :80
EXPOSE 80