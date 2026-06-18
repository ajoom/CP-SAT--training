#!/usr/bin/env python3
from ortools.sat.python import cp_model

jobs_data = [  # task = (machine_id, processing_time).
    [(0, 3), (1, 2), (2, 2)],  # Job0
    [(0, 2), (2, 1), (1, 4)],  # Job1
    [(1, 4), (2, 3)],  # Job2
]






no_machines = 1 + max(task[0] for job in jobs_data for task in job)
tasks_of_machine = {machine: [] for machine in range(no_machines)} 
horizon = sum(task[1] for job in jobs_data for task in job)





# Variables

start_time = {}
end_time = {}
intervals = {}


model = cp_model.CpModel()


for job_index, job in enumerate(jobs_data):
    for task_index, task in enumerate(job):
        machine, duration = task

        start_time[(job_index, task_index)] = model.new_int_var(
            0, 
            horizon, 
            f"start_job{job_index}_task_{task_index}"
        )

        end_time[(job_index, task_index)] = start_time[(job_index, task_index)] + duration

        intervals[(job_index, task_index)] = model.new_interval_var( # <======== new_interval_var ============
            start_time[(job_index, task_index)],
            duration,
            end_time[(job_index, task_index)],
            f"interval_job{job_index}_task_{task_index}",
        )

        tasks_of_machine[machine].append((job_index, task_index))










# Constraints

# 1- each job should be assigned to the right machine (what matterns, tassk with same machine id)
# & no jobs should be overlaping on the same mahcine 

for machine in range(no_machines):
    machine_intervals = [
        intervals[(job_id, task_id)]
        for job_id, task_id in tasks_of_machine[machine]
    ]

    model.add_no_overlap(machine_intervals)   # <======== add_no_overlap ============


# 2- dependencies between tasks: 
for job_id, job in enumerate(jobs_data):
    for task_id in range(1, len(job)):
        model.add(
            start_time[(job_id, task_id)] >= end_time[(job_id, task_id - 1)]
        )








# Objective function
makespan = model.new_int_var(0, horizon, "makespan")
model.add_max_equality(makespan, end_time.values())  # <======== add_max_equality ============
model.minimize(makespan)



# solver
solver = cp_model.CpSolver()
status = solver.solve(model)

print(f"Status: {solver.status_name(status)}")

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print(f"Makespan: {solver.value(makespan)}")

    assigned_tasks = {machine: [] for machine in range(no_machines)}

    for job_id, job in enumerate(jobs_data):
        for task_id, task in enumerate(job):
            machine, duration = task
            start = solver.value(start_time[(job_id, task_id)])
            end = start + duration
            assigned_tasks[machine].append((start, end, job_id, task_id))

    for machine in range(no_machines):
        assigned_tasks[machine].sort()
        print(f"Machine {machine}:")

        for start, end, job_id, task_id in assigned_tasks[machine]:
            print(f"  job {job_id} task {task_id}: {start} -> {end}")


    # Colored schedule printing only.
    colors = [
        "\033[48;5;39m\033[30m",
        "\033[48;5;214m\033[30m",
        "\033[48;5;82m\033[30m",
        "\033[48;5;199m\033[30m",
        "\033[48;5;141m\033[30m",
        "\033[48;5;226m\033[30m",
    ]
    reset = "\033[0m"
    cell_width = 6
    solved_makespan = solver.value(makespan)

    print("\nColored schedule:")
    print("Time:    " + "".join(str(time).center(cell_width) for time in range(solved_makespan)))

    for machine in range(no_machines):
        row = [".".center(cell_width) for _ in range(solved_makespan)]

        for start, end, job_id, task_id in assigned_tasks[machine]:
            label = f"J{job_id}T{task_id}".center(cell_width)
            color = colors[job_id % len(colors)]

            for time in range(start, end):
                row[time] = f"{color}{label}{reset}"

        print(f"M{machine}:     " + "".join(row))

    print("\nLegend:")
    for job_id in range(len(jobs_data)):
        color = colors[job_id % len(colors)]
        print(f"  {color} Job {job_id} {reset}")
