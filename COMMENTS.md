---


## Objetivo da entrega

Este projeto implementa o **desafio técnico do jogo tipo Banco Imobiliário**, buscando atender todos os requisitos propostos pelo desafio:

- **API HTTP documentada via Swagger**
- **Persistência de dados com PostgreSQL**
- **Teste local via Docker (API + DB no mesmo container)**
- **Arquitetura limpa e modular (core separado da API)**
- **Logs e auditoria de partidas armazenados em banco**

---

---

## Estrutura de execução

O ambiente é criado automaticamente dentro do container:

1. O script `start.sh` inicializa o PostgreSQL
2. Define senha segura (`1234`) para o usuário `postgres`
3. Cria o banco `simulador` e aplica o `init_db.sql`
4. Inicializa a API na porta `8080`

---

## Organização Arquitetura

| Módulo         | Responsabilidade                                                            |
| --------------- | --------------------------------------------------------------------------- |
| `core/`       | Simula o jogo, processa rodadas, avalia saldo e comportamento dos jogadores |
| `db/`         | Modelos e conexão SQLAlchemy com PostgreSQL                                |
| `api/`        | Exposição dos endpoints REST via FastAPI                                  |
| `main.py`     | Inicialização da aplicação                                              |
| `start.sh`    | Automação de setup do ambiente Docker                                     |
| `init_db.sql` | Criação das tabelas e inserção dos dados base                           |

---

## Endpoint principal

### `POST /jogo/simular`

Executa uma simulação completa de jogo.

**Exemplo de resposta:**

```json
{
  "vencedor": "exigente",
  "jogadores": ["exigente", "impulsivo", "aleatorio", "cauteloso"]
}
```

## Execução e interpretação dos resultados

Ao executar o endpoint `POST /jogo/simular`, o sistema inicia uma simulação completa do jogo com os quatro perfis de jogadores:

- Impulsivo
- Exigente
- Cauteloso
- Aleatório

Durante a simulação:

1. Cada jogador começa com **saldo inicial de 300**.
2. O tabuleiro possui **20 propriedades**, com preços e aluguéis variados.
3. Os jogadores se alternam jogando o dado (1 a 6) e movendo-se pelo tabuleiro.
4. Se cair em uma propriedade **sem dono**, ele pode comprar conforme seu perfil de decisão.
5. Se cair em uma propriedade **com dono**, ele paga o aluguel ao proprietário.
6. Ao completar uma volta no tabuleiro, o jogador recebe **100** de bônus.
7. Se o saldo ficar **negativo**, o jogador é **eliminado** e perde suas propriedades, que voltam a estar disponíveis.

O jogo termina quando:

- Restar **apenas um jogador ativo** (saldo positivo), ou
- For atingido o limite de **1000 rodadas** (vencedor é quem tiver maior saldo).

---

## Exemplo detalhado de saída

```json
{
  "vencedor": "Impulsivo",
  "rodadas": 23,
  "jogadores": [
    {
      "nome": "Exigente",
      "saldo_final": -5,
      "propriedades": 2,
      "ativo": false,
      "gasto_total": 790,
      "ganho_total": 285
    },
    {
      "nome": "Cauteloso",
      "saldo_final": -75,
      "propriedades": 2,
      "ativo": false,
      "gasto_total": 445,
      "ganho_total": 70
    },
    {
      "nome": "Impulsivo",
      "saldo_final": 260,
      "propriedades": 6,
      "ativo": true,
      "gasto_total": 1305,
      "ganho_total": 765
    },
    {
      "nome": "Aleatório",
      "saldo_final": -60,
      "propriedades": 1,
      "ativo": false,
      "gasto_total": 460,
      "ganho_total": 0
    }
  ]
}
```

---

### Como interpretar o resultado

- **"vencedor"**: jogador que encerrou o jogo com saldo positivo ou maior saldo no caso de empate.
- **"rodadas"**: quantidade total de rodadas até o encerramento (ou 1000 no limite).
- **"jogadores"**: lista completa dos quatro perfis, incluindo:
  - `saldo_final`: dinheiro restante ao final.
  - `propriedades`: total de propriedades possuídas.
  - `ativo`: indica se o jogador ainda estava ativo ao final.
  - `gasto_total`: total gasto com compras e aluguéis.
  - `ganho_total`: total recebido com aluguéis e bônus por volta no tabuleiro.

Os saldos negativos indicam jogadores **eliminados durante a simulação**, conforme a regra do desafio:

> Um jogador que fica com saldo negativo perde o jogo e suas propriedades retornam ao tabuleiro.

---

### Detalhamento técnico

Os resultados da simulação são persistidos no banco de dados:

- `game_result`: resumo de cada partida executada.
- `player_stats`: estatísticas individuais de cada jogador.
- `game_log`: auditoria da execução da simulação.

Essas tabelas permitem acompanhar o histórico de jogos e validar a consistência do comportamento do simulador.
