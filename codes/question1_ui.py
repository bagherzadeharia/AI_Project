import sys
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont
from collections import deque

GRID_SIZE = 5
DELAY = 250

class Cell(QLabel):
    def __init__(self, value):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        # Allow cells to expand and shrink with the grid
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyle(value)

    def setStyle(self, value):
        if value == 1:
            self.setStyleSheet("background-color: #E74C3C;")  # Red for obstacles
        elif value == 'visited':
            self.setStyleSheet("background-color: #3498DB;")  # Blue for visited
        elif value == 'path':
            self.setStyleSheet("background-color: #28A745;")  # Green for path
        else:
            self.setStyleSheet("background-color: #D7D7D7;")  # White for empty

class BFSVisualizer(QWidget):
    def __init__(self, grid):
        super().__init__()
        self.setWindowTitle("AstroBot SatNav System")
        # Set white background for the entire window
        self.setStyleSheet("background-color: #F3F3F3;")
        self.grid_data = grid
        self.cells = []
        self.queue = deque()
        self.visited = set()
        self.path_found = False

        self.setup_ui()

    def setup_ui(self):
        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title label
        title_label = QLabel("AstroBot SatNav System")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333;")
        main_layout.addWidget(title_label, 0)  # No stretch

        # Grid widget
        grid_widget = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(2)  # 2px spacing between cells for separation
        for r in range(GRID_SIZE):
            row = []
            for c in range(GRID_SIZE):
                cell = Cell(self.grid_data[r][c])
                grid_layout.addWidget(cell, r, c)
                row.append(cell)
            self.cells.append(row)
        grid_widget.setLayout(grid_layout)
        main_layout.addWidget(grid_widget, 1)  # Stretch to fill available space

        # Controls layout
        controls_layout = QHBoxLayout()
        controls_layout.addStretch(1)  # Center controls
        self.start_button = QPushButton("Navigate")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                font-size: 16px;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        self.start_button.clicked.connect(self.start_bfs)
        controls_layout.addWidget(self.start_button)

        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #333333; font-size: 14px;")
        controls_layout.addWidget(self.status_label)
        controls_layout.addStretch(1)  # Center controls

        main_layout.addLayout(controls_layout, 0)  # No stretch
        self.setLayout(main_layout)

    def color_cell(self, r, c, value):
        self.cells[r][c].setStyle(value)

    def start_bfs(self):
        if self.grid_data[0][0] == 1 or self.grid_data[4][4] == 1:
            self.status_label.setText("Start or end blocked.")
            return

        self.status_label.setText("Navigating...")
        self.queue.append((0, 0, [(0, 0)]))
        self.visited.add((0, 0))
        QTimer.singleShot(DELAY, self.bfs_step)

    def bfs_step(self):
        if not self.queue:
            if not self.path_found:
                self.status_label.setText("No path found.")
            return

        r, c, path = self.queue.popleft()
        if (r, c) != (0, 0):
            self.color_cell(r, c, 'visited')

        if (r, c) == (4, 4):
            for pr, pc in path:
                self.color_cell(pr, pc, 'path')
            self.path_found = True
            self.status_label.setText("Path found!")
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
    app.setFont(QFont("Arial", 12))
    window = BFSVisualizer(grid)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()