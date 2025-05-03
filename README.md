# PureEats Chatbot

This repository contains the Dockerized version of the Rasa chatbot and custom actions server used in the PureEats app. The purpose of this document is to help anyone run the chatbot locally and to showcase how it is hosted on Render and integrated with the frontend.

---

## 🐳 Running Locally with Docker

### 1. Build the Image

First, build the Docker image from the Dockerfile:

```bash
docker build -t rasa-project .
```

### 2. Run the Container

After building, run the container with:

```bash
docker run -it -p 5005:5005 -p 5055:5055 rasa-project
```

- **5005** → Rasa model server  
- **5055** → Actions server  

### 3. Access the Chatbot Locally

- **Rasa Model API**: [http://localhost:5005](http://localhost:5005)  
- **Rasa Actions API**: [http://localhost:5055](http://localhost:5055)  

These endpoints can be tested with tools like Postman, `curl`, or integrated into your frontend.

### 4. Stopping the Container

If you run locally, to stop the container, you can either:

- Press `CTRL+C` in the terminal running the container, or  
- Run the following commands:

```bash
docker ps        # Find the container ID
docker stop <container_id>
```

---

## 🌐 Hosting on Render

The chatbot is hosted on **Render**, with both the Rasa model server and custom actions server running together in a single Docker container. Below is an overview of the hosting setup:

1. **Dockerized Deployment**:
   - The Rasa model and custom actions are combined into a single Docker image.
   - This image is deployed as a web service on Render.

2. **Exposed Ports**:
   - **5005** → Rasa model server  
   - **5055** → Actions server  

3. **Frontend Integration**:
   - The chatbot is integrated with the PureEats app frontend via API calls to the hosted endpoints.

### Hosted Endpoints

- **Rasa Model API**: `https://<RenderAppURL>:5005`  
- **Rasa Actions API**: `https://<RenderAppURL>:5055`

---

This setup demonstrates how the chatbot can be run locally for testing and how it is deployed and integrated into the PureEats app for production use.


