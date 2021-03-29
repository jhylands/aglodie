class OrderStack:
    def __init__(self, orders):
        self.orders = orders
        self.sorted = False

    @property
    def top(self):
        if not self.sorted:
            self.sort()
        for top_item in self.orders:
            if top_item.quantity>0:
                return top_item
            else:
                self.orders.remove(top_item)
        # No items left
        raise Exception("No items left")

    @property
    def top_price(self):
        self.top.price

    def sort(self):
        raise Exception("Not overwritten")

class BidStack(OrderStack):
    def sort(self):
        sorted(self.orders, key=lambda x:x.price)
        self.sorted = True

class OfferStack(OrderStack):
    def sort(self):
        sorted(self.orders, key=lambda x:x.price, reverse=True)
        self.sorted = True
