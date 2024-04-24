"""
Contains the Deck class

"""

import random

from src.constants import RANKS, SUITS
from src.game.card import Card

class Deck:
    """ A deck containing 52 cards."""

    def __init__(self):
        """Creates a full deck of cards."""
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                c = Card(rank, suit)
                self.cards.append(c)

    def __str__(self): 
        """Returns the string representation of a deck."""
        result = ''
        for c in self.cards:
            result += str(c) + '\n'
        return result

    def __len__(self):
       """Returns the number of cards left in the deck."""
       return len(self.cards)

    def shuffle(self):
        """Shuffles the cards."""
        random.shuffle(self.cards)

    def deal(self):
        """Removes and returns the top card or None 
        if the deck is empty."""
        if len(self) == 0:
           return None
        else:
           return self.cards.pop(0)

    def peek(self, index):
        """Prints attributes of indexed card or
        an error if the index is invalid."""
        if type(index) == int:
            if index <= len(self) and index > 0:
                print(self.cards[index-1])
            else:
                print("index is out of range")
        else:
            print("index is invalid")

    def highestCard(self, c):
        """Function returns True if top card is higher
        rank than c, False otherwise."""
        topcard = self.cards[0]
        if topcard.rank > c.rank:
            return True
        elif topcard.rank == c.rank:
            if topcard.suit.lower() > c.suit.lower():
                return True
            else:
                return False
        else:
            return False
