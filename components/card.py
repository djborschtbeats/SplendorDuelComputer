from PIL import Image, ImageDraw, ImageFont
from typing import Optional

from components.t0ken import Token


class Card:
    def __init__(
        self,
        level: int,
        points: int,
        feature: Optional[str] = None,  # TODO: features are limited, could be an Enum
        requirements: Optional[dict[str, int]] = None,
        output: Optional[dict[str, int]] = None,
        crowns: int = 0,
    ) -> None:
        self.level = level
        self.points = points
        self.feature = feature
        self.requirements = self.parse_tokens(requirements)
        self.output = self.parse_tokens(output)
        self.crowns = crowns

    def __str__(self) -> str:
        def token_str(tokens: Optional[list[Token]]) -> str:
            return ", ".join(token.name for token in tokens) if tokens else "None"

        return "Card: \n" \
               f"\tLevel: {self.level}\n" \
               f"\tPoints: {self.points}\n" \
               f"\tCrowns: {self.crowns}\n" \
               f"\tFeature: {self.feature}\n" \
               f"\tRequirements: {token_str(self.requirements)}\n" \
               f"\tOutput: {token_str(self.output)}\n"

    @staticmethod
    def parse_tokens(
        token_quantities: Optional[dict[str, int]] = None
    ) -> Optional[list[Token]]:
        """
        Parses a dict of token colors and quantities into a list of tokens.

        Args:
            token_quantities: Dictionary of token color string to quantity,
            e.g. {"red": 2, "green": 3}

        Returns:
            a list of Token enums
        """
        if not token_quantities:
            return

        tokens = []

        for color, quantity in token_quantities.items():
            if color not in Token.__members__:
                raise ValueError(f"Unknown token color: {color.__name__}")
            tokens.extend([Token[color]] * quantity)

        return tokens

    # TODO: Clean up/add typehints from here on
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
