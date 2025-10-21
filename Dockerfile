# Imagem base
FROM python:3.11-slim

# Instalando dependências do sistema (desde raiz à inners)
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*


# Cria diretório da aplicação
WORKDIR /app

# Copia arquivos do projeto
COPY . /app

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1

# Copia script de inicialização
RUN chmod +x /app/start.sh

# Expõe porta da API
EXPOSE 8080

# Comando padrão de inicialização
CMD ["/bin/bash", "/app/start.sh"]
