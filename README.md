# CP-SAT Training

This repository is for learning and practicing constraint programming with
Google OR-Tools CP-SAT in Python.

The examples are training exercises based on the Google OR-Tools docs:

- [Google OR-Tools](https://developers.google.com/optimization)
- [CP-SAT solver guide](https://developers.google.com/optimization/cp/cp_solver)
- [Job shop scheduling example](https://developers.google.com/optimization/scheduling/job_shop)

## Setup

Create a local virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run any example with:

```bash
python job_shop.py
```

If you already have another Python environment, just install the requirements:

```bash
python -m pip install -r requirements.txt
```

## Examples

| File | Description |
| --- | --- |
| `linear_cp_sat_example.py` | Small integer optimization starter example with a few variables, constraints, and a maximization objective. |
| `cryptarithmetic.py` | Solves the cryptarithmetic puzzle `CP + IS + FUN = TRUE`. |
| `n_queens.py` | Models the N-Queens problem with row and diagonal constraints, then counts solutions found. |
| `nurses.py` | Nurse scheduling example with shift coverage, one-shift-per-day limits, balanced assignments, and shift request optimization. |
| `job_shop.py` | Job shop scheduling example with interval variables, machine no-overlap constraints, task dependencies, makespan minimization, and colored terminal output. |

## Notes

- This is a training repo, so some files may be intentionally simple or written step by step.
- For large N-Queens boards, exact solution counting can be expensive. Use smaller board sizes while experimenting.
- Terminal colors in `job_shop.py` use ANSI escape codes, so they work best in a normal terminal.
