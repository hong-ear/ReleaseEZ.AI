import asyncpg

DB_DSN = "postgresql://hongear@localhost:5432/fhirdb"

async def init_db(app):
    app.state.db = await asyncpg.create_pool(dsn=DB_DSN)

# app/models.py
from pydantic import BaseModel
from typing import List

class FHIRBundle(BaseModel):
    resourceType: str
    type: str
    entry: List[dict]
