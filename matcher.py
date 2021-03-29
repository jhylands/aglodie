from pymemcache.client import base
from collections import namedtuple
import json

class User:
    def __init__(self):
        self.id = None
        self.cash = 0
        self.holding = 0
        self.bid = None
        self.offer = None

    @staticmethod
    def from_json(json_content):
        if isinstance(json_content, str):
            json_content = json.loads(json_content)
        elif isinstance(json_content, dict):
            pass
        else:
            raise Exception("Not valid json content")
        user = User()
        user.id = json_content["user_id"]
        user.cash = json_content["cash"]
        user.holding = json_content["holding"]
        bid_content = json_content["bid"]
        user.bid = Bid(user, bid_content["price"], bid_content["quantity"])
        offer_content = json_content["offer"]
        user.offer = Offer(user, offer_content["price"], offer_content["quantity"])
        return user

class Order:
    def __init__(self, user, price, quantity):
        self.user = user
        self.price = price
        self.quantity = quantity

class Bid(Order):
    pass

class Offer(Order):
    pass

class BidderCantAfford(Exception):
    pass

class OfferCantProvide(Exception):
    pass

class NeitherPartyValid(Exception):
    pass

def validate_trade(bid_user, offer_user, price, qty):
    # type: (User, User, int, int)->None
    if bid_user.cash < price * qty and offer_user.holding < qty:
        raise NeitherPartyValid("bid cash: %s, price: %s, holding qty: %s"%(
            bid_user.cash, price*qty, offer_user.holding))
    if bid_user.cash < price * qty:
        raise BidderCantAfford()
    if offer_user.holding < qty:
        raise OfferCantProvide()

def trade(bid, offer, qty=None):
    # type: (Bid, Offer, optional[int])->int
    # So this gives us something of a trade function
    # but I don't think we should be returning None on failed
    max_qty =min(bid.qty, offer.qty)
    if qty is None or qty>max_qty:
        qty = max_qty
    price = (bid.price + offer.price) // 2
    validate_trade(bid.user, offer.user, price, qty)
    # The trade can go through 
    bid.user.cash -= price * qty
    offer.user.cash += price * qty
    bid.user.holding += qty
    offer.user.holding -= qty
    return price


def extract_bid(user_data):
    # type: (Dict)->Tuple[Bid, Bid]
    #{"shares":0, "cash":100, "bid":{"price":0, "quantity":0}, "offer":{"price":0, "quantity":0}}
    bid_quantity = user_data["bid"]["quantity"]
    bid_price = user_data["bid"]["price"]
    offer_quantity = user_data["offer"]["quantity"]
    offer_price = user_data["offer"]["price"]
    return Bid(bid_price, bid_quantity), Bid(offer_price, offer_quantity)
    

def extract_bids(cache):
    users = cache.get("users") or []
    for user in users:
        user_data = cache.get(str(user))
        bid, offer = extract_bid(user_data)
    
    return bids



def making_trade_draft():
    # sort bids lowest first
    # sort offers highest first
    # Match off from there

    sort(bids, key=lambda x:x.price)
    sort(offers, key=lambda x:x.price, reverse=True)
    # if the head of the queues aren't equal then
    # the price won't be equal
    if bids[0].price>=offers[0].price:
        #a sale can be made
        # Take the smaller of the two
        if bid[0].quantity == offers[0].quantity:
            trade(bid.pop(), offer.pop())
        elif bid[0].quantity > offers[0].quantity:
            trade(bid[0].quantity - offers[0].quantity)
            offers.pop()
        else:
            trade(offers[0].quantity - bid[0].quantity)
            bid.pop()
    


def main():
    while True:
        # connect to the database
        cache = base.Client(('127.0.0.1', 11211,))
        # gather the bids and offers

        # if any match match them

if __name__=="__main__":
    main()
