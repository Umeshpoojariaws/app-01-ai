# This Dockerfile creates a custom MLflow image that includes the
# PostgreSQL driver (psycopg2), which is missing from the official image.
FROM ghcr.io/mlflow/mlflow:latest

# Install the PostgreSQL driver
RUN pip install --no-cache-dir psycopg2-binary
# In your existing Dockerfile for mlflow-gcp
# Install Python dependencies
# Adding gunicorn is critical to force MLflow to use a production server
RUN pip install mlflow[extras] psycopg2-binary google-cloud-storage gunicorn

# # Copy the rest of the application code
# COPY . .