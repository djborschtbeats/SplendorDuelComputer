from collections import defaultdict


class Player:
    def __init__(self, name):
        self.name = name
        self.resources = defaultdict(int)  # e.g., {'gold': 10, 'wood': 5}
        self.tokens = defaultdict(int)  # Tokens the player owns
        self.cards = []  # Cards in the player's hand
        self.victory_points = 0  # Victory points the player has earned
        self.active_effects = []  # Active effects or abilities
        self.crowns = 0  # Number of crowns owned by the player
        self.actions_taken = []  # Track actions in a turn
        self.max_actions_per_turn = 3  # Limit actions per turn

    def __str__(self):
        return f"Player: {self.name}, Victory Points: {self.victory_points}, Resources: {dict(self.resources)}"

    def add_resource(self, resource, quantity):
        """Add resources to the player's pool."""
        self.resources[resource] += quantity
        print(f"{self.name} gained {quantity} {resource}(s). Total: {self.resources[resource]}.")

    def spend_resource(self, resource, quantity):
        """Spend resources if available."""
        if self.resources[resource] >= quantity:
            self.resources[resource] -= quantity
            print(f"{self.name} spent {quantity} {resource}(s). Remaining: {self.resources[resource]}.")
        else:
            print(f"{self.name} does not have enough {resource} to spend.")

    def add_token(self, token, quantity):
        """Add tokens to the player's pool."""
        self.tokens[token] += quantity

    def play_card(self, card):
        """Play a card from the player's hand."""
        if card in self.cards:
            self.cards.remove(card)
            print(f"{self.name} played the card: {card}.")
            return card
        else:
            print(f"{self.name} does not have that card.")
            return None

    def take_action(self, action):
        """Perform an action."""
        if len(self.actions_taken) < self.max_actions_per_turn:
            self.actions_taken.append(action)
            print(f"{self.name} performed the action: {action}.")
        else:
            print(f"{self.name} has reached the action limit for this turn.")

    def end_turn(self):
        """Reset player state at the end of their turn."""
        self.actions_taken.clear()
        print(f"{self.name}'s turn has ended.")

    def gain_victory_points(self, points):
        """Add victory points to the player."""
        self.victory_points += points
        print(f"{self.name} gained {points} victory points. Total: {self.victory_points}.")

    def check_win_condition(self, victory_points_needed):
        """Check if the player meets the win condition."""
        return self.victory_points >= victory_points_needed