#!/bin/bash
set +e  # evita encerramento imediato se pg_isready ou psql falharem brevemente

echo "🚀 Iniciando processo de inicialização do container..."

# Dá um tempim para o RDS respirar e responder
sleep 10

# Carrega variáveis do .env
export $(grep -v '^#' .env | xargs)

echo "⏳ Aguardando conexão com banco RDS em $DB_HOST:$DB_PORT..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 3
done
echo "✅ Banco RDS acessível!"

# Testa se existem tabelas já criadas
TABLE_COUNT=$(psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" | xargs)

if [ "$TABLE_COUNT" -eq 0 ]; then
  echo "📦 Nenhuma tabela encontrada — aplicando init_db.sql..."
  psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -f init_db.sql
  echo "✅ Tabelas criadas com sucesso!"
else
  echo "📋 Tabelas já existentes — pulando criação..."
fi

echo "🚀 Iniciando API FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8080
