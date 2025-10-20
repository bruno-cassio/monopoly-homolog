class StatsCalculator:
    @staticmethod
    def compute_player_stats(players):
        """Retorna resumo estatístico dos jogadores ao fim do jogo"""
        results = []
        for p in players:
            results.append({
                "nome": p.name,
                "saldo_final": round(p.balance, 2),
                "propriedades": len(p.properties),
                "ativo": p.active,
                "gasto_total": p.stats["total_spent"],
                "ganho_total": p.stats["total_earned"],
            })
        return results
