class Token:
    # Mapping of token abbreviations to full color names
    ABBREVIATIONS = {
        'R': 'red',
        'G': 'green',
        'B': 'blue',
        'K': 'black',
        'P': 'purple',
        'W': 'white',
        '*': 'gold'
    }

    # Mapping of token names to their colors
    COLORS = {
        'white': "#FFFFFF",
        'red': "#FF0000",
        'blue': "#0000FF",
        'green': "#00FF00",
        'black': "#000000",
        'purple': "#800080",
        'gold': "#FFFF00"
    }

    def __init__(self, color):
        if (color not in Token.COLORS) and (color not in Token.ABBREVIATIONS):
            raise ValueError(f"Invalid token color: {color}")
        if len(color) == 1: 
            color = self.ABBREVIATIONS[color]
        self.color = color

    def __str__(self):
        return f"{self.color} token(s)"

    @property
    def color_code(self):
        """Return the color code of the token."""
        return Token.COLORS[self.color]

    @classmethod
    def from_abbreviation(cls, abbreviation):
        """Create a Token from an abbreviation."""
        if abbreviation not in cls.ABBREVIATIONS:
            raise ValueError(f"Invalid abbreviation: {abbreviation}")
        color = cls.ABBREVIATIONS[abbreviation]
        return cls(color)

    @staticmethod
    def available_colors():
        """List all available token colors."""
        return list(Token.COLORS.keys())