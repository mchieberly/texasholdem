"""
Utility functions for poker game
"""

from src.constants import RANK_TO_FACE

def print_hand_info(rank, hand):
    """Prints the info for a hand."""
    
    converted_hand = [RANK_TO_FACE.get(r, str(r)) for r in hand]
    article = "an" if converted_hand[0] == "Ace" else "an"
    
    if rank == 10:
        return "{article} Royal Flush!"
    elif rank == 9:
        return f"{article} {converted_hand[0]} High Straight Flush"
    elif rank == 8:
        return f"Four {converted_hand[0]}s"
    elif rank == 7:
        return f"{article} Full House: {converted_hand[0]}s over {converted_hand[1]}s"
    elif rank == 6:
        return f"{article} {converted_hand[0]} High Flush"
    elif rank == 5:
        return f"{article} {converted_hand[0]} High Straight"
    elif rank == 4:
        return f"Three {converted_hand[0]}s"
    elif rank == 3:
        return f"Two Pair: {converted_hand[0]}s and {converted_hand[1]}s"
    elif rank == 2:
        return f"{article} Pair of {converted_hand[0]}s"
    elif rank == 1:
        return f"{article} {converted_hand[0]} High"
    