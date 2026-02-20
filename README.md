# 🤖 AI Embedding API

A REST API built with **FastAPI** that generates and compares **AI sentence embeddings** using **Sentence-Transformers**.

---

## 📌 Project Objective

This project implements an intelligent API capable of:

- Converting text into numerical vector representations (**embeddings**)
- Automatically selecting the most appropriate AI model
- Storing embeddings in memory
- Comparing semantic similarity between texts

---

## 🛠 Technologies Used

- **Python 3.11**
- **FastAPI**
- **Uvicorn**
- **Sentence-Transformers**
- **Postman**
- **Swagger UI**

---

## 🧠 AI Models

The API uses two NLP embedding models:

| Model | Purpose |
|------|---------|
| `paraphrase-multilingual-mpnet-base-v2` | General semantic similarity & sentence embeddings |
| `multi-qa-MiniLM-L6-cos-v1` | Optimized for question-answer tasks |

---

## ⚙️ Features

✅ REST API design  
✅ Automatic model selection  
✅ Embedding generation  
✅ Memory storage  
✅ Cosine similarity computation  
✅ Input validation  
✅ Exception handling  
✅ Swagger documentation  
✅ Postman testing  

---

## 🚀 How to Run the Project

### 1️⃣ Install dependencies

```bash
pip install fastapi uvicorn sentence-transformers
2️⃣ Start the server
uvicorn main:app --reload
3️⃣ Open API documentation

Swagger UI:

http://127.0.0.1:8000/docs
🔌 API Endpoints
✅ Health Check
GET /health

Response:

{
  "status": "API running"
}
✅ List Available Models
GET /models
✅ Generate Embedding
POST /embed

Request:

{
  "text": "AI is amazing"
}

Response:

{
  "text": "AI is amazing",
  "model_used": "paraphrase-multilingual-mpnet-base-v2",
  "vector": [...]
}
✅ Compare Text Similarity
POST /compare

Request:

{
  "text1": "AI is powerful",
  "text2": "Artificial intelligence is strong"
}

Response:

{
  "similarity": 0.873
}
✅ View Stored Embeddings
GET /memory
🔍 Model Selection Logic

The API automatically selects the model:

If text contains ? → QA Model

Otherwise → Paraphrase Model

📐 Similarity Metric

Semantic similarity is computed using:

Cosine Similarity

Why?

Measures angle between vectors

Independent of vector magnitude

Standard for embedding comparison

⚠️ Error Handling
Scenario	HTTP Code
Missing / Empty input	400 Bad Request
Internal processing error	500 Internal Server Error
Success	200 OK
✅ Testing

The API was tested using:

Swagger UI

Postman Collection

🎯 Learning Outcomes

✔ REST API design
✔ GET vs POST
✔ NLP embeddings
✔ Cosine similarity
✔ Model routing
✔ Validation & exceptions
✔ API testing workflow

📚 Conclusion

This project successfully integrates AI/NLP models into a functional API capable of embedding generation, storage, and semantic similarity analysis.

👩‍💻 Author

Developed as part of an AI / NLP academic project.
