
# Artificial Intelligence Systems Project Repository

## CORAS — Context-Based Intelligent Knowledge Retrieval System

![image](https://github.com/user-attachments/assets/caceae83-5405-485a-9682-87d64ff02188)

## Overview

CORAS is a **Context-Based Intelligent Knowledge Retrieval System** built with **Retrieval Augmented Generation (RAG)** architecture. It allows users to upload unstructured data (text, audio, or PDFs), processes it for relevance, and generates context-based responses using AI. 

The system is designed to answer user queries by extracting real-time, relevant information from documents, audio files, and PDFs, without compromising confidentiality. The backend uses **Pinecone** for vector indexing and **OpenAI's GPT-3.5** for text generation, integrated in a seamless Flask application.

## Features

- **Query Response Generation**: Provide relevant responses based on user queries, using context retrieved from documents.
- **Document Upload**: Supports uploading PDF and audio files for indexing and later query-based retrieval.
- **Metrics & Monitoring**: Integration with **Prometheus** for system metrics and performance monitoring.
- **Real-Time Processing**: Process documents on-the-fly and generate contextual responses using embedded data.
  
## Technologies Used

- **Flask**: Web framework for building the API.
- **ReactJS**: Frontend framework for User interface.
- **Pinecone**: Managed vector database for fast document search and retrieval.
- **OpenAI**: For generating embeddings and query responses.
- **Whisper**: For audio transcription.
- **Prometheus**: For system monitoring and metrics.
- **Docker**: For containerizing the application and ensuring smooth deployment.

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ananyd36/CORAS
cd CORAS
```

### 2. Install Dependencies

#### Backend:

Install the required dependencies using `pip`. It is recommended to create a virtual environment first.

```bash
# Create a virtual environment

cd kloop_back
python3 -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'

# Install dependencies
pip install -r requirements.txt
```

#### Frontend:

```bash

cd kloop_front
# Install dependencies
npm install (Node Version : 18.20.4)

```

### 3. Environment Variables

Create a `.env` file in the root directory and add the following variables:

```ini
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_CLOUD=your_pinecone_cloud (default: aws)
PINECONE_REGION=your_pinecone_region (default: us-east-1)
OPENAI_API_KEY=your_openai_api_key
```

### 4. Docker (Optional)

You can also run the application using Docker. The project is containerized using Docker to ensure smooth deployment.

```bash
# Build the Docker image
docker compose build -t CORAS.

docker compose up -d
```

---

## Running the Application

To start the Flask development server, use the following command:

```bash
python app.py
```

This will start the backend server at `http://localhost:5000`.

```bash
npm start
```

This will start the frontend server at `http://localhost:3000`.

---

## API Endpoints

### `GET /`

**Description**: Welcome endpoint to confirm the server is running.

**Response**:

```json
{
  "message": "Welcome to the backend API!"
}
```

### `POST /query`

**Description**: Accepts a user query and returns a relevant response based on the context retrieved from Pinecone.

**Request Body**:

```json
{
  "query": "What is the best way to extract information from unstructured data?"
}
```

**Response**:

```json
{
  "response": "The best way to extract information from unstructured data is by using embeddings to convert text into vector form, and then using a vector database like Pinecone for fast retrieval."
}
```

### `POST /upload`

**Description**: Upload a PDF or audio file for indexing.

**Request Body**: A `multipart/form-data` containing the file.

**Response**:

```json
{
  "message": "File indexed successfully"
}
```

### `POST /feedback`

**Description**: Allows users to submit feedback on the responses provided by CORAS.

**Request Body**:

```json
{
  "feedback": "up",
  "query": "What is the best way to extract information from unstructured data?",
  "response": "The best way to extract information from unstructured data is by using embeddings to convert text into vector form."
}
```

**Response**:

```json
{
  "message": "Feedback received successfully"
}
```

### `GET /metrics`

**Description**: Exposes Prometheus-compatible metrics for monitoring.

**Response**:

Metrics in Prometheus format.

---

## Folder Structure

![image](https://github.com/user-attachments/assets/767779fb-83e5-4d22-9adf-16f9b7f14138)


## Contributing

We welcome contributions! Feel free to fork the repository and submit pull requests. 

To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a pull request

---


## Acknowledgements

- **Pinecone** for the powerful vector database.
- **OpenAI** for the GPT model and embeddings.
- **Whisper** for accurate audio transcription.
- **Flask** for being a simple yet powerful web framework.
- **ReactJS** for interactive and clean UI.
---


#### This repository is handled by Aryan and Anany
