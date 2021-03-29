import pytest
from matcher import (
    BidderCantAfford,
    OfferCantProvide,
    NeitherPartyValid,
    validate_trade,
    User,
    Bid,
    Offer,
)


def test_order():
    bids, offers
    order(bids, offers)

def test_match(bids, offers):
    bids, offers = order(bids, offers)
    match(bids, offers)


# It's all very well sketching out these tests but we
# need to come up with a structure for holding the
# orders

def test_trade():
    bid = Bid()
    offer = Offer()

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
