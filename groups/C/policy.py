
import numpy as np
import random
from connect4.policy import Policy
from connect4.connect_state import ConnectState

class Policy(Policy):
    def __init__(self, depth=2):
        super().__init__()
        self.depth = depth
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7
        self.WINDOW_LENGTH = 4

    def act(self, board):
        pieces = np.sum(board != 0)
        player = 1 if pieces % 2 == 0 else -1
        state = ConnectState(board=board, player=player)
        
        # Bloqueo de emergencia
        opp_state = ConnectState(board=board, player=-player)
        for col in state.get_free_cols():
            if opp_state.transition(col).get_winner() == -player:
                return col

        best_col, _ = self.minimax(state, self.depth, -float('inf'), float('inf'), True, player)
        return int(best_col)

    def minimax(self, state, depth, alpha, beta, maximizingPlayer, player):
        if depth == 0 or state.is_final():
            return (None, self.score_position(state.board, player))
        
        valid_cols = state.get_free_cols()
        if maximizingPlayer:
            value = -float('inf')
            best_col = random.choice(valid_cols)
            for col in valid_cols:
                new_state = state.transition(col)
                _, new_score = self.minimax(new_state, depth-1, alpha, beta, False, player)
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta: break
            return best_col, value
        else:
            value = float('inf')
            best_col = random.choice(valid_cols)
            for col in valid_cols:
                new_state = state.transition(col)
                _, new_score = self.minimax(new_state, depth-1, alpha, beta, True, player)
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta: break
            return best_col, value

    def score_position(self, board, piece):
        return 0 # Placeholder
