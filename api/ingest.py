from fastapi import APIRouter, Query, BackgroundTasks
import requests
from pathlib import Path
import uuid

from config import UPLOAD_DIR
from parser.parse import parse_pdf
from embeddings.embedder import store_embeddings

router = APIRouter()

def ingest_task(file_path: Path, file_name: str, doc_id: str):
    """
    Background task: parse PDF, chunk, and store embeddings.
    """
    # Parse PDF and split into chunks
    chunks = parse_pdf(file_path)  # Make sure parse_pdf returns list of chunks efficiently

    # Store embeddings in batch
    store_embeddings(
        chunks,
        metadata=[{"file": file_name}] * len(chunks),
        doc_id=doc_id
    )
    print(f"✅ {file_name} processed with {len(chunks)} chunks.")


@router.post("/ingest-url/")
async def ingest_url(pdf_url: str = Query(..., description="PDF URL to ingest"),
                     background_tasks: BackgroundTasks = None):
    try:
        # Stream download in 1MB chunks to avoid memory issues
        response = requests.get(pdf_url, stream=True, timeout=60)
        response.raise_for_status()

        file_name = pdf_url.split("/")[-1]
        file_path = UPLOAD_DIR / file_name
        UPLOAD_DIR.mkdir(exist_ok=True, parents=True)

        with open(file_path, "wb") as buffer:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    buffer.write(chunk)

        # Generate unique document ID
        doc_id = str(uuid.uuid4())

        # Run ingestion in background
        if background_tasks:
            background_tasks.add_task(ingest_task, file_path, file_name, doc_id)
        else:
            ingest_task(file_path, file_name, doc_id)

        return {
            "file_name": file_name,
            "document_id": doc_id,
            "status": "processing"
        }

    except Exception as e:
        return {"error": str(e), "status": "failed"}
