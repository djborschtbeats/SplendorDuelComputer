from collections import defaultdict

from components.card import Card
from components.t0ken import Token


class Player:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.tokens: list[Token] = []
        self.privileges: int = 0
        self.cards: list[Card] = []  # Cards in the player's hand (general cards)
        self.jewel_cards = []  # Cards specifically representing jewels
        self.prestige_cards = []  # Cards specifically representing prestige
        self.crowns = 0  # Number of crowns owned by the player

    def __str__(self):
        return (
            f"Player: {self.name}, Tokens: {dict(self.tokens)}, "
            f"Privilege Tokens: {self.privileges}, Crowns: {self.crowns}"
        )

    def add_token(self, token, quantity):
        """Add tokens to the player's pool."""
        self.tokens[token] += quantity
        print(f"{self.name} gained {quantity} {token} token(s). Total: {self.tokens[token]}.")

    def use_privilege_token(self):
        """Use a privilege token if available."""
        if self.privileges > 0:
            self.privileges -= 1
            print(f"{self.name} used a privilege token. Remaining: {self.privileges}.")
        else:
            print(f"{self.name} has no privilege tokens left to use.")

    def add_card(self, card, card_type="general"):
        """
        Add a card to the player's collection.
        :param card: The card to add.
        :param card_type: The type of card ("general", "jewel", or "prestige").
        """
        if card_type == "jewel":
            self.jewel_cards.append(card)
        elif card_type == "prestige":
            self.prestige_cards.append(card)
        else:
            self.cards.append(card)
        print(f"{self.name} acquired a {card_type} card: {card}.")

    def end_turn(self):
        """Indicate the end of the player's turn."""
        print(f"{self.name}'s turn has ended.")

    def calculate_crowns(self):
        """
        Calculate crowns by summing the crowns from all jewel cards.
        """
        total_crowns = sum(card.get("crowns", 0) for card in self.jewel_cards)
        self.crowns = total_crowns
        print(f"{self.name} recalculated crowns: {self.crowns}.")
        return self.crowns

    def calculate_prestige(self):
        """
        Calculate prestige points by summing points from jewel and prestige cards.
        """
        total_prestige = sum(card.get("points", 0) for card in self.jewel_cards)
        total_prestige += sum(card.get("points", 0) for card in self.prestige_cards)
        print(f"{self.name} recalculated prestige points: {total_prestige}.")
        return total_prestige

    def calculate_prestige_colors(self):
        """
        Calculate the highest sum of prestige points by output color across jewel cards.
        Returns the maximum sum of any color's prestige points.
        """
        color_totals = defaultdict(int)
        for card in self.jewel_cards:
            output = card.get("output", {})
            for color, value in output.items():
                color_totals[color] += value

        max_prestige_color_value = max(color_totals.values(), default=0)
        print(f"{self.name}'s highest color prestige points: {max_prestige_color_value}.")
        return max_prestige_color_value
        
    def check_win_condition(self):
        """
        Check if the player meets any of the win conditions:
        - 10 or more crowns.
        - 20 or more total prestige points.
        - 10 or more points in any single prestige color.

        Returns True if any condition is met, otherwise False.
        """
        crowns = self.calculate_crowns()
        total_prestige = self.calculate_prestige()
        max_prestige_color = self.calculate_prestige_colors()

        if crowns >= 10:
            print(f"{self.name} wins with {crowns} crowns!")
            return True
        elif total_prestige >= 20:
            print(f"{self.name} wins with {total_prestige} prestige points!")
            return True
        elif max_prestige_color >= 10:
            print(f"{self.name} wins with {max_prestige_color} prestige points in a single color!")
            return True

        print(f"{self.name} does not meet the win conditions yet.")
        return False