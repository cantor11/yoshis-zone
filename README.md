# Proyecto 2 - Yoshi’s Zones

## Universidad del Valle – Ingeniería de Sistemas y Computación  
- **Asignatura:** Inteligencia Artificial  
- **Semestre:**  2025-I

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

---

## Cómo ejecutar

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT.

---