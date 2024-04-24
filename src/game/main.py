import pygame
import sys

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 30
CARD_WIDTH, CARD_HEIGHT = 100, 140  # Adjust based on your card images

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Poker Game")
clock = pygame.time.Clock()

# Load resources
card_image = pygame.image.load('path_to_card_image.png').convert_alpha()  # Update this path
card_image = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))

# Utility functions
def draw_text(text, position, size=20, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def draw_button(text, x, y, width, height):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, (0, 0, 0), button_rect)
    draw_text(text, (x + 10, y + 10))

    return button_rect  # Return the rectangle for click detection

def draw_card(x, y):
    screen.blit(card_image, (x, y))

def main_loop():
    button_fold = draw_button("Fold", 50, 500, 80, 30)
    button_check = draw_button("Check", 140, 500, 80, 30)
    button_call = draw_button("Call", 230, 500, 80, 30)
    button_bet = draw_button("Bet", 320, 500, 80, 30)
    button_allin = draw_button("All-in", 410, 500, 80, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                mouse_pos = event.pos
                if button_fold.collidepoint(mouse_pos):
                    print("Fold clicked")
                elif button_check.collidepoint(mouse_pos):
                    print("Check clicked")
                elif button_call.collidepoint(mouse_pos):
                    print("Call clicked")
                elif button_bet.collidepoint(mouse_pos):
                    print("Bet clicked")
                elif button_allin.collidepoint(mouse_pos):
                    print("All-in clicked")

        screen.fill((0, 128, 0))  # Green background

        # Re-draw buttons each frame to ensure they appear over the background
        button_fold = draw_button("Fold", 50, 500, 80, 30)
        button_check = draw_button("Check", 140, 500, 80, 30)
        button_call = draw_button("Call", 230, 500, 80, 30)
        button_bet = draw_button("Bet", 320, 500, 80, 30)
        button_allin = draw_button("All-in", 410, 500, 80, 30)

        # Draw a card for demonstration purposes
        draw_card(50, 50)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main_loop()
