import random
import math


diceRoll = lambda: random.randint(1, 6)

class Company:
    def __init__(self):
        self.wealth = 10

    def bet(self):
        pass
        #return (guess, bet)

class Fixed(Company):
    def __init__(self, fixed_on):
        super(Fixed, self).__init__()
        self.fixed_on = fixed_on

    def bet(self):
        return (math.floor(self.wealth/10)+1, self.fixed_on)


class Iterator(Company):
    def __init__(self):
        super(Iterator, self).__init__()
        self.guess = 1

    def bet(self):
        self.guess = (self.guess%6) + 1
        return (math.floor(self.wealth/10)+1, self.guess)


class Market:
    def __init__(self):
        self.companies = []

    def next(self):
        outcome = diceRoll()
        print("Outcome: ", outcome)
        for company in self.companies:
            wager, guess = company.bet()
            print(company, " wagers ", wager, " on ", guess)
            company.wealth += 6*wager if guess==outcome else -wager
            print("£", company.wealth)
