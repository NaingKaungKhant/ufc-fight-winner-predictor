"""Data collection helpers for the UFC fight winner prediction project.

This file does not train a model. Its job is to help organize raw UFC data
after you download it from a source such as Kaggle, a public CSV, or a scraped
dataset you are allowed to use.
"""

from __future__ import annotations

from pathlib import Path


# Path(__file__) points to src/data_collection.py.
# parents[1] moves up one level to the project root folder.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"


def list_raw_data_files() -> list[Path]:
    """Return all visible files currently stored in the raw data folder.

    This is useful at the start of the project because we want to know exactly
    which original data files are available before cleaning or analysis begins.
    """
    return sorted(
        path
        for path in RAW_DATA_DIR.rglob("*")
        if path.is_file() and not path.name.startswith(".")
    )


def load_raw_csv(file_name: str) -> pd.DataFrame:
    """Load a CSV file from data/raw into a pandas DataFrame.

    Parameters
    ----------
    file_name:
        The CSV path inside data/raw. Example: "ufcstats/ufc_fight_results.csv".

    Returns
    -------
    pandas.DataFrame
        The loaded dataset.
    """
    import pandas as pd

    file_path = RAW_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"Could not find {file_path}. Put the CSV file in data/raw first."
        )

    return pd.read_csv(file_path)


if __name__ == "__main__":
    # This block runs only when you execute:
    # python src/data_collection.py
    #
    # It gives a quick check of which raw data files are available.
    raw_files = list_raw_data_files()

    if not raw_files:
        print("No raw data files found yet. Add CSV files to data/raw/.")
    else:
        print("Raw data files:")
        for file_path in raw_files:
            print(f"- {file_path.name}")
