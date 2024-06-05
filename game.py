import os
import pygame
import random
import sys

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CARD_WIDTH = 100
CARD_HEIGHT = 150
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("SET Game")

# Function to load card images from folder
def load_card_images(folder):
    card_images = {}
    for filename in os.listdir(folder):
        name, ext = os.path.splitext(filename)
        if ext == ".png" or ext == ".jpg":
            card_images[name] = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
    return card_images

# Function to draw card images on the screen
def draw_cards(card_images, cards):
    x = 50
    y = 50
    for index, card in enumerate(cards, start=1):
        image_name = card.color + card.symbol + card.shading + str(card.number)
        card_image = card_images.get(image_name)
        if card_image:
            card_image = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))
            screen.blit(card_image, (x, y))
        x += CARD_WIDTH + 10
        if index % 4 == 0:
            x = 50
            y += CARD_HEIGHT + 10

# Function to handle events
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Main game loop
def main():
    running = True
    card_images = load_card_images("kaarten")
    deck = generate_deck()
    random.shuffle(deck)
    game_cards = deck[:12]

    while running:
        screen.fill(WHITE)
        draw_cards(card_images, game_cards)
        pygame.display.flip()
        handle_events()
        clock.tick(FPS)

# Start the game
if __name__ == "__main__":
    main()
