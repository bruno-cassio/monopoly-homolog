#!/bin/bash
set -e  # encerra o script se algo der errado

echo "🚀 Iniciando processo de inicialização do container..."

# Aguarda o RDS ficar pronto
sleep 10

# Carrega variáveis do .env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
  echo "✅ Variáveis de ambiente carregadas"
else
  echo "⚠️ Arquivo .env não encontrado — prosseguindo com variáveis do ambiente"
fi

echo "⏳ Aguardando conexão com banco RDS em $DB_HOST:$DB_PORT..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1; do
  echo "🕐 Ainda aguardando banco..."
  sleep 3
done
echo "✅ Banco RDS acessível!"

# Verifica se o schema public tem tabelas
TABLE_COUNT=$(psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -t -c \
"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" | xargs)

if [ "$TABLE_COUNT" -eq 0 ]; then
  echo "📦 Nenhuma tabela encontrada — aplicando init_db.sql..."
  psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -f init_db.sql
  echo "✅ Tabelas criadas com sucesso!"
else
  echo "📋 Tabelas já existentes — pulando criação..."
fi

echo "🚀 Iniciando API FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8080
