import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.animation import FuncAnimation
from collections import deque

GRID_SIZE = 5

def gridValidation(grid) -> bool:
    return len(grid) == GRID_SIZE and all(len(row) == GRID_SIZE and all(cell in {0, 1} for cell in row) for row in grid)

def BFS_with_animation(grid):
    if not gridValidation(grid):
        return [], [], False

    if grid[0][0] == 1 or grid[GRID_SIZE-1][GRID_SIZE-1] == 1:
        return [], [], False

    visited_order = []
    path = []
    queue = deque()
    queue.append((0, 0, [(0, 0)]))
    visited = set()
    visited.add((0, 0))

    while queue:
        row, col, curr_path = queue.popleft()
        visited_order.append((row, col))

        if (row, col) == (GRID_SIZE-1, GRID_SIZE-1):
            path = curr_path
            return visited_order, path, True

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                if grid[r][c] == 0 and (r, c) not in visited:
                    visited.add((r, c))
                    queue.append((r, c, curr_path + [(r, c)]))

    return visited_order, [], False


def visualize(grid, visited_order, path, success):
    cmap = colors.ListedColormap(['white', 'black', 'lightblue', 'green', 'red'])
    norm = colors.BoundaryNorm([0, 1, 2, 3, 4, 5], cmap.N)

    display_grid = [[cell for cell in row] for row in grid]
    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(display_grid, cmap=cmap, norm=norm)

    def update(frame):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if (i, j) in visited_order[:frame]:
                    if display_grid[i][j] == 0:
                        display_grid[i][j] = 2


        if frame >= len(visited_order):
            for r, c in path:
                display_grid[r][c] = 3

            if success:
                display_grid[0][0] = 3
                display_grid[GRID_SIZE - 1][GRID_SIZE - 1] = 3
            else:
                display_grid[0][0] = 4
                display_grid[GRID_SIZE - 1][GRID_SIZE - 1] = 4

        im.set_data(display_grid)
        return [im]

    ani = FuncAnimation(fig, update, frames=len(visited_order) + 10, interval=300, repeat=False)

    ax.set_xticks(range(GRID_SIZE))
    ax.set_yticks(range(GRID_SIZE))
    ax.set_xticklabels(range(GRID_SIZE))
    ax.set_yticklabels(range(GRID_SIZE))
    ax.set_title("BFS Pathfinding Visualization")
    ax.grid(True, color='gray', linewidth=0.5)
    ax.set_xticks([x - 0.5 for x in range(1, GRID_SIZE)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, GRID_SIZE)], minor=True)
    ax.tick_params(bottom=True, left=True, labelbottom=True, labelleft=True)
    plt.show()


def main():
    grid = [
        [0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    visited_order, path, success = BFS_with_animation(grid)
    print("Path Found:" if success else "No path found.")
    print("Path:", path)
    visualize(grid, visited_order, path, success)


if __name__ == "__main__":
    main()
