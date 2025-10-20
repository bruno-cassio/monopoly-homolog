import random

class Player:
    def __init__(self, name: str, behavior: str, balance: float = 300):
        self.name = name
        self.behavior = behavior
        self.balance = balance
        self.position = 0
        self.properties = []
        self.active = True
        self.stats = {
            "rents_paid": 0,
            "rents_received": 0,
            "total_spent": 0,
            "total_earned": 0,
            "turns_survived": 0,
        }

    def move(self, steps: int, board_size: int):
        """Move o jogador no tabuleiro"""
        self.position = (self.position + steps) % board_size
        if self.position + steps >= board_size:
            self.balance += 100  # completou uma volta

    def pay(self, amount: float):
        self.balance -= amount
        self.stats["total_spent"] += amount

    def receive(self, amount: float):
        self.balance += amount
        self.stats["total_earned"] += amount

    def buy(self, property_obj):
        self.balance -= property_obj.purchase_price
        self.properties.append(property_obj)
        property_obj.owner = self
        self.stats["total_spent"] += property_obj.purchase_price

    def decide_purchase(self, property_obj):
        """Método polimórfico (implementado nas subclasses)"""
        raise NotImplementedError


class Impulsivo(Player):
    def decide_purchase(self, property_obj):
        return self.balance >= property_obj.purchase_price


class Exigente(Player):
    def decide_purchase(self, property_obj):
        return self.balance >= property_obj.purchase_price and property_obj.rent_price > 50


class Cauteloso(Player):
    def decide_purchase(self, property_obj):
        return (self.balance - property_obj.purchase_price) >= 80


class Aleatorio(Player):
    def decide_purchase(self, property_obj):
        return self.balance >= property_obj.purchase_price and random.choice([True, False])
