from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from embeddings.embedder import collection, model

router = APIRouter()

# ---------------- Request/Response Schemas ----------------

class QueryRequest(BaseModel):
    document_id: str
    question: str

class QueryResponse(BaseModel):
    answer: str

# ---------------- Helper Functions ----------------

def get_top_chunks(doc_id: str, query: str, top_k: int = 5):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        where={"doc_id": doc_id}  # filter by document ID
    )
    # Return chunk texts
    return results["documents"][0] if results["documents"] else []

def generate_answer(chunks, question):
    """
    Simple RAG style answer: concatenate chunks + question.
    Replace with LLM for better results.
    """
    context = "\n".join(chunks)
    return f"Question: {question}\n\nContext:\n{context}\n\nAnswer: Based on document content."

# ---------------- API Endpoint ----------------

@router.post("/query/", response_model=QueryResponse)
async def query_document(req: QueryRequest):
    try:
        print(req.document_id, req.question)
        chunks = get_top_chunks(req.document_id, req.question)
        if not chunks:
            return {"answer": "No relevant content found for this document."}
        answer = generate_answer(chunks, req.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
