"""Create a lightweight inventory of raw UFC data files.

This script is intentionally simple and does not require pandas. It is meant
for the early data collection stage, where we only want to confirm what files
exist and what their basic shapes look like.
"""

from __future__ import annotations

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_UFCSTATS_DIR = PROJECT_ROOT / "data" / "raw" / "ufcstats"


def inspect_csv(file_path: Path) -> dict[str, object]:
    """Return basic information about one CSV file.

    The row count excludes the header row because the header contains column
    names, not fight or fighter observations.
    """
    with file_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader, [])
        row_count = sum(1 for _ in reader)

    return {
        "file_name": file_path.name,
        "rows": row_count,
        "columns": len(header),
        "size_mb": round(file_path.stat().st_size / (1024 * 1024), 2),
        "first_columns": header[:8],
    }


def build_inventory() -> list[dict[str, object]]:
    """Inspect every visible CSV file in the UFCStats raw data folder."""
    csv_files = sorted(RAW_UFCSTATS_DIR.glob("*.csv"))
    return [inspect_csv(file_path) for file_path in csv_files]


def print_inventory(inventory: list[dict[str, object]]) -> None:
    """Print a readable summary of the raw dataset inventory."""
    if not inventory:
        print("No CSV files found in data/raw/ufcstats/.")
        return

    print("Raw UFCStats data inventory")
    print("=" * 28)

    for item in inventory:
        print(f"\nFile: {item['file_name']}")
        print(f"Rows: {item['rows']}")
        print(f"Columns: {item['columns']}")
        print(f"Size: {item['size_mb']} MB")
        print(f"First columns: {', '.join(item['first_columns'])}")


if __name__ == "__main__":
    print_inventory(build_inventory())

