FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create and set the working directory
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt /app/

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


# Copy the Django project files
COPY . /app

# Expose the Django development server port (change as needed)

# Set the entrypoint or command to start the Django development server
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
