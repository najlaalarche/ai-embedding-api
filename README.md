# 🤖 AI Vector Search API

A production-style **FastAPI backend** that generates AI embeddings and performs **semantic vector search** using **Redis Stack (HNSW)**.

---

## 🚀 Project Overview

This project implements a real-world AI backend capable of:

- Converting text into numerical vector representations (embeddings)
- Automatically selecting the most appropriate embedding model
- Storing embeddings in Redis using FLOAT32 binary format
- Creating HNSW vector indexes
- Performing fast semantic similarity search (KNN)
- Supporting multiple embedding dimensions

This is not simple in-memory storage.  
It uses a real **vector database architecture**.

---

## 🏗 Architecture


User
↓
FastAPI
↓
SentenceTransformers
↓
Embedding (384 or 768 dim)
↓
FLOAT32 Conversion
↓
Redis HASH Storage
↓
HNSW Vector Index
↓
KNN Semantic Search


---

## 🛠 Technologies Used

- Python 3.11
- FastAPI
- Uvicorn
- Sentence-Transformers
- Redis Stack
- NumPy
- Swagger UI
- Postman

---

## 🧠 AI Models

The API uses two NLP embedding models:

| Model | Dimension | Redis Index | Prefix | Purpose |
|--------|------------|------------|------------|----------|
| `multi-qa-MiniLM-L6-cos-v1` | 384 | `idx_minilm` | `minilm:` | Question-answer optimization |
| `paraphrase-multilingual-mpnet-base-v2` | 768 | `idx_mpnet` | `mpnet:` | General semantic similarity |

Each model uses a separate HNSW index due to different vector dimensions.

---

## ⚙️ Features

- ✅ REST API design  
- ✅ Automatic model detection  
- ✅ FLOAT32 binary vector storage  
- ✅ Redis HASH storage  
- ✅ HNSW vector indexing  
- ✅ Multi-index architecture  
- ✅ KNN semantic similarity search  
- ✅ Cosine distance metric  
- ✅ Input validation  
- ✅ Exception handling  
- ✅ Swagger documentation  

---

## 🗄 Redis Setup (Required)

This project requires **Redis Stack** (not plain Redis).

After installing Redis Stack, create the vector indexes:

### MiniLM (384 dimensions)

```bash
FT.CREATE idx_minilm ON HASH PREFIX 1 "minilm:" SCHEMA vector VECTOR HNSW 6 TYPE FLOAT32 DIM 384 DISTANCE_METRIC COSINE
MPNet (768 dimensions)
FT.CREATE idx_mpnet ON HASH PREFIX 1 "mpnet:" SCHEMA vector VECTOR HNSW 6 TYPE FLOAT32 DIM 768 DISTANCE_METRIC COSINE
🚀 Running the Project
1️⃣ Install dependencies
pip install -r requirements.txt
2️⃣ Start the server
uvicorn main:app --reload
3️⃣ Open API documentation

Swagger UI:

http://127.0.0.1:8000/docs
🔌 API Endpoints
✅ GET /health

Health check endpoint.

✅ GET /models

Lists available models and index configuration.

✅ POST /embed

Generates embedding and stores it in Redis.

Request:

{
  "text": "Machine learning is powerful"
}

Response:

{
  "text": "Machine learning is powerful",
  "model_used": "paraphrase-multilingual-mpnet-base-v2",
  "vector_dim": 768,
  "stored_key": "mpnet:Machine learning is powerful"
}
✅ POST /similarity_search

Performs KNN semantic search using Redis HNSW.

Request:

{
  "text": "What is machine learning?"
}

Returns the most semantically similar stored texts.

✅ POST /compare

Computes cosine similarity directly between two texts.

📐 Similarity Metric

Semantic similarity is computed using:

Cosine Similarity

Why?

Measures angular similarity

Independent of vector magnitude

Standard metric for embedding comparison

⚠️ Error Handling
Scenario	HTTP Code
Missing input	400
Internal error	500
Success	200
🎯 Learning Outcomes

✔ Vector embeddings

✔ Multi-model architecture

✔ Redis Stack integration

✔ HNSW indexing

✔ FLOAT32 vector storage

✔ KNN search

✔ Semantic search backend design

✔ Clean Git workflow

✔ AI backend system architecture

📚 Conclusion

This project demonstrates a complete AI vector search pipeline:

Embedding generation

Vector storage

HNSW indexing

Semantic similarity search

Multi-model support

It reflects a backend AI engineering architecture rather than a simple academic API.

👩‍💻 Author

Developed as an AI backend engineering project integrating NLP models with vector database architecture.

