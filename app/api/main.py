"""
DraftVision API - Plataforma de análise estratégica de LoL.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.players.routes import router as players_router

app = FastAPI(
    title="DraftVision API",
    description="Análise estratégica de jogadores e times de League of Legends",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "DraftVision API", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(players_router)
