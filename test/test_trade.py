from tradematcher.trade import (
    validate_trade,
    BidderCantAfford,
    OfferCantProvide,
    NeitherPartyValid,
    get_price,
)
from user import User
from order import Bid, Offer
import pytest


@pytest.mark.parametrize("bid, offer", [
(Bid(), Offer())
])
def test_get_price(bid, offer):
    price = get_price(bid, offer)
    assert isinstance(price, int)
    assert price < bid.price + offer.price


def test_get_tradebale_quantity(bid, offer):
    pass

def test_validate_trade():
    # 3 test cases
    # - Trade can go through
    # - Bidder cannot afford
    # - Offerer cannot provide
    # - Neither can provide
    bid_user_content = """
{"user_id": 1, "holding":0, "cash":100, "bid":{"price":3, "quantity":1}, "offer":{"price":0, "quantity":0}}
    """
    offer_user_content = """
{"user_id": 2, "holding":1, "cash":100, "bid":{"price":0, "quantity":0}, "offer":{"price":1, "quantity":1}}
    """
    price = 2 
    quantity = 1

    # BOTH VALID
    bid_user = User.from_json(bid_user_content)
    offer_user = User.from_json(offer_user_content)

    validate_trade(bid_user, offer_user, price, quantity)

    # BIDDER CANNOT AFFORD
    bid_user = User.from_json(bid_user_content)
    bid_user.cash = 0
    offer_user = User.from_json(offer_user_content)

    with pytest.raises(BidderCantAfford):
        validate_trade(bid_user, offer_user, price, quantity)


    # OFFERER CANNOT PROVIDE
    bid_user = User.from_json(bid_user_content)
    offer_user = User.from_json(offer_user_content)
    offer_user.holding = 0

    with pytest.raises(OfferCantProvide):
        validate_trade(bid_user, offer_user, price, quantity)

    # NEITHER VALID
    bid_user = User.from_json(bid_user_content)
    offer_user = User.from_json(offer_user_content)
    bid_user.cash=0
    offer_user.holding=0

    with pytest.raises(NeitherPartyValid):
        validate_trade(bid_user, offer_user, price, quantity)
