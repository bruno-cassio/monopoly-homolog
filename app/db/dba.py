from app.db.database import SessionLocal
from app.db import models
from sqlalchemy.orm import Session

class DBA:
    """Camada de acesso ao banco (Data Access Layer)"""

    def __init__(self):
        self.db: Session = SessionLocal()

    def get_active_players(self):
        """Retorna todos os jogadores ativos"""
        return self.db.query(models.PlayerProfile).filter(models.PlayerProfile.active == True).all()

    def get_board_properties(self):
        """Retorna todas as propriedades do tabuleiro"""
        return self.db.query(models.BoardProperty).order_by(models.BoardProperty.position).all()

    def create_game_log(self, status="RUNNING"):
        log = models.GameLog(status=status)
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log.id

    def update_game_log(self, log_id, **kwargs):
        self.db.query(models.GameLog).filter(models.GameLog.id == log_id).update(kwargs)
        self.db.commit()

    def save_round_snapshot(self, game_id, round_number, summary):
        round_rec = models.GameRound(
            game_id=game_id,
            round_number=round_number,
            summary=summary
        )
        self.db.add(round_rec)
        self.db.commit()

    def create_game_result(self, log_id):
        result = models.GameResult(log_id=log_id)
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        return result.id

    def update_game_result(self, game_id, **kwargs):
        self.db.query(models.GameResult).filter(models.GameResult.id == game_id).update(kwargs)
        self.db.commit()

    def close(self):
        self.db.close()
