from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import numpy as np
import redis




app = FastAPI(
    title="AI Embedding API",
    description="API for generating and comparing sentence embeddings",
    version="1.0"
)

# ✅ Load models (locally)
paraphrase_model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
qa_model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")



# ✅ Request schemas
class TextInput(BaseModel):
    text: str

class CompareInput(BaseModel):
    text1: str
    text2: str

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
@app.get("/redis-health")
def redis_health():
    return {"redis_alive": r.ping()}

@app.post("/redis-test")
def redis_test(data: TextInput):
    r.set(data.text, "stored")
    return {"message": "stored in redis"}

# -----------------------------
# ✅ GET /health
# -----------------------------
@app.get("/health")
def health():
    return {"status": "API running"}


# -----------------------------
# ✅ GET /models
# -----------------------------
@app.get("/models")
def list_models():
    return {
        "available_models": [
            "paraphrase-multilingual-mpnet-base-v2",
            "multi-qa-MiniLM-L6-cos-v1"
        ]
    }


# -----------------------------
# ✅ POST /embed
# -----------------------------
@app.post("/embed")
def embed_text(data: TextInput):

    text = data.text.strip()

    # ✅ Validation
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        # ✅ Detect type (very simple)
        if "?" in text:
            model = qa_model
            model_used = "multi-qa-MiniLM-L6-cos-v1"
            prefix = "minilm:"
        else:
            model = paraphrase_model
            model_used = "paraphrase-multilingual-mpnet-base-v2"
            prefix = "mpnet:"

        # ✅ Generate embedding
        vector = model.encode(text)
        vector_np = np.array(vector, dtype=np.float32)
        vector_bytes = vector_np.tobytes()

        # ✅ Store in memory
        r.hset(f"{prefix}{text}", mapping={
            "text": text,
            "vector": vector_bytes
        })
        # ✅ Response
        return {
            "text": text,
            "model_used": model_used,
            "vector": vector.tolist()
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Vector generation failed")


# -----------------------------
# ✅ POST /compare
# -----------------------------
@app.post("/compare")
def compare_texts(data: CompareInput):

    text1 = data.text1.strip()
    text2 = data.text2.strip()

    # ✅ Validation
    if not text1 or not text2:
        raise HTTPException(status_code=400, detail="Texts cannot be empty")

    try:
        emb1 = paraphrase_model.encode(text1)
        emb2 = paraphrase_model.encode(text2)

        similarity = util.cos_sim(emb1, emb2).item()

        return {
            "text1": text1,
            "text2": text2,
            "similarity": round(similarity, 3)
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Comparison failed")
    
@app.post("/similarity_search")
def similarity_search(data: TextInput):

    query = data.text.strip()

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # 🔎 Detect model like /embed
    if "?" in query:
        model = qa_model
        index_name = "idx_minilm"
    else:
        model = paraphrase_model
        index_name = "idx_mpnet"

    # Encode
    vector = model.encode(query)
    vector_np = np.array(vector, dtype=np.float32)
    vector_bytes = vector_np.tobytes()

    query_str = "*=>[KNN 3 @vector $vec AS score]"

    results = r.execute_command(
        "FT.SEARCH",
        index_name,
        query_str,
        "PARAMS", 2,
        "vec", vector_bytes,
        "SORTBY", "score",
        "RETURN", 2, "text", "score",
        "DIALECT", 2
    )

    return {"results": results}