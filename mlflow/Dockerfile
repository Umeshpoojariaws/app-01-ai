FROM ghcr.io/mlflow/mlflow:latest

# Install dependencies
RUN pip install --no-cache-dir psycopg2-binary google-cloud-storage gunicorn

# Expose the port
EXPOSE 5000

# Explicitly set Entrypoint to gunicorn to override base image defaults
ENTRYPOINT ["gunicorn"]

# Set default arguments (can be overridden by K8s args if needed)
CMD ["--bind=0.0.0.0:5000", "--workers=2", "mlflow.server:app"]