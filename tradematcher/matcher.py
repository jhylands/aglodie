from pymemcache.client import base
from collections import namedtuple

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


class BidderCantAfford(Exception):
    pass

class OfferCantProvide(Exception):
    pass

class NeitherPartyValid(Exception):
    pass

    


def main():
    while True:
        # connect to the database
        cache = base.Client(('127.0.0.1', 11211,))
        # gather the bids and offers

        # if any match match them

if __name__=="__main__":
    main()
