from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .presentation.routers.municipios_router import router as municipios_router
from .presentation.routers.periodos_router import router as periodos_router
from .presentation.routers.evolucao_router import router as evolucao_router
from .presentation.routers.eventos_router import router as eventos_router

app = FastAPI(
    title="Painel Cesta Básica — API",
    version="1.0.0",
    description="API REST para análise de preços da cesta básica no Brasil.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(municipios_router, prefix="/api")
app.include_router(periodos_router, prefix="/api")
app.include_router(evolucao_router, prefix="/api")
app.include_router(eventos_router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}
