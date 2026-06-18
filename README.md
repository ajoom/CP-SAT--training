# CP-SAT / OR-Tools Python Setup

This machine has a reusable OR-Tools virtual environment at:

```bash
/Users/bassemthread/.venvs/or-tools
```

Activate it from any folder:

```bash
source /Users/bassemthread/.venvs/or-tools/bin/activate
```

Then run Python files normally:

```bash
python queens.py
```

Run the included starter example:

```bash
python linear_cp_sat_example.py
```

To use the same dependency version in another project folder:

```bash
python -m pip install -r requirements.txt
```

Installed package:

```text
ortools==9.15.6755
```
