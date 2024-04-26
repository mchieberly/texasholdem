"""
Utility functions for poker game
"""

from src.constants import RANK_TO_FACE

import pygame

def print_hand_info(rank, hand):
    """Prints the info for a hand."""
    
    converted_hand = [RANK_TO_FACE.get(r, str(r)) for r in hand]
    article = "an" if converted_hand[0] == "Ace" else "an"
    
    if rank == 10:
        return f"{article} Royal Flush!"
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
    
def draw_card(screen, card_images, card_key, position):
    card_image = card_images[card_key]
    screen.blit(card_image, position)

def draw_text(screen, text, position, size=20, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def draw_button(screen, text, position, width, height):
    font = pygame.font.Font(None, 36)
    button_color = (0, 0, 0)  # Example color
    text_color = (255, 255, 255)
    rect = pygame.Rect(position[0], position[1], width, height)
    pygame.draw.rect(screen, button_color, rect)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    return rect  # Returning the rectangle can help in detecting clicks later
