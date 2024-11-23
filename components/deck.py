import json
from collections import defaultdict
from random import shuffle

from components.card import Card


class Deck:
    def __init__(self, card_spec_file_path: str) -> None:
        self.deck: list[Card] = self._load_card_specs(card_spec_file_path)
        self.piles: dict[int, list[Card]] = self._load_piles()
        self.active_cards: dict[int, list[Card]] = self._load_active_cards()

    @staticmethod
    def _load_card_specs(card_spec_file_path: str) -> list[Card]:
        """Parse cards and their properties from JSON file."""
        with open(card_spec_file_path, "r") as file:
            return [Card(**item) for item in json.load(file)]  # todo: validate levels

    def _load_piles(self) -> dict[int, list[Card]]:
        """Shuffle cards and separate them into piles by level."""
        shuffle(self.deck)
        piles = defaultdict(list)
        for card in self.deck:
            piles[card.level].append(card)
        return dict(piles)

    def _load_active_cards(self) -> dict[int, list[Card]]:
        """Deal playable cards to start per level."""
        return {
            level: [
                self.piles[level].pop()
                for _ in range(self._get_max_card_count(level))
            ]
            for level in self.piles.keys()
        }

    @staticmethod
    def _get_max_card_count(level: int) -> int:
        return 5 - level  # 5 cards for level 0; 4 for level 1; 3 for level 2

    @staticmethod
    def display_cards(cards: list[Card]) -> None:
        for card in cards:
            print(card)

    def display_deck(self) -> None:
        print("\n--- Deck ---\n")
        self.display_cards(self.deck)

    def display_piles(self) -> None:
        print("\n--- Piles by Level ---\n")
        for level, pile in self.piles.items():
            print(f"Level {level}: {len(pile)} cards\n")
            self.display_cards(pile)

    def display_active_cards(self) -> None:
        print("\n--- Active Cards by Level ---\n")
        for level, cards in self.active_cards.items():
            print(f"Level {level}: {len(cards)} cards\n")
            self.display_cards(cards)

    # TODO: Clean up/add typehints from here on
    def replenish_card(self, level, num_cards):
        # TODO: consolidate with pop
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



