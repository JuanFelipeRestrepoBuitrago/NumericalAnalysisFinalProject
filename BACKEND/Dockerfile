FROM python:3.9.13-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY ./requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install gcc curl -y \
    && apt-get clean

RUN pip install -r requirements.txt

# Copy the entire application code to the container
COPY . /app/

# Expose the port the app runs on (optional, depending on your setup)
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]

# Add the HEALTHCHECK instruction
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f http://localhost:8000/api/${API_VERSION}/${API_NAME}/ || exit 1
