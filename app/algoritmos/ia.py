import math
import random
from .estado import GameState, ZONAS

def manhattan_distance(pos1, pos2):
    """Calcula la distancia Manhattan entre dos posiciones."""
    return abs(pos1[0] -  pos2[0]) + abs(pos1[1] - pos2[1])

def zona_controlada_por(zona, state):
    """
    Retorna quien controla la zona: 'verde', 'rojo', o None si esta disputada.
    Una zona se considera controlada si un jugador tiene mayoria de casillas.
    """
    verde_count = sum(1 for cell in zona if state.painted.get(cell) == "verde")
    rojo_count = sum(1 for cell in zona if state.painted.get(cell) == "rojo")

    if verde_count > rojo_count:
        return "verde"
    elif rojo_count > verde_count:
        return "rojo"
    return None

def evaluate_position(state: GameState, difficulty: str):
    """
    Funcion heuristica avanzada que evalua la posicion considerando:
    1. Zonas completamente ganadas (máxima prioridad)
    2. Control parcial de zonas
    3. Posicionamiento estratégico
    4. Comportamiento específico por dificultad
    5. Prevención de bucles
    """
    if state.is_terminal():
        verde_zones, rojo_zones = state.zonas_ganadas()
        if verde_zones > rojo_zones:
            return 10000 # Victoria de verde
        elif rojo_zones > verde_zones:
            return -10000 # Victoria de rojo
        else:
            return 0 # Empate
        
    score = 0
    verde_pos = state.positions["verde"]
    rojo_pos = state.positions["rojo"]

    # 1. ZONAS GANADAS (peso maximo)
    verde_zones, rojo_zones = state.zonas_ganadas()
    score += (verde_zones - rojo_zones) * 5000
    
    # 2. CONTROL PARCIAL DE ZONAS
    for zona in ZONAS:
        verde_cells = sum(1 for cell in zona if state.painted.get(cell) == "verde")
        rojo_cells = sum(1 for cell in zona if state.painted.get(cell) == "rojo")
        total_painted = verde_cells + rojo_cells

        # Si la zona no esta completamente pintada
        if total_painted < len(zona):
            # Ventaja por tener mas casillas en la zona
            score += (verde_cells - rojo_cells) * 200
            
            # Bonus por estar cerca de ganar la zona\
            if verde_cells > rojo_cells and verde_cells >= len(zona) // 2:
                score += 300
            elif rojo_cells > verde_cells and rojo_cells >= len(zona) // 2:
                score -= 300

    # 3. POSICIONAMIENTO ESTRATEGICO
    for zona in ZONAS:
        controller = zona_controlada_por(zona, state)
        if controller is None: # Zona disputada
            # Calcular distancia minima a casillas no pintadas de la zona
            unpainted_cells = [cell for cell in zona if cell not in state.painted]
            if unpainted_cells:
                min_dist_verde = min(manhattan_distance(verde_pos, cell) for cell in unpainted_cells)
                min_dist_rojo = min(manhattan_distance(rojo_pos, cell) for cell in unpainted_cells)

                # Ventaja por estar mas cerca de zona disputada
                score += (min_dist_rojo - min_dist_verde) * 20

    # 4. COMPORTAMIENTO ESPECIFICO POR DIFICULTAD
    if difficulty == "Principiante":
        # DEFENSIVO: Evita riesgos, prioriza zonas seguras
        score *= 0.7 # Reduce agresividad general
        
        # Penaliza estar muy cerca del oponente
        if manhattan_distance(verde_pos, rojo_pos) <= 3:
            score -= 100
            
        # Bonus por mantener distancia segura
        if manhattan_distance(verde_pos, rojo_pos) >= 5:
            score += 50
            
        # Favorece zonas menos disputadas
        for zona in ZONAS:
            rojo_cells = sum(1 for cell in zona if state. painted.get(cell)) == "rojo"
            if rojo_cells == 0: # Zona sin presencia roja
                verde_cells = sum(1 for cell in zona if state. painted.get(cell)) == "verde"
                score += verde_cells * 50 # Bonus para zona "segura"

    elif difficulty == "Amateur":
        # BALANCEADO: Equilibrio entre ataque y defensa

        # Considera bloqueos adicionales
        for zona in ZONAS:
            rojo_cells = sum(1 for cell in zona if state.painted.get(cell) == "rojo")
            verde_cells = sum(1 for cell in zona if state.painted.get(cell) == "verde")

            # Si rojo esta ganando una zona, intenta bloquear
            if rojo_cells > verde_cells and rojo_cells >= 2:
                unpainted = [cell for cell in zona if cell not in state.painted] 
                if unpainted:
                    min_dist = min(manhattan_distance(verde_pos, cell) for cell in unpainted)
                    if min_dist <= 2: # Puede intervenir
                        score += 150 # Bonus por posibilidad de bloqueo
                        
                        
    elif difficulty == "Experto":
        # AGRESIVO: Maximiza control y bloquea activamente 
        score *= 1.3 # Incrementa agresividad general
        
        # Bonus por controlar el centro del tablero
        center_distance = manhattan_distance(verde_pos, (3.5, 3.5)) # Centro aproximado
        score += (7 - center_distance) * 10
        
        # Agresivo en bloqueos
        for zona in ZONAS:
            rojo_cells = sum(1 for cell in zona if state.painted.get(cell) == "rojo")
            verde_cells = sum(1 for cell in zona if state.painted.get(cell) == "verde")

            # Si rojo tiene ventaja, bloquear es prioridad alta
            if rojo_cells > verde_cells:
                unpainted = [cell for cell in zona if cell not in state.painted]
                if unpainted:
                    min_dist = min(manhattan_distance(verde_pos, cell) for cell in unpainted)
                    score += (5 - min_dist) * 80 # Fuerte incentivo a bloquear

            # Si verde tiene ventaja, proteger al zona
            elif verde_cells > rojo_cells:
                unpainted = [cell for cell in zona if cell not in state.painted]
                if unpainted:
                    min_dist = min(manhattan_distance(verde_pos, cell) for cell in unpainted)
                    score += (5 - min_dist) * 60 # Incentivo a asegurar zona
                    
    # 5. PREVENCIÓN DE POSICIONES ESTATICAS
    # Pequeño bonus aleatorio para evitar bucles
    score += random.randint(-10, 10)

    return score                        
    
    
def minimax_with_imperfection(state: GameState, depth: int, max_player: bool, limit: int, difficulty: str, alpha=float('-inf'), beta=float('inf')):
    """
    Minimax con poda Alpha-Beta y decisiones imperfectas.
    Las decisiones imperfectas se implementan eligiendo ocasionalmente 
    el segundo o tercer mejor movimiento según la dificultad.
    """
    if depth == limit or state.is_terminal():
        return evaluate_position(state, difficulty), None 

    player = "verde" if max_player else "rojo"
    moves = state.legal_moves(player)

    if not moves:
        return evaluate_position(state, difficulty), None

    # Evaluar todos los movimientos
    moves_scores = []
    for move in moves:
        child = state.clone()
        child.apply(player, move)
        score, _= minimax_with_imperfection(child, depth + 1, not max_player, limit, difficulty, alpha, beta)
        moves_scores.append((score, move))

        # Poda Alpha-Beta
        if max_player:
            alpha = max(alpha, score)
        else:
            beta = min(beta, score)
        if beta <= alpha:
            break

    # Ordenar movimientos por puntaje
    moves_scores.sort(reverse=max_player)

    # DECISIONES IMPERFECTAS: No siempre elegir el mejor movimiento
    if max_player:  # Solo aplicar imperfeccion a la IA (verde)
        imperfection_chance = {
            "Principiante": 0.4,  # 40% de chance de no elegir el mejor
            "Amateur": 0.2,       # 20% de chance 
            "Experto": 0.1        # 10% de chance
        }.get(difficulty, 0.1)

        if random.random() < imperfection_chance and len(moves_scores) > 1:
            # Elegir entre los 2-3 mejores movimientos en lugar del optimo
            top_moves = moves_scores[:min(3, len(moves_scores))]
            chosen_score, chosen_move = random.choice(top_moves)
            return chosen_score, chosen_move
        
    # Movimiento óptimo
    best_score, best_move = moves_scores[0]
    return best_score, best_move

    
def choose_move(state: GameState, difficulty: str):
    """
    Selecciona el mejor movimiento apra la IA usando Minimax mejorado.
    
     Args:
        state: Estado actual del juego
        difficulty: "Principiante", "Amateur" o "Experto"
    
    Returns:
        Mejor movimiento (fila, columna) o None si no hay movimientos
    """
    # Confiigurar profundidad segun dificultad
    depth_limits = {
        "Principiante": 2,
        "Amateur": 4,
        "Experto": 6
    }
    
    limit = depth_limits.get(difficulty, 2)

    # Ejecutar minimax mejorado

    _, best_move = minimax_with_imperfection(state, 0, True, limit, difficulty)

    return best_move