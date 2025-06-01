from collections import deque

def validate_grid(grid):
    if len(grid) != 5:
        return False
    if any(len(row) != 5 for row in grid):
        return False
    for row in grid:
        for cell in row:
            if cell not in {0, 1}:
                return False
    return True

def bfs_shortest_path(grid):
    if not validate_grid(grid):
        return "Invalid input. Grid must be 5x5 with only 0s and 1s."
    
    if grid[0][0] == 1 or grid[4][4] == 1:
        return "No path found. Start or end position is blocked."
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque()
    queue.append((0, 0, [(0, 0)]))
    visited = set()
    visited.add((0, 0))
    
    while queue:
        row, col, path = queue.popleft()
        
        if row == 4 and col == 4:
            return path
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 5 and 0 <= new_col < 5:
                if grid[new_row][new_col] == 0 and (new_row, new_col) not in visited:
                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col, path + [(new_row, new_col)]))
    
    return "No path exists to the destination."

grid = [
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

path = bfs_shortest_path(grid)
print("Path found:", path)