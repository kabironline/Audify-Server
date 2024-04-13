FROM python:3.11

WORKDIR /music-streaming-app-iitm

# Copy the requirements file into the container
COPY requirements/requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Set the PYTHONPATH to include the app directory
ENV PYTHONPATH="${PYTHONPATH}:/music-streaming-app-iitm"

# Copy the rest of your Flask app code into the container
COPY . .

# Command to start the Flask app
CMD flask run --host=0.0.0.0
