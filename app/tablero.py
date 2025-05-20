import pygame
import random
import os
from algoritmos.estado import GameState
from algoritmos.ia import choose_move
from algoritmos.estado import ZONAS

# --- configuración gráfica ---
DIM = 60
ROWS, COLS = 8, 8
MARGIN = 40  # espacio superior para marcador
MOVES_L = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

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

    # 2) recalcular zonas ganadas y propietarios
    vg, rg = state.zonas_ganadas()
    
    # 3) marcador numérico de zonas en margen
    font = pygame.font.Font(None, 24)
    screen.blit(font.render(f"Zonas Verde: {vg}", True, (0,255,0)), (5, 8))
    screen.blit(font.render(f"Zonas Rojo:  {rg}", True, (255,0,0)), (150, 8))

    # 4) banderas de casillas especiales no pintadas
    for cell in state.special:
        if cell not in state.painted:
            x = cell[1] * DIM
            y = cell[0] * DIM + MARGIN
            screen.blit(IMG_BF, (x, y))

    # 5) banderas ya pintadas
    for cell, owner in state.painted.items():
        img = IMG_BV if owner == "verde" else IMG_BR
        x = cell[1] * DIM
        y = cell[0] * DIM + MARGIN
        screen.blit(img, (x, y))

    # 6) resaltado de movimientos legales del rojo (si está seleccionado)
    if selected:
        for mv in state.legal_moves("rojo"):
            r0, c0 = mv
            s = pygame.Surface((DIM, DIM), pygame.SRCALPHA)
            s.fill((255, 0, 0, 100))
            screen.blit(s, (c0*DIM, r0*DIM + MARGIN))

    # 7) grid
    for row in range(ROWS):
        for col in range(COLS):
            x = col * DIM
            y = row * DIM + MARGIN
            pygame.draw.rect(screen, (0,0,0), (x, y, DIM, DIM), 1)

    # 8) Yoshis
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
    # Obtener celdas especiales
    special_cells = set().union(*ZONAS)
    
    # Inicializar estado con celdas especiales
    state = GameState(tuple(special_cells))
    state.positions["verde"] = generar_posicion_aleatoria(special_cells)
    #Elige posición de 'verde' evitando **todas** las zonas especiales
    evitar = special_cells | {state.positions["verde"]}
    # Para 'rojo', evita las zonas especiales **y** la casilla ocupada por 'verde'
    state.positions["rojo"] = generar_posicion_aleatoria(evitar)

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
            vg, rg = state.zonas_ganadas()
            winner = ("Verde" if vg>rg else "Rojo") if vg!=rg else "Empate"
            return vg, rg, winner

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