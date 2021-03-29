from order import Order, Bid, Offer
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
