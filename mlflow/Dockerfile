# This Dockerfile creates a custom MLflow image that includes the
# PostgreSQL driver (psycopg2), which is missing from the official image.
FROM ghcr.io/mlflow/mlflow:latest

# Install the PostgreSQL driver
RUN pip install --no-cache-dir psycopg2-binary