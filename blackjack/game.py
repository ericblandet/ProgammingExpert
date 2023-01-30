from player import Player
from dealer import Dealer
from deck import Deck

"""
Many class variables of games should in fact be variables of player and dealer
the logic could be way simpler by modfiying the initializations of the loops
"""


class Game:
    def __init__(self):
        self.deck = Deck()

    def initialize(self, start_money):
        self.player = Player(start_money)
        self.dealer = Dealer()
        self.hit_or_stay = None
        self.dealer_stay = None

    def _deal(self, number_of_cards, person):
        new_cards = self.deck.deal(number_of_cards)
        person.current_hand.extend(new_cards)
        if person == self.player:
            print("You are dealt:", end="")
            print(*map(lambda x: x[0], new_cards), sep=", ")
            print("You now have ", end="")
            print(*map(lambda x: x[0], self.player.current_hand), sep=", ")
            print(self.player.current_hand)
        elif person == self.dealer:
            if number_of_cards == 2:
                print(
                    f"Dealer is dealt: {self.dealer.current_hand[0][0]}, Unknown")
            else:
                print("Dealer is dealt: ", end="")
                print(*map(lambda x: x[0], self.dealer.current_hand), sep=", ")

    def _player_bet(self):
        while True:
            self.current_bet = int(input("Place your bet: "))
            if self.current_bet < 1:
                print("The minimum bet is $1.")
            elif self.current_bet > self.player.current_worth:
                print("You do not have sufficient funds.")
            else:
                break
        self.player.place_bet(self.current_bet)

    def _ask_hit_or_stay(self):
        while True:
            self.hit_or_stay = input("Would you like to hit or stay? ")
            if self.hit_or_stay in ["stay", "hit"]:
                break
            print("That is not a valid option.")

    def _replace_ace_value_by_one(self, hand):
        for idx, el in enumerate(hand):
            if el[0][1] == "1":
                hand[idx] = (el[0], 1)
        return hand

    def _compute_player_score(self):
        self.player_score = sum(card[1] for card in self.player.current_hand)
        if self.player_score > 21:
            new_hand = self._replace_ace_value_by_one(self.player.current_hand)
            self.player_score = sum(card[1] for card in new_hand)
        print("Your current hand score is", self.player_score)

    def _compute_dealer_score(self):
        self.dealer_score = sum(card[1] for card in self.dealer.current_hand)
        if self.dealer_score > 21:
            new_hand = self._replace_ace_value_by_one(self.player.current_hand)
            self.player_score = sum(card[1] for card in new_hand)
        print("Dealer's score is", self.dealer_score)

    # should be commented and refactored
    def _win_or_lose(self):
        if self.player_score == 21:
            if self.dealer_score == 21:
                self.player.current_worth += self.current_bet
                print("This is a Tie !")
                return "end"
            else:
                self.player.current_worth += self.current_bet * 2
                print(
                    f"You win {self.current_bet * 2} and your worth is {self.player.current_worth}")
                return "end"
        elif self.player_score > 21:
            print(
                f"Your hand value is over 21 and you lose ${self.current_bet}: (")
            return "end"
        elif self.dealer_score == 21:
            print(
                f"Dealer's hand value is 21, and you lose ${self.current_bet}: (")
            return "end"
        elif self.dealer_score > 21:
            self.player.current_worth += self.current_bet * 2
            print(
                f"You win {self.current_bet * 2} and your worth is {self.player.current_worth}")
            return "end"
        elif self.hit_or_stay == "stay" and self.dealer_stay == True:
            if self.player_score > self.dealer_score:
                self.player.current_worth += self.current_bet * 2
                print(
                    f"You win {self.current_bet * 2} and your worth is {self.player.current_worth}")
                return "end"
            elif self.player_score < self.dealer_score:
                print(
                    f"Dealer's hand value is {self.dealer_score}, and you lose ${self.current_bet}: (")
                return "end"
            elif self.player_score == self.dealer_score:
                self.player.current_worth += self.current_bet
                print("This is a Tie !")
                return "end"

    def _compute_dealer_play(self):
        while self.dealer_score <= 17:
            self._deal(1, self.dealer)
            self._compute_dealer_score()
        self.dealer_stay = True

    def _play_round(self):
        self.deck.shuffle()
        self.player.current_hand = []
        self.dealer.current_hand = []
        self.player_score = 0
        self.dealer_score = 0
        self.hit_or_stay = None
        self.dealer_stay = None
        # Bet
        self._player_bet()
        # init
        self._deal(2, self.player)
        self._deal(2, self.dealer)
        self._compute_player_score()
        self._compute_dealer_score()
        if self._win_or_lose() == "end":
            return
        self._ask_hit_or_stay()

        while self.hit_or_stay == "hit":
            self._deal(1, self.player)
            self._compute_player_score()
            if self._win_or_lose() == "end":
                return
            self._ask_hit_or_stay()

        self._compute_dealer_play()
        what_to_do = self._win_or_lose()
        if what_to_do == "end":
            return

    def _ask_to_play_hand(self):
        if self.player.current_worth <= 0:
            print("no money left, sorry !")
            self.want_to_play = "no"
        else:
            self.want_to_play = input(
                f"You are starting with ${self.player.current_worth}. Would you like to play a hand? ")

    def play(self):
        self._play_round()

        self._ask_to_play_hand()
        while self.want_to_play in ["yes", "y"]:
            self._play_round()
            self._ask_to_play_hand()
