# This Dockerfile creates a custom MLflow image that includes the
# PostgreSQL driver (psycopg2) and Gunicorn.
FROM ghcr.io/mlflow/mlflow:latest

# Install Python dependencies required for GKE deployment
# - psycopg2-binary: For connecting to a PostgreSQL backend (if needed later)
# - google-cloud-storage: For using GCS as an artifact store
# - gunicorn: A production-grade WSGI server to run MLflow
RUN pip install --no-cache-dir psycopg2-binary google-cloud-storage gunicorn

# # Copy the rest of the application code
# COPY . .