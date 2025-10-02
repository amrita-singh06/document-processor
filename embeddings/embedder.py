# embeddings/embedder.py

from pathlib import Path
import uuid
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from config import CHROMA_DB_DIR

# ---------------------------
# Ensure CHROMA_DB_DIR exists and is Windows-safe
# ---------------------------
CHROMA_DB_DIR = Path(CHROMA_DB_DIR).resolve()
CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------
# Initialize Chroma client
# ---------------------------
# chroma_client = chromadb.PersistentClient(Settings(
#     persist_directory=str(CHROMA_DB_DIR),
#     chroma_db_impl="sqlite"
# ))
chroma_client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))

# Create or get collection
# Use a consistent collection name
collection_name = "documents"
collection = chroma_client.get_or_create_collection(name=collection_name)

# ---------------------------
# Initialize embedding model
# ---------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------------------------
# Helper function: store embeddings
# ---------------------------
def store_embeddings(chunks, metadata=None, doc_id=None):
    """
    Convert text chunks into embeddings and store in ChromaDB.
    Each chunk will have a unique id.
    """

    if not doc_id:
        doc_id = str(uuid.uuid4())

    # Encode embeddings
    embeddings = model.encode(chunks).tolist()

    # Generate unique IDs for each chunk
    chunk_ids = [f"{doc_id}_{i}" for i in range(len(chunks))]

    # Prepare metadata per chunk
    metadata = metadata or [{} for _ in chunks]
    for m in metadata:
        m["doc_id"] = doc_id

    # Add to Chroma collection
    collection.add(
        ids=chunk_ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadata
    )

    # Persist to disk
    #chroma_client.persist()

    return doc_id
