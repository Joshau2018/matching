import pygame
import random

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_WIDTH = 100
CARD_HEIGHT = 100
CARD_GAP = 10
NUM_ROWS = 4
NUM_COLS = 4

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Matching Game")

# Load background 
background_image = pygame.image.load(f"images/backgroundGalaxy.jpeg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)) # sets image to background at the screens width and height

# sets the back of the cards
back_of_card = pygame.image.load(f"images/backofcard.jpeg")
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
def main():
    board = generate_board()
    # Game loop
    running = True
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

    # Cleanup
    pygame.quit()

if __name__ == "__main__":
    main()