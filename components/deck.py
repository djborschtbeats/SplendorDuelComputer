import json
from collections import defaultdict
from random import shuffle

from components.card import Card


class Deck:
    def __init__(self, card_spec_file_path: str) -> None:
        self.deck: list[Card] = self.load_card_specs(card_spec_file_path)
        self.piles: dict[int, list[Card]] = self.load_piles()
        self.active_cards: dict[int, list[Card]] = {}

    def load_card_specs(self, card_spec_file_path: str) -> list[Card]:
        """Parse cards and their properties from JSON file,"""
        with open(card_spec_file_path, "r") as file:
            return [Card(**item) for item in json.load(file)]

    def load_piles(self) -> dict[int, list[Card]]:
        """Shuffle cards and separate them into piles by level."""
        shuffle(self.deck)
        piles = defaultdict(list)
        for card in self.deck:
            piles[card.level].append(card)  # TODO: validate level values
        return dict(piles)

    # TODO: Clean up/add typehints from here on
    def display_deck(self):
        """Print all the cards in the deck"""
        for card in self.deck:
            print(card)

    def deal(self, level, num_cards):
        """Deal a number of cards from the top of the pile of a specific level"""
        if level in self.piles and len(self.piles[level]) >= num_cards:
            dealt_cards = [self.piles[level].pop() for _ in range(num_cards)]
            return dealt_cards
        else:
            print(f"Not enough cards to deal from level {level}.")
            return []

    def take(self, level, card_index):
        """
        Take a specific card from a level pile by index.
        Note: Ensure the index is valid.
        """
        if level in self.piles and 0 <= card_index < len(self.piles[level]):
            return self.piles[level].pop(card_index)
        else:
            print(f"Invalid card index or level: Level {level}, Index {card_index}.")
            return None

    def pop(self, level):
        """Pop the top card from a specific level pile"""
        if level in self.piles and self.piles[level]:
            return self.piles[level].pop()
        else:
            print(f"No cards left in level {level}.")
            return None

    def display_piles(self):
        """Print the piles by level"""
        for level, pile in self.piles.items():
            print(f"Level {level}: {len(pile)} cards")
