"""
Contains the Deck class

"""

import random

import src.constants as constants
from src.game.resources.card import Card

class Deck:
    """ A deck containing 52 cards."""

    def __init__(self):
        """Creates a full deck of cards."""
        self.reset()

    def __str__(self): 
        """Returns the string representation of a deck."""
        result = ''
        for c in self.cards:
            result += str(c) + '\n'
        return result

    def __len__(self):
       """Returns the number of cards left in the deck."""
       return len(self.cards)
   
    def reset(self):
        self.cards = []
        for suit in constants.SUITS:
            for rank in constants.RANKS:
                c = Card(rank, suit)
                self.cards.append(c)

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

    def deal_specific_card(self, rank, suit):
        """Removes and returns the specific card with the given rank and suit, or None if not found."""
        rank = [rank if rank not in constants.HIGH_RANK_NUM else constants.HIGH_RANK_NUM[rank]]
        for card in self.cards:
            if card.rank == rank and card.suit == suit:
                self.cards.remove(card)
                return card
        return None
    
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
