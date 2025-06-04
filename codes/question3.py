def isValidAssignment(assignment, task, time_slot, subsystems, power_needs, power_limits):
    if time_slot in assignment.values():
        return False

    if power_needs[task] > power_limits[time_slot - 1]:
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


def main() -> None:
    tasks = ['T1', 'T2', 'T3', 'T4', 'T5']
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
    power_limits = [10, 6, 12, 8, 10]
    assignment = backtrack({}, tasks, subsystems, power_needs, power_limits)

    if assignment:
        print("Task assignment found:")
        for task, time_slot in assignment.items():
            print(f"{task}: Time slot {time_slot} (Subsystem: {subsystems[task]}, Power: {power_needs[task]})")
    else:
        print("No solution found")


if __name__ == "__main__":
    main()
