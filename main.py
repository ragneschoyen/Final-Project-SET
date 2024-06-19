# This file implements the SET game using Pygame, managing the game state, user input, and a timer
# Also using the functions made in set_game

# Necessary imports
import pygame
import set_game 
import random
import time


# Class for creating a countdown timer displayed on the pygame window
class CountdownTimer:
    def __init__(self, duration, callback):
        self.counter = duration
        self.callback = callback
        self.font = pygame.font.SysFont(None, 100)
        self.text = self.font.render(str(self.counter), True, (200, 70, 140))
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    # Update function to decrement the timer and update the timer text
    def update(self, event):
        if event.type == pygame.USEREVENT:
            self.counter -= 1
            self.text = self.font.render(str(self.counter), True, (200, 70, 140))
            if self.counter <= 0:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                self.callback()

    # Draw function to display the timer text on the window
    def draw(self, window):
        window.blit(self.text, (window.get_width() - 100, 10))


# Class for managing the SET game functionality and display
class Game:
    def __init__(self):
        pygame.init()

        # Initialize the game window dimentions and title
        self.screen_width = 850  
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("SET Game")

        # Initialize various attributes 
        self.clock = pygame.time.Clock()
        self.all_cards = set_game.create_all_cards()
        self.selected_cards = []
        self.timer = CountdownTimer(30, self.timer_expired)
        self.player_score = 0
        self.computer_score = 0
        self.round_counter = 1 
        self.font = pygame.font.SysFont(None, 40)
        self.user_input = ""
        self.message_log = []


    # Fucntion to add a message to the game message log
    def add_message(self, message):
        timestamp = time.time()  
        self.message_log.append((str(message), timestamp))


    # Function to handle when time has run out
    def timer_expired(self):
        sets_found = set_game.find_all_sets(self.selected_cards)
        if sets_found:
            self.add_message("Oh no! Time is up:(\nComputer found a set!\nTry again:)")
            self.computer_score += 1
            self.replace_set(sets_found[0])
        else:
            self.add_message("No sets found.\nReplacing top 3 cards.")
            self.replace_top_3_cards()
        self.round_counter += 1
        self.timer = CountdownTimer(30, self.timer_expired)  # Reset the timer
        self.draw_elements()


    # Function to handle game over event
    def game_over(self):
        if self.player_score > self.computer_score:
            winner_message = "You won:)"
        elif self.player_score < self.computer_score:
            winner_message = "Computer won:("
        else:
            winner_message = "It's a tie!"

        # Display the winner of the round and the Game Over text
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
        
        # Close the game
        pygame.quit()
        exit()
    

    # Function to select a random set of 12 cards for the game
    def select_random_cards(self, num_cards=12):
        self.selected_cards = random.sample(self.all_cards, num_cards)

    # Function to replace top 3 cards in the game
    def replace_top_3_cards(self):
        cards_already_in_game = [card.image_name for card in self.selected_cards[:3]]
        for i in range(3):
            available_cards = [card for card in self.all_cards if card.image_name not in cards_already_in_game]
            self.selected_cards[i] = random.choice(available_cards)
            available_cards.append(self.selected_cards[i].image_name)
        self.draw_elements()

    def replace_set_cards(self, indices):
        cards_already_in_game = [card.image_name for card in self.selected_cards]
        for i in indices:
            available_cards = [card for card in self.all_cards if card.image_name not in cards_already_in_game]
            self.selected_cards[i] = random.choice(available_cards)
            cards_already_in_game.append(self.selected_cards[i].image_name)
        self.draw_elements()

    def replace_set(self, set_cards):
        indices = [self.selected_cards.index(card) for card in set_cards]
        self.replace_set_cards(indices)


    # Function to get user input and check if set is valid
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

                self.replace_set_cards(indices)
                self.player_score += 1
                self.round_counter += 1
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


    # Function to draw all elements of the game screen
    def draw_elements(self):
        self.screen.fill((255, 255, 255))

        # Draw cards
        num_rows = 4
        num_cols = 3
        card_width = 100  
        card_height = 150  
        margin_x = 20  
        margin_y = 20  
        top_margin = 110

        for i, card in enumerate(self.selected_cards):
            row = i // num_cols  
            col = i % num_cols  
            x = margin_x + col * (card_width + margin_x)
            y = top_margin + row * (card_height + margin_y)
            card_image = pygame.image.load(f"kaarten/{card.image_name}")
            card_image = pygame.transform.scale(card_image, (card_width, card_height))
            self.screen.blit(card_image, (x, y))
            card_number = self.font.render(str(i + 1), True, (0, 0, 0))
            self.screen.blit(card_number, (x, y))

        # Draw timer and other text elements
        self.timer.draw(self.screen)
        prefix_text = self.font.render("Input: ", True, (0, 0, 0))  
        self.screen.blit(prefix_text, (10, 60))

        input_text = self.font.render(self.user_input, True, (200, 70, 140))
        self.screen.blit(input_text, (10 + prefix_text.get_width(), 60))  # Position input text relative to prefix text

        score_text = self.font.render(f"Player: {self.player_score}  Computer: {self.computer_score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 15))

        round_text = self.font.render(f"Round: {self.round_counter}", True, (0, 0, 0))
        self.screen.blit(round_text, (710, 70))

        # Draw the message log
        current_time = time.time()
        self.message_log = [(msg, ts) for msg, ts in self.message_log if current_time - ts < 5]  

        message_start_x = self.screen_width - 450  
        message_start_y = (self.screen_height - (len(self.message_log) * 30)) // 2  

        for i, (message, _) in enumerate(self.message_log):
                message_lines = message.split('\n')
                for line_index, line in enumerate(message_lines):
                    message_text = self.font.render(line, True, (0, 0, 0))  
                    message_pos_y = message_start_y + i * 60 + line_index * 30  
                    self.screen.blit(message_text, (message_start_x, message_pos_y))

        pygame.display.flip()


    # Function for running the game loop
    def run(self):
        self.running = True
        self.select_random_cards()
        self.draw_elements()

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

            self.draw_elements()
            self.clock.tick(60)

            if self.round_counter > 15:
                self.game_over()

        pygame.quit()


# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
