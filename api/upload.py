from fastapi import APIRouter, UploadFile, File
import shutil
import uuid
import os
from db.models import Document, SessionLocal
from api.parse import parse_document
from embeddings.embedder import generate_and_store_embedding
from config import STORAGE_DIR

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    doc_id = str(uuid.uuid4())
    file_path = os.path.join(STORAGE_DIR, f"{doc_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    content = parse_document(file_path)
    
    db = SessionLocal()
    doc = Document(file_name=file.filename, file_path=file_path, content=content)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    generate_and_store_embedding(doc.id, content)
    
    return {"document_id": doc.id, "file_name": file.filename}
