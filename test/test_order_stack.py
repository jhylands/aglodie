from tradematcher.order_stack import BidStack, OfferStack
from user import User

def test_bid_from_user_list():
    bid_user = User()
    bid_user.bid_price = 10
    bid_user.bid_quantity = 1
    bid_user.cash = 100
    bid_user.holding = 0
    offer_user = User()
    offer_user.offer_price = 11
    offer_user.offer_quantity = 1
    offer_user.cash = 100
    offer_user.holding = 10
    bids = BidStack.from_user_list([bid_user, offer_user])
    print(bids)

    assert bids.top_price == 10
    assert bids.top.quantity == 1

def test_offer_from_user_list():
    bid_user = User()
    bid_user.bid_price = 10
    bid_user.bid_quantity = 1
    bid_user.cash = 100
    bid_user.holding = 0
    offer_user = User()
    offer_user.offer_price = 11
    offer_user.offer_quantity = 1
    offer_user.cash = 100
    offer_user.holding = 10
    offers = OfferStack.from_user_list([bid_user, offer_user])
    print(offers)

    assert offers.top_price == 11
    assert offers.top.quantity == 1
