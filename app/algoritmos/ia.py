# app/algoritmos/ia.py
import math
from .estado import GameState

def minimax(state: GameState, depth: int, max_player: bool, limit: int):
    """
    Minimax recursivo sin poda:
      - max_player=True => turno de la IA (verde), quiere MAXimizar.
      - max_player=False => turno del humano (rojo), quiere MINimizar.
    depth: nivel actual
    limit: profundidad límite (2, 4 o 6 según dificultad)
    Devuelve (valor, movimiento_elegido)
    """
    # Si llegamos a límite o terminal, devolvemos score - small_penalty*depth
    if depth == limit or state.is_terminal():
        return state.score() - 0.001 * depth, None

    player = "verde" if max_player else "rojo"
    best_val = -math.inf if max_player else math.inf
    best_move = None

    for m in state.legal_moves(player):
        child = state.clone()
        child.apply(player, m)
        val, _ = minimax(child, depth+1, not max_player, limit)
        if max_player and val > best_val:
            best_val, best_move = val, m
        if not max_player and val < best_val:
            best_val, best_move = val, m
    
    return best_val, best_move
def choose_move(state: GameState, difficulty: str):
    """
    Envuelve Minimax y devuelve el mejor movimiento para la IA ("verde").
    difficulty: "Principiante", "Amateur" o "Experto"
    """
    limits = {"Principiante": 2, "Amateur": 4, "Experto": 6}
    limit = limits.get(difficulty, 2)
    _, mv = minimax(state, 0, True, limit)
    return mv
