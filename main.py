from fastapi import FastAPI
from api import upload
from db.models import init_db

app = FastAPI(title="Document Upload and Embedding API")

app.include_router(upload.router)

@app.on_event("startup")
def startup():
    init_db()
