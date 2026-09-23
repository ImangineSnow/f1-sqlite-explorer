"""Query a small SQLite database of the 2023 Formula 1 season."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


DEFAULT_DATABASE = Path(__file__).parent / "database" / "f12023_database.db"


def connect(database: str | Path = DEFAULT_DATABASE) -> sqlite3.Connection:
    """Open the project database with foreign-key checks enabled."""
    connection = sqlite3.connect(database)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def race_results(connection: sqlite3.Connection, grand_prix: str) -> list[tuple]:
    """Return driver results for one Grand Prix, ordered by finishing position."""
    return connection.execute(
        """
        SELECT driver_name, position, points, fast_lap
        FROM Race_Drivers
        WHERE grand_prix = ?
        ORDER BY position IS NULL, CAST(position AS INTEGER)
        """,
        (grand_prix,),
    ).fetchall()


def team_results(connection: sqlite3.Connection, team: str) -> list[tuple]:
    """Return a team's points in each race in calendar order."""
    return connection.execute(
        """
        SELECT r.grand_prix, rt.total_points
        FROM Race_Teams AS rt
        JOIN Races AS r ON r.grand_prix = rt.grand_prix
        WHERE rt.team_name = ?
        ORDER BY r.date
        """,
        (team,),
    ).fetchall()


def team_drivers(connection: sqlite3.Connection, team: str) -> list[tuple]:
    """Return season totals for drivers on a team."""
    return connection.execute(
        """
        SELECT name, wins, podiums, points
        FROM Drivers
        WHERE team_name = ?
        ORDER BY points DESC, wins DESC
        """,
        (team,),
    ).fetchall()


def format_table(headers: tuple[str, ...], rows: list[tuple]) -> str:
    """Format query output without third-party dependencies."""
    if not rows:
        return "No matching records found."
    values = [["N/A" if value is None else str(value) for value in row] for row in rows]
    widths = [
        max(len(headers[index]), *(len(row[index]) for row in values))
        for index in range(len(headers))
    ]
    line = " | ".join(header.ljust(width) for header, width in zip(headers, widths))
    divider = "-+-".join("-" * width for width in widths)
    body = [" | ".join(value.ljust(width) for value, width in zip(row, widths)) for row in values]
    return "\n".join([line, divider, *body])


def interactive_menu(connection: sqlite3.Connection) -> None:
    """Run a small terminal menu for exploring the database."""
    while True:
        print("\nF1 Database Explorer")
        print("1. Driver results for a Grand Prix")
        print("2. Team results across races")
        print("3. Drivers on a team")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            rows = race_results(connection, input("Grand Prix name (for example, Bahrain): ").strip())
            print(format_table(("Driver", "Position", "Points", "Fast lap"), rows))
        elif choice == "2":
            rows = team_results(connection, input("Team name (for example, Red Bull Racing): ").strip())
            print(format_table(("Grand Prix", "Points"), rows))
        elif choice == "3":
            rows = team_drivers(connection, input("Team name (for example, Red Bull Racing): ").strip())
            print(format_table(("Driver", "Wins", "Podiums", "Points"), rows))
        elif choice == "4":
            return
        else:
            print("Please enter a number from 1 to 4.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--race", help="Show results for a Grand Prix")
    parser.add_argument("--team", help="Show a team's race-by-race results")
    parser.add_argument("--drivers", help="Show season totals for drivers on a team")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with connect(args.database) as connection:
        if args.race:
            print(format_table(("Driver", "Position", "Points", "Fast lap"), race_results(connection, args.race)))
        elif args.team:
            print(format_table(("Grand Prix", "Points"), team_results(connection, args.team)))
        elif args.drivers:
            print(format_table(("Driver", "Wins", "Podiums", "Points"), team_drivers(connection, args.drivers)))
        else:
            interactive_menu(connection)


if __name__ == "__main__":
    main()

