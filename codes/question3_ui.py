import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, QHeaderView
)
from PyQt5.QtCore import Qt


def isValidAssignment(assignment, task, time_slot, subsystems, power_needs, power_limits):
    if (time_slot in assignment.values()) or power_needs[task] > power_limits[time_slot - 1]:
        return False


    current_subsystem = subsystems[task]
    for adj_time in [time_slot - 1, time_slot + 1]:
        if adj_time in assignment.values():
            for t, slot in assignment.items():
                if slot == adj_time and subsystems[t] == current_subsystem:
                    return False
    return True


def backtrack(assignment, tasks, subsystems, power_needs, power_limits):
    if len(assignment) == len(tasks):
        return assignment

    for task in tasks:
        if task not in assignment:
            for time_slot in range(1, 6):
                if isValidAssignment(assignment, task, time_slot, subsystems, power_needs, power_limits):
                    assignment[task] = time_slot
                    result = backtrack(assignment.copy(), tasks, subsystems, power_needs, power_limits)
                    if result is not None:
                        return result
            break

    return None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AstroBot Task Assignment System")
        self.resize(800, 600)

        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Title
        self.title_label = QLabel("Task Scheduler")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Input section
        self.input_layout = QHBoxLayout()

        # Tasks group
        self.tasks_group = QGroupBox("Tasks")
        self.tasks_table = QTableWidget()
        self.tasks_table.setRowCount(5)
        self.tasks_table.setColumnCount(3)
        self.tasks_table.setHorizontalHeaderLabels(["Task", "Subsystem", "Power Need"])
        self.tasks_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tasks_table.verticalHeader().setVisible(False)

        self.tasks = ('T1', 'T2', 'T3', 'T4', 'T5')
        self.subsystems = {'T1': 'Navigation', 'T2': 'Sampling', 'T3': 'Communication', 'T4': 'Navigation', 'T5': 'Sampling'}
        self.power_needs = {'T1': 5, 'T2': 4, 'T3': 6, 'T4': 7, 'T5': 3}

        for i, task in enumerate(self.tasks):
            self.tasks_table.setItem(i, 0, QTableWidgetItem(task))
            self.tasks_table.setItem(i, 1, QTableWidgetItem(self.subsystems[task]))
            self.tasks_table.setItem(i, 2, QTableWidgetItem(str(self.power_needs[task])))

        self.tasks_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tasks_group.setLayout(QVBoxLayout())
        self.tasks_group.layout().addWidget(self.tasks_table)
        self.input_layout.addWidget(self.tasks_group)

        # Time slots group
        self.time_slots_group = QGroupBox("Time Slots")
        self.time_slots_table = QTableWidget()
        self.time_slots_table.setRowCount(5)
        self.time_slots_table.setColumnCount(2)
        self.time_slots_table.setHorizontalHeaderLabels(["Time Slot", "Power Limit"])
        self.time_slots_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.time_slots_table.verticalHeader().setVisible(False)

        self.power_limits = (10, 6, 12, 8, 10)
        for i in range(5):
            self.time_slots_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.time_slots_table.setItem(i, 1, QTableWidgetItem(str(self.power_limits[i])))

        self.time_slots_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.time_slots_group.setLayout(QVBoxLayout())
        self.time_slots_group.layout().addWidget(self.time_slots_table)
        self.input_layout.addWidget(self.time_slots_group)

        self.layout.addLayout(self.input_layout)

        # Find assignment button
        self.find_button = QPushButton("Find Assignment")
        self.find_button.clicked.connect(self.find_assignment)
        self.layout.addWidget(self.find_button)

        # Assignment group
        self.assignment_group = QGroupBox("Assignment")
        self.assignment_table = QTableWidget()
        self.assignment_table.setRowCount(5)
        self.assignment_table.setColumnCount(2)
        self.assignment_table.setHorizontalHeaderLabels(["Task", "Time Slot"])
        self.assignment_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.assignment_table.verticalHeader().setVisible(False)
        self.assignment_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.assignment_group.setLayout(QVBoxLayout())
        self.assignment_group.layout().addWidget(self.assignment_table)
        self.layout.addWidget(self.assignment_group)
        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 16px;
            }
            QTableWidget {
                background-color: white;
                gridline-color: #d0d0d0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
            }
        """)

    def find_assignment(self):
        assignment = backtrack({}, self.tasks, self.subsystems, self.power_needs, self.power_limits)
        if assignment:
            self.status_label.setText("Assignment found")
            for i, task in enumerate(sorted(assignment.keys())):
                self.assignment_table.setItem(i, 0, QTableWidgetItem(task))
                self.assignment_table.setItem(i, 1, QTableWidgetItem(str(assignment[task])))
        else:
            self.status_label.setText("No solution found")
            self.assignment_table.clearContents()


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
