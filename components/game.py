from components.player import Player
from components.deck import Deck
from components.t0ken import Token
from components.token_bag import TokenBag
from components.token_board import TokenBoard

import hashlib
import datetime
from secrets import randbelow
from tqdm import tqdm
import time


class Game:
    def __init__(self, card_spec_file_path: str = "../resources/deck/deck.json"):
        self.player_count = 2
        self.players = self.add_players()
        self.deck = Deck(card_spec_file_path)
        self.token_bag = TokenBag()
        self.token_board = TokenBoard()

    def add_players(self) -> list[Player]:
        print("Setting up players...")
        players = [
            Player(
                input(f"Enter name for Player {i + 1}: ").strip()
            ) for i in range(self.player_count)
        ]
        print("Shuffling ")
        print(f"Players: {', '.join([player.name for player in players])}")
        # TODO: resolve first player
        return players

    def resolve_first_player(self):
        #This is extra security to prevent Alina from using the random() function because she can hack that. 
        print("Resolving who goes first...")

        # Step 1: Get the current day of the year and approximate moon phase
        today = datetime.date.today()
        day_of_year = today.timetuple().tm_yday
        moon_phase = day_of_year % 30  # Approximate moon phase (0-29)

        # Step 2: Use the length of the players' names as entropy
        name_lengths = [len(player.name) for player in self.players]

        # Step 3: Add cryptographic randomness
        crypto_random = randbelow(100)

        # Step 4: Create a weird hash
        seed_string = f"{today}-{moon_phase}-{name_lengths}-{crypto_random}"
        hash_value = int(hashlib.sha256(seed_string.encode()).hexdigest(), 16)

        # Step 5: Determine first player based on hash parity
        first_player_index = hash_value % len(self.players)
        first_player = self.players[first_player_index]
        
        # Step 6: Unbearable pause 
        # Progress bar before revealing
        print("\nCalculating who goes first...")
        for _ in tqdm(range(100), desc="Progress", ascii=" █", ncols=50):
            time.sleep(0.02)  # Simulate processing time

        print(f"{first_player.name} will go first.")
        return first_player

    def player_turn(self, context):
        """Handle the turn logic for the current player."""
        current_player = self.players[self.current_player_index]
        print(f"\nIt's {current_player.name}'s turn.")
        
        # OPTIONAL: Example of replenishing tokens or taking actions
        action = input(f"{current_player.name}, do you want to 'replenish' or 'take token'? ").strip().lower()
        if action == "replenish":
            self.token_bag = self.token_board.replenish(self.token_bag)
        elif action == "take token":
            token_color = input(f"Choose a token color to take ({', '.join(t.name for t in Token)}): ").strip().lower()
            token = Token[token_color]
            current_player.add_token(token, 1)
        else:
            print("No valid action taken.")

        # MANDATORY: Example of playing cards or gaining resources
        # Add specific game logic here, such as choosing a card or gaining resources

        # Check if the player has won
        if current_player.check_win_condition(self.victory_points_needed):
            return "GameOver"

        return "EndTurn"

    def end_turn(self, context):
        """End the current player's turn and rotate to the next player."""
        current_player = self.players[self.current_player_index]
        current_player.end_turn()

        # Rotate to the next player
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return "PlayerTurn"

    def game_over(self, context):
        """Handle the end of the game."""
        print("\nGame Over! Calculating scores...")
        for player in self.players:
            print(f"{player.name} - Victory Points: {player.victory_points}")

        winner = max(self.players, key=lambda p: p.victory_points)
        print(f"The winner is {winner.name} with {winner.victory_points} points!")
        return None


if __name__ == '__main__':
    game = Game()