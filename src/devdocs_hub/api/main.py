from fastapi import FastAPI

from .routers import documents

app = FastAPI()
app.include_router(documents.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
