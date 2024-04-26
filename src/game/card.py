"""
Contains the Card class

"""

from src.constants import CARD_IMAGES_DIR
from src.game.utilities import get_image_file_name

from pygame.image import load

class Card:
    """ A card object with a suit and rank."""

    def __init__(self, rank, suit):
        """Creates a card with the given rank and suit."""
        self.rank = rank
        self.suit = suit
        self.image = self.load_image()
                
    def __str__(self):
        """Returns the string representation of a card."""
        if self.rank == 11:
            rank = 'Jack'
        elif self.rank == 12:
            rank = 'Queen'
        elif self.rank == 13:
            rank = 'King'        
        elif self.rank == 14:
            rank = 'Ace'
        else:
            rank = self.rank
        return str(rank) + ' of ' + self.suit

    def load_image(self):
        filename = CARD_IMAGES_DIR + get_image_file_name(self)
        return load(filename).convert_alpha()
