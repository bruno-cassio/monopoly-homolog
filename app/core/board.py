from app.core.property import Property

class Board:
    def __init__(self, db_properties):
        """db_properties = lista de objetos BoardProperty vindos do banco"""
        self.spaces = [
            Property(
                id=p.id,
                name=p.name,
                purchase_price=float(p.purchase_price),
                rent_price=float(p.rent_price)
            )
            for p in db_properties
        ]

    def get_property(self, position: int):
        return self.spaces[position]
