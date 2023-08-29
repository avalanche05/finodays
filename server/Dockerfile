# Use the official Python image based on Debian
FROM python:3

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt /usr/src/app/

# Install pipenv (a tool for managing Python virtual environments)
RUN pip install pipenv

# Create and activate a virtual environment
RUN python -m venv venv
RUN . venv/bin/activate

# Install project dependencies inside the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /usr/src/app

# Expose the port your application will run on
EXPOSE 46874

# Set the entry point for the container
CMD ["python", "-m", "openapi_server"]
