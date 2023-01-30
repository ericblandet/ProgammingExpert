class Player:
    def __init__(self, start_money):
        self.current_worth = start_money
        self.current_hand = []

    def place_bet(self, money):
        self.current_worth -= money
