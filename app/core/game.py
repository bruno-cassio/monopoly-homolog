import random
from app.core.player import Impulsivo, Exigente, Cauteloso, Aleatorio
from app.core.board import Board
from app.db.dba import DBA

class Game:
    def __init__(self):
        self.dba = DBA()
        self.max_rounds = 1000
        self.rounds = []
        self.players = []
        self.board = None
        self.active_players = 0

    def setup(self):
        """Carrega jogadores e propriedades do banco"""
        db_players = self.dba.get_active_players()
        db_props = self.dba.get_board_properties()

        # Cria objetos jogadores conforme comportamento
        for p in db_players:
            if p.behavior_type == "impulsivo":
                self.players.append(Impulsivo(p.name, p.behavior_type))
            elif p.behavior_type == "exigente":
                self.players.append(Exigente(p.name, p.behavior_type))
            elif p.behavior_type == "cauteloso":
                self.players.append(Cauteloso(p.name, p.behavior_type))
            else:
                self.players.append(Aleatorio(p.name, p.behavior_type))

        # Embaralha ordem inicial (definida aleatoriamente)
        random.shuffle(self.players)
        self.active_players = len(self.players)

        # Monta tabuleiro
        self.board = Board(db_props)

    def run(self):
        """Executa a simulação completa"""
        self.setup()
        round_count = 0
        game_id = self.dba.create_game_result(self.dba.create_game_log())

        while round_count < self.max_rounds and self.active_players > 1:
            round_count += 1
            round_events = []

            for player in list(self.players):
                if not player.active:
                    continue

                dice = random.randint(1, 6)
                old_position = player.position
                player.move(dice, len(self.board.spaces))
                current_property = self.board.get_property(player.position)

                # Verifica a casa
                if current_property.owner is None:
                    if player.decide_purchase(current_property):
                        player.buy(current_property)
                        action = f"comprou {current_property.name}"
                    else:
                        action = f"não comprou {current_property.name}"

                elif current_property.owner != player:
                    rent = current_property.rent_price
                    player.pay(rent)
                    current_property.owner.receive(rent)
                    action = f"pagou aluguel em {current_property.name}"

                else:
                    action = f"passou pela própria propriedade {current_property.name}"

                player.stats["turns_survived"] += 1
                round_events.append({
                    "player": player.name,
                    "action": action,
                    "position": player.position,
                    "balance": player.balance
                })

                # Verifica quebra
                if player.balance < 0:
                    player.active = False
                    self.active_players -= 1
                    for prop in player.properties:
                        prop.reset_owner()
                    action += " e faliu!"

            # Salva rodada
            self.dba.save_round_snapshot(game_id, round_count, {"events": round_events})

        # Fim do jogo
        winner = max(
            [p for p in self.players if p.active],
            key=lambda x: x.balance,
            default=None
        )
        self.dba.update_game_result(
            game_id,
            total_rounds=round_count,
            winner_id=None,
            finished_reason="LIMIT" if round_count == self.max_rounds else "BANKRUPTCY",
            status="FINISHED"
        )

        self.dba.update_game_log(
            log_id=self.dba.get_active_players()[0].id,  # simplificado
            status="FINISHED",
            winner=winner.name if winner else "Empate"
        )

        return {
            "vencedor": winner.name if winner else "Empate",
            "rodadas": round_count,
            "jogadores": [
                {"nome": p.name, "saldo": p.balance, "ativo": p.active}
                for p in self.players
            ]
        }
