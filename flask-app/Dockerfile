# Use the same Python version as in development
FROM python:3.10.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt requirements.txt

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Set environment variables for Flask
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production

# Command to run the application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:3000", "wsgi:application"]