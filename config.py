import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "storage", "documents")
CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")
SQLITE_DB_PATH = os.path.join(BASE_DIR, "db", "documents.db")

os.makedirs(STORAGE_DIR, exist_ok=True)
