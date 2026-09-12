from fastapi import FastAPI
from sqlalchemy import create_engine

from devdocs_hub.db.core import emit_ddl
from .routers import documents

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
emit_ddl(engine)

app = FastAPI()
app.include_router(documents.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
