from user import User


class Order:
    def __init__(self, user, price, quantity):
        # type: (User, int, int)->None
        self.user = user
        self.price = price
        self.quantity = quantity

    @staticmethod
    def from_user(user):
        # type: (User)->Order
        raise Exception("Not overwritten")


class Bid(Order):

    @staticmethod
    def user_can_bid(user):
        return user.bid_quantity>0 and user.cash>user.bid_quantity*user.bid_price

    @staticmethod
    def from_user(user):
        # type: (User)->Bid
        return Bid(user, user.bid_price, user.bid_quantity)


class Offer(Order):
    @staticmethod
    def user_can_offer(user):
        return user.offer.quantity>0 and user.holding>user.offer.quantity

    @staticmethod
    def from_user(user):
        # type: (User)->Offer
        return Offer(user, user.offer.price, user.offer.quantity)
