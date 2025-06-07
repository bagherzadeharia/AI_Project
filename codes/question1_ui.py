import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QPalette
from collections import deque

GRID_SIZE = 5
DELAY = 250


class Cell(QLabel):
    def __init__(self, value):
        super().__init__()
        self.setFixedSize(60, 60)
        self.setAlignment(Qt.AlignCenter)
        self.setAutoFillBackground(True)
        self.setStyle(value)

    def setStyle(self, value):
        palette = self.palette()
        if value == 1:
            palette.setColor(QPalette.Window, QColor('black'))
        elif value == 'visited':
            palette.setColor(QPalette.Window, QColor('skyblue'))
        elif value == 'path':
            palette.setColor(QPalette.Window, QColor('green'))
        else:
            palette.setColor(QPalette.Window, QColor('white'))
        self.setPalette(palette)


class BFSVisualizer(QWidget):
    def __init__(self, grid):
        super().__init__()
        self.setWindowTitle("AstroBot SatNav System")
        self.grid_data = grid
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.cells = []
        self.queue = deque()
        self.visited = set()
        self.path_found = False

        self.setup_grid()
        self.start_button = QPushButton("Navigate")
        self.grid_layout.addWidget(self.start_button, GRID_SIZE, 0, 1, GRID_SIZE)
        self.start_button.clicked.connect(self.start_bfs)

    def setup_grid(self):
        for r in range(GRID_SIZE):
            row = []
            for c in range(GRID_SIZE):
                cell = Cell(self.grid_data[r][c])
                self.grid_layout.addWidget(cell, r, c)
                row.append(cell)
            self.cells.append(row)

    def color_cell(self, r, c, value):
        self.cells[r][c].setStyle(value)

    def start_bfs(self):
        if self.grid_data[0][0] == 1 or self.grid_data[4][4] == 1:
            print("Start or end blocked.")
            return

        self.queue.append((0, 0, [(0, 0)]))
        self.visited.add((0, 0))
        QTimer.singleShot(DELAY, self.bfs_step)

    def bfs_step(self):
        if not self.queue or self.path_found:
            return

        r, c, path = self.queue.popleft()
        if (r, c) != (0, 0):
            self.color_cell(r, c, 'visited')

        if (r, c) == (4, 4):
            for pr, pc in path:
                self.color_cell(pr, pc, 'path')
            self.path_found = True
            print("Path:", path)
            return

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                if self.grid_data[nr][nc] == 0 and (nr, nc) not in self.visited:
                    self.visited.add((nr, nc))
                    self.queue.append((nr, nc, path + [(nr, nc)]))

        QTimer.singleShot(DELAY, self.bfs_step)


def main():
    grid = [
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    app = QApplication(sys.argv)
    window = BFSVisualizer(grid)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
