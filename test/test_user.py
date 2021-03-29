from user import User
import json

def test_user_from_json():
    json_content = """
{"user_id": 1, "holding":0, "cash":100, "bid":{"price":0, "quantity":0}, "offer":{"price":0, "quantity":0}}
    """
    user = User.from_json(json_content)
    assert user.id == 1
    assert user.cash == 100
    assert user.holding == 0
    assert user.bid_price == 0
    assert user.bid_quantity == 0
    assert user.offer_price == 0
    assert user.offer_quantity == 0

def test_user_to_json():
    user = User()
    user.id = 1
    user.cash = 100
    user.holding = 10
    user.bid_price = 1
    user.bid_quantity = 1
    user.offer_price = 1
    user.offer_quantity = 0
    user_dict = json.loads(str(user))
    assert user_dict["user_id"] == 1
    assert user_dict["cash"] == 100
    assert user_dict["holding"] == 10
    assert user_dict["bid"]["price"] == 1
    assert user_dict["bid"]["quantity"] == 1
    assert user_dict["offer"]["price"] == 1
    assert user_dict["offer"]["quantity"] == 0
