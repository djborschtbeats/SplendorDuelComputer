class StateMachine:
    def __init__(self):
        self.states = {}  # Dictionary of states and their corresponding functions
        self.current_state = None  # Track the current state

    def add_state(self, name, handler):
        """Add a state and its handler function."""
        self.states[name] = handler

    def set_state(self, name):
        """Set the current state."""
        if name in self.states:
            self.current_state = name
        else:
            raise ValueError(f"State {name} does not exist.")

    def run(self):
        """Run the handler for the current state."""
        if self.current_state and self.current_state in self.states:
            next_state = self.states[self.current_state]()
            if next_state:
                self.set_state(next_state)
        else:
            raise RuntimeError(f"No handler for state {self.current_state}.")
    
    def setup_phase():
        print("Setting up the game...")
        return "PlayerTurn"

    def player_turn():
        print("It's the player's turn...")
        return "EndTurn"

    def end_turn():
        print("Ending the turn...")
        return "GameOver"