# Weather Forecaster ML Application

This project is a complete machine learning application that predicts tomorrow's temperature based on today's weather conditions. It is designed to be deployed on Google Kubernetes Engine (GKE) and includes a full CI/CD pipeline using GitHub Actions.

## Architecture

The application is composed of four main services:

*   **Frontend**: A Streamlit web application that provides a user interface for making predictions.
*   **Backend**: A FastAPI server that receives requests from the frontend, loads the trained model from the MLflow Model Registry, and returns predictions.
*   **Training**: A Kubernetes Job that runs on a schedule or on-demand to train a weather forecasting model and register it with MLflow.
*   **MLflow**: An open-source platform used for managing the ML lifecycle, including experiment tracking, model registry, and artifact storage.

### GKE Architecture Overview

*   **GKE Cluster**: The application runs on a GKE cluster.
*   **Artifact Registry**: Docker images for each service are stored in Google Artifact Registry.
*   **Persistent Volume**: MLflow uses a `PersistentVolumeClaim` to store its tracking data and model artifacts, ensuring that data persists across pod restarts.
*   **Service Discovery**: Kubernetes services are used for communication between the frontend, backend, and MLflow pods.

---

## Prerequisites

Before deploying, you must have the following:

1.  A Google Cloud Platform (GCP) project.
2.  `gcloud` CLI installed and authenticated.
3.  `kubectl` installed.
4.  A GKE cluster running.
5.  A Google Artifact Registry repository named `ml-repo`.

---

## Deployment

This project is configured for continuous deployment using GitHub Actions.

### CI/CD Workflow (`.github/workflows/ci-cd.yaml`)

The workflow automates the entire build and deployment process. On every push to the `main` branch, the following jobs are executed:

1.  **`build-and-push`**:
    *   Authenticates to Google Cloud using Workload Identity Federation.
    *   Builds Docker images for the `frontend`, `backend`, `training`, and `mlflow` services using `docker buildx` to ensure `linux/amd64` compatibility.
    *   Pushes the tagged images to the specified Google Artifact Registry repository.

2.  **`deploy`**:
    *   Authenticates to Google Cloud and connects to the GKE cluster.
    *   Replaces the `DOCKER_REPO_URL` placeholder in the Kubernetes manifests with the correct Artifact Registry path.
    *   Deletes any previously completed `training` job to avoid deployment errors.
    *   Applies all manifests from the `kubernetes/` directory using `kubectl apply`.

### Manual Deployment

To deploy the application manually, follow these steps:

1.  **Build and Push Images**:
    Run the following commands from the root of the `app-01-ai` directory, replacing `GCP_PROJECT_ID` with your project ID.

    ```bash
    export GCP_PROJECT_ID="your-gcp-project-id"
    export IMAGE_REPO_URL="us-central1-docker.pkg.dev/${GCP_PROJECT_ID}/ml-repo"

    # Build and push all images
    docker buildx build --platform linux/amd64 -t ${IMAGE_REPO_URL}/mlflow-gcp:latest --push ./mlflow
    docker buildx build --platform linux/amd64 -t ${IMAGE_REPO_URL}/training:latest --push ./training
    docker buildx build --platform linux/amd64 -t ${IMAGE_REPO_URL}/backend:latest --push ./backend
    docker buildx build --platform linux/amd64 -t ${IMAGE_REPO_URL}/frontend:latest --push ./frontend
    ```

2.  **Deploy to GKE**:
    First, substitute the image repository URL in the Kubernetes manifests.

    ```bash
    # For macOS
    find ./kubernetes -type f -name "*.yaml" -exec sed -i '' "s|DOCKER_REPO_URL|${IMAGE_REPO_URL}|g" {} +
    # For Linux
    # find ./kubernetes -type f -name "*.yaml" -exec sed -i "s|DOCKER_REPO_URL|${IMAGE_REPO_URL}|g" {} +
    ```

    Then, apply the manifests.

    ```bash
    kubectl apply -f kubernetes/
    ```

---

## Accessing the Application

1.  **Find the Frontend Service IP**:
    The `frontend` service is exposed via a `LoadBalancer`. Find its external IP address with:

    ```bash
    kubectl get svc frontend -n dev
    ```

2.  **Access the UI**:
    Open your web browser and navigate to `http://<EXTERNAL_IP>:8501`.

3.  **Access MLflow UI (Optional)**:
    To view the MLflow UI, you can use port-forwarding:

    ```bash
    kubectl port-forward svc/mlflow 5000:5000 -n dev
    ```
    Then, open `http://localhost:5000` in your browser.