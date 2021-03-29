from pymemcache.client import base
from user import User
from order_stack import BidStack, OfferStack
from tradematcher.trade import do_trading 
from typing import List, Dict
from time import sleep

def extract_user(user_data):
    # type: (Dict)->User
    #{"shares":0, "cash":100, "bid":{"price":0, "quantity":0}, "offer":{"price":0, "quantity":0}}
    return User.from_json(user_data)
    

def read_users(cache):
    # type: (base.Client)->List[User]
    user_ids = cache.get("users") or []
    users = []
    for user_id in user_ids:
        user_data = cache.get(str(user_id))
        users.append(extract_user(user_data))
    return users

def write_users(cache, users):
    # type: (base.Client, List[User])->None
    for user in users:
        cache.set(str(user.id), str(user))


def main():
    while True:
        # connect to the database
        cache = base.Client(('127.0.0.1', 11211,))
        # gather the bids and offers
        users = read_users(cache)
        bid_stack = BidStack.from_user_list(users)
        offer_stack = OfferStack.from_user_list(users)
        do_trading(bid_stack, offer_stack)
        write_users(cache, users)
        # some kind of delay
        sleep(0.1)

if __name__=="__main__":
    main()
