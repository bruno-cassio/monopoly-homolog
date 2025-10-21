# Imagem base leve com cliente PostgreSQL
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
 && rm -rf /var/lib/apt/lists/*

# Criar diretório da aplicação
WORKDIR /app

# Copiar apenas requirements primeiro (melhora cache)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código
COPY . .

# Permissão de execução do start.sh
RUN chmod +x start.sh

# Variáveis e porta
ENV PYTHONUNBUFFERED=1
EXPOSE 8080

# Comando de inicialização
CMD ["bash", "start.sh"]
