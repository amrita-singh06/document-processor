from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from config import CHROMA_DB_DIR
from chromadb import Client

model = SentenceTransformer("all-MiniLM-L6-v2")

#chroma_client = chromadb.Client(Settings(chroma_db_impl="sqlite", persist_directory=CHROMA_DB_DIR))
#chroma_client = Client(persist_directory=CHROMA_DB_DIR)
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)


collection = chroma_client.get_or_create_collection(name="documents")

def generate_and_store_embedding(doc_id, text):
    embedding = model.encode(text)
    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[str(doc_id)]
    )
