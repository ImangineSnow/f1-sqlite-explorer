# Formula 1 SQLite Explorer

This coursework-based project uses a normalized SQLite database and a Python command-line interface to explore the 2023 Formula 1 season. The database connects races, drivers, teams, race results, and team results through primary and foreign keys.

The repository is a cleaned and documented version of an academic database project. Assignment instructions, student identifiers, and grading notes are intentionally excluded.

## Database contents

| Table | Records | Purpose |
| --- | ---: | --- |
| `Teams` | 10 | Constructor information and season totals |
| `Drivers` | 22 | Driver information and season totals |
| `Races` | 22 | Grand Prix dates, winners, and lap counts |
| `Race_Drivers` | 435 | Driver results for each race |
| `Race_Teams` | 220 | Team points for each race |

The table definitions are also available in [`schema.sql`](schema.sql).

## Run locally

Python 3.10 or later is recommended. SQLite support is included with Python, so there are no third-party dependencies.

```bash
python main.py
```

You can also run a query directly:

```bash
python main.py --race Bahrain
python main.py --team "Red Bull Racing"
python main.py --drivers "Red Bull Racing"
```

## Example

```text
Driver          | Wins | Podiums | Points
----------------+------+---------+-------
Max Verstappen  | 19   | 21      | 575
Sergio Perez    | 2    | 10      | 285
```

## Tests

```bash
python -m pip install pytest
pytest -q
```

## Notes

- This is an educational project and is not affiliated with Formula 1.
- The dataset was assembled for coursework and may differ from official records.
- The original project was completed in 2024 and reorganized for public presentation in 2026.
