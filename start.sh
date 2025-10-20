#!/bin/bash
set -e

echo "🚀 Iniciando PostgreSQL (modo inicial)..."
service postgresql start
sleep 3

echo "🔧 Configurando autenticação temporária para trust..."
# Muda para trust temporariamente (sem senha)
sed -i "s/^local\s\+all\s\+postgres\s\+peer/local all postgres trust/" /etc/postgresql/*/main/pg_hba.conf
sed -i "s/^local\s\+all\s\+all\s\+peer/local all all trust/" /etc/postgresql/*/main/pg_hba.conf
service postgresql restart
sleep 3

echo "🔐 Definindo senha para o usuário postgres..."
psql -U postgres -c "ALTER USER postgres PASSWORD '1234';"

echo "🧩 Reativando autenticação segura (md5)..."
# Agora volta para modo seguro com senha md5
sed -i "s/^local\s\+all\s\+postgres\s\+trust/local all postgres md5/" /etc/postgresql/*/main/pg_hba.conf
sed -i "s/^local\s\+all\s\+all\s\+trust/local all all md5/" /etc/postgresql/*/main/pg_hba.conf
service postgresql restart
sleep 3

echo "🗃️ Criando banco e aplicando init_db.sql..."
PGPASSWORD=1234 psql -U postgres -h localhost -c "CREATE DATABASE simulador;" || true
PGPASSWORD=1234 psql -U postgres -h localhost -d simulador -f /app/init_db.sql

echo "✅ Banco configurado com sucesso!"
echo "📦 Iniciando API FastAPI na porta 8080..."
uvicorn app.main:app --host 0.0.0.0 --port 8080
