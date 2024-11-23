class StateMachine:
    def __init__(self):
        self.states = {}  # Dictionary of states and their corresponding functions
        self.current_state = None  # Track the current state
        self.context = {}  # Shared data between states

    def add_state(self, name, handler):
        """Add a state and its handler function."""
        self.states[name] = handler

    def set_state(self, name):
        """Set the current state."""
        if name in self.states:
            self.current_state = name
        else:
            raise ValueError(f"State {name} does not exist.")

    def run(self, context=None):
        """Run the handler for the current state."""
        if self.current_state and self.current_state in self.states:
            if context is not None:
                self.context.update(context)  # Merge new context into shared state
            next_state = self.states[self.current_state](self.context)
            if next_state:
                self.set_state(next_state)
        else:
            raise RuntimeError(f"No handler for state {self.current_state}.")
    
    def setup_phase(context):
        print("Setting up the game...")
        # Example setup logic
        context['tokens'] = "Tokens shuffled and placed"
        context['cards'] = "Cards shuffled and opened"
        context['first_player'] = "Player 1"
        print("Setup complete.")
        print(f"Tokens: {context['tokens']}, Cards: {context['cards']}, First Player: {context['first_player']}")
        return "PlayerTurn"


    def player_turn(context):
        current_player = context.get('current_player', "Unknown Player")
        print(f"It's {current_player}'s turn.")
        # Example turn actions
        context['action_taken'] = "Player replenished tokens"
        print(f"{current_player} has taken action: {context['action_taken']}")
        return "EndTurn"


    def end_turn(context):
        print("Ending the turn...")
        # Rotate to the next player or end the game
        context['current_player'] = "Next Player"
        if context.get('game_over', False):
            return "GameOver"
        return "PlayerTurn"
'''

States: 
Game Initialization: 
setup
  - tokens shuffled and placed on board
  - cards shuffled and opened 
  - first player is decided (opponent given privledge)

player_turn [X player]
  - OPTIONAL 
    - use privledge 
    OR 
    - replenish 
  - MANDATORY
    - purchase card 
    - take tokens 

'''
