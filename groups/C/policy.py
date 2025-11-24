import numpy as np
import random
from connect4.policy import Policy
from connect4.connect_state import ConnectState

class Policy(Policy):
    def __init__(self):
        super().__init__()
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7
        self.WINDOW_LENGTH = 4

    def act(self, board):
        pieces = np.sum(board != 0)
        player = 1 if pieces % 2 == 0 else -1
        state = ConnectState(board=board, player=player)
        valid_cols = state.get_free_cols()
        
        best_col = random.choice(valid_cols)
        best_score = -10000

        for col in valid_cols:
            next_state = state.transition(col)
            score = self.score_position(next_state.board, player)
            if score > best_score:
                best_score = score
                best_col = col
        return int(best_col)

    def score_position(self, board, piece):
        score = 0
        center_array = [int(i) for i in list(board[:, 3])]
        score += center_array.count(piece) * 3
        return score
