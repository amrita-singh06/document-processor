from fastapi import APIRouter, UploadFile, File
import shutil
from pathlib import Path
import uuid

from config import UPLOAD_DIR
from parser.parse import parse_pdf
from embeddings.embedder import store_embeddings

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Save file to disk in streaming mode
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer, length=1024*1024)  # 1MB chunks

    # Generate a unique document ID
    doc_id = str(uuid.uuid4())

    # Parse PDF into chunks
    chunks = parse_pdf(file_path)

    # Store embeddings in Chroma
    store_embeddings(chunks, metadata=[{"file": file.filename}] * len(chunks), doc_id=doc_id)

    return {
        "file_name": file.filename,
        "document_id": doc_id,
        "chunks_stored": len(chunks),
        "size_mb": round(file_path.stat().st_size / (1024*1024), 2),
        "status": "success"
    }
