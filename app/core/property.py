class Property:
    def __init__(self, id, name, purchase_price, rent_price):
        self.id = id
        self.name = name
        self.purchase_price = purchase_price
        self.rent_price = rent_price
        self.owner = None

    def reset_owner(self):
        self.owner = None
