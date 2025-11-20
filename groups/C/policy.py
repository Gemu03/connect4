
import numpy as np
import random
from connect4.policy import Policy
from connect4.connect_state import ConnectState

class Policy(Policy):
    def __init__(self):
        super().__init__()
        self.name = "GioPolicy v0.1"

    def act(self, board):
        # Placeholder: Random move
        state = ConnectState(board=board, player=1)
        return random.choice(state.get_free_cols())
