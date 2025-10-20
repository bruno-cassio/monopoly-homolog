# Simulador Monopoly - Desafio Técnico

Este projeto é uma implementação de um simulador simplificado de um jogo do tipo Banco Imobiliário, desenvolvido em Python com FastAPI e PostgreSQL.
O objetivo é permitir a execução de partidas automatizadas entre quatro perfis de jogadores, conforme as regras propostas no desafio técnico.

---

## Objetivo

Implementar uma API HTTP capaz de simular partidas de um jogo de tabuleiro, registrar resultados e expor o vencedor e o ranking final via Swagger.

---

## Tecnologias utilizadas

- Python 3.11
- FastAPI
- PostgreSQL 17
- SQLAlchemy
- Docker
- Swagger (documentação automática)

---

## Estrutura de execução

O ambiente é criado automaticamente dentro do container Docker:

1. O script `start.sh` inicializa o PostgreSQL.
2. Define a senha segura (`1234`) para o usuário `postgres`.
3. Cria o banco `simulador` e aplica o `init_db.sql`.
4. Inicializa a API na porta `8080`.

Não é necessário instalar dependências locais, apenas o Docker.

---

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/seuusuario/monopoly-homolog.git
cd monopoly-homolog
```

### 2. Construir a imagem Docker

```bash
docker build -t monopoly-homolog .
```

### 3. Executar o container

```bash
docker run -p 8080:8080 monopoly-homolog
```

A API será iniciada automaticamente e ficará disponível na porta **8080**.

---

## Acessando a API

### Documentação Swagger

Abra no navegador:

```
http://localhost:8080/docs
```

### Endpoint principal

```
POST /jogo/simular
```

Executa uma simulação completa de jogo e retorna o vencedor e o ranking final.

Exemplo de resposta:

```json
{
  "vencedor": "exigente",
  "jogadores": ["exigente", "impulsivo", "aleatorio", "cauteloso"]
}
```

---

## Estrutura do projeto

| Diretório / Arquivo | Descrição                             |
| -------------------- | --------------------------------------- |
| `app/api`          | Rotas HTTP e endpoints da API           |
| `app/core`         | Lógica do jogo e engine de simulação |
| `app/db`           | Conexão e modelos SQLAlchemy           |
| `init_db.sql`      | Criação do banco e dados iniciais     |
| `start.sh`         | Script de inicialização do container  |
| `Dockerfile`       | Definição da imagem Docker            |
| `.env`             | Configurações de ambiente             |

---

## Variáveis de ambiente (.env)

O arquivo `.env` contém as configurações básicas do banco e API:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=simulador
DB_USER=postgres
DB_PASSWORD=1234
API_PORT=8080
```

---

## Autor

**Bruno Cássio Chiaca**
Desenvolvedor Python / FastAPI / RPA / Cloud AWS
