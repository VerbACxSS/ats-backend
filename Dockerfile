FROM bitnami/python:3.9.18

# Move in server folder
WORKDIR /server

# Copy requirements.txt and install all dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files in server directory
COPY . .

# Expose server port
EXPOSE 8000

# Run FastAPI application
CMD ["uvicorn", "app.app:app", "--host=0.0.0.0"]
