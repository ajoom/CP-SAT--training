#!/usr/bin/env python3
from ortools.sat.python import cp_model


#       CP
# +     IS
# +    FUN
# --------
# =   TRUE

model = cp_model.CpModel()

base = 10

# create variables
c = model.new_int_var(1, base - 1, "C") # lower bound, upper bound, name
p = model.new_int_var(0, base - 1, "P") 
i = model.new_int_var(1, base - 1, "I") 
s = model.new_int_var(0, base - 1, "S") 
f = model.new_int_var(1, base - 1, "F") 
u = model.new_int_var(0, base - 1, "U") 
n = model.new_int_var(0, base - 1, "N") 
t = model.new_int_var(1, base - 1, "T") 
r = model.new_int_var(0, base - 1, "R") 
e = model.new_int_var(0, base - 1, "E") 


letters = [c, p, i, s, f, u, n, t, r, e]

# make sure we have enough letters
assert len(letters) <= base


# define constraints
model.add_all_different(letters)

model.add(
    (p + s + n) * 1
    + (c + i + u) * base
    + f * base * base
    ==
    e * 1
    + u * base
    + r * base * base
    + t * base * base * base
)


# solver
solver = cp_model.CpSolver()
solver.parameters.enumerate_all_solutions = True # Don't stop after finding the first feasible solution. Keep searching and report every solution.
status = solver.solve(model)

print(f"Status: {solver.status_name(status)}")

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print(f"C={solver.value(c)} P={solver.value(p)} I={solver.value(i)} S={solver.value(s)} F={solver.value(f)} U={solver.value(u)} N={solver.value(n)} T={solver.value(t)} R={solver.value(r)} E={solver.value(e)}")
