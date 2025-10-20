from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes

app = FastAPI(
    title="Simulador Monopoly",
    description="API de simulação de partidas baseada no desafio técnico (Banco Imobiliário simplificado).",
    version="1.0.0"
)

# Permitindo requisições locais de modo geral e testes via Swagger
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Inclusão das rotas da API
app.include_router(routes.router)

@app.get("/", tags=["Healthcheck"])
def root():
    return {"status": "ok", "message": "Simulador Monopoly ativo"}
