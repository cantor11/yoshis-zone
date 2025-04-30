import pygame
import random
import time
import os

# Configuraciones del entorno
DIMENSION_CELDA = 60
FILAS, COLUMNAS = 8, 8
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_GRIS = (160, 160, 160)

# Casillas especiales (esquinas)
CASILLAS_ESPECIALES = [(0, 0), (0, 1), (0, 2), (0, 5), (0, 5), (0, 6), (0, 7), (1, 0), (1, 7), (2, 0), (2, 7), (5, 0), (5, 7), (6, 0), (6, 7), (7, 0), (7, 1), (7, 2), (7, 5), (7, 6), (7, 7)]

# Cargar imágenes
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img_yoshi_verde = pygame.image.load(os.path.join(BASE_DIR, "assets", "imagenes", "yoshi-verde.png"))
img_yoshi_rojo = pygame.image.load(os.path.join(BASE_DIR, "assets", "imagenes", "yoshi-rojo.png"))
img_fondo = pygame.image.load(os.path.join(BASE_DIR, "assets", "imagenes", "suelo.png"))
img_bandera_blanca = pygame.image.load(os.path.join(BASE_DIR, "assets", "imagenes", "bandera-blanca.png"))
img_bandera_verde = pygame.image.load(os.path.join(BASE_DIR, "assets", "imagenes", "bandera-verde.png"))
img_bandera_roja = pygame.image.load(os.path.join(BASE_DIR, "assets", "imagenes", "bandera-roja.png"))

# Escalar imágenes
img_yoshi_verde = pygame.transform.scale(img_yoshi_verde, (DIMENSION_CELDA, DIMENSION_CELDA))
img_yoshi_rojo = pygame.transform.scale(img_yoshi_rojo, (DIMENSION_CELDA, DIMENSION_CELDA))
img_fondo = pygame.transform.scale(img_fondo, (COLUMNAS * DIMENSION_CELDA, FILAS * DIMENSION_CELDA))
img_bandera_blanca = pygame.transform.scale(img_bandera_blanca, (DIMENSION_CELDA, DIMENSION_CELDA))
img_bandera_verde = pygame.transform.scale(img_bandera_verde, (DIMENSION_CELDA, DIMENSION_CELDA))
img_bandera_roja = pygame.transform.scale(img_bandera_roja, (DIMENSION_CELDA, DIMENSION_CELDA))

# Movimientos válidos en L (caballo de ajedrez)
MOVIMIENTOS_L = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1)]

def generar_posicion_random(evitar):
    while True:
        pos = (random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1))
        if pos not in evitar:
            return pos

def dibujar_tablero(pantalla, y_verde, y_rojo):
    pantalla.blit(img_fondo, (0, 0))  # Fondo general del tablero

    for fila in range(FILAS):
        for col in range(COLUMNAS):
            x, y = col * DIMENSION_CELDA, fila * DIMENSION_CELDA

            # Si es casilla especial, dibuja bandera
            if (fila, col) in CASILLAS_ESPECIALES:
                pantalla.blit(img_bandera, (x, y))

            # Bordes de celda
            pygame.draw.rect(pantalla, COLOR_NEGRO, (x, y, DIMENSION_CELDA, DIMENSION_CELDA), 1)

    # Dibujar Yoshis
    pantalla.blit(img_yoshi_verde, (y_verde[1] * DIMENSION_CELDA, y_verde[0] * DIMENSION_CELDA))
    pantalla.blit(img_yoshi_rojo, (y_rojo[1] * DIMENSION_CELDA, y_rojo[0] * DIMENSION_CELDA))

def obtener_movimientos_legales(pos):
    movimientos = []
    for dx, dy in MOVIMIENTOS_L:
        nx, ny = pos[0] + dx, pos[1] + dy
        if 0 <= nx < FILAS and 0 <= ny < COLUMNAS:
            movimientos.append((nx, ny))
    return movimientos

def main():
    pygame.init()
    icono = pygame.image.load(os.path.join(BASE_DIR, "assets", "imagenes", "yoshi-verde.png"))
    pygame.display.set_icon(icono)
    pantalla = pygame.display.set_mode((COLUMNAS * DIMENSION_CELDA, FILAS * DIMENSION_CELDA))
    pygame.display.set_caption("Yoshi's zones")

    # Generar posiciones iniciales válidas
    yoshi_verde = generar_posicion_random(CASILLAS_ESPECIALES)
    yoshi_rojo = generar_posicion_random(CASILLAS_ESPECIALES + [yoshi_verde])

    reloj = pygame.time.Clock()
    en_juego = True

    while en_juego:
        pantalla.fill(COLOR_NEGRO)
        dibujar_tablero(pantalla, yoshi_verde, yoshi_rojo)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                en_juego = False

            # Movimiento de prueba con teclas
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    # Mueve aleatoriamente los Yoshis en forma de "L"
                    posibles_verde = obtener_movimientos_legales(yoshi_verde)
                    posibles_rojo = obtener_movimientos_legales(yoshi_rojo)
                    if posibles_verde:
                        yoshi_verde = random.choice(posibles_verde)
                    if posibles_rojo:
                        yoshi_rojo = random.choice(posibles_rojo)

        pygame.display.flip()
        reloj.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()