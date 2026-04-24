# astar.py
import heapq

def heuristic(a, b):
    """Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos, grid_size, obstacles):
    """Get walkable neighbors (up, down, left, right)."""
    neighbors = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        x, y = pos[0] + dx, pos[1] + dy
        if 0 <= x < grid_size and 0 <= y < grid_size and (x, y) not in obstacles:
            neighbors.append((x, y))
    return neighbors

def astar_search(start, goal, grid_size, obstacles):
    """A* algorithm to find the shortest path."""
    pq = []
    heapq.heappush(pq, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while pq:
        current = heapq.heappop(pq)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in get_neighbors(current, grid_size, obstacles):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(pq, (f_score[neighbor], neighbor))

    return None  # No path found
