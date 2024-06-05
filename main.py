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
                self.color == other.color and
                self.shading == other.shading)



