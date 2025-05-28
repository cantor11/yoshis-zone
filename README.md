# Proyecto 2 - Yoshi’s Zones

## Universidad del Valle – Ingeniería de Sistemas y Computación  
- **Asignatura:** Inteligencia Artificial  
- **Semestre:**  2025-I

---

## Autores

    Kevin Jordan Alzate – 2228507 <kevin.jordan@correounivalle.edu.co>

    Heidy Mina Garcia – 1931720 <heidy.mina@correounivalle.edu.co>

    Junior Orlando Cantor Arévalo – 2224949 <junior.cantor@correounivalle.edu.co>

    -

---

## Descripción

**Yoshi’s Zones** es un juego de dos jugadores (máquina vs. humano) sobre un tablero de 8×8. Cada jugador controla un Yoshi (verde para la máquina, rojo para el humano) que se mueve como un caballo de ajedrez. En las cuatro esquinas del tablero hay “zonas especiales”, cada una compuesta por la esquina y sus cuatro casillas adyacentes.  

- Cuando un Yoshi aterriza en una casilla de zona especial, pinta esa casilla con su color.  
- Las casillas pintadas quedan inhabilitadas para ambos jugadores.  
- El objetivo es pintar la mayoría de casillas de cada zona especial.  
- Gana quien conquiste más zonas al agotarse todas las casillas de zonas especiales.  

---

## Reglas y dinámica

1. La máquina (Yoshi verde) siempre inicia la partida.  
2. Los Yoshis se ubican aleatoriamente al inicio, fuera de las zonas especiales y sin coincidir.  
3. Cada turno un jugador mueve su Yoshi en “L” (movimiento de caballo).  
4. Si el movimiento aterriza en una casilla de zona especial no pintada, la pinta.  
5. El juego termina cuando no quedan casillas de zonas especiales libres.  
6. Se muestra en todo momento el conteo de zonas ganadas por cada jugador.  
7. Al final, se declara ganador o empate.

---

## Niveles de dificultad

| Nivel       | Profundidad límite del árbol minimax |
|-------------|---------------------------------------|
| Principiante| 2                                     |
| Amateur     | 4                                     |
| Experto     | 6                                     |

---

## Implementación

- **Minimax con poda imper­fecta**: La máquina construye un árbol de juego hasta la profundidad límite según el nivel y elige la jugada que maximice su utilidad heurística.  
- **Heurística**: Diferencia entre casillas pintadas por la máquina y por el humano en las zonas especiales aún no decididas.  

---

## Estructura del repositorio

### Carpeta `app/algoritmos/`

- **`estado.py`**  
  Contiene la lógica del juego, incluyendo el estado actual, las reglas de movimiento, el control de turnos, las zonas especiales, y la detección del final de la partida.



- **`ia.py`**  
  Implementa el algoritmo Minimax con profundidad variable según la dificultad, para que el Yoshi verde (IA) tome decisiones estratégicas durante el juego.

### Carpeta `app/interfaz/`

- **`menu.py`**  
    Script de la **interfaz gráfica** (Tkinter):
    - Ofrece un **ComboBox** para seleccionar la dificultad: Principiante, amateur o experto.
    - Se muestra un **panel de texto** con introducción e instrucciones de juego, tambien señala la dificultad en que se inicio el juego y el resultad.
    - Al pulsar "Iniciar" ejecuta el el juego con la dificultad deseada.
    - Incluye boton **salir**.

- **`tablero.py`**  
  Se encarga de generar y mostrar visualmente el tablero de juego de Yoshi's Zones en una ventana con **Pygame**. Inicializa las posiciones aleatorias de los Yoshis (verde y rojo), resalta las casillas especiales (zonas grises en las esquinas), y permite su movimiento en "L" como caballos de ajedrez. Controlará la lógica del juego, conteo de casillas marcadas y el sistema de turnos.

### Archivo `app/main.py`

Script principal para ejecutar la aplicación:
- Lanza la interfaz gráfica del proyecto.
- Punto de entrada para toda la aplicación.

---

## Ejecución del Proyecto

### Requisitos previos
- **Python** versión 3.8 o superior
- **Git** para clonar el repositorio

### Inicialización estándar

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/cantor11/yoshis-zone.git
   cd yoshis-zone
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación principal:**
   ```bash
   python main.py
   ```

Esto abrirá una interfaz gráfica construida con Tkinter. Desde allí, podrás seleccionar una dificultad y hacer clic en **Iniciar**, lo cual lanzará el tablero de juego generado con Pygame.

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT.

---