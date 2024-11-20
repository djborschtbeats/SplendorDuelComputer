from Card import *

import csv
import random
from collections import defaultdict, namedtuple

class Deck:
    def __init__(self, filename):
        self.cards = []  # Initialize an empty list of cards
        self.load_deck(filename)        
        self.piles = defaultdict(list)  # Dictionary to hold shuffled piles by level


    def load_deck(self, filename):
        """Reads a CSV file and creates Card objects"""
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)  # Skip the header row
                for row in reader:
                    if row:  # Skip any empty rows
                        # Extract information from the CSV row
                        # "Level","Points","Feature","Requirements","Output","Crowns" 
                        level = int(row[0])
                        points = int(row[1])
                        feature = row[2]
                        requirements = row[3] 
                        output = row[4]  # Permanent token if applicable
                        crowns = int(row[5])

                        # Create a Card object and add it to the list of cards
                        card = Card(level, points, feature, requirements, output, crowns)
                        print(f"card: {card}")
                        self.cards.append(card)
        except FileNotFoundError:
            print(f"Error: The file {filename} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def display_deck(self):
        """Print all the cards in the deck"""
        for card in self.cards:
            print(card)

    def shuffle(self):
        """Shuffle cards into piles by level"""
        self.piles.clear()  # Clear previous piles
        random.shuffle(self.cards)  # Shuffle all cards
        for card in self.cards:
            self.piles[card.level].append(card)  # Add to the appropriate level pile

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

    def display_deck(self):
        """Print all the cards in the deck"""
        for card in self.cards:
            print(str(card))

    def display_piles(self):
        """Print the piles by level"""
        for level, pile in self.piles.items():
            print(f"Level {level}: {len(pile)} cards")

def test_deck():
    # Step 1: Create and load the deck from a sample CSV file
    deck = Deck('deck.csv')  # Replace 'cards.csv' with the actual path to your file
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
    i = 0
    for card in level_0_cards: 
        deck.generate_card_graphic(card, str(i) + '.jpg')
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