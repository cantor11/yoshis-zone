# game.py
from copy import deepcopy

MOVES = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]

class GameState:
    def __init__(self, special_cells):
        self.special = set(special_cells)
        self.painted = {}    # (r,c) -> "verde"|"rojo"
        self.positions = {"verde": None, "rojo": None}
        self.turn = "verde"  # verde (AI) siempre inicia
    def clone(self):
        return deepcopy(self)
    def legal_moves(self, who):
        r,c = self.positions[who]
        other = self.positions["verde" if who=="rojo" else "rojo"]
        moves = []
        for dr,dc in MOVES:
            nr,nc = r+dr, c+dc
            if (0<=nr<8 and 0<=nc<8
                and (nr,nc) not in self.painted
                and (nr,nc)!= other):
                moves.append((nr,nc))
        return moves
    def apply(self, who, dest):
        self.positions[who] = dest
        if dest in self.special:
            self.painted[dest] = who
        self.turn = "rojo" if who=="verde" else "verde"
    def is_terminal(self):
        return len(self.painted) == len(self.special)
    def score(self):
        # diferencia de casillas pintadas: verde−rojo
        v = sum(1 for p in self.painted.values() if p=="verde")
        r = sum(1 for p in self.painted.values() if p=="rojo")
        return v - r
