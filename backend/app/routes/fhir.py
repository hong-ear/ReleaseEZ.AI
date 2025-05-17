import json

from fastapi import APIRouter, Request
from uuid import uuid4
from app.models import FHIRBundle
from app.services import simplify_discharge

router = APIRouter()

@router.post("/fhir/bundle")
async def receive_fhir_bundle(bundle: FHIRBundle, request: Request):
    raw_id = str(uuid4())
    simplified_id = str(uuid4())

    async with request.app.state.db.acquire() as conn:
        await conn.execute(
            "INSERT INTO raw_bundles (id, bundle) VALUES ($1, $2)", 
            raw_id, 
            json.dumps(bundle.dict())  # serialize to JSON string
        )

    simplified_result = await simplify_discharge(bundle.dict())

    async with request.app.state.db.acquire() as conn:
        await conn.execute(
            "INSERT INTO simplified_bundles (id, raw_id, simplified) VALUES ($1, $2, $3)",
            simplified_id,
            raw_id,
            json.dumps(simplified_result)  # serialize to JSON string
        )
    return {"status": "stored", "raw_id": raw_id, "simplified_id": simplified_id}

@router.get("/doctor/{raw_id}")
async def get_doctor_view(raw_id: str, request: Request):
    async with request.app.state.db.acquire() as conn:
        raw = await conn.fetchrow("SELECT bundle FROM raw_bundles WHERE id = $1", raw_id)
        simplified = await conn.fetchrow("SELECT simplified FROM simplified_bundles WHERE raw_id = $1", raw_id)
    return {"raw": raw["bundle"], "simplified": simplified["simplified"]}

@router.get("/patient/{simplified_id}")
async def get_patient_view(simplified_id: str, request: Request):
    async with request.app.state.db.acquire() as conn:
        result = await conn.fetchrow("SELECT simplified FROM simplified_bundles WHERE id = $1", simplified_id)
    return result["simplified"]