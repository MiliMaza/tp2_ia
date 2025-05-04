class Node:
    def __init__(self, position, parent=None):
        self.position = position  # Posición del nodo (sobre x)
        self.parent = parent      # Nodo padre
    
    def __eq__(self, other):
        return self.position == other.position

"""
Método de búsqueda primero en profundidad para encontrar la posición correcta de montaje.
Recibe como parámetros:
    -start_position: Posición inicial del brazo (punto B)
    -target_position: Posición objetivo (punto A) (que inicialmente se desconoce)
    -delta: Incremento de posición en cada movimiento
    -max_depth: Profundidad máxima de búsqueda
Devuelve el camino encontrado o nada (si no hay solución)
"""
def depth_first_search(start_position, target_position, delta=1, max_depth=10):
    # Nodo inicial
    start_node = Node(start_position)
    
    # Pila
    stack = [(start_node, 0)]  # Incluimos la profundidad como parte del estado
    
    # Grupo para nodos visitados
    visited = set([start_position])
    
    # Mientras la pila no esté vacía
    while stack:
        # Extraer nodo y su profundidad de la pila
        current_node, depth = stack.pop()
        
        # Verificar si es el objetivo
        if current_node.position == target_position:
            # Construir el camino
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Invertir para obtener el camino de inicio a fin
        
        # Si la profundidad actual es menor al límite, expandir nodos
        if depth < max_depth:
            # Generar posiciones a la izquierda y a la derecha
            left_pos = current_node.position - delta
            right_pos = current_node.position + delta
            
            # Primero intentamos a la derecha (profundidad)
            if right_pos not in visited:
                right_node = Node(right_pos, current_node)
                stack.append((right_node, depth + 1))
                visited.add(right_pos)
            
            # Luego a la izquierda
            if left_pos not in visited:
                left_node = Node(left_pos, current_node)
                stack.append((left_node, depth + 1))
                visited.add(left_pos)
    
    # Si no se encontró solución
    return None

# Ejemplo de uso con espacio reducido
start_pos = 0        # Posición inicial B
target_pos = 3       # Posición objetivo A (desconocida para el algoritmo)
delta_h = 1          # Incremento en cada paso

# Ejecutar la búsqueda y mostrar el resultado
path = depth_first_search(start_pos, target_pos, delta_h)

# Si hay solución
if path:
    print("Camino encontrado por DFS:", path)
    print("Número de pasos:", len(path) - 1)
    
    # Simulamos los movimientos en el espacio de estados
    print("\nSimulación de la búsqueda:")
    for i, pos in enumerate(path):
        print(f"Paso {i}: Posición = {pos}")
else:
    print("No se encontró un camino hacia el objetivo.")