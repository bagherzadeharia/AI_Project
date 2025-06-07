import sys
import random
import copy
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QSpinBox, QLabel, QPushButton,
    QTextEdit
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt

# Genetic algorithm functions

def create_initial_population(pop_size, genome_length, n_ones):
    population = []
    for _ in range(pop_size):
        individual = [0] * genome_length
        ones_indices = random.sample(range(genome_length), n_ones)
        for idx in ones_indices:
            individual[idx] = 1
        population.append(individual)
    return population


def calculate_fitness(individual, exposures):
    return sum(bit * exposures[i] for i, bit in enumerate(individual))


def tournament_selection(population, exposures, k=3):
    contenders = random.sample(population, k)
    return max(contenders, key=lambda ind: calculate_fitness(ind, exposures))


def repair(child, n_ones):
    while sum(child) > n_ones:
        i = random.choice([i for i, b in enumerate(child) if b == 1])
        child[i] = 0
    while sum(child) < n_ones:
        i = random.choice([i for i, b in enumerate(child) if b == 0])
        child[i] = 1


def crossover(parent1, parent2, n_ones):
    length = len(parent1)
    child1, child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
    p1, p2 = sorted(random.sample(range(1, length - 1), 2))
    child1[p1:p2], child2[p1:p2] = parent2[p1:p2], parent1[p1:p2]
    repair(child1, n_ones)
    repair(child2, n_ones)
    return child1, child2


def mutate(individual, mutation_rate, n_ones):
    if random.random() < mutation_rate:
        ones = [i for i, b in enumerate(individual) if b == 1]
        zeros = [i for i, b in enumerate(individual) if b == 0]
        if ones and zeros:
            i1 = random.choice(ones)
            i0 = random.choice(zeros)
            individual[i1], individual[i0] = 0, 1
    return individual


def genetic_algorithm(exposures, pop_size, generations, n_ones, mutation_rate):
    population = create_initial_population(pop_size, len(exposures), n_ones)
    for _ in range(generations):
        new_pop = []
        elite = max(population, key=lambda ind: calculate_fitness(ind, exposures))
        new_pop.append(elite)
        while len(new_pop) < pop_size:
            p1 = tournament_selection(population, exposures)
            p2 = tournament_selection(population, exposures)
            while p2 == p1:
                p2 = tournament_selection(population, exposures)
            c1, c2 = crossover(p1, p2, n_ones)
            new_pop.append(mutate(c1, mutation_rate, n_ones))
            if len(new_pop) < pop_size:
                new_pop.append(mutate(c2, mutation_rate, n_ones))
        population = new_pop
    best = max(population, key=lambda ind: calculate_fitness(ind, exposures))
    return best, calculate_fitness(best, exposures)

# Main GUI
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AstroBot Solar Panel Placement")
        self.resize(650, 450)
        self.init_ui()

    def init_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(spacing=10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Exposure table
        self.table = QTableWidget(1, 0)
        self.table.setHorizontalHeaderLabels(["Exposure Values"])
        default = [8.5, 2.3, 9.1, 4.2, 7.8, 3.1, 6.7, 9.8, 1.5, 5.4]
        for val in default:
            idx = self.table.columnCount()
            self.table.insertColumn(idx)
            item = QTableWidgetItem(str(val))
            item.setFont(QFont("Arial", 16))
            self.table.setItem(0, idx, item)
        layout.addWidget(QLabel("Exposures (edit directly):"))
        layout.addWidget(self.table)

        # Parameters
        controls = [
            ("Population", 10, 2, 1000),
            ("Generations", 20, 1, 1000),
            ("Panels", 5, 1, self.table.columnCount()),
            ("Mutation", 10, 0, 100)
        ]
        params_layout = QHBoxLayout(spacing=20)
        for name, val, mn, mx in controls:
            box = QVBoxLayout()
            lbl = QLabel(f"{name}:")
            lbl.setFont(QFont("Arial", 16))
            spin = QSpinBox()
            spin.setRange(mn, mx)
            spin.setValue(val)
            spin.setFont(QFont("Arial", 16))
            if name == "Mutation":
                spin.setSuffix(" %")
            setattr(self, f"{name.lower()}_spin", spin)
            box.addWidget(lbl)
            box.addWidget(spin)
            params_layout.addLayout(box)
        layout.addLayout(params_layout)

        # Run button
        self.run_btn = QPushButton("Run GA")
        self.run_btn.setFont(QFont("Arial", 16))
        self.run_btn.setFixedHeight(40)
        self.run_btn.clicked.connect(self.run_ga)
        layout.addWidget(self.run_btn, alignment=Qt.AlignCenter)

        # Output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Courier New", 16))
        layout.addWidget(self.output)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Light Fusion theme
        QApplication.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        QApplication.setPalette(palette)

        # Global font
        QApplication.setFont(QFont("Arial", 16))

    def parse_exposures(self):
        vals = []
        for c in range(self.table.columnCount()):
            item = self.table.item(0, c)
            try:
                vals.append(float(item.text()))
            except:
                pass
        return vals

    def run_ga(self):
        exposures = self.parse_exposures()
        pop = self.population_spin.value()
        gens = self.generations_spin.value()
        panels = self.panels_spin.value()
        mutation = self.mutation_spin.value() / 100.0
        best, fit = genetic_algorithm(exposures, pop, gens, panels, mutation)
        self.output.setPlainText(
            f"Best Genome: {best}\nTotal Exposure: {fit:.2f}"
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
