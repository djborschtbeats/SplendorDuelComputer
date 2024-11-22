import csv
import random
from collections import defaultdict, namedtuple
from PIL import Image, ImageDraw, ImageFont

from components.token import * 

class Card:
    def __init__(self, level, points, feature, requirements, output, crowns):
        self.level = level
        self.points = points
        self.feature = feature
        self.requirements = self.parse_tokens(requirements)
        self.output = self.parse_tokens(output)
        self.crowns = crowns

    def __str__(self):
        return f"Card: " \
               f"\tLevel: {self.level}, Points: {self.points}, Crowns: {self.crowns}, \n" \
               f"\tFeature: {self.feature}, \n" \
               f"\tRequirements: {self.requirements}, \n" \
               f"\tOutput: {self.output}\n"

    def parse_tokens(self, requirements):
        """
        Parses a requirements string into a list of Token namedtuples.
        Args:
            requirements (str): The requirements string (e.g., "2G3R").
        Returns:
            List[Token]: A list of Token namedtuples with color and quantity.
        """
        tokens = []
        quantity = 0

        if requirements.lower() == "None".lower():
            return None

        for char in requirements:
            if char.isdigit():
                quantity += int(char)  # Accumulate digits for the quantity
            elif char in Token.ABBREVIATIONS:
                if quantity > 0:  # If there's an accumulated quantity
                    for i in range(quantity-1):
                        tokens.append(Token(color=char))
                    quantity = 0 # Reset quantity for next token
                else:
                    raise ValueError("Invalid format: quantity missing before color.")
            else:
                raise ValueError(f"Unknown token color code: {char}")
        return tokens
    
    def _draw_border_text(self, draw, x, y, _text, _font, offset=2):
        """
        Draws text with a black border and white fill.

        Args:
            draw (ImageDraw): The drawing context.
            x (int): X-coordinate for the text.
            y (int): Y-coordinate for the text.
            _text (str): The text to draw.
            _font (ImageFont): The font to use.
            offset (int): Thickness of the border.

        Returns:
            None
        """
        # Draw black outline
        for dx, dy in [(-offset, 0), (offset, 0), (0, -offset), (0, offset),
                    (-offset, -offset), (-offset, offset), (offset, -offset), (offset, offset)]:
            draw.text((x + dx, y + dy), _text, font=_font, fill="black")

        # Draw white text on top
        draw.text((x, y), _text, font=_font, fill="white")
        return draw

    def generate_card_graphic(self, output_path):
        """
        Generates a card graphic similar to Splendor.

        Args:
            card (Card): The card object containing its details.
            output_path (str): Path to save the generated image.

        Returns:
            None
        """
        # Card dimensions
        width, height = 400, 600
        background_color = "grey"
        text_color = "white"

        # Fonts
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
            number_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
        except IOError:
            print("FONT ERROR!")
            title_font = ImageFont.load_default()
            number_font = ImageFont.load_default()

        # Create image
        image = Image.new("RGB", (width, height), background_color)
        draw = ImageDraw.Draw(image)

        # Draw top-left: Feature icons (if applicable)
        if self.feature.lower() != "None".lower():
            draw = self._draw_border_text(draw, 20, 20, self.feature, _font=title_font)

        # Draw top-right: Output tokens
        x_start, y_start = width - 120, 20
        for i, token in enumerate(self.output):
            # Draw token color as a small square
            square_size = 30
            x = x_start
            y = y_start + i * (square_size + 10)
            draw.rectangle([x, y, x + square_size, y + square_size], fill=token.color, outline="black")
            # Draw quantity as text next to the square
            draw = self._draw_border_text(draw, x + square_size + 10, y, str(token.quantity), _font=number_font)

        if self.crowns > 0: 
            # Load crown image
            try:
                crown_image = Image.open(
                    "../images/card_icons/crown.png").convert("RGBA")
                crown_width, crown_height = 40, 40  # Resize crowns to fit
                crown_image = crown_image.resize((crown_width, crown_height))
            except IOError:
                print("Crown image not found at 'Images/CardIcons/crown.png'. Please check the file path.")
                return

            # Draw middle: Crowns
            crown_start_x = (width - (self.crowns * crown_width + (self.crowns - 1) * 10)) // 2
            crown_y = 20 - crown_height // 2
            for i in range(self.crowns):
                crown_x = crown_start_x + i * (crown_width + 10)
                # Use the alpha channel of the image as a mask to handle transparency
                image.paste(crown_image, (crown_x, crown_y), crown_image.split()[3])  # Use the alpha channel as mask

        # Draw bottom-left: Requirements
        x_start, y_start = 30, height - 150
        spacing = 60  # Spacing between circles

        for i, token in enumerate(self.requirements):
            # Draw circle for token color
            x = x_start + i * spacing
            y = y_start
            radius = 25
            draw.ellipse([x, y, x + radius * 2, y + radius * 2], fill=token.color, outline="black")
            # Draw quantity inside the circle
            draw = self._draw_border_text(draw, x + radius - 10, y + radius - 10, str(token.quantity), _font=number_font)

        # Save the image
        image.save(output_path)
        print(f"Card graphic saved to {output_path}")
