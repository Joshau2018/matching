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
DARKER_GRAY = (200, 200, 200)

# Difficulty levels (time in seconds between turns)
EASY = 12
MEDIUM = 8
HARD = 4

cards = []

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Matching Game")

# Load background
background_image = pygame.image.load("images/backgroundGalaxy.jpeg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Sets the back of the cards
back_of_card = pygame.image.load("images/backofcard.jpeg")
back_of_card = pygame.transform.scale(back_of_card, (CARD_WIDTH, CARD_HEIGHT))

# Define function to render text with background
def render_text_with_background(font, text, color, background_color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    background_surface = pygame.Surface((text_rect.width + 20, text_rect.height + 10))
    background_surface.fill(background_color)
    background_surface.blit(text_surface, (10, 5))
    return background_surface

class Card:
    def __init__(self, image_path, num):
        self.image_path = image_path
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        self.rect = self.image.get_rect()
        self.is_face_up = False
        self.is_flippable = True
        self.card_num = num  # Fixed assignment of card number here
        self.show_time = 0

    def show_card(self, screen, row, col, current_time):
        x = col * (CARD_WIDTH + CARD_GAP) + (SCREEN_WIDTH - (NUM_COLS * (CARD_WIDTH + CARD_GAP))) / 2
        y = row * (CARD_HEIGHT + CARD_GAP) + (SCREEN_HEIGHT - (NUM_ROWS * (CARD_HEIGHT + CARD_GAP))) / 2
        self.rect.topleft = (x, y)
        if self.is_face_up and self.is_flippable:
            screen.blit(self.image, self.rect.topleft)
            if current_time - self.show_time >= 1.0:  # Keep the card face up for 1 second
                self.is_face_up = False
        else:
            screen.blit(back_of_card, self.rect.topleft)

def generate_board():
    values = random.sample(range(1, 9), (NUM_ROWS * NUM_COLS) // 2) * 2
    random.shuffle(values)
    board = [[None for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    index = 0
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            image_path = f'images/cards/card{values[index]}.jpg'
            card = Card(image_path, values[index])
            board[row][col] = card
            index += 1
    return board

def main(difficulty):
    board = generate_board()
    running = True
    turn_timer = 0
    turn_delay = difficulty
    selected_card = None
    first_card = None
    second_card = None
    matched_pairs = []

    # Create a clock object to regulate the frame rate
    clock = pygame.time.Clock()

    # Game loop
    while running:
        current_time = pygame.time.get_ticks() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse clicks
                for row in range(NUM_ROWS):
                    for col in range(NUM_COLS):
                        card = board[row][col]
                        if card.rect.collidepoint(event.pos) and card.is_flippable:
                            if not matched_pairs:
                                card.is_face_up = True
                                card.show_time = current_time
                                if not selected_card:
                                    selected_card = card
                                    if not first_card:
                                        first_card = selected_card
                                elif card != selected_card:
                                    second_card = card
                                    turn_timer = current_time
                                    selected_card = None
                            break

        screen.blit(background_image, (0, 0))

        # Draw cards on the screen
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                card = board[row][col]
                if card in matched_pairs or (card == first_card and current_time - turn_timer < 1.0):
                    card.show_card(screen, row, col, current_time)
                elif card == second_card and current_time - turn_timer < 1.0:
                    card.show_card(screen, row, col, current_time)
                else:
                    card.show_card(screen, row, col, current_time)

        pygame.display.flip()

        # Update turn timer
        if second_card:
            if current_time - turn_timer >= 1.0:  # Check if it's time to flip cards back
                if first_card.card_num == second_card.card_num:  # Check for a match
                    matched_pairs.extend([first_card, second_card])
                first_card = None
                second_card = None

        # Check if all pairs are matched
        if len(matched_pairs) == NUM_ROWS * NUM_COLS:
            # Game over
            running = False

        # Regulate the frame rate
        clock.tick(60)

if __name__ == "__main__":
    difficulty = None
    # Difficulty selection loop
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

        # Display difficulty selection menu
        screen.blit(background_image, (0, 0))
        font = pygame.font.Font(None, 36)
        text_easy = render_text_with_background(font, "Press 'E' for Easy (1.0s between turns)", (255, 255, 255),
                                                (100, 100, 100, 150))
        text_medium = render_text_with_background(font, "Press 'M' for Medium (0.5s between turns)", (255, 255, 255),
                                                  (100, 100, 100, 150))
        text_hard = render_text_with_background(font, "Press 'H' for Hard (0.2s between turns)", (255, 255, 255),
                                                (100, 100, 100, 150))
        text_quit = render_text_with_background(font, "Press 'Q' to Quit", (255, 255, 255), (100, 100, 100, 150))
        screen.blit(text_easy, (SCREEN_WIDTH // 2 - text_easy.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(text_medium, (SCREEN_WIDTH // 2 - text_medium.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(text_hard, (SCREEN_WIDTH // 2 - text_hard.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_quit, (SCREEN_WIDTH // 2 - text_quit.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()

    main(difficulty)
