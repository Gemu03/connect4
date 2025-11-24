import numpy as np
import pickle
import random
from pathlib import Path
from collections import defaultdict
from connect4.policy import Policy
from connect4.connect_state import ConnectState

class GioPolicy(Policy):
    def __init__(self, depth=4):
        super().__init__()
        self.depth = depth  # Profundidad 4 ve ~4500-10000 estados por jugada
        self.q_table = defaultdict(float)
        # Pesos para la heurística posicional
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7
        self.WINDOW_LENGTH = 4

    def mount(self):
        """Carga conocimiento previo si existe"""
        path = Path(__file__).parent / "train" / "q_table.pkl"
        if path.exists():
            try:
                with open(path, 'rb') as f:
                    self.q_table = pickle.load(f)
            except:
                pass

    def encode_state(self, board):
        return board.tobytes()

    def act(self, board):
        # Identificar jugador
        pieces = np.sum(board != 0)
        player = 1 if pieces % 2 == 0 else -1
        state = ConnectState(board=board, player=player)

        # 1. MATA-INSTANTANEA: Si puedo ganar ya, gano.
        valid_cols = state.get_free_cols()
        for col in valid_cols:
            if state.transition(col).get_winner() == player:
                return col

        # 2. BLOQUEO DE EMERGENCIA: Si el rival gana en la siguiente, bloqueo.
        opp_state = ConnectState(board=board, player=-player)
        for col in valid_cols:
            if opp_state.transition(col).get_winner() == -player:
                return col

        # 3. MINIMAX CON PODA ALFA-BETA
        # Ordenamos columnas priorizando el centro para podar más rápido
        ordered_cols = sorted(valid_cols, key=lambda x: abs(x - 3))
        
        best_score = -float('inf')
        best_col = random.choice(ordered_cols)

        alpha = -float('inf')
        beta = float('inf')

        for col in ordered_cols:
            # Simulamos jugada
            new_state = state.transition(col)
            score = self.minimax(new_state, self.depth - 1, alpha, beta, False, player)
            
            if score > best_score:
                best_score = score
                best_col = col
            
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
                
        return int(best_col)

    def minimax(self, state, depth, alpha, beta, maximizingPlayer, player_id):
        winner = state.get_winner()
        if winner == player_id: return 10000000
        if winner == -player_id: return -10000000
        if not state.get_free_cols(): return 0 # Empate

        if depth == 0:
            # AQUI ESTA LA CLAVE: Híbrido Q-Table + Heurística
            state_key = self.encode_state(state.board)
            if state_key in self.q_table:
                return self.q_table[state_key] # Usar conocimiento aprendido
            else:
                return self.score_position(state.board, player_id) # Usar heurística matemática

        valid_cols = sorted(state.get_free_cols(), key=lambda x: abs(x - 3))

        if maximizingPlayer:
            value = -float('inf')
            for col in valid_cols:
                new_state = state.transition(col)
                score = self.minimax(new_state, depth - 1, alpha, beta, False, player_id)
                value = max(value, score)
                alpha = max(alpha, value)
                if alpha >= beta: break
            return value
        else:
            value = float('inf')
            for col in valid_cols:
                new_state = state.transition(col)
                score = self.minimax(new_state, depth - 1, alpha, beta, True, player_id)
                value = min(value, score)
                beta = min(beta, value)
                if alpha >= beta: break
            return value

    def score_position(self, board, piece):
        """Evalúa el tablero matemáticamente buscando patrones"""
        score = 0
        opp_piece = -piece

        # 1. Preferir centro (Columna 3)
        center_array = [int(i) for i in list(board[:, 3])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # 2. Evaluar ventanas horizontales
        for r in range(self.ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.COLUMN_COUNT - 3):
                window = row_array[c:c + self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece, opp_piece)

        # 3. Evaluar ventanas verticales
        for c in range(self.COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.ROW_COUNT - 3):
                window = col_array[r:r + self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece, opp_piece)

        # 4. Diagonales positivas
        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece, opp_piece)

        # 5. Diagonales negativas
        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece, opp_piece)

        return score

    def evaluate_window(self, window, piece, opp_piece):
        score = 0
        # Conteo de fichas
        my_count = window.count(piece)
        opp_count = window.count(opp_piece)
        empty_count = window.count(0)

        # Reglas de puntuación
        if my_count == 4:
            score += 100
        elif my_count == 3 and empty_count == 1:
            score += 5
        elif my_count == 2 and empty_count == 2:
            score += 2

        # Castigar severamente si el oponente tiene 3 (Bloquear)
        if opp_count == 3 and empty_count == 1:
            score -= 4  # Prioridad defensiva

        return score
