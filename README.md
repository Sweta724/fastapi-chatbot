# Chatbot Assignment

This project is a simple chatbot built with FastAPI and Google's Gemini API. It's designed to answer questions about any company, and if it doesn't know the answer, it will generate a creative and plausible one.

## Code Safety Settings

The chatbot uses Google's Generative AI with specific safety settings to filter out harmful content. The following settings are configured to block content with a high probability of being harmful:

```python
safety_settings = {
    "HARASSMENT": "BLOCK_ONLY_HIGH",
    "HATE_SPEECH": "BLOCK_ONLY_HIGH",
    "SEXUALLY_EXPLICIT": "BLOCK_ONLY_HIGH"
}
```

These settings are applied to the `genai.GenerativeModel` to ensure the chatbot's responses are appropriate.

## Dockerization

The application is containerized using Docker for easy deployment and scalability.

### Dockerfile

The `Dockerfile` sets up the Python environment, installs the required dependencies, and runs the FastAPI application.

- Uses the official `python:3.9-slim` image.
- Sets the working directory to `/app`.
- Copies the application files into the container.
- Installs dependencies from `requirements.txt`.
- Exposes port `8000`.
- Starts the application using `uvicorn`.

### .dockerignore

The `.dockerignore` file is used to exclude unnecessary files from the Docker build context, such as `__pycache__` directories and `.pyc` files.

## Deployment to Google Cloud Run

The application can be deployed to Google Cloud Run using the provided shell script.

### Prerequisites

- Google Cloud SDK installed and configured.
- A Google Cloud project with the Artifact Registry and Cloud Run APIs enabled.

### Deployment Steps

1.  **Set Environment Variables:**
    The `deploy.sh` script requires the following environment variables to be set:
    - `GCP_PROJECT`: Your Google Cloud project ID.
    - `GCP_REGION`: The region where you want to deploy the service (e.g., `us-central1`).
    - `AR_REPO`: The name of the Artifact Registry repository (e.g., `chatbot-demo`).
    - `SERVICE_NAME`: The name of the Cloud Run service (e.g., `chatbot-demo`).

2.  **Run the Deployment Script:**
    Execute the `deploy.sh` script from your terminal:
    ```bash
    bash deploy.sh
    ```

The script will:
1.  Create an Artifact Registry repository if it doesn't exist.
2.  Build the Docker image using Cloud Build.
3.  Tag and push the image to the Artifact Registry.
4.  Deploy the image to Cloud Run, making it publicly accessible.

## Testing the Deployed Application

Once the application is deployed, you can test it using the FastAPI documentation UI.

1.  Open your browser and navigate to the following URL:
    [https://chatbot-demo-443805814946.us-central1.run.app/docs](https://chatbot-demo-443805814946.us-central1.run.app/docs)

2.  You will see the FastAPI interactive API documentation.

3.  Click on the `/chat` endpoint to expand it.

4.  Click on the "Try it out" button.

5.  In the "Request body" section, enter your message in the following JSON format:
    ```json
    {
      "message": "Tell me about Google"
    }
    ```

6.  Click the "Execute" button to send the request to the chatbot.

7.  The response from the chatbot will be displayed in the "Response body" section.