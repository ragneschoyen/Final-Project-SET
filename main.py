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

        self.screen_width = 800  # Fixed typo: 'screen_with' to 'screen_width'
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("SET Game")

        self.clock = pygame.time.Clock()
        self.all_cards = set_game.create_all_cards()
        self.selected_cards = []
        self.card_objects = []

        self.timer = CountdownTimer(30, self.game_over)
        self.player_score = 0
        self.computer_score = 0
        self.font = pygame.font.SysFont(None, 40)

    def game_over(self):
        print("Game Over!")
        pygame.quit()
        exit()

    def timer_expired(self):
        sets_found = set_game.find_all_sets(self.selected_cards)
        if sets_found:
            self.computer_score += 1
        else: 
            for i in range(3):
                self.selected_cards[i] = random.choice(self.all_cards)
        
        self.timer = CountdownTimer(30, self.timer_expired)
        self.draw_cards()


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

            # Draw card number
            card_number = self.font.render(str(i + 1), True, (0, 0, 0))
            self.screen.blit(card_number, (x, y))


        
        self.timer.draw(self.screen)
        score_text = self.font.render(f"Player: {self.player_score}  Computer: {self.computer_score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 50))


        # Update display
        pygame.display.flip()

    
    def check_for_sets(self):
        sets_found = set_game.find_all_sets(self.selected_cards)
        if sets_found:
            print("Sets found:")
            for i, set_found in enumerate(sets_found):
                print(f"Set {i + 1}: {set_found}")
        else:
            print("No sets found.")


#############

    def get_user_input(self):
        try:
            indices = [int(i) - 1 for i in self.user_input.split(',')]
            if len(indices) != 3:
                print("Please enter exactly three numbers.")
                return False
            selected_cards = [self.selected_cards[i] for i in indices]
            if set_game.is_set(*selected_cards):
                print("Correct! You've found a set.")
                self.player_score += 1
                return True
            else:
                print("Incorrect. This is not a valid set.")
                return False
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")
            return False
        except IndexError:
            print("Invalid input. Please enter valid card numbers.")
            return False
            

#############


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

            if self.timer.counter == 0:
                if self.get_user_input():
                    for i in range(3):
                        self.selected_cards[i] = random.choice(self.all_cards)
                self.timer_expired()

        
        pygame.quit()

# Example usage:
if __name__ == "__main__":
    game = Game()
    game.run()

    
