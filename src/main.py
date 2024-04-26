"""
Main file for running poker game GUI

"""

import src.constants as constants

import os
import pygame
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Texas Hold'em")
clock = pygame.time.Clock()

def load_card_images():
    card_images = {}
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['h', 'd', 'c', 's']
    base_path = os.path.join(constants.CARD_IMAGES_DIR)
    
    for rank in ranks:
        for suit in suits:
            filename = f"{rank}{suit}.png"
            path = os.path.join(base_path, filename)
            card_key = f"{rank}{suit}"
            card_images[card_key] = pygame.image.load(path).convert_alpha()
    return card_images

def load_background():
    base_path = os.path.join("./src/resources/")
    bg_path = os.path.join(base_path, "table.png")
    table_bg = pygame.image.load(bg_path).convert()
    table_bg = pygame.transform.scale(table_bg, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    return table_bg

card_images = load_card_images()
table = load_background()

def draw_card(card_key, position):
    card_image = card_images[card_key]
    screen.blit(card_image, position)

def draw_text(text, position, size=20, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def draw_button(text, position, width, height):
    button_rect = pygame.Rect(position[0], position[1], width, height)
    pygame.draw.rect(screen, (0, 0, 0), button_rect)
    draw_text(text, (position[0] + 10, position[1] + 10))
    return button_rect

def game_loop():    
    button_fold = draw_button("Fold", (850, 700), 100, 50)
    button_check = draw_button("Check", (750, 700), 100, 50)
    button_call = draw_button("Call", (650, 700), 100, 50)
    button_bet = draw_button("Bet", (550, 700), 100, 50)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_fold.collidepoint(mouse_pos):
                    print("Fold clicked")
                elif button_check.collidepoint(mouse_pos):
                    print("Check clicked")
                elif button_call.collidepoint(mouse_pos):
                    print("Call clicked")
                elif button_bet.collidepoint(mouse_pos):
                    print("Bet clicked")

        screen.blit(table, (0, 0))  # Draw the table background

        # Update the display
        pygame.display.flip()
        clock.tick(constants.FPS)

if __name__ == "__main__":
    game_loop()
    