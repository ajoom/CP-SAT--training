#!/usr/bin/env python3
from ortools.sat.python import cp_model

board_size = 100


model = cp_model.CpModel()


# we can have at most "board_size" queens, for each one, we're loooing for what row they'll be placed on 
queens = [model.new_int_var(0, board_size - 1, f"x_{i}") for i in range(board_size)] 




# no two queens on the same row
model.add_all_different(queens)

# no two queens on the same diagonal
model.add_all_different(
    queens[i] + i for i in range(board_size)
)

model.add_all_different(
    queens[i] - i for i in range(board_size)
)


solver = cp_model.CpSolver()

# solver.parameters.enumerate_all_solutions = True 
# solver.parameters.max_time_in_seconds = 10.0 we can set time limit for the solver, we also have "solution_limit": how many solutions before you stop

status = solver.solve(model)

print(f"Status: {solver.status_name(status)}")

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    for row in range(board_size):
        print(" ".join("Q" if solver.value(queens[col]) == row else "." for col in range(board_size)))
