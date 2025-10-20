from fastapi import APIRouter, HTTPException
from app.core.game import Game
from app.core.stats import StatsCalculator

router = APIRouter()

@router.post("/jogo/simular", tags=["Simulação"])
def simular_partida():
    """
    Executa a simulação completa de uma partida.
    Retorna o vencedor e o ranking final dos jogadores.
    """
    try:
        game = Game()
        resultado = game.run()

        stats = StatsCalculator.compute_player_stats(game.players)
        response = {
            "vencedor": resultado["vencedor"],
            "rodadas": resultado["rodadas"],
            "jogadores": stats
        }
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao simular partida: {str(e)}")


@router.get("/jogo/health", tags=["Healthcheck"])
def health_check():
    """Verifica se a API está ativa"""
    return {"status": "ok", "service": "simulador", "version": "1.0.0"}
