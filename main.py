from fastapi import FastAPI
from api.upload import router as upload_router
from api.ingest import router as ingest_router
from api.query import router as query_router


app = FastAPI(title="Document Processor API")

# Register routers
app.include_router(upload_router)
app.include_router(ingest_router)
app.include_router(query_router)


@app.get("/")
def root():
    return {"message": "Welcome to Document Processor API"}
