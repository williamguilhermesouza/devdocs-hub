from contextlib import asynccontextmanager

from fastapi import FastAPI

from devdocs_hub.rag.embeddings import get_embedding_provider

from .routers import documents

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model before accepting requests; dependencies reuse this instance.
    get_embedding_provider()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(documents.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
