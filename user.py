from typing import Union
import json


class User:
    def __init__(self):
        self.id = None
        self.cash = 0
        self.holding = 0
        self.bid_price = 0
        self.bid_quantity = 0
        self.offer_price = 0
        self.offer_quantity = 0

    @staticmethod
    def from_json(content):
        # type: (Union[dict, str])->User
        if isinstance(content, str):
            json_content = json.loads(content)  # type: dict
        elif isinstance(content, dict):
            json_content = content  # type: dict
        else:
            raise Exception("Not valid json content")
        user = User()
        user.id = json_content["user_id"]
        user.cash = json_content["cash"]
        user.holding = json_content["holding"]
        bid_content = json_content["bid"]
        user.bid_price = bid_content["price"]
        user.bid_quantity = bid_content["quantity"]
        offer_content = json_content["offer"]
        user.offer_price = offer_content["price"]
        user.offer_quantity = offer_content["quantity"]
        return user

    def __str__(self):
        return json.dumps({
            "user_id":self.id,
            "cash": self.cash,
            "holding": self.holding,
            "bid": {
                "price": self.bid_price,
                "quantity": self.bid_quantity},
            "offer": {
                "price": self.offer_price,
                "quantity": self.offer_quantity}
        })
