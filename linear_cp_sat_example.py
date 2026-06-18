"""Small Google OR-Tools CP-SAT optimization example."""

from ortools.sat.python import cp_model


def main() -> None:
    model = cp_model.CpModel()

    x = model.NewIntVar(0, 10, "x")
    y = model.NewIntVar(0, 10, "y")

    model.Add(x + 2 * y <= 14)
    model.Add(3 * x - y >= 0)
    model.Add(x - y <= 2)

    model.Maximize(2 * x + 3 * y)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    print(f"Status: {solver.StatusName(status)}")

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f"Objective: {solver.ObjectiveValue()}")
        print(f"x = {solver.Value(x)}")
        print(f"y = {solver.Value(y)}")


if __name__ == "__main__":
    main()
