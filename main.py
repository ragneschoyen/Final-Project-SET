# Necessary imports
import pygame
import set_game
import random
import time


# 
class CountdownTimer:
    def __init__(self, duration, callback):
        self.counter = duration
        self.callback = callback
        self.font = pygame.font.SysFont(None, 100)
        self.text = self.font.render(str(self.counter), True, (200, 70, 140))
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    def update(self, event):
        if event.type == pygame.USEREVENT:
            self.counter -= 1
            self.text = self.font.render(str(self.counter), True, (200, 70, 140))
            if self.counter <= 0:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                self.callback()

    def draw(self, window):
        window.blit(self.text, (window.get_width() - 100, 10))


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

        self.timer = CountdownTimer(30, self.timer_expired)
        self.player_score = 0
        self.computer_score = 0
        self.round_counter = 1  # Initialize round counter
        self.font = pygame.font.SysFont(None, 40)
        self.user_input = ""
        self.message_log = []

    def add_message(self, message):
        timestamp = time.time()  # Get the current time
        self.message_log.append((str(message), timestamp))  # Ensure message is a string

    def game_over(self):
        if self.player_score > self.computer_score:
            winner_message = "You won:)"
        elif self.player_score < self.computer_score:
            winner_message = "Computer won:("
        else:
            winner_message = "It's a tie!"

        
        pygame.time.delay(3000)
        game_over_font = pygame.font.SysFont(None, 120)
        game_over_text = game_over_font.render("Game Over!", True, (255, 0, 0))
        winner_text = game_over_font.render(winner_message, True, (0, 0, 0))
        self.screen.fill((255, 255, 255))
        text_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        winner_rect = winner_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 100))
        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(winner_text, winner_rect)
        pygame.display.flip()
        pygame.time.delay(4000)
        pygame.quit()
        exit()

    def timer_expired(self):
        sets_found = set_game.find_all_sets(self.selected_cards)
        if sets_found:
            self.add_message("Oh no! Time is up:(\nComputer found a set!\nTry again:)")
            self.computer_score += 1
            self.replace_all_cards()
        else:
            self.add_message("No sets found.\nReplacing top 3 cards.")
            self.replace_top_3_cards()
        self.round_counter += 1
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
        top_margin = 110

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
        prefix_text = self.font.render("Input: ", True, (0, 0, 0))  # Render prefix text in default color
        self.screen.blit(prefix_text, (10, 60))

        # Render user input text in pink color
        input_text = self.font.render(self.user_input, True, (200, 70, 140))
        self.screen.blit(input_text, (10 + prefix_text.get_width(), 60))  # Position input text relative to prefix text

        score_text = self.font.render(f"Player: {self.player_score}  Computer: {self.computer_score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 15))

        round_text = self.font.render(f"Round: {self.round_counter}", True, (0, 0, 0))
        self.screen.blit(round_text, (725, 70))

    # Draw the message log
        current_time = time.time()
        self.message_log = [(msg, ts) for msg, ts in self.message_log if current_time - ts < 5]  # Remove old messages

    # Calculate the starting position for the messages
        message_start_x = self.screen_width - 450  # Adjust as needed to center horizontally on the right side
        message_start_y = (self.screen_height - (len(self.message_log) * 30)) // 2  # Center vertically


        for i, (message, _) in enumerate(self.message_log):
                message_lines = message.split('\n')
                for line_index, line in enumerate(message_lines):
                    message_text = self.font.render(line, True, (0, 0, 0))  # Ensure message is a string
                    message_pos_y = message_start_y + i * 60 + line_index * 30  # Adjust vertical position for each line
                    self.screen.blit(message_text, (message_start_x, message_pos_y))

        # Update display
        pygame.display.flip()


    def replace_top_3_cards(self):
        for i in range(3):
            self.selected_cards[i] = random.choice(self.all_cards)
        self.draw_cards()



    def get_user_input(self):
        if ',' not in self.user_input:
            self.add_message("Invalid input. Please enter\nnumbers separated by commas.")
            self.user_input = ""
            return False

        try:
            indices = [int(i) - 1 for i in self.user_input.split(',')]
            if len(indices) != 3:
                self.add_message("Please enter exactly\nthree numbers.")
                self.user_input = ""
                return False
            selected_cards = [self.selected_cards[i] for i in indices]
            if set_game.is_set(*selected_cards):
                self.add_message("Correct! You\nfound a set!")
                self.player_score += 1
                self.round_counter += 1
                self.replace_all_cards()
                self.user_input = ""
                self.timer = CountdownTimer(30, self.timer_expired)
                return True
            else:
                self.add_message("Incorrect. This\nis not a valid set.")
                self.user_input = ""
                return False
        except ValueError:
            self.add_message("Invalid input. Please enter\nnumbers separated by commas.")
            self.user_input = ""
            return False
        except IndexError:
            self.add_message("Invalid input. Please enter\nvalid card numbers.")
            self.user_input = ""
            return False



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
                        self.get_user_input()
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    else:
                        self.user_input += event.unicode

                self.timer.update(event)

            self.draw_cards()
            self.clock.tick(30)

            if self.round_counter > 2:
                self.game_over()

        pygame.quit()


# Example usage:
if __name__ == "__main__":
    game = Game()
    game.run()



