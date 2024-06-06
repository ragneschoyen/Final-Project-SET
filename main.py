import pygame
import set_game
import random
import time

class CountdownTimer:
    def __init__(self, duration, callback):
        self.counter = duration
        self.callback = callback
        self.font = pygame.font.SysFont(None, 100)
        self.text = self.font.render(str(self.counter), True, (0, 128, 0))
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    def update(self, event):
        if event.type == pygame.USEREVENT:
            self.counter -= 1
            self.text = self.font.render(str(self.counter), True, (0, 128, 0))
            if self.counter <= 0:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                self.callback()

    def draw(self, window):
        window.blit(self.text, (10, 10))

class Game:
    def __init__(self):
        pygame.init()

        self.screen_width = 600  # Fixed typo: 'screen_with' to 'screen_width'
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("SET Game")

        self.clock = pygame.time.Clock()
        self.all_cards = set_game.create_all_cards()
        self.selected_cards = []
        self.card_objects = []

        self.timer = CountdownTimer(30, self.game_over)

    def game_over(self):
        print("Game Over!")
        pygame.quit()
        exit()

    def select_random_cards(self, num_cards=12):
        self.selected_cards = random.sample(self.all_cards, num_cards)

    def draw_cards(self):
        # Clear the screen
        self.screen.fill((255, 255, 255))

        # Draw cards on the screen
        num_rows = 3
        num_cols = 4
        card_width = 100  # Adjust as needed
        card_height = 150  # Adjust as needed
        margin_x = 20  # Adjust as needed
        margin_y = 20  # Adjust as needed

        for i, card in enumerate(self.selected_cards):
            row = i // num_cols  # Calculate current row
            col = i % num_cols   # Calculate current column

            # Calculate x and y position for the current card
            x = margin_x + col * (card_width + margin_x)
            y = margin_y + row * (card_height + margin_y)

            # Load the image for the card
            card_image = pygame.image.load(f"kaarten/{card.image_name}")

            # Scale the image to fit the card width and height
            card_image = pygame.transform.scale(card_image, (card_width, card_height))

            # Blit (draw) the card image onto the screen at the calculated position
            self.screen.blit(card_image, (x, y))
        
        self.timer.draw(self.screen)

        # Update display
        pygame.display.flip()

    
    def check_for_sets(self):
        sets_found = set_game.find_all_sets(self.selected_cards)
        if sets_found:
            print("Sets found:")
            for i, sets_found in enumerate(sets_found):
                print(f"Set {i + 1}: {sets_found}")
        else:
            print("No sets found.")


    def run(self):
        # Main game loop
        self.running = True
        self.select_random_cards()
        self.draw_cards()

        start_time = time.time()
        timer_duration = 30  # seconds

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.timer.update(event)

            elapsed_time = time.time() - start_time
            if elapsed_time >= timer_duration:
                for i in range(3):
                    self.selected_cards[i] = random.choice(self.all_cards)
                start_time = time.time()

            self.check_for_sets()
            self.draw_cards()
            self.clock.tick(30) 
        
        pygame.quit()

# Example usage:
if __name__ == "__main__":
    game = Game()
    game.run()

    













