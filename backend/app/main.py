from fastapi import FastAPI
from app.routes import fhir
from app.db import init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_db(app)

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

app.include_router(fhir.router)