from tradematcher.user import User
from tradematcher.order import Bid, Offer

def test_user_from_json():
    json_content = """
{"user_id": 1, "holding":0, "cash":100, "bid":{"price":0, "quantity":0}, "offer":{"price":0, "quantity":0}}
    """
    user = User.from_json(json_content)
    assert user.id == 1
    assert user.cash == 100
    assert user.holding == 0
    assert isinstance(user.bid, Bid)
    assert isinstance(user.offer, Offer)
