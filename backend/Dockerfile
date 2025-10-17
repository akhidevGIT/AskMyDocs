FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY app/requirements-core.txt .
RUN pip install --no-cache-dir -r requirements-core.txt

COPY app/requirements-ml.txt .
RUN pip install --no-cache-dir --prefer-binary -r requirements-ml.txt

# Copy backend code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
