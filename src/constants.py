"""
Contains constants for the poker game.
"""

# Deck attributes
RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
SUITS = ('Spades', 'Diamonds', 'Hearts', 'Clubs')
CARD_IMAGES_DIR = "./src/resources/deck/"

# Game attributes
HANDS = {1: "High Card",
         2: "Pair",
         3: "Two Pair",
         4: "Three of a Kind",
         5: "Straight",
         6: "Flush",
         7: "Full House",
         8: "Four of a Kind",
         9: "Straight Flush",
         10: "Royal Flush"}

RANK_TO_FACE = {1: "Ace", 
                2: "Two", 
                3: "Three", 
                4: "Four", 
                5: "Five", 
                6: "Six", 
                7: "Seven", 
                8: "Eight", 
                9: "Nine", 
                10: "Ten", 
                11: 'Jack', 
                12: 'Queen', 
                13: 'King', 
                14: 'Ace'}

# GUI attributes
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 30
CARD_WIDTH = 71
CARD_HEIGHT = 96
