#!/bin/bash
set -e

echo "🏗️ Iniciando ambiente da aplicação Monopoly..."

# Espera o RDS estar acessível
echo "⏳ Aguardando disponibilidade do banco de dados externo..."
sleep 10

# Testa conexão com o banco RDS
python - <<'EOF'
import psycopg2, os, time
for i in range(10):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        print("✅ Banco acessível, prosseguindo para inicialização.")
        conn.close()
        break
    except Exception as e:
        print(f"❌ Tentativa {i+1}/10 - Banco indisponível: {e}")
        time.sleep(5)
EOF

# Inicializa o banco apenas se ele ainda não tiver tabelas
python - <<'EOF'
from app.db import models
from app.db.database import engine, Base
print("🧩 Criando estrutura de tabelas, se ainda não existir...")
Base.metadata.create_all(bind=engine)
EOF

# Inicia a aplicação FastAPI
echo "🚀 Iniciando API FastAPI na porta 8080..."
uvicorn app.main:app --host 0.0.0.0 --port 8080
