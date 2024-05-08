import pygame
import random
import sys

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_WIDTH = 100
CARD_HEIGHT = 100
CARD_GAP = 10
NUM_ROWS = 4
NUM_COLS = 4
WHITE = (255, 255, 255)
# makes the textbox for the difficulty menu a little darker
DARKER_GRAY = (200, 200, 200)

# Difficulty levels (time in seconds between turns)
EASY = 1.0
MEDIUM = 0.5
HARD = 0.2

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Matching Game")

# Load background 
background_image = pygame.image.load("images/backgroundGalaxy.jpeg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# sets the back of the cards
back_of_card = pygame.image.load("images/backofcard.jpeg")
back_of_card = pygame.transform.scale(back_of_card, (CARD_WIDTH, CARD_HEIGHT))


# Define Card class
class Card:
    def __init__(self, value):
        self.value = value
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)
        self.is_face_up = False

# Generate board with pairs of cards
def generate_board():
    values = list(range((NUM_ROWS * NUM_COLS) // 2)) * 2
    random.shuffle(values)
    board = [[Card(value) for value in values[row * NUM_COLS:(row + 1) * NUM_COLS]] for row in range(NUM_ROWS)]
    return board

# Main game function
def main(difficulty):
    board = generate_board()
    # Game loop
    running = True
    turn_timer = 0  # Timer for tracking turn time
    turn_delay = difficulty  # Set turn delay based on difficulty
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Creates the galaxy background and sets it in the center
        screen.blit(background_image, (0,0))

        # draws the cards in the correct pos
        for row in board:
            for card in row:
                if not card.is_face_up:
                    screen.blit(back_of_card, card.rect.topleft)

        # Update display
        pygame.display.flip()

        # Update timer
        turn_timer += pygame.time.get_ticks() / 1000  # Convert milliseconds to seconds
        if turn_timer >= turn_delay:
            # Reset timer and process turn
            turn_timer = 0
            process_turn()

    # Cleanup
    pygame.quit()

# Function to handle turn processing
def process_turn():
    pass  # Placeholder for turn processing logic

if __name__ == "__main__":
    difficulty = None
    while difficulty is None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    difficulty = EASY
                elif event.key == pygame.K_m:
                    difficulty = MEDIUM
                elif event.key == pygame.K_h:
                    difficulty = HARD
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen.blit(background_image, (0, 0))
        font = pygame.font.Font(None, 36)
        text_easy = font.render("Press 'E' for Easy (1.0s between turns)", True, DARKER_GRAY)
text_medium = font.render("Press 'M' for Medium (0.5s between turns)", True, DARKER_GRAY)
text_hard = font.render("Press 'H' for Hard (0.2s between turns)", True, DARKER_GRAY)
text_quit = font.render("Press 'Q' to Quit", True, DARKER_GRAY)
        screen.blit(text_medium, (SCREEN_WIDTH // 2 - text_medium.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(text_hard, (SCREEN_WIDTH // 2 - text_hard.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_quit, (SCREEN_WIDTH // 2 - text_quit.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()

    main(difficulty)
