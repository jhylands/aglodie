from tradematcher.order import Order, Bid, Offer
from user import User
import pytest

def test_user_can_bid():
    user = User()
    user.bid_price = 10
    user.bid_quantity = 10
    user.cash = 0
    assert Bid.user_can_bid(user) is False
    user = User()
    user.bid_price = 10
    user.bid_quantity = 10
    user.cash = 100
    assert Bid.user_can_bid(user) is True

def test_user_can_offer():
    user = User()
    user.offer_price = 10
    user.offer_quantity = 10
    user.holding = 9
    assert Offer.user_can_offer(user) is False
    user = User()
    user.offer_price = 10
    user.offer_quantity = 10
    user.holding = 10
    assert Offer.user_can_offer(user) is True
