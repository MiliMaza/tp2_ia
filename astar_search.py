import heapq # Para la cola de prioridad

class Node:
    def __init__(self, position, parent=None, g=0, h=0):
        self.position = position  # Posición del nodo (sobre x)
        self.parent = parent      # Nodo padre
        self.g = g                # Costo acumulado desde el inicio
        self.h = h                # Valor heurístico (estimación a la meta)
        self.f = g + h            # Función de evaluación f(n) = g(n) + h(n)
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other):
        return self.f < other.f

"""
Función heurística que estima la distancia al objetivo.
Recibe como parámetros:
    -position: Posición actual del brazo (punto B)
    -target: Posición objetivo (punto A, desconocida inicialmente)
    -surface_profile: Información del relieve de la superficie (simulada como un diccionario)
Devuelve un valor heurístico que estima la distancia al objetivo (menor es mejor)
"""
def heuristic(position, target, surface_profile):
    # Distancia directa (valor absoluto)
    direct_distance = abs(position - target)
    
    # Factor de corrección basado en el relieve
    # Cuanto más cerca del punto de montaje, mejor el "ajuste" del relieve
    correction = surface_profile.get(position, 10) / 10
    
    return direct_distance * correction

"""
Método de búsqueda A* para encontrar la posición correcta de montaje.
Recibe como parámetros:
    -start_position: Posición inicial del brazo (punto B)
    -target_position: Posición objetivo (punto A, desconocida inicialmente)
    -delta: Incremento de posición en cada movimiento
    -surface_profile: Información del relieve de la superficie (simulada como un diccionario)
Devuelve el camino encontrado o None si no hay solución.
"""
def a_star_search(start_position, target_position, delta=1, surface_profile=None):
    # Si no se proporciona perfil de superficie, crea uno simple
    if surface_profile is None:
        # Simula un perfil donde los valores más bajos están cerca del objetivo
        surface_profile = {
            0: 10,    # Posición inicial
            1: 7,     # Mejora al acercarse
            2: 3,     # Mejora sustancial
            3: 1,     # Punto óptimo (objetivo)
            4: 4,     # Se aleja
            5: 8      # Se aleja más
        }
    
    # Nodo inicial
    start_node = Node(
        position=start_position,
        g=0,
        h=heuristic(start_position, target_position, surface_profile)
    )
    
    # Cola de prioridad para A*
    open_list = []
    heapq.heappush(open_list, start_node)
    
    # Lista abierta y cerrada para los nodos que vamos visitando y que nos quedan por visitar
    open_set = {start_position}
    closed_set = set()
    
    while open_list:
        # Obtener nodo con menor f
        current_node = heapq.heappop(open_list)
        open_set.remove(current_node.position)
        
        # Verificar si es el objetivo
        if current_node.position == target_position:
            # Construir el camino
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Invertir para obtener el camino de inicio a fin
        
        # Añadir a cerrados
        closed_set.add(current_node.position)
        
        # Explorar vecinos
        for move in [-delta, delta]:  # Izquierda y derecha
            neighbor_pos = current_node.position + move
            
            # Verificar si está en cerrados
            if neighbor_pos in closed_set:
                continue
            
            # Calcular costos
            g = current_node.g + 1  # Costo del movimiento
            h = heuristic(neighbor_pos, target_position, surface_profile)
            
            # Crear nodo vecino
            neighbor = Node(
                position=neighbor_pos,
                parent=current_node,
                g=g,
                h=h
            )
            
            # Si ya está en abiertos con mejor costo, ignorar
            if neighbor_pos in open_set:
                # Verificar si este camino es mejor
                continue
            
            # Añadir a abiertos
            heapq.heappush(open_list, neighbor)
            open_set.add(neighbor_pos)
    
    # No se encontró solución
    return None

# Ejemplo de uso con espacio reducido
start_pos = 0        # Posición inicial B
target_pos = 3       # Posición objetivo A (desconocida para el algoritmo)
delta_h = 1          # Incremento en cada paso

# Crear un perfil de superficie simulado
# Los valores más bajos indican mejor "ajuste" cerca del punto de montaje
surface_profile = {
    0: 10,   # Punto inicial B
    1: 7,    # Un paso hacia el objetivo
    2: 3,    # Dos pasos hacia el objetivo  
    3: 1,    # Punto objetivo A (óptimo)
    4: 4,    # Alejándose del objetivo
    5: 8     # Más lejos
}

# Ejecutar la búsqueda A*
path = a_star_search(start_pos, target_pos, delta_h, surface_profile)

# Mostrar resultado
print("Camino encontrado por A*:", path)
print("Número de pasos:", len(path) - 1)

# Simulación de movimientos en el espacio de estados
print("\nSimulación de la búsqueda:")
for i, pos in enumerate(path):
    print(f"Paso {i}: Posición = {pos}, Valor superficie = {surface_profile[pos]}")