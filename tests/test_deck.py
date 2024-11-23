from components.deck import *


def test_deck():
    deck = Deck('../resources/deck/deck.json')
    deck.display_deck()
    deck.display_piles()
    deck.display_active_cards()


if __name__ == '__main__':
    test_deck()