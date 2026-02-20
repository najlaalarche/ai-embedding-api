from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util

app = FastAPI(
    title="AI Embedding API",
    description="API for generating and comparing sentence embeddings",
    version="1.0"
)

# ✅ Load models (locally)
paraphrase_model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
qa_model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

# ✅ Memory storage
memory = {}

# ✅ Request schemas
class TextInput(BaseModel):
    text: str

class CompareInput(BaseModel):
    text1: str
    text2: str


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
# ✅ GET /memory
# -----------------------------
@app.get("/memory")
def get_memory():
    return {"stored_embeddings": memory}


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
        else:
            model = paraphrase_model
            model_used = "paraphrase-multilingual-mpnet-base-v2"

        # ✅ Generate embedding
        vector = model.encode(text).tolist()

        # ✅ Store in memory
        memory[text] = vector

        # ✅ Response
        return {
            "text": text,
            "model_used": model_used,
            "vector": vector
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