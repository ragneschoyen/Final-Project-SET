# This file includes a class for the cards in the SET game, aswell as several functions like generating all possible cards
# These functions are used in the main.py file 

import itertools # Necessary import 

# Class representing a card in the SET game
class SetCards:
    # Initialize the card with four properties: number, symbol, color, and shading
    def __init__(self, color, symbol, shading, number, image_name):
        self.color = color # red, green, or purple
        self.symbol = symbol # ⋄, ∼, ◦
        self.shading = shading # solid, striped, or open
        self.number = number # 1, 2, or 3
        self.image_name = image_name # to link card to image

    def __repr__(self): 
        # Return a string representation of the card
        # Used for debugging
        return f"Card({self.color}, {self.symbol}, {self.shading}, {self.number}, {self.image_name})"
    
    def __eq__(self, other):
        # Define equality comparison between two cards based on their properties
        return (self.color == other.color and
                self.symbol == other.symbol and
                self.shading == other.shading and     
                self.number == other.number)
    

# Function for checking if three cards is a set 
def is_set(card_1, card_2, card_3):
    for attribute in ['color', 'symbol', 'shading', 'number']:
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


# Function to find one (first) set
def find_one_set(cards):
    combinations = itertools.combinations(cards, 3)

    for combo in combinations:
        card_1, card_2, card_3 = combo

        if is_set(card_1, card_2, card_3):
            return (card_1, card_2, card_3) 
    
    return None


# Generate image names to match with the name of the picture files (e.g. greendiamondempty1.gif)
def create_image_name():
    colors = ['red', 'green', 'purple']
    shapes = ['oval', 'diamond', 'squiggle']
    shadings = ['filled', 'shaded', 'empty']
    numbers = [1, 2, 3]

    combinations = list(itertools.product(colors, shapes, shadings, numbers))
    image_names = [(color, shape, shading, number, f"{color}{shape}{shading}{number}.gif") for color, shape, shading, number in combinations]
    return image_names


# Generate the actual cards with the corresponding image names 
def create_all_cards():
    image_data = create_image_name()
    all_cards = []

    for color, shape, shading, number, image_name in image_data:
        card =  SetCards(color, shape, shading, number, image_name)
        all_cards.append(card)
    
    return all_cards

