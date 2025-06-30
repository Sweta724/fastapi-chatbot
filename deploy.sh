export GCP_PROJECT="regal-ceiling-461217-a1" 
export GCP_REGION="us-central1" 
export AR_REPO="chatbot-demo” 
export SERVICE_NAME="chatbot-demo"

gcloud artifacts repositories create "$AR_REPO" --location="$GCP_REGION" --repository-format=Docker


gcloud builds submit --tag "$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME"


gcloud run deploy "$SERVICE_NAME" \
  --port=8000 \
  --image="$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME" \
  --allow-unauthenticated \
  --region=$GCP_REGION \
  --platform=managed  \
  --project=$GCP_PROJECT \
  --set-env-vars=GCP_PROJECT=$GCP_PROJECT,GCP_REGION=$GCP_REGION