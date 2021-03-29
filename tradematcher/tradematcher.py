from order import Order, Bid, Offer
from order_stack import OrderStack, BidStack, OfferStack

class TradeMatcher:
    def __init__(self):
        self.bids = BidStack([])
        self.offers = OfferStack([])

    def making_trade_draft():
        # Match off from there

        # if the head of the queues aren't equal then
        # the price won't be equal
        try:
            while bids.top_price>=offers.top_price:
                #a sale can be made
                # Take the smaller of the two
                bid = bids.top
                offer = offers.top
                quantity = self.get_tradeable_quantity(bid, offer)
                price = self.get_price(bid, offer)
                self.validate_trade(bid.user, offer.user, price, qty)
                # The trade can go through 
                self.trade(bid, offer, price, qty)
        except EndOfOrders:
            print("Reached end of orders, awaiting more")
    
    @staticmethod
    def get_price(bid, offer):
        # type: (Bid, Offer)->int
        return (bid.price + offer.price) // 2

    @staticmethod
    def get_tradeable_quantity(bid, offer, qty=None):
        # type: (Bid, Offer, optional[int])->int
        # So this gives us something of a trade function
        # but I don't think we should be returning None on failed
        max_qty =min(bid.qty, offer.qty)
        if qty is None or qty>max_qty:
            qty = max_qty
        return qty

    @staticmethod
    def validate_trade(bid_user, offer_user, price, qty):
        # type: (User, User, int, int)->None
        if bid_user.cash < price * qty and offer_user.holding < qty:
            raise NeitherPartyValid("bid cash: %s, price: %s, holding qty: %s"%(
                bid_user.cash, price*qty, offer_user.holding))
        if bid_user.cash < price * qty:
            raise BidderCantAfford()
        if offer_user.holding < qty:
            raise OfferCantProvide()

    @staticmethod
    def trade(bid, offer, price, qty):
        # type: (User, User, int, int)->None
        bid.user.cash -= price * qty
        offer.user.cash += price * qty
        bid.user.holding += qty
        offer.user.holding -= qty
        bid.quantity -= qty
        offer.quantity -= qty
