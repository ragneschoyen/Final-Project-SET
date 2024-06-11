import pygame
import set_game
import random


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
        window.blit(self.text, (window.get_width() - 275, 10))


class Game:
    def __init__(self):
        pygame.init()

        self.screen_width = 850  # Fixed typo: 'screen_with' to 'screen_width'
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("SET Game")

        self.clock = pygame.time.Clock()
        self.all_cards = set_game.create_all_cards()
        self.selected_cards = []
        self.card_objects = []

        self.timer = CountdownTimer(30, self.timer_expired)
        self.player_score = 0
        self.computer_score = 0
        self.font = pygame.font.SysFont(None, 40)
        self.user_input = ""

    def game_over(self):
        print("Game Over!")
        pygame.quit()
        exit()

    def timer_expired(self):
        sets_found = set_game.find_all_sets(self.selected_cards)
        if not self.get_user_input():
            if sets_found:
                print("Computer found a set!")
                self.computer_score += 1
                self.replace_all_cards()
            else:
                print("No sets found. Replacing top 3 cards.")
                self.replace_top_3_cards()
        self.timer = CountdownTimer(30, self.timer_expired)  # Reset the timer
        self.draw_cards()

    def select_random_cards(self, num_cards=12):
        self.selected_cards = random.sample(self.all_cards, num_cards)

    def replace_all_cards(self):
        self.select_random_cards()
        self.draw_cards()

    def draw_cards(self):
        # Clear the screen
        self.screen.fill((255, 255, 255))

        # Draw cards on the screen
        num_rows = 4
        num_cols = 3
        card_width = 100  # Adjust as needed
        card_height = 150  # Adjust as needed
        margin_x = 20  # Adjust as needed
        margin_y = 20  # Adjust as needed
        top_margin = 75

        for i, card in enumerate(self.selected_cards):
            row = i // num_cols  # Calculate current row
            col = i % num_cols  # Calculate current column

            # Calculate x and y position for the current card
            x = margin_x + col * (card_width + margin_x)
            y = top_margin + row * (card_height + margin_y)

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
        user_input_text = self.font.render(f"Input: {self.user_input}", True, (0, 0, 0))
        self.screen.blit(user_input_text, (10, self.screen_height - 60))

        score_text = self.font.render(f"Player: {self.player_score}  Computer: {self.computer_score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 15))

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

    def replace_top_3_cards(self):
        for i in range(3):
            self.selected_cards[i] = random.choice(self.all_cards)
        self.draw_cards()

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
                self.replace_all_cards()
                self.user_input = ""
                return True
            else:
                print("Incorrect. This is not a valid set.")
                self.user_input = ""
                return False
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")
            return False
        except IndexError:
            print("Invalid input. Please enter valid card numbers.")
            return False

    #############

    def run(self):
        self.running = True
        self.select_random_cards()
        self.draw_cards()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.timer_expired()
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    else:
                        self.user_input += event.unicode

                self.timer.update(event)

            self.draw_cards()
            self.clock.tick(30)

        pygame.quit()


# Example usage:
if __name__ == "__main__":
    game = Game()
    game.run()



