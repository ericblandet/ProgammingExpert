import random


class Deck:

    def __init__(self):
        # self.shuffle()
        pass

    def deal(self, number_of_cards):
        dealt_cards = []
        for i in range(number_of_cards):
            idx = random.randrange(0, len(self.cards))
            dealt_cards.append(self.cards[idx])
            del (self.cards[idx])
        return dealt_cards

    def __str__(self):
        return '\n'.join(map(lambda x: x[0], self.cards))

    def shuffle(self):
        diamond = u"\u2666"
        heart = u"\u2665"
        club = u"\u2663"
        spade = u"\u2660"
        colors = [diamond, heart, club, spade]
        vals = [("1", 11), ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6),
                ("7", 7), ("8", 8), ("9", 9), ("T", 10), ("J", 11), ("Q", 12), ("K", 13)]

        self.cards = []
        for val in vals:
            for color in colors:
                self.cards.append((color+val[0], val[1]))
