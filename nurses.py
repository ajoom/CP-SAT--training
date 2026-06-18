#!/usr/bin/env python3
from ortools.sat.python import cp_model



no_nurses = 5
no_shifts = 3
no_days = 7
shift_requests = [
    [[0, 0, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 1]],
    [[0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 1, 0], [1, 0, 0], [0, 0, 0], [0, 0, 1]],
    [[0, 1, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0], [0, 1, 0], [0, 0, 0]],
    [[0, 0, 1], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0]],
    [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0]],
]



model = cp_model.CpModel()

# create the variables
shifts = {}
for nurse in range(no_nurses):
    for day in range(no_days):
        for shift in range(no_shifts):
            shifts[(nurse, day, shift)] = model.new_bool_var(f"shift{nurse}_day{day}_shift{shift}")






# constraints

# 1- each shift is assigned to one nurse 
for day in range(no_days):
    for shift in range(no_shifts):
        model.add_exactly_one(shifts[(nurse, day, shift)] for nurse in range(no_nurses))

# 2- Each nurse works at most one shift per day.
for nurse in range(no_nurses):
    for day in range(no_days):
        model.add_at_most_one(shifts[(nurse, day, shift)] for shift in range(no_shifts)) # <======= add_at_most_one =====









# Assign as evenly as possible 

total_shifts = no_shifts * no_days

min_shifts_per_nurse = total_shifts // no_nurses

if total_shifts % no_nurses == 0:
    max_shifts_per_nurse = min_shifts_per_nurse
else:
    max_shifts_per_nurse = min_shifts_per_nurse + 1


# min <=  sum of shifts[{nurse, day, shift}]  <= max

for nurse in range(no_nurses):
    nurse_shifts_sum = sum(
        shifts[(nurse, day, shift)] 
        for day in range(no_days) 
        for shift in range(no_shifts)
    )

    model.add(
        min_shifts_per_nurse <= nurse_shifts_sum
    )

    model.add(
        nurse_shifts_sum <= max_shifts_per_nurse
    )






# objective

model.maximize(
    sum(
    shift_requests[nurse][day][shift] * shifts[(nurse, day, shift)]
    for nurse in range(no_nurses)
    for day in range(no_days)
    for shift in range(no_shifts)
    )
)





# solver 
solver = cp_model.CpSolver()
status = solver.solve(model)

print(f"Status: {solver.status_name(status)}")

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print(f"Objective value: {solver.objective_value}")

    for day in range(no_days):
        print(f"Day {day}")
        for nurse in range(no_nurses):
            for shift in range(no_shifts):
                if solver.value(shifts[(nurse, day, shift)]):
                    print(f"  Nurse {nurse} works shift {shift}")

