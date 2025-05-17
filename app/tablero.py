import pygame
import random
import os
from algoritmos.estado import GameState
from algoritmos.ia import choose_move

# --- configuración gráfica ---
DIM = 60
ROWS, COLS = 8, 8
MARGIN = 40  # espacio superior para marcador
MOVES_L = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
CASILLAS_ESPECIALES = [
    (0, 0), (0, 1), (0, 2), (0, 5), (0, 6), (0, 7),
    (1, 0), (1, 7),
    (2, 0), (2, 7),
    (5, 0), (5, 7),
    (6, 0), (6, 7),
    (7, 0), (7, 1), (7, 2), (7, 5), (7, 6), (7, 7)
]

# Rutas de imágenes
BASE = os.path.dirname(os.path.abspath(__file__))
IMG_BG = pygame.image.load(os.path.join(BASE, "assets/imagenes/suelo.png"))
IMG_BF = pygame.image.load(os.path.join(BASE, "assets/imagenes/bandera-blanca.png"))
IMG_BV = pygame.image.load(os.path.join(BASE, "assets/imagenes/bandera-verde.png"))
IMG_BR = pygame.image.load(os.path.join(BASE, "assets/imagenes/bandera-roja.png"))
IMG_YV = pygame.image.load(os.path.join(BASE, "assets/imagenes/yoshi-verde.png"))
IMG_YR = pygame.image.load(os.path.join(BASE, "assets/imagenes/yoshi-rojo.png"))

# Escalar imágenes
IMG_BG = pygame.transform.scale(IMG_BG, (COLS * DIM, ROWS * DIM))
for img_attr in ("IMG_BF", "IMG_BV", "IMG_BR", "IMG_YV", "IMG_YR"):
    img = globals()[img_attr]
    globals()[img_attr] = pygame.transform.scale(img, (DIM, DIM))

def generar_posicion_aleatoria(evitar: set):
    """Devuelve una celda (fila, col) al azar que no esté en 'evitar'."""
    while True:
        p = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
        if p not in evitar:
            return p

def screen_to_cell(pos):
    """Convierte coordenadas de pantalla a (fila, col)."""
    x, y = pos
    return (y - MARGIN) // DIM, x // DIM

def draw_board(screen, state: GameState, selected):
    """Dibuja todo el tablero en pantalla."""
    # 1) fondo de tablero y margen
    screen.fill((0, 0, 0))
    screen.blit(IMG_BG, (0, MARGIN))
    pygame.draw.rect(screen, (30, 30, 30), (0, 0, COLS*DIM, MARGIN))

    # 2) marcador en margen superior
    font = pygame.font.SysFont(None, 24)
    v = sum(1 for o in state.painted.values() if o == "verde")
    r = sum(1 for o in state.painted.values() if o == "rojo")
    screen.blit(font.render(f"Verde: {v}", True, (0,255,0)), (5, 8))
    screen.blit(font.render(f"Rojo: {r}", True, (255,0,0)), (100, 8))

    # 3) banderas de casillas especiales no pintadas
    for cell in state.special:
        if cell not in state.painted:
            x = cell[1] * DIM
            y = cell[0] * DIM + MARGIN
            screen.blit(IMG_BF, (x, y))

    # 4) banderas ya pintadas
    for cell, owner in state.painted.items():
        img = IMG_BV if owner == "verde" else IMG_BR
        x = cell[1] * DIM
        y = cell[0] * DIM + MARGIN
        screen.blit(img, (x, y))

    # 5) resaltado de movimientos legales del rojo (si está seleccionado)
    if selected:
        for mv in state.legal_moves("rojo"):
            r0, c0 = mv
            s = pygame.Surface((DIM, DIM), pygame.SRCALPHA)
            s.fill((255, 0, 0, 100))
            screen.blit(s, (c0*DIM, r0*DIM + MARGIN))

    # 6) grid
    for row in range(ROWS):
        for col in range(COLS):
            x = col * DIM
            y = row * DIM + MARGIN
            pygame.draw.rect(screen, (0,0,0), (x, y, DIM, DIM), 1)

    # 7) Yoshis
    yv = state.positions["verde"]
    yr = state.positions["rojo"]
    screen.blit(IMG_YV, (yv[1]*DIM, yv[0]*DIM + MARGIN))
    screen.blit(IMG_YR, (yr[1]*DIM, yr[0]*DIM + MARGIN))

def main(difficulty="Principiante"):
    """Arranca Pygame, ejecuta el juego y al cerrar devuelve (v, r, winner)."""
    pygame.init()
    pygame.display.set_caption("Yoshi's zones")
    icon = pygame.image.load(os.path.join(BASE, "assets/imagenes/yoshi-verde.png"))
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((COLS*DIM, ROWS*DIM + MARGIN))
    clock = pygame.time.Clock()

    # Inicializar estado
    state = GameState(tuple(CASILLAS_ESPECIALES))
    state.positions["verde"] = generar_posicion_aleatoria(state.special)
    used = set(state.special) | {state.positions["verde"]}
    state.positions["rojo"] = generar_posicion_aleatoria(used)

    selected = None
    running = True

    while running:
        # IA mueve cuando sea su turno y no terminal
        if state.turn == "verde" and not state.is_terminal():
            mv = choose_move(state, difficulty)
            if mv:
                state.apply("verde", mv)

        draw_board(screen, state, selected)
        pygame.display.flip()

        # Si terminó, mostrar mensaje final y salir
        if state.is_terminal():
            pygame.time.delay(500)
            v = sum(1 for o in state.painted.values() if o=="verde")
            r = sum(1 for o in state.painted.values() if o=="rojo")
            winner = "Empate" if v == r else ("Verde" if v > r else "Rojo")
            pygame.time.delay(1500)
            running = False
            continue

        # Manejo de eventos
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.MOUSEBUTTONDOWN and state.turn == "rojo":
                cell = screen_to_cell(e.pos)
                # primer clic: seleccionar Yoshi
                if selected is None:
                    if cell == state.positions["rojo"]:
                        selected = cell
                else:
                    # segundo clic: mover si es legal
                    if cell in state.legal_moves("rojo"):
                        state.apply("rojo", cell)
                    selected = None

        clock.tick(30)

    pygame.quit()
    # devolvemos métricas finales
    return v, r, winner