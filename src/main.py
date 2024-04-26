"""
Main file for running poker game GUI

"""

import src.constants as constants
from src.game.deck import Deck
from src.game.game import Game
from src.game.inputbox import InputBox
from src.game.player import Player
import src.game.utilities as utilities

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

players = [
    Player(1, 1000, (50, 650), screen),
    Player(2, 1000, (50, 50), screen),
    # Add more players as needed
]
game = Game(players)
current_player_index = 0

button_fold = utilities.draw_button(screen, "Fold", (850, 700), 100, 50)
button_check = utilities.draw_button(screen, "Check", (750, 700), 100, 50)
button_call = utilities.draw_button(screen, "Call", (650, 700), 100, 50)
button_bet = utilities.draw_button(screen, "Bet", (550, 700), 100, 50)
bet_input_box = InputBox(400, 700, 140, 32)

def handle_buttons():
    """Handle button presses and update game state accordingly."""
    global current_player_index
    current_player = players[current_player_index]
    mouse_pos = pygame.mouse.get_pos()
    
    if button_fold.collidepoint(mouse_pos):
        current_player.fold()
        next_player()
    elif button_check.collidepoint(mouse_pos):
        if game.current_highest_bet == 0 or current_player.current_bet == game.current_highest_bet:
            current_player.check()  # Can only check if no bet has been placed
            next_player()
        else:
            print("Cannot check, there is an active bet.")
    elif button_call.collidepoint(mouse_pos):
        if game.current_highest_bet > 0:
            bet_amount = game.current_highest_bet - current_player.current_bet
            current_player.bet(bet_amount)
            next_player()
    elif button_bet.collidepoint(mouse_pos):
        bet_amount = int(bet_input_box.get_text())
        if bet_amount >= 2 * game.current_highest_bet:
            current_player.bet(bet_amount)
            game.current_highest_bet = bet_amount
            bet_input_box.clear_text()
            next_player()

def next_player():
    """Move to the next player, handling game round transitions."""
    global current_player_index
    current_player_index = (current_player_index + 1) % len(players)
    if current_player_index == 0:
        game.play_round()
        
def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Properly handle text input for the bet amount
            bet_input_box.handle_event(event)

            # Correctly detect mouse clicks on buttons
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 is the left mouse button
                handle_buttons()

        screen.blit(table, (0, 0))  # Draw the background table
        for player in players:
            player.draw(card_images)  # Draw each player's cards and information
        bet_input_box.draw(screen)  # Draw the betting input box
        utilities.draw_button(screen, "Fold", (850, 700), 100, 50)  # Redraw buttons
        utilities.draw_button(screen, "Check", (750, 700), 100, 50)
        utilities.draw_button(screen, "Call", (650, 700), 100, 50)
        utilities.draw_button(screen, "Bet", (550, 700), 100, 50)
        pygame.display.flip()
        clock.tick(constants.FPS)

if __name__ == "__main__":
    game_loop()