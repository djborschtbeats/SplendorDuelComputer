import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from components.card import *
from components.deck import *


def test_deck():
    # Step 1: Create and load the deck from a sample CSV file
    deck = Deck('resources/deck/deck.json')
    print("\n--- Loaded Deck ---")
    deck.display_deck()
    
    # Step 2: Shuffle the deck into piles by level
    deck.shuffle()
    print("\n--- Shuffled Piles ---")
    deck.display_piles()

    # Step 3: Deal cards
    level_0_cards = deck.deal(level=0, num_cards=5)
    level_1_cards = deck.deal(level=1, num_cards=4)
    level_2_cards = deck.deal(level=2, num_cards=3)

    print("\n--- Dealt Cards ---")
    print(f"Level 0: {len(level_0_cards)} \n")
    for card in level_0_cards: 
        print(f"{str(card)}")
    print(f"Level 1: {len(level_1_cards)} \n")
    for card in level_1_cards: 
        print(f"{str(card)}")
    print(f"Level 2: {len(level_2_cards)} \n")
    for card in level_2_cards: 
        print(f"{str(card)}")

    # Step 4: Display remaining piles
    print("\n--- Remaining Piles ---")
    deck.display_piles()


if __name__ == '__main__':
    test_deck()