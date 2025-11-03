FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies (needed for a later successful build)
# Note: requirements.txt must exist for a successful build, though we're using a placeholder command for now.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || echo "Requirements file is a placeholder; skipping install for now."

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to start the API (using the main.py created in Commit 004)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]