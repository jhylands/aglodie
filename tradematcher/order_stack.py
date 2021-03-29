from typing import List
from tradematcher.order import Order, Offer, Bid
from user import User

class EndOfOrders(Exception):
    pass


class OrderStack:
    def __init__(self, orders):
        # type: (List[Order])
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
        raise EndOfOrders("No items left")

    @property
    def top_price(self):
        return self.top.price

    def sort(self):
        raise Exception("Not overwritten")

    def __str__(self):
        return str(self.orders)


class BidStack(OrderStack):
    def sort(self):
        sorted(self.orders, key=lambda x:x.price)
        self.sorted = True

    @staticmethod
    def from_user_list(users):
        # type: (List[User])->BidStack
        return BidStack([Bid.from_user(user) for user in users if Bid.user_can_bid(user)])

class OfferStack(OrderStack):
    def sort(self):
        sorted(self.orders, key=lambda x:x.price, reverse=True)
        self.sorted = True

    @staticmethod
    def from_user_list(users):
        # type: (List[User])->BidStack
        return OfferStack([Offer.from_user(user) for user in users if Offer.user_can_offer(user)])
