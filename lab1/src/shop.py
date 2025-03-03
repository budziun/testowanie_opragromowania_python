class ShoppingCart:

    def __init__(self):
        self.items = {}
    def add_item(self, item_name: str,price: float,quantity: int = 1):
        if item_name in self.items:
            self.items[item_name]['quantity'] += quantity
        else:
            self.items[item_name] = {'price': price, 'quantity': quantity}

    def remove_item(self,item_name: str,quantity: int = None):
        if item_name in self.items:
            if quantity is None or quantity >= self.items[item_name]['quantity']:
                del self.items[item_name]
            else:
                self.items[item_name]['quantity'] -= quantity

    def get_total(self) -> float:
        return sum(item['price'] * item['quantity'] for item in self.items.values())

    def clear(self):
        self.items.clear()