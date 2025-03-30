import heapq
from src.models.nav_graph import NavGraph  # Import NavGraph

def a_star_pathfinding(graph: NavGraph, start, goal):
    """
    A* pathfinding algorithm.
    """
    open_set = [(0, start)]  # Priority queue (f_score, node)
    came_from = {}
    g_score = {node: float('inf') for node in graph.vertices}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph.vertices}
    f_score[start] = heuristic(graph, start, goal)

    while open_set:
        current_f_score, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in graph.get_neighbors(current):
            temp_g_score = g_score[current] + 1  # Assuming edge cost is 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(graph, neighbor, goal)
                if (f_score[neighbor], neighbor) not in open_set:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found

def heuristic(graph: NavGraph, node, goal):
    """
    Heuristic function (Euclidean distance).
    """
    x1, y1 = graph.vertices[node]["coordinates"]
    x2, y2 = graph.vertices[goal]["coordinates"]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def reconstruct_path(came_from, current):
    """
    Reconstructs the path from the came_from dictionary.
    """
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]