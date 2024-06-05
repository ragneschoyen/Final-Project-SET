import itertools
import pygame

# Class representing a card in the SET game
class SetCards:
    # Initialize the card with four properties: number, symbol, color, and shading
    def __init__(self, number, symbol, color, shading):
        self.number = number # 1, 2, or 3
        self.symbol = symbol # ⋄, ∼, ◦
        self.color = color # red, green, or purple
        self.shading = shading # solid, striped, or open

    def __repr__(self): 
        # Return a string representation of the card
        return f"Card({self.number}, {self.symbol}, {self.color}, {self.shading})"
    
    def __eq__(self, other):
        # Define equality comparison between two cards based on their properties
        return (self.number == other.number and
                self.symbol == other.symbol and
                self.color == other.color and     #KAN EVT DROPPAS ????????
                self.shading == other.shading)
    

# Function for checking if three cards is a set 
def is_set(card_1, card_2, card_3):
    for attribute in ['number', 'symbol', 'color', 'shading']:
        value_1 = getattr(card_1, attribute)
        value_2 = getattr(card_2, attribute)
        value_3 = getattr(card_3, attribute)

        if not (value_1 == value_2 == value_3 or (value_1 != value_2 and value_2 != value_3 and value_1 != value_3)):
            return False
    return True

# Function to find all sets
def find_all_sets(cards):
    sets_found = []
    combinations = itertools.combinations(cards, 3)

    for combo in combinations:
        card_1, card_2, card_3 = combo

        if is_set(card_1, card_2, card_3):
            sets_found.append((card_1, card_2, card_3))

    return sets_found

# Function to find one (fist) set
def find_one_set(cards):
    combinations = itertools.combinations(cards, 3)

    for combo in combinations:
        card_1, card_2, card_3 = combo

        if is_set(card_1, card_2, card_3):
            return (card_1, card_2, card_3) 
    
    return None



