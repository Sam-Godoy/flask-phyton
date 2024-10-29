class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        # Validación de tipos: convierte a float e int
        self.price = float(price) if price else 0.0
        self.quantity = int(quantity) if quantity else 0

    def toDBCollection(self):
        return {
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity
        }
