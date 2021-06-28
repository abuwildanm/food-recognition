# Web App

[Gradio](https://gradio.app/) allows you to quickly create customizable UI components around your TensorFlow or PyTorch models, or even arbitrary Python functions. Mix and match components to support any combination of inputs and outputs. Gradio is free and open-source!

## Project Structure

    .             
    ├── images/                         # Folder that contains test images
    ├── Dockerfile                      # Docker configuration
    ├── main.py                         # Gradio web app
    ├── requirements.txt                # Dependencies
    └── README.md


## Getting Started

1. Make sure you are in `web-app` directory
```
cd web-app
```
2. Set your project and region
```
gcloud config set project [PROJECT-ID]
gcloud config set run/region [REGION]
```
3. Build your container image using Cloud Build, by running the following command from the directory containing the Dockerfile
```
gcloud builds submit --tag gcr.io/$(gcloud config get-value project)/webapp
```
4. Deploy to Cloud Run using the following command
```
gcloud run deploy webapp --image gcr.io/$(gcloud config get-value project)/webapp --platform managed --port 8080
```