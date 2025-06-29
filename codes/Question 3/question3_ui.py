import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Dict
import time


steps = []


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
        steps.append(dict(assignment))
        return assignment

    for task in tasks:
        if task not in assignment:
            for time_slot in range(1, 6):
                if isValidAssignment(assignment, task, time_slot, subsystems, power_needs, power_limits):
                    assignment[task] = time_slot
                    steps.append(dict(assignment))
                    result = backtrack(assignment.copy(), tasks, subsystems, power_needs, power_limits)
                    if result is not None:
                        return result
            break

    return None


def visualize_assignment(steps, tasks, subsystems, power_needs):
    fig, ax = plt.subplots()
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0, len(tasks) + 1)
    ax.set_xticks(range(1, 6))
    ax.set_yticks(range(1, len(tasks)+1))
    ax.set_yticklabels(tasks)
    ax.set_xlabel("Time Slot")
    ax.set_title("Task Scheduling Visualization")

    texts = []

    def update(frame):
        ax.clear()
        ax.set_xlim(0.5, 5.5)
        ax.set_ylim(0, len(tasks) + 1)
        ax.set_xticks(range(1, 6))
        ax.set_yticks(range(1, len(tasks)+1))
        ax.set_yticklabels(tasks)
        ax.set_xlabel("Time Slot")
        ax.set_title("Task Scheduling Visualization")

        assignment = steps[frame]
        for idx, task in enumerate(tasks, start=1):
            if task in assignment:
                time_slot = assignment[task]
                subsystem = subsystems[task]
                power = power_needs[task]
                rect = plt.Rectangle((time_slot - 0.4, idx - 0.4), 0.8, 0.8, color='skyblue')
                ax.add_patch(rect)
                ax.text(time_slot, idx, f"{task}\n{subsystem}\n{power}", ha='center', va='center', fontsize=8)

    ani = FuncAnimation(fig, update, frames=len(steps), interval=800, repeat=False)
    plt.tight_layout()
    plt.show()


def main():
    print("=== Task Scheduling with Backtracking ===")
    tasks = ('T1', 'T2', 'T3', 'T4', 'T5')
    subsystems: Dict[str, str] = {
        'T1': 'Navigation',
        'T2': 'Sampling',
        'T3': 'Communication',
        'T4': 'Navigation',
        'T5': 'Sampling'
    }
    power_needs: Dict[str, int] = {
        'T1': 5,
        'T2': 4,
        'T3': 6,
        'T4': 7,
        'T5': 3
    }
    power_limits = (10, 6, 12, 8, 10)

    assignment = backtrack({}, tasks, subsystems, power_needs, power_limits)

    if assignment:
        print("\n--- Task Assignment Found ---")
        for task, time_slot in assignment.items():
            print(f"{task}: Time slot {time_slot} (Subsystem: {subsystems[task]}, Power: {power_needs[task]})")
    else:
        print("No solution found.")

    visualize_assignment(steps, tasks, subsystems, power_needs)


if __name__ == "__main__":
    main()
